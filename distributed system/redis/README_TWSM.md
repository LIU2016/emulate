# 1.引言

## 1.1 设计背景

- 框架的调整是为了满足**接口详情，服务节点数据缓存使用**场景，不让代码中直接出现缓存操作。不和已有的缓存框架对业务单表缓存的功能上冲突，不在持久层上缓存。可以把他当成类似事务处理的框架。

- 同一个系统的不常更新的接口数据。

  - 某些系统查询详情数据，一个接口可能要查询一堆复杂的业务数据集合（多张表、多种类型的缓存集合），**但接口本身的数据不会有什么变更，或者能明确找到清理的方法**，例如作业中心的线下数据，要请求**6张表**才能获取需要的详情数据。无论是请求数据库，还是redis，网络开销太大，性能低，需要缓存整个的接口数据，而不仅仅是单表数据。

- 非同一个系统服务之间的调度压力大。

  - 因为我们采用的微服务框架，存在很多节**点之间的相互调用，频次太高会给调用服务造成的压力太大**。要减少服务之间的调用。
  - 请求**服务之间的接口请求数据太大**，例如ecr的获取试卷详情接口，一份只有4道题的试卷，返回了10Kb的数据集，网络开销太大，减少大数据接口的访问。

- 不在持久层上缓存数据，因为很难维护，可能会导致数据库数据已经清除，但缓存数据一直留在Redis里头，长时间会导致垃圾数据剧增。例如：公司目前的框架采用的Mybatis，当数据添加到缓存后，后面使用带条件的sql删除数据清理的时候，很容易忘记或者忽略去掉缓存，这时你只能强调每一位使用者在做这步操作的时候先查出数据去清理缓存。所以**使用缓存最好是明确指出来，且保证每份数据的时效性**，**缓存不要长期有效。对于应用类数据可以定时刷新**，**日志类数据周期性清理**

- **业务系统的缓存的key设计，要求带上租户编码**，例如：租户:产品:表名:值 。不然不同租户的下相同的表相同的主键会导致数据错乱。

- 要支持不同的数据类型，可以分为应用类、日志类，有点像ES~~，应用类数据例如的试题、学生、科目等，日志类数据例如：作答、作业、考试、错题等等。**不同的数据类型存储的redis数据格式不一样，需要维护的过期时间不一样。**

- Redis缓存在高并发下，网络开销和序列化的代价高昂，要尽量**减少Redis的请求**。

- Jedis客户端目前不支持集群环境下的pipeline模式，无法有效减少TCP的交互。这个版本先不做修改，后续版本再做调整，升级成Lettuce客户端（需要分布式锁等分布式的特性，可以结合Redisson使用）。

# 2.软件支持

| 软件           | 版本   | 配置                                       |
| -------------- | ------ | ------------------------------------------ |
| redis          | 3.2.9  | 使用eco服务                                |
| caffeine cache | 2.6.0  |                                            |
| fastjson       | 1.2.29 |                                            |
| kryo-shaded    | 3.0.3  | 后续针对不同的数据类型使用不同的序列化方式 |

# 3.总体功能概述

## 3.1 功能总体需求

- 构建两级缓存（本地应用缓存、远程缓存服务）。
- 缓存、清理详情接口数据，支持不同参数传值缓存不同的key。
- 缓存非本系统的接口数据，因为系统之间没有消息服务，暂时没有扩展清理缓存功能。
- 获取非本系统的缓存数据，在调用非本系统数据的接口之前先去查缓存。

## 3.2 整体框架视图

![多级缓存 (1)](C:\Users\lqd\Downloads\多级缓存 (1).png)

## 3.3 实现

1. 构建多级缓存，一级缓存用caffeine，二级缓存用redis。

   ```java
   public RedisCaffeineCacheManager(CacheRedisCaffeineProperties cacheRedisCaffeineProperties,
   			RedisTemplate<Object, Object> redisTemplate) {
   		super();
   		this.cacheRedisCaffeineProperties = cacheRedisCaffeineProperties;
   		this.redisTemplate = redisTemplate;
   		this.dynamic = cacheRedisCaffeineProperties.isDynamic();
   		this.cacheNames = cacheRedisCaffeineProperties.getCacheNames();
   	}
   ```

2. 对spring cache框架进行扩展。满足我们的缓存规范，例如：租户:产品:表名:值

   ```java
   **
    * @program: microservice-framework
    * @description: RedisCaffeineCache
    * @author: Mr.LQDing
    * @create: 2019-11-11 10:51
    **/
   @Slf4j
   public class RedisCaffeineCache extends AbstractValueAdaptingCache {
       ....
            /**
            * 接口请求的方式，返回string类型的数据
            */
           if(DataType.STRING==dataType || DataType.NONE==dataType)
           {
               Object object = redisTemplate.opsForValue().get(cacheKeyList.get(0));
               if (null!=object)
               {
                   caffeineCache.put(caffeineKey, object);
               }
               return object;
           }
           /**
            * 单表的请求，返回hash对象
            */
           else if (DataType.HASH==dataType)
           {
               List<Object> finalObjectList = objectList;
               HashMapper mapper =getMapper();
               cacheKeyList.stream().forEach(cacheKey->{
                   Map<Object,Object> map = redisTemplate.boundHashOps(cacheKey).entries();
                   Object object = mapper.fromHash(map);
                   finalObjectList.add(object);
               });
               if (CollectionUtils.isNotEmpty(objectList)) {
                   caffeineCache.put(caffeineKey, objectList);
               }
           }
      
   ```

3. 二级缓存清理的同时，通过redis的发布订阅功能发消息清理掉一级缓存。

   ```
   private void push(CacheMessage message) {
   
           String prefix = getCacheName(this.name).replace(OTHER_REDIS_KEY,"") ;
           if (getCacheName(this.name).indexOf(CACHE_OPERATOR)!=-1)
           {
               prefix = prefix.substring(0,prefix.indexOf(CACHE_OPERATOR));
   
           }
           String topic = this.topic.concat(CACHE_OPERATOR).concat(prefix);
           redisTemplate.convertAndSend(topic, message);
       }
   
   public void clearLocal(String cacheName, Object key) {
   		Cache cache = cacheMap.get(cacheName);
   		if(cache == null) {
   			return ;
   		}
   		RedisCaffeineCache redisCaffeineCache = (RedisCaffeineCache) cache;
   		redisCaffeineCache.clearLocal(key);
   	}
   
   ```

4. 修改序列化方式为FastJsonRedisSerializer：

   ```java
   public RedisTemplate<Object, Object>
       redisTemplate(JedisConnectionFactory jedisConnectionFactory) {
   
           RedisTemplate<Object, Object> redisTemplate = new RedisTemplate<>();
           redisTemplate.setConnectionFactory(jedisConnectionFactory);
           FastJsonRedisSerializer fastJsonRedisSerializer = new FastJsonRedisSerializer(Object.class);
           ParserConfig.getGlobalInstance().addAccept("com.tianwen.springcloud.microservice.");
           ParserConfig.getGlobalInstance().setAutoTypeSupport(true);
           redisTemplate.setValueSerializer(fastJsonRedisSerializer);
           redisTemplate.setHashValueSerializer(fastJsonRedisSerializer);
           redisTemplate.setKeySerializer(new StringRedisSerializer());
           redisTemplate.setHashKeySerializer(new StringRedisSerializer());
           redisTemplate.afterPropertiesSet();
           return redisTemplate;
       }
   ```

5. 缓存属性配置（日志类数据我们二级缓存配置7天的超时时间，二级缓存ECO采用了默认的内存淘汰策略，no-enviction：禁止驱逐数据，其实没必要，当内存不足时会报错！！。一级缓存配置了30秒，采用lru淘汰策略。）：

   ```
   #设置多级缓存属性
   multiCache.Caffeine.initialCapacity=50
   multiCache.Caffeine.maximumSize=500
   multiCache.Caffeine.expireAfterWrite=30000
   
   #日志类数据，例如作答 存7天
   multiCache.Redis.defaultExpiration=604800000
   ```

## 3.4 效果

- 存储效果

  ![缓存存储](C:\Users\lqd\Desktop\缓存\缓存存储.png)

- 是否使用了一级缓存性能比较

  - 使用二级缓存但未使用一级缓存情况：单次请求 87ms![redis请求](C:\Users\lqd\Desktop\缓存\redis请求.png)
  - 使用一级缓存后的情况：单次请求 15ms![应用缓存](C:\Users\lqd\Desktop\缓存\应用缓存.png)

- 请求非当前系统的接口，使用框架后与未使用框架之前的请求性能比较：

  - 使用框架之前，网络稳定的情况下ECR接口试卷详情单次请求：380ms

    ![ECR](C:\Users\lqd\Desktop\缓存\ECR.png)

  - 使用框架之后，ECR接口试卷详情单次请求：60ms

    ![ECR缓存](C:\Users\lqd\Desktop\缓存\ECR缓存.png)

- 本系统的请求性能比较

  - 使用框架之前，线下数据详情接口请求：131ms

    ![线下](C:\Users\lqd\Desktop\缓存\线下.png)

  - 使用框架之后，线下数据详情接口请求：20ms

    ![线下缓存](C:\Users\lqd\Desktop\缓存\线下缓存.png)

  总结：性能提升是明显的，但这是用空间换时间的方式，后面对内存的要求可能更高。

## 3.5 使用

目前只支持三种情况缓存，其他情况的业务切勿使用。

1. 支持本系统的接口详情缓存，详情接口的清理。
2. 支持对非本系统的详情接口缓存，但不支持清理，需要系统之间提供消息通信，才能扩展这部分功能。例如：ECR的试卷详情接口。
3. 支持获取非本系统的hash类数据对象缓存，例如ECO的字典、用户。

使用步骤：

1. 在功能的core.properties中配置：MicroService.Project.Cache.Key=产品名称

2. 添加pom依赖，可以在父pom中添加：

   ```xml
   <dependency>
         <groupId>com.tianwen.springcloud</groupId>
         <artifactId>microservice-redis</artifactId>
         <version>1.1.1-SNAPSHOT</version>
   </dependency>
   ```

3. 我们采用注解的方式做到在业务逻辑层上加了一层缓存。这样不会入侵正常的业务逻辑操作。

   1. 定义统一的缓存key的管理：

      在我们的domain层按业务定义cachekey：

      ```java
      /**
       * @program: aihomework
       * @description: 线下作业cahekey
       * @author: Mr.LQDing
       * @create: 2019-11-28 13:33
       **/
      public interface IOfflineTaskCacheKey {
      
          String TABLE_CACHEKEY = "t_e_offlinetask" ;
          String COLUMN_CACHEKEY_TASKID = "taskid" ;
      }
      
      ```

      ![cachekey](C:\Users\lqd\Desktop\缓存\cachekey.png)

   2. 针对本系统的接口详情缓存使用（作业或者考试详情）：

      1. 添加缓存

         ```java
         @MicroServiceCacheable(table = IOfflineTaskCacheKey.TABLE_CACHEKEY,
                 column = IOfflineTaskCacheKey.COLUMN_CACHEKEY_TASKID)
          public Response<OfflineTaskDetailResp> searchTaskDetail(GetOfflineTaskInfoReq req)
         ```

         注意，（同下，下面不在重复）：

         - **请求方法的参数只能有一个且是对象，例如GetOfflineTaskInfoReq。**

         - **参数对象要有与缓存定义中指定的COLUMN同名的属性，或者在属性上指定@MicroServiceCacheField(value = "taskid")。**
         - **详情暂不支持COLUMN属性的值传的集合类型的数据。**

      2. 清理缓存

         ```java
         @MicroServiceCacheEvict(table = IOfflineTaskCacheKey.TABLE_CACHEKEY,
                     column = IOfflineTaskCacheKey.COLUMN_CACHEKEY_TASKID)
             public Response addTeacherAnswer(@RequestBody AddTeacherAnswerReq req)
         ```

         注意：

         - **key指向添加缓存的key 。**

   3. 针对非本系统的详情接口缓存（ECR的试卷详情）：

      1. 添加缓存

         ```java
          @HystrixCommand(fallbackMethod = "getPaperDetailFallback")
             @MicroServiceCacheable(table = IPaperInfoCacheKey.TABLE_CACHEKEY,
                     column = IPaperInfoCacheKey.COLUMN_CACHEKEY_PAPERID)
             public PaperInfo getPaperDetail(PaperDetailReq req)
             {
         ```

   4. 针对获取非本系统的hash类数据对象（ECO的字典、用户）：

      1. 添加缓存

         ```java
          @HystrixCommand(fallbackMethod = "getDicFallback")
             @MicroServiceCacheable(source = ISourceCacheKey.SOURCE_ECO,
                     table = IDictItemCacheKey.TABLE_CACHEKEY,
                     column = IDictItemCacheKey.COLUMN_CACHEKEY_DICTTYPE_LANG_DICTVALUE)
             public List<DictItemInfo> getDic(EcoDict ecoDict)
             {
         ```

         ```java
         @Data
         public class EcoDict {
         
             @MicroServiceCacheField(value = "dicttypeid")
             private String dictTypeId ;
             @MicroServiceCacheField(value = "lang")
             private String lang ;
             @MicroServiceCacheField(value = "dictvalue")
             private Set<String> dictValueList ;
         }
         ```

         注意：

         - **多个参数的时候 ，注意传参对象的定义的顺序跟缓存上的key保持一致。**

         - **支持其中一个指定的参数传集合类型**

# 4.性能

略

# 5.附录

略