[TOC]

## Spring MVC设计原理

### Spring MVC 请求处理流程

引用 Spring in Action 上的一张图来说明了 SpringMVC 的核心组件和请求处理流程

![1544089867128](C:\Users\lqd\AppData\Roaming\Typora\typora-user-images\1544089867128.png)

DispatcherServlet 是 SpringMVC 中的前端控制器(Front Controller),负责接收 Request并将 Request 转发给对应的处理组件.

HanlerMapping 是 SpringMVC 中完成 url 到 Controller 映射的组件.DispatcherServlet接收 Request,然后从 HandlerMapping 查找处理 Request 的 Controller.



Cntroller 处理 Request,并返回 ModelAndView 对象,Controller 是 SpringMVC 中负责处理 Request 的组件(类似于 Struts2 中的 Action),ModelAndView 是封装结果视图的组件.

④ ⑤ ⑥：视图解析器解析 ModelAndView 对象并返回对应的视图给客户端.

### Spring MVC 的工作机制

在容器初始化时会建立所有 url 和 Controller 的对应关系,保存到 Map<url,Controller>中.

Tomcat 启动时会通知 Spring 初始化容器(加载 Bean 的定义信息和初始化所有单例 Bean),然后SpringMVC 会遍历容器中的 Bean,获取每一个 Controller 中的所有方法访问的 url,然后将 url 和Controller 保存到一个 Map 中;

这样就可以根据 Request 快速定位到 Controller,因为最终处理 Request 的是 Controller 中的方法,Map 中只保留了 url 和 Controller 中的对应关系,所以要根据 Request 的 url 进一步确认Controller 中 的 Method, 这 一 步 工 作 的 原 理 就 是 拼 接 Controller 的 url(Controller 上@RequestMapping 的值)和方法的 url(Method 上@RequestMapping 的值),与 request 的 url 进行匹配,找到匹配的那个方法;

确定处理请求的Method后,接下来的任务就是参数绑定,把Request中参数绑定到方法的形式参数上,这一步是整个请求处理过程中最复杂的一个步骤。SpringMVC 提供了两种 Request 参数与方法形参的绑定方法:

① 通过注解进行绑定,@RequestParam
② 通过参数名称进行绑定.

使用注解进行绑定,我们只要在方法参数前面声明@RequestParam("a"),就可以将 Request 中参数 a 的值绑定到方法的该参数上.

使用参数名称进行绑定的前提是必须要获取方法中参数的名称,Java反射只提供了获取方法的参数的类型,并没有提供获取参数名称的方法.

SpringMVC 解决这个问题的方法是用 asm 框架读取字节码文件,来获取方法的参数称.asm 框架是一个字节码操作框架,关于 asm 更多介绍可以参考它的官网。个人建议,使用注解来完成参数绑定,这样就可以省去 asm 框架的读取字节码的操作。

### Spring MVC 源码分析

web项目一般首先通过org.springframework.web.context.ContextLoaderListener对容器初始化。web.xml配置：

```xml
<context-param>
    <param-name>contextConfigLocation</param-name>
    <param-value>classpath*:spring-base.xml</param-value>
</context-param>
```

```java
/**
 * Initialize Spring's web application context for the given servlet context,
 * using the application context provided at construction time, or creating a new one
 * according to the "{@link #CONTEXT_CLASS_PARAM contextClass}" and
 * "{@link #CONFIG_LOCATION_PARAM contextConfigLocation}" context-params.
 * @param servletContext current servlet context
 * @return the new WebApplicationContext
 * @see #ContextLoader(WebApplicationContext)
 * @see #CONTEXT_CLASS_PARAM
 * @see #CONFIG_LOCATION_PARAM
 */
public WebApplicationContext initWebApplicationContext(ServletContext servletContext) {
   if (servletContext.getAttribute(WebApplicationContext.ROOT_WEB_APPLICATION_CONTEXT_ATTRIBUTE) != null) {
      throw new IllegalStateException(
            "Cannot initialize context because there is already a root application context present - " +
            "check whether you have multiple ContextLoader* definitions in your web.xml!");
   }

   servletContext.log("Initializing Spring root WebApplicationContext");
   Log logger = LogFactory.getLog(ContextLoader.class);
   if (logger.isInfoEnabled()) {
      logger.info("Root WebApplicationContext: initialization started");
   }
   long startTime = System.currentTimeMillis();

   try {
      // Store context in local instance variable, to guarantee that
      // it is available on ServletContext shutdown.
      if (this.context == null) {
         this.context = createWebApplicationContext(servletContext);
      }
      if (this.context instanceof ConfigurableWebApplicationContext) {
         ConfigurableWebApplicationContext cwac = (ConfigurableWebApplicationContext) this.context;
         if (!cwac.isActive()) {
            // The context has not yet been refreshed -> provide services such as
            // setting the parent context, setting the application context id, etc
            if (cwac.getParent() == null) {
               // The context instance was injected without an explicit parent ->
               // determine parent for root web application context, if any.
               ApplicationContext parent = loadParentContext(servletContext);
               cwac.setParent(parent);
            }
            configureAndRefreshWebApplicationContext(cwac, servletContext);
         }
      }
      servletContext.setAttribute(WebApplicationContext.ROOT_WEB_APPLICATION_CONTEXT_ATTRIBUTE, this.context);

      ClassLoader ccl = Thread.currentThread().getContextClassLoader();
      if (ccl == ContextLoader.class.getClassLoader()) {
         currentContext = this.context;
      }
      else if (ccl != null) {
         currentContextPerThread.put(ccl, this.context);
      }

      if (logger.isInfoEnabled()) {
         long elapsedTime = System.currentTimeMillis() - startTime;
         logger.info("Root WebApplicationContext initialized in " + elapsedTime + " ms");
      }

      return this.context;
   }
   catch (RuntimeException | Error ex) {
      logger.error("Context initialization failed", ex);
      servletContext.setAttribute(WebApplicationContext.ROOT_WEB_APPLICATION_CONTEXT_ATTRIBUTE, ex);
      throw ex;
   }
}
```

其中configureAndRefreshWebApplicationContext(cwac, servletContext);用来加载上下文配置内容，例如扫描启动等。

```xml
<?xml version="1.0" encoding="utf-8" ?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
        http://www.springframework.org/schema/beans/spring-beans.xsd http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context.xsd">

    <context:annotation-config></context:annotation-config>
    <context:component-scan base-package="com.lqd.**.**"></context:component-scan>

</beans>
```

```java
// Register annotation config processors, if necessary.
boolean annotationConfig = true;
if (element.hasAttribute(ANNOTATION_CONFIG_ATTRIBUTE)) {
   annotationConfig = Boolean.valueOf(element.getAttribute(ANNOTATION_CONFIG_ATTRIBUTE));
}
```

什么源码解释了为什么要加annotation-config，才能将注解的类注册到ioc容器。

**要注意的是**：springmvc的扫描器要和DispatcherServlet的init-param的configureApplicationcontext放一起？为什么？

然后我们根据工作机制中三部分来分析 SpringMVC 的源代码.。

其一,ApplicationContext 初始化时建立所有 url 和 Controller 类的对应关系(用 Map 保存);
其二,根据请求 url 找到对应的 Controller,并从 Controller 中找到处理请求的方法;
其三,request 参数绑定到方法的形参,执行方法处理请求,并返回结果视图.

第一步、建立 Map<urls,Controller>的关系，我们首先看第一个步骤,也就是建立 Map<url,Controller>关系的部分.入口类为**RequestMappingHandlerMapping**的 afterPropertiesSet方法.

afterPropertiesSet方法中核心 部 分 就 是 初 始 化 容 器 initHandlerMethods(), 子 类AbstractHandlerMethodMapping.processCandidateBean 实现了该方法,所以我们直接看子类中的初始化容器方法:

```java
/**
	 * Scan beans in the ApplicationContext, detect and register handler methods.
	 * @see #getCandidateBeanNames()
	 * @see #processCandidateBean
	 * @see #handlerMethodsInitialized
	 */
	protected void initHandlerMethods() {
		for (String beanName : getCandidateBeanNames()) {
			if (!beanName.startsWith(SCOPED_TARGET_NAME_PREFIX)) {
				processCandidateBean(beanName);
			}
		}
		handlerMethodsInitialized(getHandlerMethods());
	}

	/**
	 * Determine the names of candidate beans in the application context.
	 * @since 5.1
	 * @see #setDetectHandlerMethodsInAncestorContexts
	 * @see BeanFactoryUtils#beanNamesForTypeIncludingAncestors
	 */
	protected String[] getCandidateBeanNames() {
		return (this.detectHandlerMethodsInAncestorContexts ?
				BeanFactoryUtils.beanNamesForTypeIncludingAncestors(obtainApplicationContext(), Object.class) :
				obtainApplicationContext().getBeanNamesForType(Object.class));
	}

	/**
	 * Determine the type of the specified candidate bean and call
	 * {@link #detectHandlerMethods} if identified as a handler type.
	 * <p>This implementation avoids bean creation through checking
	 * {@link org.springframework.beans.factory.BeanFactory#getType}
	 * and calling {@link #detectHandlerMethods} with the bean name.
	 * @param beanName the name of the candidate bean
	 * @since 5.1
	 * @see #isHandler
	 * @see #detectHandlerMethods
	 */
	protected void processCandidateBean(String beanName) {
		Class<?> beanType = null;
		try {
			beanType = obtainApplicationContext().getType(beanName);
		}
		catch (Throwable ex) {
			// An unresolvable bean type, probably from a lazy bean - let's ignore it.
			if (logger.isTraceEnabled()) {
				logger.trace("Could not resolve type for bean '" + beanName + "'", ex);
			}
		}
		if (beanType != null && isHandler(beanType)) {
			detectHandlerMethods(beanName);
		}
	}
```

到这里 HandlerMapping 组件就已经建立所有 url 和 Controller 的对应关系。

第二步、根据访问 url 找到对应的 Controller 中处理请求的方法下面我们开始分析第二个步骤,第二个步骤是由请求触发的,所以入口为 DispatcherServlet 的核心方法为doService(),doService()中的核心逻辑由doDispatch()实现,我们查看doDispatch()的源代码.

```java
/** 中央控制器 , 控制请求的转发 **/
protected void doDispatch(HttpServletRequest request, HttpServletResponse response) throws Exception {
HttpServletRequest processedRequest = request;
HandlerExecutionChain mappedHandler = null;
boolean multipartRequestParsed = false;
WebAsyncManager asyncManager = WebAsyncUtils.getAsyncManager(request);
try {
ModelAndView mv = null;
Exception dispatchException = null;
try {
// 1.检查是否是文件上传的请求
processedRequest = checkMultipart(request);
multipartRequestParsed = (processedRequest != request);
// 2.取得处理当前请求的 Controller,这里也称为 hanlder,处理器,
// 第一个步骤的意义就在这里体现了.这里并不是直接返回 Controller,
// 而是返回的 HandlerExecutionChain 请求处理器链对象,
// 该对象封装了 handler 和 interceptors.
mappedHandler = getHandler(processedRequest);
// 如果 handler 为空,则返回 404
if (mappedHandler == null) {
noHandlerFound(processedRequest, response);
return;
}
//3. 获取处理 request 的处理器适配器 handler adapter
HandlerAdapter ha = getHandlerAdapter(mappedHandler.getHandler());
// 处理 last-modified 请求头
String Method = request.getMethod();
boolean isGet = "GET".equals(Method);
if (isGet || "HEAD".equals(Method)) {
long lastModified = ha.getLastModified(request, mappedHandler.getHandler());
if (logger.isDebugEnabled()) {
logger.debug("Last-Modified value for [" + getRequestUri(request) + "] is: " + lastModified);
}
if (new ServletWebRequest(request, response).checkNotModified(lastModified) && isGet) {
return;
}
}
if (!mappedHandler.applyPreHandle(processedRequest, response)) {
return;
}
// 4.实际的处理器处理请求,返回结果视图对象
mv = ha.handle(processedRequest, response, mappedHandler.getHandler());
if (asyncManager.isConcurrentHandlingStarted()) {
return;
}
// 结果视图对象的处理
applyDefaultViewName(processedRequest, mv);
mappedHandler.applyPostHandle(processedRequest, response, mv);
}
catch (Exception ex) {
dispatchException = ex;
}
catch (Throwable err) {
dispatchException = new NestedServletException("Handler dispatch failed", err);
}
processDispatchResult(processedRequest, response, mappedHandler, mv, dispatchException);
}
catch (Exception ex) {
triggerAfterCompletion(processedRequest, response, mappedHandler, ex);
}
catch (Throwable err) {
triggerAfterCompletion(processedRequest, response, mappedHandler,
new NestedServletException("Handler processing failed", err));
}
finally {
if (asyncManager.isConcurrentHandlingStarted()) {
if (mappedHandler != null) {
// 请求成功响应之后的方法
mappedHandler.applyAfterConcurrentHandlingStarted(processedRequest, response);
}
}
else {
if (multipartRequestParsed) {
cleanupMultipart(processedRequest);
}
}
}
}
```

第 2 步 :getHandler(processedRequest) 方 法 实 际 上 就 是 从 HandlerMapping 中 找 到 url 和Controller 的对应关系.这也就是第一个步骤:建立 Map<url,Controller>的意义.我们知道,最终处理 Request 的是 Controller 中的方法,我们现在只是知道了 Controller,还要进一步确认Controller 中处理 Request 的方法.由于下面的步骤和第三个步骤关系更加紧密,直接转到第三个步骤.

第三步、反射调用处理请求的方法，返回结果视图

上面的方法中,第 2 步其实就是从第一个步骤中的 Map<urls,beanName>中取得 Controller,然后经过拦截器的预处理方法,到最核心的部分--第5步调用Controller的方法处理请求.在第2步中我们可以知道处理 Request 的 Controller,第 5 步就是要根据 url 确定 Controller 中处理请求的方法,然后通过反射获取该方法上的注解和参数,解析方法和参数上的注解,最后反射调用方法获取ModelAndView结果视图。因为上面采用注解 url 形式说明的.第 5 步调用的就是 RequestMappingHandlerAdapter的 handle()中的核心逻辑由 handleInternal(request, response, handler)实现。

```java
@Override
protected ModelAndView handleInternal(HttpServletRequest request,
HttpServletResponse response, HandlerMethod handlerMethod) throws Exception {
ModelAndView mav;
checkRequest(request);
if (this.synchronizeOnSession) {
HttpSession session = request.getSession(false);
if (session != null) {
Object mutex = WebUtils.getSessionMutex(session);
synchronized (mutex) {
mav = invokeHandlerMethod(request, response, handlerMethod);
}
}
else {
mav = invokeHandlerMethod(request, response, handlerMethod);
}
}
else {
mav = invokeHandlerMethod(request, response, handlerMethod);
}
if (!response.containsHeader(HEADER_CACHE_CONTROL)) {
if (getSessionAttributesHandler(handlerMethod).hasSessionAttributes()) {
applyCacheSeconds(response, this.cacheSecondsForSessionAttributeHandlers);
}
else {
prepareResponse(response);
}
}
return mav;
}
```

这一部分的核心就在 2 和 4 了.先看第 2 步,通过 Request 找 Controller 的处理方法.实际上就是拼接Controller 的 url 和方法的 url,与 Request 的 url 进行匹配,找到匹配的方法.

```java
/** 根据 url 获取处理请求的方法 **/
@Override
protected HandlerMethod getHandlerInternal(HttpServletRequest request) throws Exception {
// 如果请求 url 为,http://localhost:8080/web/hello.json, 则 lookupPath=web/hello.json
String lookupPath = getUrlPathHelper().getLookupPathForRequest(request);
if (logger.isDebugEnabled()) {
logger.debug("Looking up handler method for path " + lookupPath);
}
this.mappingRegistry.acquireReadLock();
try {
// 遍历 Controller 上的所有方法,获取 url 匹配的方法
HandlerMethod handlerMethod = lookupHandlerMethod(lookupPath, request);
if (logger.isDebugEnabled()) {
if (handlerMethod != null) {
logger.debug("Returning handler method [" + handlerMethod + "]");
}
else {
logger.debug("Did not find handler method for [" + lookupPath + "]");
}
}
return (handlerMethod != null ? handlerMethod.createWithResolvedBean() : null);
}
finally {
this.mappingRegistry.releaseReadLock();
}
}
```

通过上面的代码,已经可以找到处理 Request 的 Controller 中的方法了,现在看如何解析该方法上的参数,并调用该方法。也就是执行方法这一步。执行方法这一步最重要的就是获取方法的参数,然后我们就可以反射调用方法了。

invocableMethod.invokeAndHandle最终要实现的目的就是:完成Request中的参数和方法参数上数据的绑定。
SpringMVC 中提供两种 Request 参数到方法中参数的绑定方式:

① 通过注解进行绑定,@RequestParam
② 通过参数名称进行绑定.

使用注解进行绑定,我们只要在方法参数前面声明@RequestParam("a"),就可以将 request 中参数 a 的值绑定到方法的该参数上.使用参数名称进行绑定的前提是必须要获取方法中参数的名称,Java反射只提供了获取方法的参数的类型,并没有提供获取参数名称的方法.SpringMVC 解决这个问题的方法是用 asm 框架读取字节码文件,来获取方法的参数名称.asm 框架是一个字节码操作框架,关于 asm 更多介绍可以参考它的官网.个人建议,使用注解来完成参数绑定,这样就可以省去 asm 框架的读取字节码的操作.

```java
@Nullable
public Object invokeForRequest(NativeWebRequest request, @Nullable ModelAndViewContainer mavContainer,
Object... providedArgs) throws Exception {
Object[] args = getMethodArgumentValues(request, mavContainer, providedArgs);
if (logger.isTraceEnabled()) {
logger.trace("Invoking '" + ClassUtils.getQualifiedMethodName(getMethod(), getBeanType()) +
"' with arguments " + Arrays.toString(args));
}
Object returnValue = doInvoke(args);
if (logger.isTraceEnabled()) {
logger.trace("Method [" + ClassUtils.getQualifiedMethodName(getMethod(), getBeanType()) +
"] returned [" + returnValue + "]");
}
return returnValue;
}
private Object[] getMethodArgumentValues(NativeWebRequest request, @Nullable ModelAndViewContainer mavContainer,
Object... providedArgs) throws Exception {
MethodParameter[] parameters = getMethodParameters();
Object[] args = new Object[parameters.length];
for (int i = 0; i < parameters.length; i++) {
MethodParameter parameter = parameters[i];
parameter.initParameterNameDiscovery(this.parameterNameDiscoverer);
args[i] = resolveProvidedArgument(parameter, providedArgs);
if (args[i] != null) {
continue;
}
if (this.argumentResolvers.supportsParameter(parameter)) {
try {
args[i] = this.argumentResolvers.resolveArgument(
parameter, mavContainer, request, this.dataBinderFactory);
continue;
}
catch (Exception ex) {
if (logger.isDebugEnabled()) {
logger.debug(getArgumentResolutionErrorMessage("Failed to resolve", i), ex);
}
throw ex;
}
}
if (args[i] == null) {
throw new IllegalStateException("Could not resolve method parameter at index " +
parameter.getParameterIndex() + " in " + parameter.getExecutable().toGenericString() +
": " + getArgumentResolutionErrorMessage("No suitable resolver for", i));
}
}
return args;
}
```

关于 asm 框架获取方法参数的部分,这里就不再进行分析了.感兴趣的话自己去就能看到这个过程.到这里,方法的参数值列表也获取到了,就可以直接进行方法的调用了.整个请求过程中最复杂的一步就是在这里了.ok,到这里整个请求处理过程的关键步骤都分析完了.理解了 SpringMVC 中的请求处理流程,整个代码还是比较清晰的.

#### 工具默认初始化

```java
/**
	 * Name of the class path resource (relative to the DispatcherServlet class)
	 * that defines DispatcherServlet's default strategy names.
	 */
	private static final String DEFAULT_STRATEGIES_PATH = "DispatcherServlet.properties";

static {
   // Load default strategy implementations from properties file.
   // This is currently strictly internal and not meant to be customized
   // by application developers.
   try {
      ClassPathResource resource = new ClassPathResource(DEFAULT_STRATEGIES_PATH, DispatcherServlet.class);
      defaultStrategies = PropertiesLoaderUtils.loadProperties(resource);
   }
   catch (IOException ex) {
      throw new IllegalStateException("Could not load '" + DEFAULT_STRATEGIES_PATH + "': " + ex.getMessage());
   }
}
```

```
# Default implementation classes for DispatcherServlet's strategy interfaces.
# Used as fallback when no matching beans are found in the DispatcherServlet context.
# Not meant to be customized by application developers.

org.springframework.web.servlet.LocaleResolver=org.springframework.web.servlet.i18n.AcceptHeaderLocaleResolver

org.springframework.web.servlet.ThemeResolver=org.springframework.web.servlet.theme.FixedThemeResolver

org.springframework.web.servlet.HandlerMapping=org.springframework.web.servlet.handler.BeanNameUrlHandlerMapping,\
   org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerMapping

org.springframework.web.servlet.HandlerAdapter=org.springframework.web.servlet.mvc.HttpRequestHandlerAdapter,\
   org.springframework.web.servlet.mvc.SimpleControllerHandlerAdapter,\
   org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter

org.springframework.web.servlet.HandlerExceptionResolver=org.springframework.web.servlet.mvc.method.annotation.ExceptionHandlerExceptionResolver,\
   org.springframework.web.servlet.mvc.annotation.ResponseStatusExceptionResolver,\
   org.springframework.web.servlet.mvc.support.DefaultHandlerExceptionResolver

org.springframework.web.servlet.RequestToViewNameTranslator=org.springframework.web.servlet.view.DefaultRequestToViewNameTranslator

org.springframework.web.servlet.ViewResolver=org.springframework.web.servlet.view.InternalResourceViewResolver

org.springframework.web.servlet.FlashMapManager=org.springframework.web.servlet.support.SessionFlashMapManager

```

默认加载配置文件中的handlerMapping，handlerAdapter，viewResolver等工具。

```java
@Override
protected void onRefresh(ApplicationContext context) {
   initStrategies(context);
}

/**
 * Initialize the strategy objects that this servlet uses.
 * <p>May be overridden in subclasses in order to initialize further strategy objects.
 */
protected void initStrategies(ApplicationContext context) {
   initMultipartResolver(context);
   initLocaleResolver(context);
   initThemeResolver(context);
   initHandlerMappings(context);
   initHandlerAdapters(context);
   initHandlerExceptionResolvers(context);
   initRequestToViewNameTranslator(context);
   initViewResolvers(context);
   initFlashMapManager(context);
}
```

##### initViewResolvers

```java
/**
 * Initialize the ViewResolvers used by this class.
 * <p>If no ViewResolver beans are defined in the BeanFactory for this
 * namespace, we default to InternalResourceViewResolver.
 */
private void initViewResolvers(ApplicationContext context) {
   this.viewResolvers = null;

   if (this.detectAllViewResolvers) {
      // Find all ViewResolvers in the ApplicationContext, including ancestor contexts.
      Map<String, ViewResolver> matchingBeans =
            BeanFactoryUtils.beansOfTypeIncludingAncestors(context, ViewResolver.class, true, false);
      if (!matchingBeans.isEmpty()) {
         this.viewResolvers = new ArrayList<>(matchingBeans.values());
         // We keep ViewResolvers in sorted order.
         AnnotationAwareOrderComparator.sort(this.viewResolvers);
      }
   }
   else {
      try {
         ViewResolver vr = context.getBean(VIEW_RESOLVER_BEAN_NAME, ViewResolver.class);
         this.viewResolvers = Collections.singletonList(vr);
      }
      catch (NoSuchBeanDefinitionException ex) {
         // Ignore, we'll add a default ViewResolver later.
      }
   }

   // Ensure we have at least one ViewResolver, by registering
   // a default ViewResolver if no other resolvers are found.
   if (this.viewResolvers == null) {
      this.viewResolvers = getDefaultStrategies(context, ViewResolver.class);
      if (logger.isTraceEnabled()) {
         logger.trace("No ViewResolvers declared for servlet '" + getServletName() +
               "': using default strategies from DispatcherServlet.properties");
      }
   }
}
```

从上述代码可以看出：首先在beanDefinitionNames容器中查找是否有ViewResolver.class类型的bean，有则返回。若没有则使用默认的。

##### InternalResourceViewResolver

```java
/**
 * Prefix for special view names that specify a redirect URL (usually
 * to a controller after a form has been submitted and processed).
 * Such view names will not be resolved in the configured default
 * way but rather be treated as special shortcut.
 */
public static final String REDIRECT_URL_PREFIX = "redirect:";

/**
 * Prefix for special view names that specify a forward URL (usually
 * to a controller after a form has been submitted and processed).
 * Such view names will not be resolved in the configured default
 * way but rather be treated as special shortcut.
 */
public static final String FORWARD_URL_PREFIX = "forward:";


@Nullable
private Class<?> viewClass;

private String prefix = "";

private String suffix = "";

@Nullable
private String contentType;

private boolean redirectContextRelative = true;

private boolean redirectHttp10Compatible = true;

@Nullable
private String[] redirectHosts;

@Nullable
private String requestContextAttribute;

/** Map of static attributes, keyed by attribute name (String). */
private final Map<String, Object> staticAttributes = new HashMap<>();

@Nullable
private Boolean exposePathVariables;

@Nullable
private Boolean exposeContextBeansAsAttributes;

@Nullable
private String[] exposedContextBeanNames;

@Nullable
private String[] viewNames;

private int order = Ordered.LOWEST_PRECEDENCE;
```

###### viewClass

InternalResourceView为其中一个实现，他是默认的。他是一个forwards的view

```java
/**
 * Wrapper for a JSP or other resource within the same web application.
 * Exposes model objects as request attributes and forwards the request to
 * the specified resource URL using a {@link javax.servlet.RequestDispatcher}.
 *
 * <p>A URL for this view is supposed to specify a resource within the web
 * application, suitable for RequestDispatcher's {@code forward} or
 * {@code include} method.
 *
 * <p>If operating within an already included request or within a response that
 * has already been committed, this view will fall back to an include instead of
 * a forward. This can be enforced by calling {@code response.flushBuffer()}
 * (which will commit the response) before rendering the view.
 *
 * <p>Typical usage with {@link InternalResourceViewResolver} looks as follows,
 * from the perspective of the DispatcherServlet context definition:
 *
 * <pre class="code">&lt;bean id="viewResolver" class="org.springframework.web.servlet.view.InternalResourceViewResolver"&gt;
 *   &lt;property name="prefix" value="/WEB-INF/jsp/"/&gt;
 *   &lt;property name="suffix" value=".jsp"/&gt;
 * &lt;/bean&gt;</pre>
 *
 * Every view name returned from a handler will be translated to a JSP
 * resource (for example: "myView" -> "/WEB-INF/jsp/myView.jsp"), using
 * this view class by default.
 *
 * @author Rod Johnson
 * @author Juergen Hoeller
 * @author Rob Harrop
 * @see javax.servlet.RequestDispatcher#forward
 * @see javax.servlet.RequestDispatcher#include
 * @see javax.servlet.ServletResponse#flushBuffer
 * @see InternalResourceViewResolver
 * @see JstlView
 */
```

从InternalResourceViewResolver类中可以看到：当存在javax.servlet.jsp.jstl.core.Config类的时候，将采用JstlView作为viewClass

```java
private static final boolean jstlPresent = ClassUtils.isPresent(
      "javax.servlet.jsp.jstl.core.Config", InternalResourceViewResolver.class.getClassLoader());
public InternalResourceViewResolver() {
		Class<?> viewClass = requiredViewClass();
		if (InternalResourceView.class == viewClass && jstlPresent) {
			viewClass = JstlView.class;
		}
		setViewClass(viewClass);
	}
```

##### ContentNegotiatingViewResolver

这是个综合处理的resolver，根据请求的contenttpye返回对应的view。该类也继承了initialializeBean

```xml
<bean class="org.springframework.web.servlet.view.ContentNegotiatingViewResolver">
    <property name="viewResolvers">
        <list>
            <bean id="internalResourceViewResolver" class="org.springframework.web.servlet.view.InternalResourceViewResolver">
                <property name="viewClass" value="org.springframework.web.servlet.view.JstlView"></property>
                <property name="prefix" value="/WEB-INF/pages/"></property>
                <property name="suffix" value=".jsp"></property>
            </bean>
        </list>
    </property>
</bean>
```

```java
@Nullable
private View getBestView(List<View> candidateViews, List<MediaType> requestedMediaTypes, RequestAttributes attrs) {
   for (View candidateView : candidateViews) {
      if (candidateView instanceof SmartView) {
         SmartView smartView = (SmartView) candidateView;
         if (smartView.isRedirectView()) {
            return candidateView;
         }
      }
   }
   for (MediaType mediaType : requestedMediaTypes) {
      for (View candidateView : candidateViews) {
         if (StringUtils.hasText(candidateView.getContentType())) {
            MediaType candidateContentType = MediaType.parseMediaType(candidateView.getContentType());
            if (mediaType.isCompatibleWith(candidateContentType)) {
               if (logger.isDebugEnabled()) {
                  logger.debug("Selected '" + mediaType + "' given " + requestedMediaTypes);
               }
               attrs.setAttribute(View.SELECTED_CONTENT_TYPE, mediaType, RequestAttributes.SCOPE_REQUEST);
               return candidateView;
            }
         }
      }
   }
   return null;
}
```

#### 怎么根据媒体类型找到view

以ContentNegotiatingViewResovler为例，一般流程：

1，ViewResovler初始化会获取mediaType获取的策略。

2，ViewResovler根据请求的路径、请求头accept、参数等获取mediaType集合。

3，ViewResovler根据mediaType集合获取view。

一般情况下，ViewResovler只是配置了jstlview，可以在默认的defaultview上配置其他view。当然也可以配置多个viewResovler。

ContentNegotiatingViewResovler实现上面的大部分的源码如下：

入口从resolveViewName方法来。只是resovler处理请求的入口方法，实现了ViewResolver接口。

``` java
@Override
	@Nullable
	public View resolveViewName(String viewName, Locale locale) throws Exception {
		RequestAttributes attrs = RequestContextHolder.getRequestAttributes();
		Assert.state(attrs instanceof ServletRequestAttributes, "No current ServletRequestAttributes");
		List<MediaType> requestedMediaTypes = getMediaTypes(((ServletRequestAttributes) attrs).getRequest());
		if (requestedMediaTypes != null) {
			List<View> candidateViews = getCandidateViews(viewName, locale, requestedMediaTypes);
			View bestView = getBestView(candidateViews, requestedMediaTypes, attrs);
			if (bestView != null) {
				return bestView;
			}
		}

		String mediaTypeInfo = logger.isDebugEnabled() && requestedMediaTypes != null ?
				" given " + requestedMediaTypes.toString() : "";

		if (this.useNotAcceptableStatusCode) {
			if (logger.isDebugEnabled()) {
				logger.debug("Using 406 NOT_ACCEPTABLE" + mediaTypeInfo);
			}
			return NOT_ACCEPTABLE_VIEW;
		}
		else {
			logger.debug("View remains unresolved" + mediaTypeInfo);
			return null;
		}
	}

/**
 * Determines the list of {@link MediaType} for the given {@link HttpServletRequest}.
 * @param request the current servlet request
 * @return the list of media types requested, if any
 */
@Nullable
protected List<MediaType> getMediaTypes(HttpServletRequest request) {
   Assert.state(this.contentNegotiationManager != null, "No ContentNegotiationManager set");
   try {
      ServletWebRequest webRequest = new ServletWebRequest(request);
      List<MediaType> acceptableMediaTypes = this.contentNegotiationManager.resolveMediaTypes(webRequest);
      List<MediaType> producibleMediaTypes = getProducibleMediaTypes(request);
      Set<MediaType> compatibleMediaTypes = new LinkedHashSet<>();
      for (MediaType acceptable : acceptableMediaTypes) {
         for (MediaType producible : producibleMediaTypes) {
            if (acceptable.isCompatibleWith(producible)) {
               compatibleMediaTypes.add(getMostSpecificMediaType(acceptable, producible));
            }
         }
      }
      List<MediaType> selectedMediaTypes = new ArrayList<>(compatibleMediaTypes);
      MediaType.sortBySpecificityAndQuality(selectedMediaTypes);
      return selectedMediaTypes;
   }
   catch (HttpMediaTypeNotAcceptableException ex) {
      if (logger.isDebugEnabled()) {
         logger.debug(ex.getMessage());
      }
      return null;
   }
}

@SuppressWarnings("unchecked")
private List<MediaType> getProducibleMediaTypes(HttpServletRequest request) {
   Set<MediaType> mediaTypes = (Set<MediaType>)
         request.getAttribute(HandlerMapping.PRODUCIBLE_MEDIA_TYPES_ATTRIBUTE);
   if (!CollectionUtils.isEmpty(mediaTypes)) {
      return new ArrayList<>(mediaTypes);
   }
   else {
      return Collections.singletonList(MediaType.ALL);
   }
}

/**
 * Return the more specific of the acceptable and the producible media types
 * with the q-value of the former.
 */
private MediaType getMostSpecificMediaType(MediaType acceptType, MediaType produceType) {
   produceType = produceType.copyQualityValue(acceptType);
   return (MediaType.SPECIFICITY_COMPARATOR.compare(acceptType, produceType) < 0 ? acceptType : produceType);
}

private List<View> getCandidateViews(String viewName, Locale locale, List<MediaType> requestedMediaTypes)
      throws Exception {

   List<View> candidateViews = new ArrayList<>();
   if (this.viewResolvers != null) {
      Assert.state(this.contentNegotiationManager != null, "No ContentNegotiationManager set");
      for (ViewResolver viewResolver : this.viewResolvers) {
         View view = viewResolver.resolveViewName(viewName, locale);
         if (view != null) {
            candidateViews.add(view);
         }
         for (MediaType requestedMediaType : requestedMediaTypes) {
            List<String> extensions = this.contentNegotiationManager.resolveFileExtensions(requestedMediaType);
            for (String extension : extensions) {
               String viewNameWithExtension = viewName + '.' + extension;
               view = viewResolver.resolveViewName(viewNameWithExtension, locale);
               if (view != null) {
                  candidateViews.add(view);
               }
            }
         }
      }
   }
   if (!CollectionUtils.isEmpty(this.defaultViews)) {
      candidateViews.addAll(this.defaultViews);
   }
   return candidateViews;
}

@Nullable
private View getBestView(List<View> candidateViews, List<MediaType> requestedMediaTypes, RequestAttributes attrs) {
   for (View candidateView : candidateViews) {
      if (candidateView instanceof SmartView) {
         SmartView smartView = (SmartView) candidateView;
         if (smartView.isRedirectView()) {
            return candidateView;
         }
      }
   }
   for (MediaType mediaType : requestedMediaTypes) {
      for (View candidateView : candidateViews) {
         if (StringUtils.hasText(candidateView.getContentType())) {
            MediaType candidateContentType = MediaType.parseMediaType(candidateView.getContentType());
            if (mediaType.isCompatibleWith(candidateContentType)) {
               if (logger.isDebugEnabled()) {
                  logger.debug("Selected '" + mediaType + "' given " + requestedMediaTypes);
               }
               attrs.setAttribute(View.SELECTED_CONTENT_TYPE, mediaType, RequestAttributes.SCOPE_REQUEST);
               return candidateView;
            }
         }
      }
   }
   return null;
}
```

```java
@Override
public List<MediaType> resolveMediaTypes(NativeWebRequest request) throws HttpMediaTypeNotAcceptableException {
   for (ContentNegotiationStrategy strategy : this.strategies) {
      List<MediaType> mediaTypes = strategy.resolveMediaTypes(request);
      if (mediaTypes.equals(MEDIA_TYPE_ALL_LIST)) {
         continue;
      }
      return mediaTypes;
   }
   return MEDIA_TYPE_ALL_LIST;
}
```

``` java
/*
 * Copyright 2002-2018 the original author or authors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.springframework.web.servlet;

import java.util.Locale;

import org.springframework.lang.Nullable;

/**
 * Interface to be implemented by objects that can resolve views by name.
 *
 * <p>View state doesn't change during the running of the application,
 * so implementations are free to cache views.
 *
 * <p>Implementations are encouraged to support internationalization,
 * i.e. localized view resolution.
 *
 * @author Rod Johnson
 * @author Juergen Hoeller
 * @see org.springframework.web.servlet.view.InternalResourceViewResolver
 * @see org.springframework.web.servlet.view.ResourceBundleViewResolver
 * @see org.springframework.web.servlet.view.XmlViewResolver
 */
public interface ViewResolver {

   /**
    * Resolve the given view by name.
    * <p>Note: To allow for ViewResolver chaining, a ViewResolver should
    * return {@code null} if a view with the given name is not defined in it.
    * However, this is not required: Some ViewResolvers will always attempt
    * to build View objects with the given name, unable to return {@code null}
    * (rather throwing an exception when View creation failed).
    * @param viewName name of the view to resolve
    * @param locale the Locale in which to resolve the view.
    * ViewResolvers that support internationalization should respect this.
    * @return the View object, or {@code null} if not found
    * (optional, to allow for ViewResolver chaining)
    * @throws Exception if the view cannot be resolved
    * (typically in case of problems creating an actual View object)
    */
   @Nullable
   View resolveViewName(String viewName, Locale locale) throws Exception;

}
```

一般ContentNegotiatingViewResolver会有多个Strategy，这些Strategy会根据不同的情况的type返回media集合。

例如：

HeadContentNegotiationStrategy的resolveMediaTypes()可以根据请求头Accept确定返回media。

ServletPathExtensionContentNegotiationStrategy则会根据请求路径是否有后缀返回media。

ParameterContentNegotiationStrategy等等。

```java
@Override
public List<MediaType> resolveMediaTypes(NativeWebRequest request)
      throws HttpMediaTypeNotAcceptableException {

   String[] headerValueArray = request.getHeaderValues(HttpHeaders.ACCEPT);
   if (headerValueArray == null) {
      return MEDIA_TYPE_ALL_LIST;
   }

   List<String> headerValues = Arrays.asList(headerValueArray);
   try {
      List<MediaType> mediaTypes = MediaType.parseMediaTypes(headerValues);
      MediaType.sortBySpecificityAndQuality(mediaTypes);
      return !CollectionUtils.isEmpty(mediaTypes) ? mediaTypes : MEDIA_TYPE_ALL_LIST;
   }
   catch (InvalidMediaTypeException ex) {
      throw new HttpMediaTypeNotAcceptableException(
            "Could not parse 'Accept' header " + headerValues + ": " + ex.getMessage());
   }
}
```

spring mvc用到的MappingJackson2JsonView，需要jack的jar包2.9x以上。

```
Spring comes with a wide array of default codecs, capable of converting from/to String, ByteBuffer, byte arrays, and also codecs that support marshalling libraries such as JAXB and Jackson (with Jackson 2.9+ support for non-blocking parsing). Within the context of Spring WebFlux, codecs are used to convert the request body into a @RequestMapping parameter, or to convert the return type into the response body that is sent back to the client. The default codecs are configured in the WebFluxConfigurationSupport class, and can easily be changed by overriding the configureHttpMessageCodecs when inheriting from that class. For more information about using codecs in WebFlux, see this section.
```

```xml
<dependency>
    <groupId>com.fasterxml.jackson.core</groupId>
    <artifactId>jackson-core</artifactId>
    <version>2.9.4</version>
</dependency>
<dependency>
    <groupId>com.fasterxml.jackson.core</groupId>
    <artifactId>jackson-annotations</artifactId>
    <version>2.9.4</version>
</dependency>
<dependency>
    <groupId>com.fasterxml.jackson.core</groupId>
    <artifactId>jackson-databind</artifactId>
    <version>2.9.4</version>
</dependency>
```

#### 怎么处理参数

入口：处理方法（DispatcherServlet.doDispatch）--- 任何参数的形式传入都是从这里开始

``` java
protected void doDispatch(HttpServletRequest request, HttpServletResponse response) throws Exception {
 ...

         // Actually invoke the handler.
         mv = ha.handle(processedRequest, response, mappedHandler.getHandler());

       ....
}
```

RequestMappingHandlerMapping.handleInternal方法

```java
@Override
protected ModelAndView handleInternal(HttpServletRequest request,
      HttpServletResponse response, HandlerMethod handlerMethod) throws Exception {

   ModelAndView mav;
   checkRequest(request);

   // Execute invokeHandlerMethod in synchronized block if required.
   if (this.synchronizeOnSession) {
      HttpSession session = request.getSession(false);
      if (session != null) {
         Object mutex = WebUtils.getSessionMutex(session);
         synchronized (mutex) {
            mav = invokeHandlerMethod(request, response, handlerMethod);
         }
      }
      else {
         // No HttpSession available -> no mutex necessary
         mav = invokeHandlerMethod(request, response, handlerMethod);
      }
   }
   else {
      // No synchronization on session demanded at all...
      mav = invokeHandlerMethod(request, response, handlerMethod);
   }

   if (!response.containsHeader(HEADER_CACHE_CONTROL)) {
      if (getSessionAttributesHandler(handlerMethod).hasSessionAttributes()) {
         applyCacheSeconds(response, this.cacheSecondsForSessionAttributeHandlers);
      }
      else {
         prepareResponse(response);
      }
   }

   return mav;
}

/**
	 * Invoke the {@link RequestMapping} handler method preparing a {@link ModelAndView}
	 * if view resolution is required.
	 * @since 4.2
	 * @see #createInvocableHandlerMethod(HandlerMethod)
	 */
	@Nullable
	protected ModelAndView invokeHandlerMethod(HttpServletRequest request,
			HttpServletResponse response, HandlerMethod handlerMethod) throws Exception {

	.....

			invocableMethod.invokeAndHandle(webRequest, mavContainer);
			if (asyncManager.isConcurrentHandlingStarted()) {
				return null;
			}

			return getModelAndView(mavContainer, modelFactory, webRequest);
		}
		finally {
			webRequest.requestCompleted();
		}
	}
```

ServletInvocableHandlerMethod.invokeAndHandle()

```java
public void invokeAndHandle(ServletWebRequest webRequest, ModelAndViewContainer mavContainer,
      Object... providedArgs) throws Exception {

   Object returnValue = invokeForRequest(webRequest, mavContainer, providedArgs);
  ......
   try {
      this.returnValueHandlers.handleReturnValue(
            returnValue, getReturnValueType(returnValue), mavContainer, webRequest);
   }
   catch (Exception ex) {
      if (logger.isTraceEnabled()) {
         logger.trace(formatErrorForReturnValue(returnValue), ex);
      }
      throw ex;
   }
}
```

```java
/**
 * Invoke the method after resolving its argument values in the context of the given request.
 * <p>Argument values are commonly resolved through
 * {@link HandlerMethodArgumentResolver HandlerMethodArgumentResolvers}.
 * The {@code providedArgs} parameter however may supply argument values to be used directly,
 * i.e. without argument resolution. Examples of provided argument values include a
 * {@link WebDataBinder}, a {@link SessionStatus}, or a thrown exception instance.
 * Provided argument values are checked before argument resolvers.
 * <p>Delegates to {@link #getMethodArgumentValues} and calls {@link #doInvoke} with the
 * resolved arguments.
 * @param request the current request
 * @param mavContainer the ModelAndViewContainer for this request
 * @param providedArgs "given" arguments matched by type, not resolved
 * @return the raw value returned by the invoked method
 * @throws Exception raised if no suitable argument resolver can be found,
 * or if the method raised an exception
 * @see #getMethodArgumentValues
 * @see #doInvoke
 */
@Nullable
public Object invokeForRequest(NativeWebRequest request, @Nullable ModelAndViewContainer mavContainer,
      Object... providedArgs) throws Exception {

   Object[] args = getMethodArgumentValues(request, mavContainer, providedArgs);
   if (logger.isTraceEnabled()) {
      logger.trace("Arguments: " + Arrays.toString(args));
   }
   return doInvoke(args);
}
```

InvocableHandlerMethod.getMethodArgumentValues方法获取页面参数。

``` java
/**
 * Get the method argument values for the current request, checking the provided
 * argument values and falling back to the configured argument resolvers.
 * <p>The resulting array will be passed into {@link #doInvoke}.
 * @since 5.1.2
 */
protected Object[] getMethodArgumentValues(NativeWebRequest request, @Nullable ModelAndViewContainer mavContainer,
      Object... providedArgs) throws Exception {

   MethodParameter[] parameters = getMethodParameters();
   Object[] args = new Object[parameters.length];
   for (int i = 0; i < parameters.length; i++) {
      MethodParameter parameter = parameters[i];
      parameter.initParameterNameDiscovery(this.parameterNameDiscoverer);
      args[i] = resolveProvidedArgument(parameter, providedArgs);
      if (args[i] != null) {
         continue;
      }
      if (this.argumentResolvers.supportsParameter(parameter)) {
         try {
            args[i] = this.argumentResolvers.resolveArgument(
                  parameter, mavContainer, request, this.dataBinderFactory);
            continue;
         }
         catch (Exception ex) {
            // Leave stack trace for later, e.g. AbstractHandlerExceptionResolver
            if (logger.isDebugEnabled()) {
               String message = ex.getMessage();
               if (message != null && !message.contains(parameter.getExecutable().toGenericString())) {
                  logger.debug(formatArgumentError(parameter, message));
               }
            }
            throw ex;
         }
      }
      if (args[i] == null) {
         throw new IllegalStateException(formatArgumentError(parameter, "No suitable resolver"));
      }
   }
   return args;
}
```

最后跳到HandlerMethodArgumentResolverComposite.resolveArgument()方法，所有的参数处理的地方从resolver.resolveArgument()这里进入。例如：@RequestBody、@RequestParam等

``` java
/**
 * Iterate over registered {@link HandlerMethodArgumentResolver HandlerMethodArgumentResolvers} and invoke the one that supports it.
 * @throws IllegalStateException if no suitable {@link HandlerMethodArgumentResolver} is found.
 */
@Override
@Nullable
public Object resolveArgument(MethodParameter parameter, @Nullable ModelAndViewContainer mavContainer,
      NativeWebRequest webRequest, @Nullable WebDataBinderFactory binderFactory) throws Exception {

   HandlerMethodArgumentResolver resolver = getArgumentResolver(parameter);
   if (resolver == null) {
      throw new IllegalArgumentException("Unknown parameter type [" + parameter.getParameterType().getName() + "]");
   }
   return resolver.resolveArgument(parameter, mavContainer, webRequest, binderFactory);
}
```

##### @RequestBody

和上面一样的流程，到了这时处理这个参数的类为：RequestResponseBodyMethodProcessor.resolveArgument()方法，他要求注册特有的messageConvert。

```java
@PostMapping("saveUser01")
public String saveUser01(@RequestBody User user,HttpServletRequest request , Model model)
{
    user.setId(UUID.randomUUID().getMostSignificantBits());
    userService.saveUser(user) ;
    return "redirect:getUserList" ;
}
```

MessageConverter怎么注册，可以通过RequestMappingHandlerAdapter如下进行注册。

``` xml
<bean class="org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter">
    <property name="messageConverters">
        <list>
            <bean id="mappingJacksonHttpMessageConverter" class="org.springframework.http.converter.json.MappingJackson2HttpMessageConverter">
                <property name="supportedMediaTypes">
                    <list>
                        <value>application/json;charset=UTF-8</value>
                    </list>
                </property>
            </bean>
        </list>
    </property>
</bean>
```

###### RequestMappingHandlerAdapter

RequestMappingHandlerAdapter继承了initializeBean，在初始化的时候，添加MessageConverter。

```java
@Override
public void afterPropertiesSet() {
   // Do this first, it may add ResponseBody advice beans
   initControllerAdviceCache();

   if (this.argumentResolvers == null) {
      List<HandlerMethodArgumentResolver> resolvers = getDefaultArgumentResolvers();
      this.argumentResolvers = new HandlerMethodArgumentResolverComposite().addResolvers(resolvers);
   }
   if (this.initBinderArgumentResolvers == null) {
      List<HandlerMethodArgumentResolver> resolvers = getDefaultInitBinderArgumentResolvers();
      this.initBinderArgumentResolvers = new HandlerMethodArgumentResolverComposite().addResolvers(resolvers);
   }
   if (this.returnValueHandlers == null) {
      List<HandlerMethodReturnValueHandler> handlers = getDefaultReturnValueHandlers();
      this.returnValueHandlers = new HandlerMethodReturnValueHandlerComposite().addHandlers(handlers);
   }
}
```

##### @RequestParam

``` java
@PostMapping("saveUser")
public String saveUser(@RequestParam(value = "userName") String userName,
                       @RequestParam(value="address") String address,
                       HttpServletRequest request , Model model)
{
    User user = new User();
    user.setId(UUID.randomUUID().getMostSignificantBits());
    user.setUserName(userName);
    user.setAddress(address);
    userService.saveUser(user) ;
    return "redirect:getUserList" ;
}
```

他的处理类是RequestParamMapMethodArgumentResolver.resolveArgument()方法。

```java
@Override
public Object resolveArgument(MethodParameter parameter, @Nullable ModelAndViewContainer mavContainer,
      NativeWebRequest webRequest, @Nullable WebDataBinderFactory binderFactory) throws Exception {

   ResolvableType resolvableType = ResolvableType.forMethodParameter(parameter);

   if (MultiValueMap.class.isAssignableFrom(parameter.getParameterType())) {
      // MultiValueMap
      Class<?> valueType = resolvableType.as(MultiValueMap.class).getGeneric(1).resolve();
      if (valueType == MultipartFile.class) {
         MultipartRequest multipartRequest = MultipartResolutionDelegate.resolveMultipartRequest(webRequest);
         return (multipartRequest != null ? multipartRequest.getMultiFileMap() : new LinkedMultiValueMap<>(0));
      }
      else if (valueType == Part.class) {
         HttpServletRequest servletRequest = webRequest.getNativeRequest(HttpServletRequest.class);
         if (servletRequest != null && MultipartResolutionDelegate.isMultipartRequest(servletRequest)) {
            Collection<Part> parts = servletRequest.getParts();
            LinkedMultiValueMap<String, Part> result = new LinkedMultiValueMap<>(parts.size());
            for (Part part : parts) {
               result.add(part.getName(), part);
            }
            return result;
         }
         return new LinkedMultiValueMap<>(0);
      }
      else {
         Map<String, String[]> parameterMap = webRequest.getParameterMap();
         MultiValueMap<String, String> result = new LinkedMultiValueMap<>(parameterMap.size());
         parameterMap.forEach((key, values) -> {
            for (String value : values) {
               result.add(key, value);
            }
         });
         return result;
      }
   }

   else {
      // Regular Map
      Class<?> valueType = resolvableType.asMap().getGeneric(1).resolve();
      if (valueType == MultipartFile.class) {
         MultipartRequest multipartRequest = MultipartResolutionDelegate.resolveMultipartRequest(webRequest);
         return (multipartRequest != null ? multipartRequest.getFileMap() : new LinkedHashMap<>(0));
      }
      else if (valueType == Part.class) {
         HttpServletRequest servletRequest = webRequest.getNativeRequest(HttpServletRequest.class);
         if (servletRequest != null && MultipartResolutionDelegate.isMultipartRequest(servletRequest)) {
            Collection<Part> parts = servletRequest.getParts();
            LinkedHashMap<String, Part> result = new LinkedHashMap<>(parts.size());
            for (Part part : parts) {
               if (!result.containsKey(part.getName())) {
                  result.put(part.getName(), part);
               }
            }
            return result;
         }
         return new LinkedHashMap<>(0);
      }
      else {
         Map<String, String[]> parameterMap = webRequest.getParameterMap();
         Map<String, String> result = new LinkedHashMap<>(parameterMap.size());
         parameterMap.forEach((key, values) -> {
            if (values.length > 0) {
               result.put(key, values[0]);
            }
         });
         return result;
      }
   }
}
```

### 谈谈Spring MVC的优化

上面我们已经对 SpringMVC 的工作原理和源码进行了分析,在这个过程发现了几个优化点:

1.Controller 如果能保持单例,尽量使用单例,这样可以减少创建对象和回收对象的开销.也就是说,如果Controller的类变量和实例变量可以以方法形参声明的尽量以方法的形参声明,不要以类变量和实例变量声明,这样可以避免线程安全问题.

2.处理 Request 的方法中的形参务必加上@RequestParam 注解,这样可以避免 SpringMVC 使用asm 框架读取 class 文件获取方法参数名的过程.即便 SpringMVC 对读取出的方法参数名进行了缓存,如果不要读取 class 文件当然是更加好.

3.阅读源码的过程中,发现 SpringMVC 并没有对处理 url 的方法进行缓存,也就是说每次都要根据请求 url 去匹配 Controller 中的方法 url,如果把 url 和 Method 的关系缓存起来,会不会带来性能上的提升呢?有点恶心的是,负责解析 url 和 Method 对应关系的 ServletHandlerMethodResolver 是一个private的内部类,不能直接继承该类增强代码,必须要该代码后重新编译.当然,如果缓存起来,必须要考虑缓存的线程安全问题