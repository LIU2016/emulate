参考：

http://www.runoob.com/vue2/vue-tutorial.html

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

Vue.js 路由允许我们通过不同的 URL 访问不同的内容。通过 Vue.js 可以实现多视图的单页Web应用（single page web application，SPA）。Vue.js 路由需要载入 [vue-router 库](https://github.com/vuejs/vue-router)

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

# vue store之状态管理模式

```
状态管理（vuex）简介
vuex是专为vue.js应用程序开发的状态管理模式。它采用集中存储管理应用的所有组件的状态，并以相应的规则保证状态以一种可预测的方式发生变化。vuex也集成刀vue的官方调试工具devtools extension，提供了诸如零配置的time-travel调试、状态快照导入导出等高级调试功能。

Vuex 的思想
当我们在页面上点击一个按钮，它会处发(dispatch)一个action, action 随后会执行(commit)一个mutation, mutation 立即会改变state, state 改变以后,我们的页面会state 获取数据，页面发生了变化。 Store 对象，包含了我们谈到的所有内容，action, state, mutation，所以是核心了
```

