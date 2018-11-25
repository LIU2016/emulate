[TOC]

# 一、背景知识

阻塞和非阻塞

> 相对于数据而言
> 阻塞和非阻塞是进程在访问数据的时候，数据是否准备就绪的一种处理方式,当数据没
> 有准备的时候 阻塞：往往需要等待缓冲区中的数据准备好过后才处理其他的事情，否则一
> 直等待在那里。
> 非阻塞:当我们的进程访问我们的数据缓冲区的时候，如果数据没有准备好则直接返回，
> 不会等待。如果数据已经准备好，也直接返回。

同步和非同步

> 相对于IO操作
> 同步和异步都是基于应用程序和操作系统处理 IO 事件所采用的方式。比如
> 同步：是应用程序要直接参与 IO 读写的操作。
> 异步：所有的 IO 读写交给操作系统去处理，应用程序只需要等待通知。
> 同步方式在处理 IO 事件的时候，必须阻塞在某个方法上面等待我们的 IO 事件完成(阻
> 塞 IO 事件或者通过轮询 IO 事件的方式),
> 对于异步来说，所有的 IO 读写都交给了操作系统。
> 这个时候，我们可以去做其他的事情，并不需要去完成真正的 IO 操作，当操作完成 IO 后，
> 会给我们的应用程序一个通知。
> 同步:
> 1)阻塞到 IO 事件，阻塞到 read 或则 write。这个时候我们就完全不能做自己的
> 事情。让读写方法加入到线程里面，然后阻塞线程来实现，对线程的性能开销比较大

# 二、bio和nio比较

IO      模型 IO               NIO
方式 从硬盘到内存      从内存到硬盘
通信 面向流(乡村公路) 面向缓冲(高速公路，多路复用技术)
处理 阻塞 IO(多线程)   非阻塞 IO(反应堆 Reactor)
触发     无                  选择器(轮询机制)

# 三、面向流与面向缓冲

Java NIO 和 IO 之间第一个最大的区别是，IO 是面向流的，NIO 是面向缓冲区的。 
Java IO 面向流意味着每次从流中读一个或多个字节，直至读取所有字节，它们没有被缓存在任何地方。此外，它不能前后移动流中的数据。如果需要前后移动从流中读取的数据，需要先将它缓存到一个缓冲区。 
Java NIO 的缓冲导向方法略有不同。数据读取到一个它稍后处理的缓冲区，需要时可在缓冲区中前后移动。这就增加了处理过程中的灵活性。但是，还需要检查是否该缓冲区中包含所有您需要处理的数据。而且，需确保当更多的数据读入缓冲区时，不要覆盖缓冲区里尚未处理的数据。

# 四、阻塞与非阻塞 IO（BIO与NIO）

Java IO 的各种流是阻塞的。这意味着，当一个线程调用 read() 或 write()时，该线程被
阻塞，直到有一些数据被读取，或数据完全写入。该线程在此期间不能再干任何事情了。Java
NIO 的非阻塞模式，使一个线程从某通道发送请求读取数据，但是它仅能得到目前可用的数
据，如果目前没有数据可用时，就什么都不会获取。而不是保持线程阻塞，所以直至数据变
的可以读取之前，该线程可以继续做其他的事情。 非阻塞写也是如此。一个线程请求写入
一些数据到某通道，但不需要等待它完全写入，这个线程同时可以去做别的事情。 线程通
常将非阻塞 IO 的空闲时间用于在其它通道上执行 IO 操作，所以一个单独的线程现在可以管
理多个输入和输出通道（channel）。

## 多路复用技术

一个线程多事件

## 选择器

Java NIO 的选择器允许一个单独的线程来监视多个输入通道，你可以注册多个通道使用一
个选择器，然后使用一个单独的线程来“选择”通道：这些通道里已经有可以处理的输入，
或者选择已准备写入的通道。这种选择机制，使得一个单独的线程很容易来管理多个通道。

## NIO 和 和 IO 如何影响应用程序的设计

无论您选择 IO 或 NIO 工具箱，可能会影响您应用程序设计的以下几个方面：
1.对 NIO 或 IO 类的 API 调用。
2.数据处理。
3.用来处理数据的线程数
API  调用
当然，使用 NIO 的 API 调用时看起来与使用 IO 时有所不同，但这并不意外，因为并不是仅
从一个 InputStream 逐字节读取，而是数据必须先读入缓冲区再处理

# 五、Nio认识与使用

在谈到缓冲区时，我们说缓冲区对象本质上是一个数组，但它其实是一个特殊的数组，缓冲区对象内
置了一些机制，能够跟踪和记录缓冲区的状态变化情况，如果我们使用 get()方法从缓冲区获取数据
或者使用 put()方法把数据写入缓冲区，都会引起缓冲区状态的变化。

在缓冲区中，最重要的属性有下面三个，它们一起合作完成对缓冲区内部状态的变化跟踪：

> position：指定了下一个将要被写入或者读取的元素索引，它的值由 get()/put()方法自动更新，在
> 新创建一个 Buffer 对象时，position 被初始化为 0。
> limit：指定还有多少数据需要取出(在从缓冲区写入通道时)，或者还有多少空间可以放入数据(在从
> 通道读入缓冲区时)。
> capacity：指定了可以存储在缓冲区中的最大数据容量，实际上，它指定了底层数组的大小，或者至
> 少是指定了准许我们使用的底层数组的容量。

以上三个属性值之间有一些相对大小的关系：0 <= position <= limit <= capacity。如果我们创建
一个新的容量大小为 10 的 ByteBuffer 对象，在初始化的时候，position 设置为 0，limit 和 capacity
被设置为 10，在以后使用 ByteBuffer 对象过程中，capacity 的值不会再发生变化，而其它两个个将
会随着使用而变化。

四个属性值分别如图所示：

现在我们可以从通道中读取一些数据到缓冲区中，注意从通道读取数据，相当于往缓冲区中写入数据。
如果读取 4 个自己的数据，则此时 position 的值为 4，即下一个将要被写入的字节索引为 4，而 limit
仍然是 10，如下图所示：

下一步把读取的数据写入到输出通道中，相当于从缓冲区中读取数据，在此之前，必须调用 flip()
方法，该方法将会完成两件事情：

> \1. 把 limit 设置为当前的 position 值
> \2. 把 position 设置为 0

由于position被设置为0，所以可以保证在下一步输出时读取到的是缓冲区中的第一个字节，而limit
被设置为当前的 position，可以保证读取的数据正好是之前写入到缓冲区中的数据，如下图所示：
现在调用 get()方法从缓冲区中读取数据写入到输出通道，这会导致 position 的增加而 limit 保持
不变，但 position 不会超过 limit 的值，所以在读取我们之前写入到缓冲区中的 4 个自己之后，
position 和 limit 的值都为 4，如下图所示：

在从缓冲区中读取数据完毕后，limit 的值仍然保持在我们调用 flip()方法时的值，调用 clear()方
法能够把所有的状态变化设置为初始化时的值，如下图所示：

最后我们用一段代码来验证这个过程，如下所示：

```java
package com.gupaoedu.nio.buffer;
import java.io.FileInputStream;
import java.nio.*;
import java.nio.channels.*;
public class BufferProgram {
public static void main(String args[]) throws Exception {
FileInputStream fin = new FileInputStream("e:\\test.txt");
FileChannel fc = fin.getChannel();
ByteBuffer buffer = ByteBuffer.allocate(10);
output("初始化", buffer);
fc.read(buffer);
output("调用 read()", buffer);
buffer.flip();
output("调用 flip()", buffer);
while (buffer.remaining() > 0) {
byte b = buffer.get();
// System.out.print(((char)b));
}
output("调用 get()", buffer);
buffer.clear();
output("调用 clear()", buffer);
fin.close();
}
public static void output(String step, Buffer buffer) {
System.out.println(step + " : ");
System.out.print("capacity: " + buffer.capacity() + ", ");
System.out.print("position: " + buffer.position() + ", ");
System.out.println("limit: " + buffer.limit());
System.out.println();
}
}
```

## 缓冲区buffer

缓冲区 Buffer
Buffer  操作基本 API
缓冲区实际上是一个容器对象，更直接的说，其实就是一个数组，在 NIO 库中，所有数据都
是用缓冲区处理的。在读取数据时，它是直接读到缓冲区中的； 在写入数据时，它也是写
入到缓冲区中的；任何时候访问 NIO 中的数据，都是将它放到缓冲区中。而在面向流 I/O
系统中，所有数据都是直接写入或者直接将数据读取到 Stream 对象中。
在 NIO 中，所有的缓冲区类型都继承于抽象类 Buffer，最常用的就是 ByteBuffer，对于 Java
中的基本类型，基本都有一个具体 Buffer 类型与之相对应

### 缓冲区的分配

在创建一个缓冲区对象时，会调用静态方法 allocate()来
指定缓冲区的容量，其实调用 allocate()相当于创建了一个指定大小的数组，并把它包装为缓冲区
对象。或者我们也可以直接将一个现有的数组，包装为缓冲区对象，如下示例代码所示：

```java
package com.gupaoedu.nio.buffer;
import java.nio.ByteBuffer;
public class BufferWrap {
public void myMethod()
{
// 分配指定大小的缓冲区
ByteBuffer buffer1 = ByteBuffer.allocate(10);
// 包装一个现有的数组
byte array[] = new byte[10];
ByteBuffer buffer2 = ByteBuffer.wrap( array );
}
}
```

### 缓冲区分片

除了可以分配或者包装一个缓冲区对象外，还可以根据现有的缓冲区对象来创建一个子缓
冲区，即在现有缓冲区上切出一片来作为一个新的缓冲区，但现有的缓冲区与创建的子缓冲区在底层
数组层面上是数据共享的，也就是说，子缓冲区相当于是现有缓冲区的一个视图窗口。调用 slice()
方法可以创建一个子缓冲区，让我们通过例子来看一下：

```java
package com.gupaoedu.nio.buffer;
import java.nio.ByteBuffer;
public class BufferSlice {
static public void main( String args[] ) throws Exception {
ByteBuffer buffer = ByteBuffer.allocate( 10 );
// 缓冲区中的数据 0-9
for (int i=0; i<buffer.capacity(); ++i) {
buffer.put( (byte)i );
}
// 创建子缓冲区
buffer.position( 3 );
buffer.limit( 7 );
ByteBuffer slice = buffer.slice();
// 改变子缓冲区的内容
for (int i=0; i<slice.capacity(); ++i) {
byte b = slice.get( i );
b *= 10;
slice.put( i, b );
}
buffer.position( 0 );
buffer.limit( buffer.capacity() );
while (buffer.remaining()>0) {
System.out.println( buffer.get() );
}
}
}
```

在该示例中，分配了一个容量大小为 10 的缓冲区，并在其中放入了数据 0-9，而在该缓冲区基础之
上又创建了一个子缓冲区，并改变子缓冲区中的内容，从最后输出的结果来看，只有子缓冲区“可见
的”那部分数据发生了变化，并且说明子缓冲区与原缓冲区是数据共享的

### 只读缓冲区

只读缓冲区非常简单，可以读取它们，但是不能向它们写入数据。可以通过调用缓冲区的
asReadOnlyBuffer()方法，将任何常规缓冲区转 换为只读缓冲区，这个方法返回一个与原缓冲区完
全相同的缓冲区，并与原缓冲区共享数据，只不过它是只读的。如果原缓冲区的内容发生了变化，只
读缓冲区的内容也随之发生变化：

```java
package com.gupaoedu.nio.buffer;
import java.nio.*;
public class ReadAbleBuffer {
static public void main( String args[] ) throws Exception {
ByteBuffer buffer = ByteBuffer.allocate( 10 );
// 缓冲区中的数据 0-9
for (int i=0; i<buffer.capacity(); ++i) {
buffer.put( (byte)i );
}
// 创建只读缓冲区
ByteBuffer readonly = buffer.asReadOnlyBuffer();
// 改变原缓冲区的内容
for (int i=0; i<buffer.capacity(); ++i) {
byte b = buffer.get( i );
b *= 10;
buffer.put( i, b );
}
readonly.position(0);
readonly.limit(buffer.capacity());
// 只读缓冲区的内容也随之改变
while (readonly.remaining()>0) {
System.out.println( readonly.get());
}
}
}
```

如果尝试修改只读缓冲区的内容，则会报 ReadOnlyBufferException 异常。只读缓冲区对于保护数据
很有用。在将缓冲区传递给某个 对象的方法时，无法知道这个方法是否会修改缓冲区中的数据。创
建一个只读的缓冲区可以保证该缓冲区不会被修改。只可以把常规缓冲区转换为只读缓冲区，而不能
将只读的缓冲区转换为可写的缓冲区。

### 直接缓冲区

直接缓冲区是为加快 I/O 速度，使用一种特殊方式为其分配内存的缓冲区，JDK 文档中的描述为：给
定一个直接字节缓冲区，Java 虚拟机将尽最大努力直接对它执行本机 I/O 操作。也就是说，它会在
每一次调用底层操作系统的本机 I/O 操作之前(或之后)，尝试避免将缓冲区的内容拷贝到一个中间缓
冲区中或者从一个中间缓冲区中拷贝数据。要分配直接缓冲区，需要调用 allocateDirect()方法，
而不是 allocate()方法，使用方式与普通缓冲区并无区别，如下面的拷贝文件示例：

```java
import [java.io](http://java.io).*;
import java.nio.*;
import java.nio.channels.*;
public class DirectBuffer {
static public void main( String args[] ) throws Exception {
String infile = "e:\\test.txt";
FileInputStream fin = new FileInputStream( infile );
FileChannel fcin = fin.getChannel();
String outfile = String.format("e:\\testcopy.txt");
FileOutputStream fout = new FileOutputStream( outfile );
FileChannel fcout = fout.getChannel();
// 使用 allocateDirect，而不是 allocate
ByteBuffer buffer = ByteBuffer.allocateDirect( 1024 );
while (true) {
buffer.clear();
int r = fcin.read( buffer );
if (r==-1) {
break;
}
buffer.flip();
fcout.write( buffer );
}
}
}
```

内存映射文件 I/O
内存映射文件I/O是一种读和写文件数据的方法，它可以比常规的基于流或者基于通道的I/O快的多。
内存映射文件 I/O 是通过使文件中的数据出现为 内存数组的内容来完成的，这其初听起来似乎不过
就是将整个文件读到内存中，但是事实上并不是这样。一般来说，只有文件中实际读取或者写入的部
分才会映射到内存中。如下面的示例代码：

```java
package com.gupaoedu.nio.buffer;
import [java.io](http://java.io).*;
import java.nio.*;
import java.nio.channels.*;
public class MappedBuffer {
static private final int start = 0;
static private final int size = 1024;
static public void main( String args[] ) throws Exception {
RandomAccessFile raf = new RandomAccessFile( "e:\\test.txt", "rw" );
FileChannel fc = raf.getChannel();
MappedByteBuffer mbb = fc.map( FileChannel.MapMode.READ_WRITE,
start, size );
mbb.put( 0, (byte)97 );
mbb.put( 1023, (byte)122 );
raf.close();
}
}
```

## 通道 Channel

通道是一个对象，通过它可以读取和写入数据，当然了所有数据都通过 Buffer 对象来处理。
我们永远不会将字节直接写入通道中，相反是将数据写入包含一个或者多个字节的缓冲区。
同样不会直接从通道中读取字节，而是将数据从通道读入缓冲区，再从缓冲区获取这个字节。
在 NIO 中，提供了多种通道对象，而所有的通道对象都实现了 Channel 接口
使用 NIO 读取数据
在前面我们说过，任何时候读取数据，都不是直接从通道读取，而是从通道读取到缓冲区。
所以使用 NIO 读取数据可以分为下面三个步骤：

> \1. 从 FileInputStream 获取 Channel
> \2. 创建 Buffer
> \3. 将数据从 Channel 读取到 Buffer 中

下面是一个简单的使用 NIO 从文件中读取数据的例子：

```java
package com.gupaoedu.nio.channel;
import [java.io](http://java.io).*;
import java.nio.*;
import java.nio.channels.*;
public class FileInputProgram {
static public void main( String args[] ) throws Exception {
FileInputStream fin = new FileInputStream("c:\\test.txt");
// 获取通道
FileChannel fc = fin.getChannel();
// 创建缓冲区
ByteBuffer buffer = ByteBuffer.allocate(1024);
// 读取数据到缓冲区
fc.read(buffer);
buffer.flip();
while (buffer.remaining()>0) {
byte b = buffer.get();
System.out.print(((char)b));
}
fin.close();
}
}
```

### 使用 NIO 写入数据

使用 NIO 写入数据与读取数据的过程类似，同样数据不是直接写入通道，而是写入缓冲区，
可以分为下面三个步骤：

> \1. 从 FileInputStream 获取 Channel
> \2. 创建 Buffer
> \3. 将数据从 Channel 写入到 Buffer 中

下面是一个简单的使用 NIO 向文件中写入数据的例子：

```java
package com.gupaoedu.nio.channel;
import [java.io](http://java.io).*;
import java.nio.*;
import java.nio.channels.*;
public class FileOutputProgram {
static private final byte message [] = { 83, 111, 109, 101, 32,
98, 121, 116, 101, 115, 46 };
static public void main(String args[]) throws Exception {
FileOutputStream fout = new FileOutputStream("e:\\test.txt");
FileChannel fc = fout.getChannel();
ByteBuffer buffer = ByteBuffer.allocate(1024);
for (int i = 0; i < message.length; ++ i) {
buffer.put(message[i]);
}
buffer.flip();
fc.write(buffer);
fout.close();
}
}
```

## 反应堆 Reactor

阻塞 I/O  通信模型
假如现在你对阻塞 I/O 已有了一定了解，我们知道阻塞 I/O 在调用 InputStream.read()方
法时是阻塞的，它会一直等到数据到来时（或超时）才会返回；同样，在调用
ServerSocket.accept()方法时，也会一直阻塞到有客户端连接才会返回，每个客户端连接
过来后，服务端都会启动一个线程去处理该客户端的请求。阻塞 I/O 的通信模型示意图如下：
如果你细细分析，一定会发现阻塞 I/O 存在一些缺点。根据阻塞 I/O 通信模型，我总结了它
的两点缺点：
\1. 当客户端多时，会创建大量的处理线程。且每个线程都要占用栈空间和一些 CPU 时间
\2. 阻塞可能带来频繁的上下文切换，且大部分上下文切换可能是无意义的。在这种情况下
非阻塞式 I/O 就有了它的应用前景。
Java NIO 是在 jdk1.4 开始使用的，它既可以说成“新 I/O”，也可以说成非阻塞式 I/O。
下面是 Java NIO 的工作原理：
\1. 由一个专门的线程来处理所有的 IO 事件，并负责分发。
\2. 事件驱动机制：事件到的时候触发，而不是同步的去监视事件。
\3. 线程通讯：线程之间通过 wait,notify 等方式通讯。保证每次上下文切换都是有意义的。
减少无谓的线程切换。
下面贴出我理解的 Java NIO 的工作原理图：
（注：每个线程的处理流程大概都是读取数据、解码、计算处理、编码、发送响应。）

## 选择器 Selector

epoll模型
selector借鉴了linux的epoll模型

## channel.configureBlocking(false);

为了向下兼容（兼容jdk1.5以下的模型Bio），默认设置为阻塞。所以要手动设置这个参数。