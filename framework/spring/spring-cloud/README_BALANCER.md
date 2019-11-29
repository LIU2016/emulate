##### Balancer超时时间设置

###### 调用feign的微服务

```java
ReflectiveFeign FeignInvocationHandler 代理每个请求
-------------------------------------------------

FeignInvocationHandler(Target target, Map<Method, MethodHandler> dispatch) {
      this.target = checkNotNull(target, "target");
      this.dispatch = checkNotNull(dispatch, "dispatch for %s", target);
    }

    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
      if ("equals".equals(method.getName())) {
        try {
          Object
              otherHandler =
              args.length > 0 && args[0] != null ? Proxy.getInvocationHandler(args[0]) : null;
          return equals(otherHandler);
        } catch (IllegalArgumentException e) {
          return false;
        }
      } else if ("hashCode".equals(method.getName())) {
        return hashCode();
      } else if ("toString".equals(method.getName())) {
        return toString();
      }
      return dispatch.get(method).invoke(args);
    }

```

###### http client的超时属性

```java
RetryableFeignLoadBalancer
-------------------------------------------------
@Override
	public RibbonResponse execute(final RibbonRequest request, IClientConfig configOverride)
			throws IOException {
		final Request.Options options;
		if (configOverride != null) {
			options = new Request.Options(
					configOverride.get(CommonClientConfigKey.ConnectTimeout,
							this.connectTimeout),
					(configOverride.get(CommonClientConfigKey.ReadTimeout,
							this.readTimeout)));
		}
		else {
			options = new Request.Options(this.connectTimeout, this.readTimeout);
		}
		final LoadBalancedRetryPolicy retryPolicy = loadBalancedRetryPolicyFactory.create(this.getClientName(), this);
		RetryTemplate retryTemplate = new RetryTemplate();
		retryTemplate.setRetryPolicy(retryPolicy == null ? new NeverRetryPolicy()
				: new FeignRetryPolicy(request.toHttpRequest(), retryPolicy, this, this.getClientName()));
		return retryTemplate.execute(new RetryCallback<RibbonResponse, IOException>() {
			@Override
			public RibbonResponse doWithRetry(RetryContext retryContext) throws IOException {
				Request feignRequest = null;
				//on retries the policy will choose the server and set it in the context
				//extract the server and update the request being made
				if(retryContext instanceof LoadBalancedRetryContext) {
					ServiceInstance service = ((LoadBalancedRetryContext)retryContext).getServiceInstance();
					if(service != null) {
						feignRequest = ((RibbonRequest)request.replaceUri(reconstructURIWithServer(new Server(service.getHost(), service.getPort()), request.getUri()))).toRequest();
					}
				}
				if(feignRequest == null) {
					feignRequest = request.toRequest();
				}
				Response response = request.client().execute(feignRequest, options);
				if(retryPolicy.retryableStatusCode(response.status())) {
					throw new RetryableStatusCodeException(RetryableFeignLoadBalancer.this.getClientName(), response.status());
				}
				return new RibbonResponse(request.getUri(), response);
			}
		});
	}
```

###### 生成http client请求对象

```java
OkHttpClient 若使用了okhttp，则进入这里
-----------------------------------------------

@Override
  public feign.Response execute(feign.Request input, feign.Request.Options options)
      throws IOException {
    okhttp3.OkHttpClient requestScoped;
    //若设置了options的超时属性，就按这个来，若没设置就按默认的来处理
    if (delegate.connectTimeoutMillis() != options.connectTimeoutMillis()
        || delegate.readTimeoutMillis() != options.readTimeoutMillis()) {
       requestScoped = delegate.newBuilder()
               .connectTimeout(options.connectTimeoutMillis(), TimeUnit.MILLISECONDS)
               .readTimeout(options.readTimeoutMillis(), TimeUnit.MILLISECONDS)
               .build();
    } else {
      requestScoped = delegate;
    }
    Request request = toOkHttpRequest(input);
    Response response = requestScoped.newCall(request).execute();
    return toFeignResponse(response).toBuilder().request(input).build();
  }
```

###### 超时异常

```java
o.s.a.i.SimpleAsyncUncaughtExceptionHandler - [SimpleAsyncUncaughtExceptionHandler.java:37] - Unexpected error occurred invoking async method 'void'.
feign.RetryableException: timeout executing POST
```

##### DynamicServerListLoadBalancer 、DiscoveryEnabledNIWSServerList

动态调整请求地址以及Eureka注册地址处理

```
 void restOfInit(IClientConfig clientConfig) {
        boolean primeConnection = this.isEnablePrimingConnections();
        // turn this off to avoid duplicated asynchronous priming done in BaseLoadBalancer.setServerList()
        this.setEnablePrimingConnections(false);
        enableAndInitLearnNewServersFeature();

        updateListOfServers();
        if (primeConnection && this.getPrimeConnections() != null) {
            this.getPrimeConnections()
                    .primeConnections(getReachableServers());
        }
        this.setEnablePrimingConnections(primeConnection);
        LOGGER.info("DynamicServerListLoadBalancer for client {} initialized: {}", clientConfig.getClientName(), this.toString());
    }
```