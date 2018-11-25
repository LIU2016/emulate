[TOC]

# 一、介绍

服务端:AsynchronousServerSocketChannel

客服端:AsynchronousSocketChannel

用户处理器:CompletionHandler接口,这个接口实现应用程序向操作系统发起IO请求,当完成后处理具体逻辑，否则做自己该做的事情，“真正”的异步IO需要操作系统更强的支持。在IO多路复用模型中，事件循环将文件句柄的状态事件通知给用户线程，由用户线程自行读取数据、处理数据。而在异步IO模型中，当用户线程收到通知时，数据已经被内核读取完毕，并放在了用户线程指定的缓冲区内，内核在IO完成后通知用户线程直接使用即可。异步IO模型使用了Proactor设计模式实现了这一机制.

Reactor和Proactor模式的主要区别就是真正的读取和写入操作是有谁来完成的，Reactor中需要应用程序自己读取或者写入数据，而Proactor模式中，应用程序不需要进行实际的读写过程，它只需要从缓存区读取或者写入即可，操作系统会读取缓存区或者写入缓存区到真正的IO设备.

# 二、参考

<https://www.cnblogs.com/pigerhan/p/3474217.html>