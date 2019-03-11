# 参考

http://www.runoob.com/vue2/vue-tutorial.html VUE菜鸟教程

https://www.cnblogs.com/blackchaos/p/8717138.html VUE问题集

https://cn.vuejs.org/v2/api/#devtools VUE开发进阶

https://vuejs.org api参考文档

# 目录结构

build\dist\src\static\config\ 

main.js App.vue

# HTML元素语法

## 起步

## 模板语法

{{}}，html(v-html)， 属性（v-bind/v-model)，表达式，指令（v-if，v-bind:href，v-on:click，v-on:submit.prevent），用户输入（v-model 指令来实现双向数据绑定，v-on:click="reverseMessag"绑定vue的方法），过滤器（{{ message | filterA | filterB }}），缩写（v-on:click--@click ，v-bind:href---:href ）

## 条件语法

v-if、v-else、v-else-if、v-show

## 循环语句

 v-for

## 计算属性

computed

## 监听属性

watch 

## 样式绑定

 v-bind:class ，v-bind:style

## 事件处理器

v-on

## 表单

v-model（单选框、复选框、select）

# VUE框架语法

## 组件

Vue.Component

```
组件（Component）是 Vue.js 最强大的功能之一。
组件可以扩展 HTML 元素，封装可重用的代码。
组件系统让我们可以用独立可复用的小组件来构建大型应用，几乎任意类型的应用的界面都可以抽象为一个组件树。

prop 是单向绑定的：当父组件的属性变化时，将传导给子组件，但是不会反过来。
v-bind用于动态绑定父组件的数据

组件可以为 props 指定验证要求。

父组件是使用 props 传递数据给子组件，但如果子组件要把数据传递回去，就需要使用自定义事件！
我们可以使用 v-on 绑定自定义事件, 每个 Vue 实例都实现了事件接口(Events interface)，即：
使用 $on(eventName) 监听事件
使用 $emit(eventName) 触发事件
另外，父组件可以在使用子组件的地方直接用 v-on 来监听子组件触发的事件。
以下实例中子组件已经和它外部完全解耦了。它所做的只是触发一个父组件关心的内部事件。

生命周期的响应函数：https://www.jb51.net/article/145474.htm
```

## 自定义指令

Vue.directive

```js
<div id="app">
    <p>页面载入时，input 元素自动获取焦点：</p>
    <input v-focus>
</div>
 
<script>
// 注册一个全局自定义指令 v-focus
Vue.directive('focus', {
  // 当绑定元素插入到 DOM 中。
  inserted: function (el) {
    // 聚焦元素
    el.focus()
  }
})

// 创建根实例
new Vue({
  el: '#app'
})
</script>
```

```
钩子
钩子函数
指令定义函数提供了几个钩子函数（可选）：

bind: 只调用一次，指令第一次绑定到元素时调用，用这个钩子函数可以定义一个在绑定时执行一次的初始化动作。

inserted: 被绑定元素插入父节点时调用（父节点存在即可调用，不必存在于 document 中）。

update: 被绑定元素所在的模板更新时调用，而不论绑定值是否变化。通过比较更新前后的绑定值，可以忽略不必要的模板更新（详细的钩子函数参数见下）。

componentUpdated: 被绑定元素所在模板完成一次更新周期时调用。

unbind: 只调用一次， 指令与元素解绑时调用。

钩子函数参数
钩子函数的参数有：

el: 指令所绑定的元素，可以用来直接操作 DOM 。
binding: 一个对象，包含以下属性：
name: 指令名，不包括 v- 前缀。
value: 指令的绑定值， 例如： v-my-directive="1 + 1", value 的值是 2。
oldValue: 指令绑定的前一个值，仅在 update 和 componentUpdated 钩子中可用。无论值是否改变都可用。
expression: 绑定值的表达式或变量名。 例如 v-my-directive="1 + 1" ， expression 的值是 "1 + 1"。
arg: 传给指令的参数。例如 v-my-directive:foo， arg 的值是 "foo"。
modifiers: 一个包含修饰符的对象。 例如： v-my-directive.foo.bar, 修饰符对象 modifiers 的值是 { foo: true, bar: true }。
vnode: Vue 编译生成的虚拟节点。
oldVnode: 上一个虚拟节点，仅在 update 和 componentUpdated 钩子中可用。
```

## 路由

```
Vue.js 路由允许我们通过不同的 URL 访问不同的内容。通过 Vue.js 可以实现多视图的单页Web应用（single page web application，SPA）。Vue.js 路由需要载入 [vue-router 库](https://github.com/vuejs/vue-router)

router-link页面上跳转，也可以在浏览器上输入path路径跳转。

router-view 展示
```



## 过渡 & 动画

```html
<transition name = "nameoftransition">
   <div></div>
</transition>
```

## 混入

混入 (mixins)定义了一部分可复用的方法或者计算属性。混入对象可以包含任意组件选项。当组件使用混入对象时，所有混入对象的选项将被混入该组件本身的选项。

## Ajax(vue-resource)

```
你可以使用全局对象方式 Vue.http 或者在一个 Vue 实例的内部使用 this.$http来发起 HTTP 请求。

// 基于全局Vue对象使用http
Vue.http.get('/someUrl', [options]).then(successCallback, errorCallback);
Vue.http.post('/someUrl', [body], [options]).then(successCallback, errorCallback);

// 在一个Vue实例内使用$http
this.$http.get('/someUrl', [options]).then(successCallback, errorCallback);
this.$http.post('/someUrl', [body], [options]).then(successCallback, errorCallback);

vue-resource 提供了 7 种请求 API(REST 风格)：
get(url, [options])
head(url, [options])
delete(url, [options])
jsonp(url, [options])
post(url, [body], [options])
put(url, [body], [options])
patch(url, [body], [options])
```

## 响应接口

```
Vue 可以添加数据动态响应接口。
例如以下实例，我们通过使用 $watch 属性来实现数据的监听，$watch 必须添加在 Vue 实例之外才能实现正确的响应。

Vue 不允许在已经创建的实例上动态添加新的根级响应式属性。
Vue 不能检测到对象属性的添加或删除，最好的方式就是在初始化实例前声明根级响应式属性，哪怕只是一个空值。

Vue.set( target, key, value )
Vue.delete( target, key )

```

## 其他语法

```
1，Vue.use
在用Vue使用别人的组件时，会用到 Vue.use()

2，import Vue from 'vue'
import...from...的from命令后面可以跟很多路径格式，若只给出vue，axios这样的包名，则会自动到node_modules中加载；若给出相对路径及文件前缀，则到指定位置寻找。可以加载各种各样的文件：.js、.vue、.less等等。可以省略掉from直接引入。可以在 bulid/webpack.base.conf.js 文件中修改相关配置。你的模块可以省略 ".js"，".vue"，“.json” 后缀，weebpack 会在之后自动添加上；可以用 "@" 符号代替 "src" 字符串等。
（参考：
https://blog.csdn.net/bujiongdan/article/details/81416100
https://www.cnblogs.com/blog-cxj2017522/p/8562536.html
）

3，export default
export 用来导出模块，Vue 的单文件组件通常需要导出一个对象，这个对象是 Vue 实例的选项对象，以便于在其它地方可以使用 import 引入。而 new Vue() 相当于一个构造函数，在入口文件 main.js 构造根组件的同时，如果根组件还包含其它子组件，那么 Vue 会通过引入的选项对象构造其对应的 Vue 实例，最终形成一棵组件树。

```

# 开源组件

## vue Vuex

https://vuex.vuejs.org/zh/

http://www.cnblogs.com/yeziTesting/p/7182904.html （博客 - 供练习）

```
状态管理（vuex）简介
vuex是专为vue.js应用程序开发的状态管理模式。它采用集中存储管理应用的所有组件的状态，并以相应的规则保证状态以一种可预测的方式发生变化。vuex也集成刀vue的官方调试工具devtools extension，提供了诸如零配置的time-travel调试、状态快照导入导出等高级调试功能。

Vuex 的思想
当我们在页面上点击一个按钮，它会处发(dispatch)一个action, action 随后会执行(commit)一个mutation, mutation 立即会改变state, state 改变以后,我们的页面会state 获取数据，页面发生了变化。 Store 对象，包含了我们谈到的所有内容，action, state, mutation，所以是核心了。
更改Vuex 的 store 中的状态的唯一方法是提交 mutation。Vuex 中的 mutation 非常类似于事件:每个 mutation 都有一个字符串的 事件类型 (type)和 一个 回调
```

## vue lodash

```

```

## vue 本地存储

```
1、本地存储(localstorage && sessionstorage)  
2、离线缓存(application cache)；
3、websql与 indexeddb

https://blog.csdn.net/dx18520548758/article/details/79740077
https://blog.csdn.net/qq_21423689/article/details/79913828
```

# 其他

## 取消Vue中格式警告

```
用vue cli脚手架搭建开发环境，会自动安装eslint严格格式，如果代码格式不按照严格模式写，会经常报警告，
在项目中打开 bulid 文件夹下的 webpack.base.config.js 文件。将以下代码删掉或注销
 rules: [
      /*...(config.dev.useEslint ? [createLintingRule()] : []),*/ --这里
      {
        test: /\.vue$/,
        loader: 'vue-loader',
        options: vueLoaderConfig
      },
```

## index.html main.js app.vue index.js怎么结合的？ 怎么打包的？

```
index的body中只有一个id为app的div，那是如何被渲染的呢。一步一步寻找
index.html → main.js → app.vue → index.js → components/组件

第一步：main.js
main.js是我们的入口文件，主要作用是初始化vue实例并使用需要的插件。
mian.js 的内容如上图。
这里new Vue代表新建vue对象
el官方解释：为实例提供挂载元素。值可以是 CSS 选择符，或实际 HTML 元素，或返回 HTML 元素的函数。
这里就通过index.html中的<div id="app"><div>中的id=“app”和这里的“#app”进行挂载。
components:代表组件。这里的App，实际是App:App的省略写法，template里使用的 <App/>标签来自组件App。
template：代表模板。官方解释：模板将会替换挂载的元素。挂载元素的内容都将被忽略。
也就是说:template: '<App/>' 表示用<app></app>替换index.html里面的<div id="app"></div>

还要重点说明index.js，在main.js中new Vue对象中写入router，实际上是router:router，作用是main.js引入了router对象，根据路由的配置方法，需要将router对象加载到根main..js中。

第二步：App.vue
App.vue是我们的主组件，所有页面都是在App.vue下进行切换的。其实你也可以理解为所有的路由也是App.vue的子组件。所以我将router标示为App.vue的子组件。
helloworld.vue中的内容能在app.vue中显示, 首先在index.js配置了路由路径,在main.js中加载了路由,在app.vue指明了路由显示位置<router-view>标签. 
<router-view>怎么作用到一个helloworld组件的,作用域是什么,跨文件了怎么弄的? 还有待学习.
转载:https://blog.csdn.net/for_weber/article/details/80414754
```

## template的写法

```

<div id="app">
    <h1>我是直接写在构造器里的模板1</h1>
</div>
 
<template id="demo3">
    <h1 style="color:red">我是选项模板3</h1>
</template>
 
<script type="x-template" id="demo4">
    <h1 style="color:red">我是script标签模板4</h1>
</script>
 
<script>
    var vm=new Vue({
        el:"#app",
        data:{
            message:1
        },
 
        //第2种模板 写在构造器里
        //template:`<h1 style="color:red">我是选项模板2</h1>`
 
        //第3种模板 写在<template>标签里
        //template:'#demo3'
 
        //第4种模板 写在<script type="x-template">标签里
        template:'#demo4'
    })
</script>
```

## vue中用async/await 来处理异步

```
用async/ await来发送异步请求，从服务端获取数据，等待获取数据，然后处理数据。 需要注意：await必须放在async中 。

>async

    async的用法，它作为一个关键字放到函数前面，用于表示函数是一个异步函数，因为async就是异步的意思， 异步函数也就意味着该函数的执行不会阻塞后面代码的执行，async 函数返回的是一个promise 对象。

>await

   await的含义为等待。意思就是代码需要等待await后面的函数运行完并且有了返回结果之后，才继续执行下面的代码。这正是同步的效果
```

## let 和 var 的区别

```
https://blog.csdn.net/superlover_/article/details/81626281
```

