[TOC]

# 一、背景知识

netty 是 reactive模式 异步非阻塞 （reactor + asyn）

## 高性能的三大主题

传输（BIO\NIO\AIO） - IO模型
数据协议
线程模型

## 异步非阻塞

## 零拷贝

1，使用直接缓冲区，堆外缓冲区
2，提供了buffer对象
3，直接将文件缓冲区的数据发送到目标channel

## 内存池

## 高效的Reactor线程模型

boss线程和work线程

无锁化的串行处理 pipeline

每个通道的所有的业务逻辑处理都是串行的，可控的，而且每个业务逻辑都是一个线程。
每个通道之间是互不干扰的，并行的。

## 序列化

# 二、使用

 .channel(NioServerSocketChannel.class)
​                    .option([ChannelOption.SO](http://ChannelOption.SO)_BACKLOG,1024).handler(null)
​                    //子线程的处理类 - - handler
​                    .childHandler(new ChannelInitializer<SocketChannel>() {
​                        @Override
​                        protected void initChannel(SocketChannel client) throws Exception
​                        {

## Reactor线程模型实现

## BootStrap

## ChannelPipeline

> Outbound 
> 请求事件(request event), 即请求某件事情的发生, 然后通过 Outbound
> 事件进行通知.
> Outbound 事件的传播方向是 tail -> customContext -> head.
>
> Inbound
> Inbound 事件是一个通知事件, 即某件事已经发生了, 然后通过 Inbound 事件进行通知.
> Inbound 通常发生在 Channel 的状态的改变或 IO 事件就绪.
> Inbound 的特点是它传播方向是 head -> customContext -> tail
>
> Handler 

## EventLoop

bosser
worker
主从性能最高

## Promise 与 与 Future  双子星的秘密

## 数据翻译官编码和解码（拆包和粘包）

TCP 是一个“流”协议，所谓流，就是没有界限的一长串二进制数据。TCP 作为传输层协议并不
不了解上层业务数据的具体含义，它会根据 TCP 缓冲区的实际情况进行数据包的划分，所以在业
务上认为是一个完整的包，可能会被 TCP 拆分成多个包进行发送，也有可能把多个小的包封装成
一个大的数据包发送，这就是所谓的 TCP 粘包和拆包问题 。
由于底层的 TCP 无法理解上层的业务数据，所以在底层是无法保证数据包不被拆分和重组的，这
个问题只能通过上层的应用协议栈设计来解决。业界的主流协议的解决方案，可以归纳如下：
\1. 消息定长，报文大小固定长度，例如每个报文的长度固定为 200 字节，如果不够空位补空格；
\2. 包尾添加特殊分隔符，例如每条报文结束都添加回车换行符（例如 FTP 协议）或者指定特殊
字符作为报文分隔符，接收方通过特殊分隔符切分报文区分；
\3. 将消息分为消息头和消息体，消息头中包含表示信息的总长度（或者消息体长度）的字段；
\4. 更复杂的自定义应用层协议。
通常我们也习惯将编码（Encode）称为序列化（serialization），它将对象序列化为字节数组，
用于网络传输、数据持久化或者其它用途。
反之，解码（Decode）/反序列化（deserialization）把从网络、磁盘等读取的字节数组还原成
原始对象（通常是原始对象的拷贝），以方便后续的业务逻辑操作。
进行远程跨进程服务调用时（例如 RPC 调用），需要使用特定的编解码技术，对需要进行网络传
输的对象做编码或者解码，以便完成远程调用。
编码 - 拆包 / 序列化
解码 - 粘包 / 反序列化