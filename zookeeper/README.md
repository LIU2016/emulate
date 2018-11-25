[TOC]



# 一、背景

以电商架构为例，早期我们是单一的应用架构，随着互联网的快速发展和体量的不断增长，后端的架构通过垂直伸缩的方式很难达到我们期望的性能要求，同时投入产出比也非常大，同时普通 PC 的性能也越来越高，所以通过水平伸缩的方式来提升性能成为了主流。

在分布式架构下，当服务越来越多，规模越来越大时，对应的机器数量也越来越大，单靠人工来管理和维护服务及
地址的配置地址信息会越来越困难，单点故障的问题也开始凸显出来，一旦服务路由或者负载均衡服务器宕机，依
赖他的所有服务均将失效。

此时，需要一个能够动态注册和获取服务信息的地方。来统一管理服务名称和其对应的服务器列表信息，称之为服务配置中心，服务提供者在启动时，将其提供的服务名称、服务器地址注册到服务配置中心，服务消费者通过服务配置中心来获得需要调用的服务的机器列表。通过相应的负载均衡算法，选取其中一台服务器进行调用。

当服务器宕机或者下线时，相应的机器需要能够动态地从服务配置中心里面移除，并通知相应的服务消费者，否则服务消费者就有可能因为调用到已经失效服务而发生错误，在这个过程中，服务消费者只有在第一次调用服务时需要查询服务配置中心，然后将查询到的信息缓存到本地，后面的调用直接使用本地缓存的服务地址列表信息，而不需要重新发起请求道服务配置中心去获取相应的服务地址列表，直到服务的地址列表有变更（机器上线或者线）。这种无中心化的结构解决了之前负载均衡设备所导致的单点故障问题，并且大大减轻了服务配置中心的压力。

# 二、什么是 zookeeper

zookeeper 是一个开源的分布式协调服务，由雅虎公司创建，是 google chubby 的开源实现。zookeeper 的设计目标是将哪些复杂且容易出错的分布式一致性服务封装起来，构成一个高效可靠的原语集（由若干条指令组成的，完成一定功能的一个过程），并且以一些列简单一用的接口提供给用户使用。zookeeper并不是用来存储数据的，通过监控数据状态的变化，达到基于数据的集群管理。

他的相关功能有：

> 数据的发布/订阅（配置中心:disconf）  、
>
> 负载均衡（dubbo利用了zookeeper机制实现负载均衡） 、
>
> 命名服务、
>
> master选举(kafka、hadoop、hbase)、
>
> 分布式队列、
>
> 分布式锁
>
> - 数据发布订阅/ 配置注册中心
>   实现配置信息的集中式管理和数据的动态更新
>   实现配置中心有两种模式：push 、pull。
>   zookeeper采用的是推拉相结合的方式。 客户端向服务器端注册自己需要关注的节点。一旦节点数据发生变化，那么服务器端就会向客户端发送watcher事件通知。客户端收到通知后，主动到服务器端获取更新后的数据。
>   1.数据量比较小
>   2.数据内容在运行时会发生动态变更
>   3.集群中的各个机器共享配置
> - 负载均衡
>   请求/数据分摊多个计算机单元上，每个服务器对应一个节点，访问的时候通过哈希算法找到对应的节点。
> - 分布式锁
>   通常实现分布式锁有几种方式
>   1.redis。 setNX 存在则会返回0， 不存在
>   2.数据方式去实现
>   创建一个表， 通过索引唯一的方式
>   create table (id , methodname …)   methodname增加唯一索引
>   insert 一条数据XXX   delete 语句删除这条记录
>   mysql  for update
>   3.zookeeper实现
>   排他锁（写锁）：不同客户端写相同的临时节点
>   共享锁（读锁）
>   实现共享锁，使用java api的方式
> - 命名服务/master选举
>   7*24小时可用，99.99999%可用master-slave模式。
>   实现价值：所有的服务器挂在同一个（临时）节点上。
> - 分布式队列
>   1，先进先出
>   1.通过getChildren获取指定根节点下的所有子节点，子节点就是任务
>   2.确定自己节点在子节点中的顺序
>   3.如果自己不是最小的子节点，那么监控比自己小的上一个子节点，否则处于等待
>   4.接收watcher通知，重复流程
>   2，barrier模式（相比1有个触发条件）
>   在1的基础上有触发的条件（达到了x个数量时才执行）

## 官网地址

http://zookeeper.apache.org/doc/r3.4.13/index.html

# 三、zookeeper数据模型

zookeeper的数据模型和文件系统类似，每一个节点称为：znode.  是zookeeper中的最小数据单元。每一znode上都可以保存数据和挂载子节点。 从而构成一个层次化的属性结构.

> 节点特性：
> 持久化节点  ： 节点创建后会一直存在zookeeper服务器上，直到主动删除.
> 持久化有序节点 ：每个节点都会为它的一级子节点维护一个顺序.
> 临时节点 ： 临时节点的生命周期和客户端的会话保持一致。当客户端会话失效，该节点自动清理.
> 临时有序节点 ： 在临时节点上多了一个顺序性特性.
> 临时节点不能挂子节点

# 四、zookeeper特性

> zookeeper的特性(所有的写请求都会到leader，读请求都会从follower中读取)。
> ​	顺序一致性 ：从同一个客户端发起的事务请求，最终会严格按照顺序被应用到zookeeper中 。
> ​	原子性： 要么同时成功、要么同时失败 （分布式事务）
> ​	单一视图： 无论客户端连接到哪个服务器，所看到的模型都是一样
> ​	可靠性：一旦服务器端提交了一个事务并且获得了服务器端返回成功的标识，那么这个事务所引起的服务器端的变更会一直保留。
> ​	实时性：一旦一个事务被成功应用，客户端就能够立即从服务器端读取到事务变更后的最新数据状态；（zookeeper仅仅保证在一定时间内，近实时）。

# 五、数据存储（内存数据和磁盘数据）

zookeeper会定时把数据存储在磁盘上。DataDir = 存储的是数据的快照。快照： 存储某一个时刻全量的内存数据内容。DataLogDir 存储事务日志
log.zxid查看事务日志的命令：java -cp :/mic/data/program/zookeeper-3.4.10/lib/slf4j-api-1.6.1.jar:/mic/data/program/zookeeper-3.4.10/zookeeper-3.4.10.jar org.apache.zookeeper.server.LogFormatter log.200000001

> zookeeper 有三种日志
> zookeeper.out：运行日志
> 快照：存储某一时刻的全量数据
> 事务日志：事务操作的日志记录(最好单独挂载一个磁盘，优化)

# 六、线程模型

boss线程和work线程

# 七、zookeeper 安装部署

zookeeper 有两种运行模式：集群模式和单机模式。

## 单机模式

> 下 载 zookeeper 安 装 包 ：http://apache.fayea.com/zookeeper/下载完成，通过 tar -zxvf 解压。
>
> 常用命令
>
> 1. 启动 ZK 服务:
>     bin/zkServer.sh start
> 2. 查看 ZK 服务状态:
>     bin/zkServer.sh status
> 3. 停止 ZK 服务:
>     bin/zkServer.sh stop
> 4. 重启 ZK 服务:
>     bin/zkServer.sh restart
> 5. 连接服务器
>     bin/zkCli.sh -timeout 0 -r -server ip:port

单机环境安装一般情况下，在开发测试环境，没有这么多资源的情况下，而且也不需要特别好的稳定性的前提下，我们可以使用单机部署；

***初次使用zookeeper ， 需要将conf目录下的zoo_sample.cfg 文件 copy 一份重命名为 zoo.cfg，***

***修改 dataDir 目录，dataDir 表示日志文件存放的路径。***

## zoo.cfg里面配置信息

tickTime=2000  zookeeper中最小的时间单位长度 （ms）

initLimit=10  follower节点启动后与leader节点完成数据同步的时间

syncLimit=5 leader节点和follower节点进行心跳检测的最大延时时间（异常：网络异常或者不归leader管理了）

dataDir=/tmp/zookeeper  表示zookeeper服务器存储快照文件的目录

dataLogDir 表示配置 zookeeper事务日志的存储路径，默认指定在dataDir目录下

clientPort 表示客户端和服务端建立连接的端口号： 2181

## 集群环境安装

zookeeper一般是由 2n+1台服务器组成。在zookeeper集群中，各个节点总共有三种角色，分别是：leader，follower，observer集群模式。我们采用模拟 3 台机器来搭建 zookeeper 集群。分别复制安装包到三台机器上并解压，同时 copy 一份zoo.cfg。

> 1. 修改配置文件zoo.cfg，修改端口：
>     server.1=IP1:2888:3888 【2888：访问 zookeeper 的端口；3888：重新选举 leader 的端口】
>     server.2=IP2.2888:3888
>     server.3=IP3.2888:3888
>     server.A=B：C：D：
>
>   其 中A 是一个数字，表示这个是第几号服务器；B 是这个服务器的 ip 地址；C 表示的是这个服务器与集群中的 Leader服务器交换信息的端口；D 表示的是万一集群中的 Leader 服务器挂了，需要一个端口来重新进行选举，选出一个新的 Leader，而这个端口就是用来执行选举时服务器相互通信的端口。如果是伪集群的配置方式，由于 B 都是一样，所以不同的 Zookeeper 实例通信端口号不能一样，所以要给它们分配不同的端号。在集群模式下，集群中每台机器都需要感知到整个集群是由 哪 几 台 机 器 组 成 的 ， 在 配 置 文 件 中 ， 按 照 格 式server.id=host:port:port，每一行代表一个机器配置。id: 指的是 server ID,用来标识该机器在集群中的机器序号。
>
>   在zoo.cfg里面增加 ()，
>
>   观察者角色配置如下：
>
>   peerType=observer 
>   server.1=192.168.11.129:2188:3181:observer
>   server.2=192.168.11.131:2188:3181
>   server.3=192.168.11.135:2188:3181
>
>   其他的角色配置如下：
>
>   server.1=192.168.11.129:2188:3181
>   server.2=192.168.11.131:2188:3181
>   server.3=192.168.11.135:2188:3181
>
>   **注意：这里的端口不能和zk的clientport一样**
>
> 2. 新建 datadir 目录，设置 myid。在每台zookeeper机器上，我们都需要在数据目录(dataDir)下创建一个 myid 文件，该文件只有一行内容，对应每台机器的 Server ID 数字；比如 server.1 的 myid 文件内容就是1。【必须确保每个服务器的 myid 文件中的数字不同，并且和自己所在机器的 zoo.cfg 中 server.id 的 id 值一致，id 的范围是 1~255】
>
> 3. 启动 zookeeper。带 Observer 角色的集群Observer：在不影响写性能的情况下扩展 zookeeper本身 zookeeper 的集群性能已经很好了，但是如果超大量的客户端访问，就势必需要增加 zookeeper 集群的服务器数量，而随着服务器的增加，zookeeper 集群的写性能就会下降；zookeeper 中 znode 的变更需要半数及以上服务器投票通过，而随着机器的增加，由于网络消耗等原因必定会导致投票成本增加。也就导致性能下降的结果。
>
>   1.observer不参与投票。 只接收投票结果。
>   2.不属于zookeeper的关键部位。

# 八、zookeeper 的设计猜想

zookeeper 主要是解决分布式环境下的服务协调问题而产生的，如果我们要去实现一个 zookeeper 这样的中间件，我们需要做什么？
> 1. 防止单点故障
>     如果要防止 zookeeper 这个中间件的单点故障，那就势必要做集群。而且这个集群如果要满足高性能要求的话，还得是一个高性能高可用的集群。高性能意味着这个集群能够分担客户端的请求流量，高可用意味着集群中的某一个节点宕机以后，不影响整个集群的数据和继续提供服务的可能性。
>     结论： 所以这个中间件需要考虑到集群,而且这个集群还需要分摊客户端的请求流量
> 2. 接着上面那个结论再来思考，如果要满足这样的一个高性能集群，我们最直观的想法应该是，每个节点都能接
>     收到请求，并且每个节点的数据都必须要保持一致。要实现各个节点的数据一致性，就势必要一个 leader 节点负责协调和数据同步操作。这个我想大家都知道，如果在这样一个集群中没有 leader 节点，每个节点都可以接收所有请求，那么这个集群的数据同步的复杂度是非常大。
>     结论：所以这个集群中涉及到数据同步以及会存在leader 节点
> 3. 继续思考，如何在这些节点中选举出 leader 节点，以及leader 挂了以后，如何恢复呢？结论：所以 zookeeper 用了基于 paxos 理论所衍生出来的 ZAB 协议
> 4. leader 节点如何和其他节点保证数据一致性，并且要求是强一致的。在分布式系统中，每一个机器节点虽然都能够明确知道自己进行的事务操作过程是成功和失败，但是却无法直接获取其他分布式节点的操作结果。所以当一个事务操作涉及到跨节点的时候，就需要用到分布式事务，分布式事务的数据一致性协议有 2PC 协议和3PC 协议。

基于这些猜想，我们基本上知道 zookeeper 为什么要用到zab 理论来做选举、为什么要做集群、为什么要用到分布式事务来实现数据一致性了。接下来我们逐步去剖析zookeeper 里面的这些内容。

## 关于 2PC 提交

（Two Phase Commitment Protocol）当一个事务操作需要跨越多个分布式节点的时候，为了保持事务处理的 ACID特性，就需要引入一个“协调者”（TM）来统一调度所有分布式节点的执行逻辑，这些被调度的分布式节点被称为 AP。TM 负责调度 AP 的行为，并最终决定这些 AP 是否要把事务真正进行提交；因为整个事务是分为两个阶段提交，所以叫 2pc。

![1542788353299](C:\Users\lqd\AppData\Roaming\Typora\typora-user-images\1542788353299.png)

![1542788360866](C:\Users\lqd\AppData\Roaming\Typora\typora-user-images\1542788360866.png)

> 阶段一：提交事务请求（投票）
> 1. 事务询问
>
>   协调者向所有的参与者发送事务内容，询问是否可以执行事务提交操作，并开始等待各参与者的响应。
>
> 2. 执行事务
>
>   各个参与者节点执行事务操作，并将 Undo 和 Redo 信息记录到事务日志中，**尽量把提交过程中所有消耗时间的操作和准备都提前完成确保后面 100%成功提交事务**。
>
> 3. 各个参与者向协调者反馈事务询问的响应
>
>   如果各个参与者成功执行了事务操作，那么就反馈给参与者yes 的响应，表示事务可以执行；如果参与者没有成功执行事务，就反馈给协调者 no 的响应，表示事务不可以执行，上面这个阶段有点类似协调者组织各个参与者对一次事务操作的投票表态过程，因此 2pc 协议的第一个阶段称为“投票阶段”，即各参与者投票表名是否需要继续执行接下去的事务提交操作。
>

> 阶段二：执行事务（提交）
>
> ​	在这个阶段，协调者会根据各参与者的反馈情况来决定最终是否可以进行事务提交操作，正常情况下包			含两种可能：执行事务、中断事务。

# 九，zookeeper集群

在 zookeeper 中，客户端会随机连接到 zookeeper 集群中的一个节点，如果是读请求，就直接从当前节点中读取数据，如果是写请求，那么请求会被转发给leader提交事务，然后 leader 会广播事务，只要有超过半数节点写入成功，那么写请求就会被提交（类 2PC 事务）。![1542788928726](C:\Users\lqd\AppData\Roaming\Typora\typora-user-images\1542788928726.png)

所有事务请求必须由一个全局唯一的服务器来协调处理，这个服务器就是 Leader 服务器，其他的服务器就是follower。leader 服务器把客户端的失去请求转化成一个事务 Proposal（提议），并把这个 Proposal 分发给集群中的所有 Follower 服务器。之后 Leader 服务器需要等待所有Follower 服务器的反馈，**一旦超过半数的 Follower 服务器进行了正确的反馈**，那么 Leader 就会再次向所有的Follower 服务器发送 Commit 消息，要求各个follower 节点对前面的一个 Proposal 进行提交;

> 集群角色
>
> Leader 角色 - 火星情报局局长
> Leader 服务器是整个 zookeeper 集群的核心，主要的工作任务有两项：
>
> 1. 事物请求的唯一调度和处理者，保证集群事物处理的顺序性。
> 2. 集群内部各服务器的调度者。
>
> Follower 角色 - 薛之谦、
> Follower 角色的主要职责是
>
> 1. 处理客户端非事物请求、转发事物请求给 leader 服务器
> 2. 参与事物请求 Proposal 的投票（需要半数以上服务器通过才能通知 leader commit 数据; Leader 发起的提案，要求 Follower 投票）。
> 3. 参与 Leader 选举的投票
>
> Observer 角色
>
> Observer 是 zookeeper3.3 开始引入的一个全新的服务器角色，从字面来理解，该角色充当了观察者的角色。**观察zookeeper集群中的最新状态变化并将这些状态变化同步到 observer 服务器上。**
>
> Observer 的工作原理与follower 角色基本一致，而它和 follower 角色唯一的不同在于 observer 不参与任何形式的投票，包括事物请求Proposal的投票和leader选举的投票。简单来说，observer服务器只提供非事物请求服务，通常在于不影响集群事物处理能力的前提下提升集群非事物处理的能力。

>
>
> 集群组成
>
> 通常 zookeeper 是由 2n+1 台 server 组成，每个 server 都知道彼此的存在。对于 2n+1 台 server，只要有 n+1 台（大多数）server 可用，整个系统保持可用。我们已经了解到，一个 zookeeper 集群如果要对外提供可用的服务，那么集群中必须要有过半的机器正常工作并且彼此之间能够正常通信，基于这个特性，如果向搭建一个能够允许 F 台机器down 掉的集群，那么就要部署 2*F+1 台服务器构成的zookeeper 集群。因此 3 台机器构成的 zookeeper 集群，能够在挂掉一台机器后依然正常工作。一个 5 台机器集群的服务，能够对 2 台机器怪调的情况下进行容灾。如果一台由 6 台服务构成的集群，同样只能挂掉 2 台机器。因此，5 台和 6 台在容灾能力上并没有明显优势，反而增加了网络通信负担。系统启动时，集群中的 server 会选举出一台
> server 为 Leader，其它的就作为 follower（这里先不考虑observer 角色）。
>
> 之所以要满足这样一个等式，是因为一个节点要成为集群中的 leader，需要有超过及群众过半数的节点支持，这个涉及到 leader 选举算法，同时也涉及到事务请求的提交投票。

# 十、ZAB 协议

ZAB（Zookeeper Atomic Broadcast） 协议是为分布式协调服务 ZooKeeper 专门设计的一种**支持崩溃恢复的原子广播协议**。在 ZooKeeper 中，主要依赖 ZAB 协议来实现分布式数据一致性。基于该协议，ZooKeeper 实现了一种主备模式的系统架构来保持集群中各个副本之间的数据一致性。

> ZAB  协议介绍
>
> ZAB 协议包含两种基本模式，分别是崩溃恢复、原子广播。
>
> 当整个集群在启动时，或者当 leader 节点出现网络中断、崩溃等情况时，ZAB 协议就会进入恢复模式并选举产生新的 Leader，**当 leader 服务器选举出来后，并且集群中有过半的机器和该 leader 节点完成数据同步后**（同步指的是数据同步，用来保证集群中过半的机器能够和 leader 服务器的**数据状态保持一致**），ZAB 协议就会退出恢复模式。
>
> 当集群中已经有过半的 Follower 节点完成了和 Leader 状态同步以后，那么整个集群就进入了消息广播模式。这个时候，在 Leader 节点正常工作时，启动一台新的服务器加入到集群，那这个服务器会直接进入数据恢复模式，和leader 节点进行数据同步。同步完成后即可正常对外提供非事务请求的理。

## 消息广播的实现原理

> 如果大家了解分布式事务的 2pc 和 3pc 协议的话（不了解也没关系，我们后面会讲），消息广播的过程实际上是一个简化版本的二阶段提交过程。
>
> 1. leader 接收到消息请求后，将消息赋予一个全局唯一的64 位**自增 id**，叫：zxid，通过 zxid 的大小比较既可以实现因果有序这个特征。
>
> 2. leader 为每个 follower 准备了一个 FIFO 队列（通过 TCP协议来实现，以实现了全局有序这一个特点）将带有 zxid的消息作为一个**提案**（proposal）分发给所有的 follower。
>
> 3. 当 follower 接收到 proposal，先把 proposal 写到磁盘，写入成功以后再向 leader 回复一个 ack。
>
> 4. 当 leader 接收到合法数量（超过半数节点）的 ACK 后，leader 就会向这些 follower 发送 commit 命令，同时会在本地执行该消息。
>
> 5. 当 follower 收到消息的 commit 命令以后，会提交该消息。
>
>   ![1542790282843](C:\Users\lqd\AppData\Roaming\Typora\typora-user-images\1542790282843.png)
>
> leader 的投票过程，不需要 Observer 的 ack，也就是Observer 不需要参与投票过程，但是 Observer 必须要同步 Leader 的数据从而在处理请求的时候保证数据的一致性。

# 十一、崩溃恢复(数据恢复)

ZAB 协议的这个基于原子广播协议的消息广播过程，在正常情况下是没有任何问题的，但是一旦 Leader 节点崩溃，或者由于网络问题导致 Leader 服务器失去了过半的Follower 节点的联系（leader 失去与过半 follower 节点联系，可能是 leader 节点和 follower 节点之间产生了网络分区，那么此时的 leader 不再是合法的 leader 了），那么就会进入到崩溃恢复模式。

在 ZAB 协议中，为了保证程序的正确运行，整个恢复过程结束后需要选举出一个新的Leader。为了使 leader 挂了后系统能正常工作，需要解决以下两个问题。

> 1. 已经被处理的消息不能丢失。
>
>   当 leader 收到合法数量 follower 的 ACKs 后，就向各个 follower 广播 COMMIT 命令，同时也会在本地执行 COMMIT 并向连接的客户端返回「成功」。但是如果在各个 follower 在收到 COMMIT 命令前 leader就挂了，导致剩下的服务器并没有执行都这条消息。![1542791254375](C:\Users\lqd\AppData\Roaming\Typora\typora-user-images\1542791254375.png)
>
>   leader 对事务消息发起 commit 操作，但是该消息在follower1 上执行了，但是 follower2 还没有收到 commit，就已经挂了，而实际上客户端已经收到该事务消息处理成功的回执了。所以在 **zab 协议下需要保证所有机器都要执行这个事务消息。**
>
> 2. 被丢弃的消息不能再次出现
>
>   当 leader 接收到消息请求生成 proposal 后就挂了，其他 follower 并没有收到此 proposal，因此经过恢复模式重新选了 leader 后，这条消息是被跳过的。 此时，之前挂了的 leader 重新启动并注册成了follower，他保留了被跳过消息的 proposal 状态，与整个系统的状态是不一致的，需要将其删除。
>
> ZAB 协议需要满足上面两种情况，就必须要设计一个leader 选举算法：**能够确保已经被 leader 提交的事务Proposal能够提交、同时丢弃已经被跳过的事务Proposal**。针对这个要求：
>
> 如果 leader 选举算法能够**保证新选举出来的 Leader 服务器拥有集群中所有机器最高编号（ZXID 最大）的事务Proposal，那么就可以保证这个新选举出来的 Leader 一定具有已经提交的提案**。因为所有提案被 COMMIT 之前必须有超过半数的 follower ACK，即必须有超过半数节点的服务器的事务日志上有该提案的 proposal，因此，只要有合法数量的节点正常工作，就必然有一个节点保存了所有被 COMMIT 消息的 proposal 状态。
>
> 另外一个，zxid 是 64 位，高 32 位是 epoch 编号，       每经过一次 Leader 选举产生一个新的 leader，新的 leader 会将epoch 号+1，低 32 位是消息计数器，每接收到一条消息这个值+1，新 leader 选举后这个值重置为 0.     这样设计的好处在于老的leader挂了以后重启，它不会被选举为leader，因此此时它的 zxid 肯定小于当前新的 leader。    当老的leader 作为 follower 接入新的 leader 后，新的 leader 会让它将所有的拥有旧的 epoch 号的未被 COMMIT 的proposal 清除。

## 关于  ZXID

zxid，也就是事务 id，为了保证事务的顺序一致性，zookeeper 采用了递增的事务 id 号（zxid）来标识事务。所有的提议（proposal）都在被提出的时候加上了 zxid。实现中 zxid 是一个 64 位的数字，它高 32 位是 epoch（ZAB 协议通过 epoch 编号来区分 Leader 周期变化的策略）用来标识 leader 关系是否改变，每次一个 leader 被选出来，它都会有一个新的epoch=（原来的 epoch+1），标识当前属于那个 leader 的统治时期。低 32 位用于递增计数。

> epoch：可以理解为当前集群所处的年代或者周期，每个leader 就像皇帝，都有自己的年号，所以每次改朝换代，leader 变更之后，都会在前一个年代的基础上加 1。这样就算旧的 leader 崩溃恢复之后，也没有人听他的了，因为follower 只听从当前年代的 leader 的命令。*epoch 的变化大家可以做一个简单的实验，
>
> 1. 启动一个 zookeeper 集群。
> 2. 在/tmp/zookeeper/VERSION-2 路径下会看到一个currentEpoch 文件。文件中显示的是当前的 epoch
> 3. 把 leader 节点停机，这个时候在看 currentEpoch 会有变化。 随着每次选举新的 leader，epoch 都会发生变化。

# 十二、leader 选举

Leader 选举会分两个过程：启动的时候的 leader 选举、 leader 崩溃的时候的的选举

## 服务器启动时的 leader 选举

> 每个节点启动的时候状态都是 LOOKING，处于观望状态，接下来就开始进行选主流程进行 Leader 选举，至少需要两台机器（具体原因前面已经讲过了），我们选取 3 台机器组成的服务器集群为例。
>
> 在集群初始化阶段，当有一台服务器 Server1 启动时，它本身是无法进行和完成 Leader 选举，当第二台服务器 Server2 启动时，这个时候两台机器可以相互通信，每台机器都试图找到 Leader，于是进入 Leader 选举过程。选举过程如下
>
> (1)  每个 Server 发出一个投票。由于是初始情况，Server1和 Server2 都会将自己作为 Leader 服务器来进行投票，每次投票会包含所推举的服务器的myid和ZXID、epoch，使用(myid, ZXID,epoch)来表示，此时 Server1的投票为(1, 0)，Server2 的投票为(2, 0)，然后各自将这个投票发给集群中其他机器。
>
> (2) 接受来自各个服务器的投票。集群的每个服务器收到投票后，首先判断该投票的有效性，如检查是否是本轮投票（epoch）、是否来自LOOKING状态的服务器。
>
> (3) 处理投票。针对每一个投票，服务器都需要将别人的投票和自己的投票进行 PK，PK 规则如下：
>
> ​	i.  优先检查 ZXID。ZXID 比较大的服务器优先作为Leader
>
> ​	ii.  如果 ZXID 相同，那么就比较 myid。myid 较大的服务器作为 Leader 服务器。
>
> 对于 Server1 而言，它的投票是(1, 0)，接收 Server2的投票为(2, 0)，首先会比较两者的 ZXID，均为 0，再比较 myid，此时 Server2 的 myid 最大，于是更新自己的投票为(2, 0)，然后重新投票，对于Server2而言，它不需要更新自己的投票，只是再次向集群中所有机器发出上一次投票信息即可。
>
> (4) 统计投票。每次投票后，服务器都会统计投票信息，判断是否已经有过半机器接受到相同的投票信息，对于 Server1、Server2 而言，都统计出集群中已经有两台机器接受了(2, 0)的投票信息，此时便认为已经选出了 Leader。
>
> (5) 改变服务器状态。一旦确定了 Leader，每个服务器就会更新自己的状态，如果是 Follower，那么就变更为FOLLOWING，如果是 Leader，就变更为 LEADING。

## 运行过程中的 leader 选举

> 当集群中的 leader 服务器出现宕机或者不可用的情况时，那么整个集群将无法对外提供服务，而是进入新一轮的Leader 选举，服务器运行期间的 Leader 选举和启动时期的 Leader 选举基本过程是一致的。
>
> (1)  变更状态。Leader 挂后，余下的非 Observer 服务器都会将自己的服务器状态变更为 LOOKING，然后开始进入 Leader 选举过程。
>
> (2) 每个 Server 会发出一个投票。在运行期间，每个服务器上的 ZXID 可能不同，此时假定 Server1 的 ZXID 为123，Server3的ZXID为122；在第一轮投票中，Server1和 Server3 都会投自己，产生投票(1, 123)，(3, 122)，然后各自将投票发送给集群中所有机器。接收来自各个服务器的投票。与启动时过程相同。
>
> (3) 处理投票。与启动时过程相同，此时，Server1 将会成为 Leader。
>
> (4) 统计投票。与启动时过程相同。
>
> (5) 改变服务器的状态。与启动时过程相同

# 十三、客户端使用

## zk的自带客户端

```shell
\0. sh zkCli.sh -server  ip:port
	help:帮助
	ls /:查看
	create -s /lqd 123:创建节点
\1. create -s path data acl
	-s 表示节点是否有序
	-e 表示是否为临时节点
	默认情况下，是持久化节点
\2. get path [watch]
	获得指定 path的信息
\3. set path data [version]
	修改节点 path对应的data
\4. delete path [version]
    删除节点

- stat信息
    cversion = 0       子节点的版本号
    aclVersion = 0     表示acl的版本号，修改节点权限
    dataVersion = 1    表示的是当前节点数据的版本号
    czxid    节点被创建时的事务ID
    mzxid   节点最后一次被更新的事务ID
    pzxid    当前节点下的子节点最后一次被修改时的事务ID
    ctime = Sat Aug 05 20:48:26 CST 2017
    mtime = Sat Aug 05 20:48:50 CST 2017
    cZxid = 0x500000015
    ctime = Sat Aug 05 20:48:26 CST 2017
    mZxid = 0x500000016
    mtime = Sat Aug 05 20:48:50 CST 2017
    pZxid = 0x500000015
    cversion = 0
    dataVersion = 1
    aclVersion = 0
    ephemeralOwner = 0x0   创建临时节点的时候，会有一个sessionId 。 该值存储的就是这个sessionid
    dataLength = 3    数据值长度
    numChildren = 0  子节点数
    
- Watcher

zookeeper提供了分布式数据发布/订阅,zookeeper允许客户端向服务器注册一个watcher监听。当服务器端的节点触发指定事件的时候会触发watcher。服务端会向客户端发送一个事件通知.watcher的通知是一次性，一旦触发一次通知后，该watcher就失效

- ACL

zookeeper提供控制节点访问权限的功能，用于有效的保证zookeeper中数据的安全性。避免误操作而导致系统出现重大事故。CREATE /READ/WRITE/DELETE/ADMIN

```

乐观锁的概念：数据库里面有一个 version 字段去控制数据行的版本号.
悲观锁的概念：无论怎样都锁.

## zk java客户端的使用

### java api

1.导入jar包

```xml
<dependency>
    <groupId>org.apache.zookeeper</groupId>
    <artifactId>zookeeper</artifactId>
    <version>3.4.8</version>
</dependency>
```

2.简单介绍权限控制、事件类型、连接状态

```properties
- 权限控制模式
    schema：授权对象
    ip     : 192.168.1.1
    Digest  : username:password
    world  : 开放式的权限控制模式，数据节点的访问权限对所有用户开放。 world:anyone
    super  ：超级用户，可以对zookeeper上的数据节点进行操作
- 事件类型
    NodeCreated  当节点被创建的时候，触发
    NodeChildrenChanged  表示子节点被创建、被删除、子节点数据发生变化
    NodeDataChanged    节点数据发生变化
    NodeDeleted        节点被删除
    None   客户端和服务器端连接状态发生变化的时候，事件类型就是None
- 连接状态
    KeeperStat.Expired  在一定时间内客户端没有收到服务器的通知， 则认为当前的会话已经过期了.
    KeeperStat.Disconnected 断开连接的状态.
    KeeperStat.SyncConnected 客户端和服务器端在某一个节点上建立连接，并且完成一次version、zxid同步.
    KeeperStat.authFailed  授权失败.
```

3.代码

server：

```java
package com.lqd.demo.zookeeper.server;

import com.lqd.demo.zookeeper.server.conf.ZkConfigure;
import org.apache.zookeeper.Watcher;
import org.apache.zookeeper.ZooKeeper;
import javax.annotation.PostConstruct;
import javax.annotation.Resource;
import java.io.IOException;

/**
 * @author lqd
 * @DATE 2018/11/22
 * @Description xxxxx
 */
public class MyZkServer
{
    private ZooKeeper zooKeeper ;

    @Resource
    private ZkConfigure zkConfigure;

    @PostConstruct
    public void init(){
            try
            {
                zooKeeper = new ZooKeeper(
                        zkConfigure.getServers() ,
                        1000*60*60,
                        event -> {
                            Watcher.Event.EventType eventType = event.getType() ;
                            if (event.getState().equals(Watcher.Event.KeeperState.SyncConnected))
                            {
                                System.out.printf(" zk已连接！\n");
                            }
                            if (eventType.equals(Watcher.Event.EventType.NodeCreated))
                            {
                                System.out.printf(" %s 被创建！\n",event.getPath());
                            }
                            else if (eventType.equals(Watcher.Event.EventType.NodeDataChanged))
                            {
                                System.out.printf(" %s 被改变！\n" ,event.getPath());
                            }
                            else if (eventType.equals(Watcher.Event.EventType.NodeDeleted))
                            {
                                System.out.printf(" %s 被删除！\n" ,event.getPath());
                            }
                        });
            } catch (IOException e) {
                e.printStackTrace();
            }
    }

    public ZooKeeper getZooKeeper()
    {
        return  zooKeeper;
    }
}

```

configure：

```java
package com.lqd.demo.zookeeper.server.conf;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Configuration;

/**
 * @author lqd
 * @DATE 2018/11/22
 * @Description xxxxx
 */
@Configuration
@ConfigurationProperties(prefix="spring.zookeeper")
public class ZkConfigure
{
    private String servers;

    public String getServers() {
        return servers;
    }

    public void setServers(String servers) {
        this.servers = servers;
    }
}

```

controller：

```java
package com.lqd.demo.zookeeper.javaApi;

import com.lqd.demo.zookeeper.server.MyZkServer;
import org.apache.zookeeper.*;
import org.apache.zookeeper.data.Stat;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

/**
 * @author lqd
 * @DATE 2018/11/22
 * @Description xxxxx
 */
@RestController
public class ZkController
{
    @Autowired
    private MyZkServer myZkServer;

    @GetMapping("/createZkPath/{path}")
    public void createZkPath(@PathVariable String path) throws KeeperException, InterruptedException
    {
        String zkPath = String.format("/%s",path);
        myZkServer.getZooKeeper().create(zkPath,"1".getBytes(), ZooDefs.Ids.OPEN_ACL_UNSAFE, CreateMode.PERSISTENT) ;
    }

    @GetMapping("/getZkData/{path}")
    public String getZkData(@PathVariable String path) throws KeeperException, InterruptedException
    {
        Stat stat = new Stat() ;
        byte[] data = myZkServer.getZooKeeper().getData(String.format("/%s",path),true,stat) ;
        return String.format("data:%s ",new String(data)) +" , version:"+ stat.getVersion();
    }

    @GetMapping("/deleteZkData/{path}/{version}")
    public String deleteZkData(@PathVariable String path,@PathVariable int version) throws KeeperException, InterruptedException
    {
        myZkServer.getZooKeeper().delete(String.format("/%s",path),version);
        return "delete ok" ;
    }

    @GetMapping("/updateZkData/{path}/{version}/{val}")
    public String updateZkData(@PathVariable String path,@PathVariable int version,@PathVariable String val) throws KeeperException, InterruptedException
    {
        myZkServer.getZooKeeper().setData(String.format("/%s",path),val.getBytes(),version);
        return "modify ok" ;
    }
}

```

application启动：

```java
package com.lqd.demo.zookeeper;

import com.lqd.demo.zookeeper.server.MyZkServer;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;

@SpringBootApplication
public class ZookeeperApplication{

	public static void main(String[] args)
	{
		SpringApplication.run(ZookeeperApplication.class, args);
	}

	@Bean
	public MyZkServer getMyZkServer()
	{
		return new MyZkServer();
	}
}

```

application.properties:

```properties
spring.application.name=demo-zookeeper
server.port=8080
management.endpoint.beans.enabled=true
management.security.enabled=true
spring.zookeeper.servers=192.168.102.112:2189,\
  192.168.102.241:2189,\
  192.168.102.114:2189,\
  192.168.130.32:2189
```

### zkclient

导入jar包 

```xml
 <dependency>
      <groupId>com.101tec</groupId>
      <artifactId>zkclient</artifactId>
      <version>0.10</version>
  </dependency>
```

### curator

1.导入jar包 

```xml
<dependency>
            <groupId>org.apache.curator</groupId>
            <artifactId>curator-framework</artifactId>
            <version>2.11.0</version>
        </dependency>
        <dependency>
            <groupId>org.apache.curator</groupId>
            <artifactId>curator-recipes</artifactId>
            <version>2.11.0</version>
        </dependency>
```

2，

```properties
Curator本身是Netflix公司开源的zookeeper客户端；
curator提供了各种应用场景的实现封装
curator-framework  提供了fluent风格api
curator-replice     提供了实现封装
curator连接的重试策略
ExponentialBackoffRetry()  衰减重试 
RetryNTimes 指定最大重试次数
RetryOneTime 仅重试一次
RetryUnitilElapsed 一直重试知道规定的时间
```

- 异步操作

  ```java
  ExecutorService service= Executors.newFixedThreadPool(1);
          CountDownLatch countDownLatch=new CountDownLatch(1);
          try {
              curatorFramework.create().creatingParentsIfNeeded().withMode(CreateMode.EPHEMERAL).
                      inBackground(new BackgroundCallback() {
                          @Override
                          public void processResult(CuratorFramework curatorFramework, CuratorEvent curatorEvent) throws Exception {
                              System.out.println(Thread.currentThread().getName()+"->resultCode:"+curatorEvent.getResultCode()+"->"
                              +curatorEvent.getType());
                              countDownLatch.countDown();
                          }
                      },service).forPath("/mic","123".getBytes());
          } catch (Exception e) {
              e.printStackTrace();
          }
          countDownLatch.await();
          service.shutdown();
  ```

- 独有的事务操作

  ```java
   try {
              Collection<CuratorTransactionResult> resultCollections=curatorFramework.inTransaction().create().forPath("/trans","111".getBytes()).and().
                      setData().forPath("/curator","111".getBytes()).and().commit();
              for (CuratorTransactionResult result:resultCollections){
                  System.out.println(result.getForPath()+"->"+result.getType());
              }
          } catch (Exception e) {
              e.printStackTrace();
          }
  ```

- 事务监听

  ```java
  /**
       * 三种watcher来做节点的监听
       * pathcache   监视一个路径下子节点的创建、删除、节点数据更新
       * NodeCache   监视一个节点的创建、更新、删除
       * TreeCache   pathcaceh+nodecache 的合体（监视路径下的创建、更新、删除事件），
       * 缓存路径下的所有子节点的数据
       */
  ```

# 十四、事件机制

​	Watcher 监听机制是 Zookeeper 中非常重要的特性，我们基于 zookeeper 上创建的节点，可以对这些节点绑定监听事件，比如可以监听节点数据变更、节点删除、子节点状态变更等事件，通过这个事件机制，可以基于 zookeeper实现分布式锁、集群管理等功能。

​	watcher 特性：当数据发生变化的时候， zookeeper 会产生一个 watcher 事件，并且会发送到客户端。但是客户端只会收到一次通知。如果后续这个节点再次发生变化，那么之前设置 watcher 的客户端不会再次收到消息。（watcher 是一次性的操作）。 可以通过循环监听去达到永久监听效果。

## 如何注册事件机制

通过这三个操作来绑定事件 ：getData、Exists、getChildren 

如何触发事件？ 凡是事务类型的操作，都会触发监听事件。create /delete /setData

watcher 事件类型

> ​	None (-1), **客户端链接状态发生变化的时候，会收到 none 的事件**
>
> ​	NodeCreated (1), 创建节点的事件。 比如 zk-persis-mic
>
> ​	NodeDeleted (2), 删除节点的事件
>
> ​	NodeDataChanged (3), 节点数据发生变更
>
> ​	NodeChildrenChanged (4); 子节点被创建、被删除、会发生事件触发

## 事件的实现原理

![1542868571555](C:\Users\lqd\AppData\Roaming\Typora\typora-user-images\1542868571555.png)

![1542868629372](C:\Users\lqd\AppData\Roaming\Typora\typora-user-images\1542868629372.png)

![1542868641953](C:\Users\lqd\AppData\Roaming\Typora\typora-user-images\1542868641953.png)

