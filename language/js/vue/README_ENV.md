[TOC]

# 开发环境搭建

```
1. 先安装node.js的最新版本. 一定要是最新的 ，可以避免很多问题
2. 安装国内npm境像(用淘宝npm境像即可)，不然下载依赖包很慢，命令行运行:
npm install -g cnpm --registry=https://registry.npm.taobao.org
3. 安装vue-cli脚手架命令：
cnpm install --global vue-cli
4.新建vue项目
vue init <template-name> <project-name>
例如:vue init webpack my-project
5.用编辑器打开项目，安装所有依赖包，在项目根目录运行:
cnpm installl
6. 运行项目
npm run dev
7. 打包项目
npm run build
```

# IDEA编译器开发vue

```
如果你想在Intellij IDEA的Terminal中构建vue-cli项目，还需要做一点准备。如果使用cmd构建，则跳过此步骤。

1，安装vue.js
File -> Settings -> Plugins -> Browse respositoties...
搜索vue.js，右侧提示Install（截图时已安装，未安装会提示Install）。安装成功后需要重启IDEA。

2，File Types: HTML 添加 *.vue类型
File -> Settings -> Editor -> File Types -> HTML
点Registered Patterns下的+，添加 *.vue

3，设置JS
File -> Settings -> Language & Frameworks -> JavaScript
选择 ECMAScript 6 和 Prefer Strict mode

4，构建及运行vue-cli项目
在命令行工具cmd，或者Intellij IDEA的Terminal中进入想要构建项目的目录，输入vue init webpack project-name，回车webpack默认版本为2.0，若要指定1.0，需在webpack后加上#1.0，即vue init webpack#1.0 project-name
这样构建出来的项目，可以直接运行。进入项目所在目录，执行npm run dev，执行完看到以下提示：
Your application is running here: http://localhost:8080

5，Intellij IDEA新建.vue格式文件
在开发的时候，会发现新建文件时并没有.vue格式文件的选择，这时我们需要做一些设置。
File -> Settings -> Editor -> File and Code Templates -> +
模板内容可以按需。可以填也可以不填
参考：
<template>
    <div> {{msg}}</div>
</template>
<style></style>
<script>
        export default{
        data () {
            return {msg: 'vue模板页'}
        }
    }
</script>

6，idea运行vue项目
要在idea中配置nodejs（配置java的jdk一样），和配置tomcat一样，可以查看下面链接：
https://blog.csdn.net/jomexiaotao/article/details/80533548
```

# 打包部署

```
1，在本地开发环境上，打开命令提示符，到项目目录下运行如下命令：
cnpm run build

2，部署到http server服务器即可。

3，若是部署到nginx，build的时候要设置项目名：
webpack.base.conf.js中修改assetsPublicPath指定项目名，例如test。
nginx则配置访问路径项目名（这样一个nginx中可以放置多个项目）：
       location /test {
	        #alias   /usr/local/nginx/html/demo/;
	        root /usr/local/nginx/html;
            index  index.html index.htm;
        }
```

# 异常

```js
SyntaxError: Block-scoped declarations (let, const, function, class) not yet supported outside strict mode
    at exports.runInThisContext (vm.js:53:16)
    at Module._compile (module.js:373:25)
    at Object.Module._extensions..js (module.js:416:10)
    at Module.load (module.js:343:32)
    at Function.Module._load (module.js:300:12)
    at Function.Module.runMain (module.js:441:10)
    at startup (node.js:139:18)
    at node.js:968:3
------node版本太低，与npm不匹配
```

