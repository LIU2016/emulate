#### spring mvc 怎么根据媒体类型找到view

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

#### spring mvc怎么处理参数

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