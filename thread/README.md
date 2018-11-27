[TOC]

# 一，**什么时候使用并发线程**

线程出现的目的是什么？解决进程中多任务的实时性问题？

其实简单来说，也就是解决“阻塞”的问题，阻塞的意思就是程序运行到某个函数或过程后等待某些事件发生而暂时停止CPU占用的情况，也就是说会使得 CPU 闲置（类比：人与人之间的交谈，A和B聊天，C来了，A说了点什么，B长时间思考，这时C想和A说话，总不能因为B在思考，C就要一直等待吧！！）。

还有一些场景就是比如对于一个函数中的运算逻辑的性能问题，我们可以通过多线程的技术，使得一个函数中的多个逻辑运算通过多线程技术达到一个并行执行，从而提升性能。所以，多线程最终解决的就是“等待”的问题，所以简单总结的使用场景：

```properties
1, 通过并行计算提高程序执行性能。
2, 需要等待网络（了解TCP窗口协议）、I/O 响应导致耗费大量的执行时间，可以采用异步线程的方法式来减少阻塞。
```

# 二，**并发编程的基础**

## (1) 多少种状态

Java 线程既然能够创建，那么也势必会被销毁，所以线程是存在生命周期的，那么我们接下来从线程的生命周期开始去了解线程。线程一共有 6 种状态（NEW、RUNNABLE、BLOCKED、**WAITING、TIME_WAITING**、TERMINATED）

```properties
NEW：初始状态，线程被构建，但是还没有调用 start 方法
RUNNABLED：运行状态，JAVA 线程把操作系统中的就绪和运行两种状态统一称为“运行中”
BLOCKED：阻塞状态，表示线程进入等待状态,也就是线程因为某种原因放弃了 CPU 使用权，阻塞也分为几种情况
Ø 等待阻塞：运行的线程执行 wait 方法，jvm 会把当前线程放入到等待队列。
Ø 同步阻塞：运行的线程在获取对象的同步锁时，若该同步锁被其他线程锁占用了，那么 jvm 会把当前的线程放入到锁池中。
Ø 其他阻塞：运行的线程执行 Thread.sleep 或者 t.join 方法，或者发出了 I/O请求时，JVM 会把当前线程设置为阻塞状态，当 sleep 结束、join 线程终止、io 处理完毕则线程恢复。
TIME_WAITING：超时等待状态，超时以后自动返回。
TERMINATED：终止状态，表示当前线程执行完毕。
```

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml\wpsDBA2.tmp.jpg)

### ① 代码演示

```java
package com.train.thread01;

import java.util.concurrent.TimeUnit;

/**
 * @author lqd
 * @DATE 2018/11/15
 * @Description 线程状态
 */
public class ThreadStatus
{
    public static void main(String[] args) {
        new Thread(()->{
            while(true){
                try {
                    TimeUnit.SECONDS.sleep(100);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        },"timewaiting").start();
        new Thread(()->{
            while(true){
                synchronized (ThreadStatus.class){
                    try {
                        ThreadStatus.class.wait();
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
            }
        },"Waiting").start();
        new Thread(new BlockedDemo(),"BlockDemo-01").start();
        new Thread(new BlockedDemo(),"BlockDemo-02").start();
    }
    static class BlockedDemo extends Thread{
        public void run(){
            synchronized (BlockedDemo.class){
                while(true){
                    try {
                        TimeUnit.SECONDS.sleep(100);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
            }
        }
    }
}

```

•  打开终端或者命令提示符，键入“jps”，（JDK1.5 提供的一个显示当前所有 java进程 pid 的命令），可以获得相应进程的 pid

•  根据上一步骤获得的 pid，继续输入 jstack pid（jstack 是 java 虚拟机自带的一种堆栈跟踪工具。jstack 用于打印出给定的 java 进程 ID 或 core file 或远程调试服务的 Java 堆栈信息）

## (2) 线程启动和终止

线程的终止，并不是简单的调用 stop 命令去。虽然 api 仍然可以调用，但是和其他的线程控制方法如 suspend、resume 一样都是过期了的不建议使用，就拿 stop 来说，stop 方法在结束一个线程时并不会保证线程的资源正常释放，因此会导致程序可能出现一些不确定的状态。要优雅的去中断一个线程，在线程中提供了一个 interrupt 方法。

当其他线程通过调用当前线程的 interrupt 方法，表示向当前线程打个招呼，告诉他可以中断线程的执行了，至于什么时候中断，取决于当前线程自己。线程通过检查资深是否被中断来进行相应，可以通过 isInterrupted()来判断是否被中断。通过下面这个例子，来实现了线程终止的逻辑。

```java
package com.train.thread01;

import java.util.concurrent.TimeUnit;

/**
 * @author lqd
 * @DATE 2018/11/15
 * @Description xxxxx
 */
public class InterruptDemo
{
    private static int i;
    public static void main(String[] args) throws InterruptedException
    {
        Thread thread=new Thread(()->{
            while(!Thread.currentThread().isInterrupted()){
                i++;
            }
            System.out.println("Num:"+i);
            /**复位**/
            /*boolean ii=Thread.currentThread().isInterrupted();
            if(ii){
                System.out.println("before:"+ii);
                Thread.interrupted();//对线程进行复位，中断标识为false
                System.out.println("after:"+Thread.currentThread()
                        .isInterrupted());
            }*/
        },"interruptDemo");
        thread.start();
        TimeUnit.SECONDS.sleep(1);
        thread.interrupt();
    }
}

```

这种通过标识位或者中断操作的方式能够使线程在终止时有机会去清理资源，而不是武断地将线程停止，因此这种终止线程的做法显得更加安全和优雅。

## (3) 线程复位

有同学在问线程为什么要复位？首先我们来看看线程执行 interrupt 以后的源码是做了什么？

os_linux.cpp

```c
void os::interrupt(Thread* thread) {
  assert(Thread::current() == thread || Threads_lock->owned_by_self(),
    "possibility of dangling Thread pointer");

  OSThread* osthread = thread->osthread();

  if (!osthread->interrupted()) {
    osthread->set_interrupted(true);
    // More than one thread can get here with the same value of osthread,
    // resulting in multiple notifications.  We do, however, want the store
    // to interrupted() to be visible to other threads before we execute unpark().
    OrderAccess::fence();
    ParkEvent * const slp = thread->_SleepEvent ;
    if (slp != NULL) slp->unpark() ;
  }

  // For JSR166. Unpark even if interrupt status already was set
  if (thread->is_Java_thread())
    ((JavaThread*)thread)->parker()->unpark();

  ParkEvent * ev = thread->_ParkEvent ;
  if (ev != NULL) ev->unpark() ;

}
```

其实就是通过 unpark 去唤醒当前线程，并且设置一个标识位为 true。 并没有所谓的中断线程的操作，所以实际上，线程复位可以用来实现多个线程之间的通信。

# 三，**线程安全问题**

## (1) 硬件层面了解

### ① CPU高速缓存

线程是 CPU 调度的最小单元，线程涉及的目的最终仍然是更充分的利用计算机处理的效能，但是绝大部分的运算任务不能只依靠处理器“计算”就能完成处理器还需要与内存交互，比如读取运算数据、存储运算结果，这个 I/O 操作是很难消除的。而由于计算机的存储设备与处理器的运算速度差距非常大，所以现代计算机系统都会增加一层读写速度尽可能接近处理器运算速度的高速缓存来作为内存和处理器之间的缓冲：将运算需要使用的数据复制到缓存中，让运算能快速进行，当运算结束后再从缓存同步到内存之中。高速缓存从上到下越接近 CPU 速度越快，同时容量也越小。现在大部分的处理器都有二级或者三级缓存，从上到下依次为 L3 cache, L2 cache, L1 cache. 缓存又可以分为指令缓存和数据缓存，指令缓存用来缓存程序的代码，数据缓存用来缓存程序的数据

L1 Cache，一级缓存，本地 core 的缓存，分成 32K 的数据缓存 L1d 和 32k 指

令缓存 L1i，访问 L1 需要 3cycles，耗时大约 1ns；

L2 Cache，二级缓存，本地 core 的缓存，被设计为 L1 缓存与共享的 L3 缓存

之间的缓冲，大小为 256K，访问 L2 需要 12cycles，耗时大约 3ns；

L3 Cache，三级缓存，在同插槽的所有 core 共享 L3 缓存，分为多个 2M 的

段，访问 L3 需要 38cycles，耗时大约 12ns；

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml\wpsDBA3.tmp.jpg) 

### ② 缓存一致性问题

CPU-0 读取主存的数据，缓存到 CPU-0 的高速缓存中，CPU-1 也做了同样的事情，而 CPU-1 把 count 的值修改成了 2，并且同步到 CPU-1 的高速缓存，但是这个修改以后的值并没有写入到主存中，CPU-0 访问该字节，由于缓存没有更新，所以仍然是之前的值，就会导致数据不一致的问题。引发这个问题的原因是**因为多核心CPU 情况下存在指令并行执行，而各个CPU 核心之间的数据不共享从而导致缓存一致性问题**，为了解决这个问题，CPU 生产厂商提供了相应的解决方案。

### ③ 总线锁

当一个 CPU 对其缓存中的数据进行操作的时候，往总线中发送一个 Lock 信号。其他处理器的请求将会被阻塞，那么该处理器可以独占共享内存。总线锁相当于把 CPU 和内存之间的通信锁住了，所以这种方式会导致 CPU 的性能下降，所以P6系列以后的处理器，出现了另外一种方式，就是缓存锁。

### ④ 缓存锁

如果缓存在处理器缓存行中的内存区域在 LOCK 操作期间被锁定，当它执行锁操作回写内存时，不处理在总线上声明 LOCK 信号，而是**修改内部的缓存地址，然后通过缓存一致性机制来保证操作的原子性**，**因为****缓存一致性机制****会阻止同时修改被两个以上处理器缓存的内存区域的数据，当其他处理器回写已经被锁定的缓存行的数据时会导致该缓存行无效**。所以如果声明了 CPU 的锁机制，会生成一个 LOCK 指令，会产生两个作用：

```properties
1. Lock 前缀指令会引起引起处理器缓存回写到内存，在 P6 以后的处理器中，LOCK 信号一般不锁总线，而是锁缓存。
2. 一个处理器的缓存回写到内存会导致其他处理器的缓存无效
```

##### 缓存一致性协议	

处理器上有一套完整的协议，来保证 Cache 的一致性，比较经典的应该就是MESI 协议了，它的方法是在 CPU 缓存中保存一个标记位，这个标记为有四种状态

```properties
Ø M(Modified) 修改缓存，当前 CPU 缓存已经被修改，表示已经和内存中的数据不一致了
Ø I(Invalid) 失效缓存，说明 CPU 的缓存已经不能使用了
Ø E(Exclusive) 独占缓存，当前 cpu 的缓存和内存中数据保持一直，而且其他处理器没有缓存该数据
Ø S(Shared) 共享缓存，数据和内存中数据一致，并且该数据存在多个 cpu
```

缓存中每个 Core 的 Cache 控制器不仅知道自己的读写操作，也监听其它 Cache 的读写操作，嗅探（snooping）"协议。

```properties
CPU 的读取会遵循几个原则
\1. 如果缓存的状态是 I，那么就从内存中读取，否则直接从缓存读取
\2. 如果缓存处于 M 或者 E 的 CPU 嗅探到其他 CPU 有读的操作，就把自己的缓存写入到内存，并把自己的状态设置为S 
\3. 只有缓存状态是 M 或 E 的时候，CPU 才可以修改缓存中的数据，修改后，缓存状态变为 MC
```

### ⑤ CPU  的优化执行

除了增加高速缓存以为，为了更充分利用处理器内内部的运算单元，处理器可能会对输入的代码进行乱序执行优化，处理器会在计算之后将乱序执行的结果充足，保证该结果与顺序执行的结果一直，但并不保证程序中各个语句计算的先后顺序与输入代码中的顺序一致，这个是处理器的优化执行；还有一个就是编程语言的编译器也会有类似的优化，比如做指令重排来提升性能。

 

## (2) 软件层面

### ① JMM

上面谈的到底和软件有啥关系，其实**原子性、可见性、有序性**问题，是我们抽象出来的概念，他们的核心本质就是刚刚提到的缓存一致性问题、处理器优化问题导致的指令重排序问题。比如缓存一致性就导致可见性问题、处理器的乱序执行会导致原子性问题、指令重排会导致有序性问题。

 

为了解决这些问题，所以在 JVM 中引入了 JMM 的概念内存模型定义了共享内存系统中多线程程序读写操作行为的规范，来屏蔽各种硬件和操作系统的内存访问差异，来实现 Java 程序在各个平台下都能达到一致的内存访问效果。Java 内存模型的主要目标是**定义程序中各个变量的访问规则，也就是在虚拟机中将变量存储到内存以及从内存中取出变量**（这里的变量，指的是共享变量，也就是实例对象、静态字段、数组对象等存储在堆内存中的变量。而对于局部变量这类的，属于线程私有，不会被共享）**这类的底层细节**。通过这些规则来规范对内存的读写操作，从而保证指令执行的正确性。

它与处理器有关、与缓存有关、与并发有关、与编译器也有关。他**解决了 CPU多级缓存、处理器优化、指令重排等导致的内存访问问题，保证了并发场景下的可见性、原子性和有序性**。

内存模型解决并发问题主要采用两种方式：**限制处理器优化和使用内存屏障**。

 

Java 内存模型定义了线程和内存的交互方式，在 JMM 抽象模型中，分为主内存、工作内存。主内存是所有线程共享的，工作内存是每个线程独有的。线程对变量的所有操作（读取、赋值）都必须在工作内存中进行，不能直接读写主内存中的变量。并且不同的线程之间无法访问对方工作内存中的变量，线程间的变量值的传递都需要通过主内存来完成，

所以，总的来说，JMM 是一种规范，目的是解决由于多线程通过共享内存进行通信时，存在的本地内存数据不一致、编译器会对代码指令重排序、处理器会对代码乱序执行等带来的问题。目的是保证并发编程场景中的原子性、可见性和有序性他们三者的交互关系如下：

![img](file:///C:\Users\lqd\AppData\Local\Temp\ksohtml\wpsDBB3.tmp.jpg) 

### ② JMM怎么解决原子性、可见性、有序性的问题？	

在Java中提供了一系列和并发处理相关的关键字，比如volatile、Synchronized、final、juc等，这些就是Java内存模型封装了底层的实现后提供给开发人员使用的关键字在开发多线程代码的时候，我们可以直接使用synchronized等关键词来控制并发，使得我们不需要关心底层的编译器优化、缓存一致性的问题了，所以在Java内存模型中，除了定义了一套规范，还提供了开放的指令在底层进行封装后，提供给开发人员使用。

#### 1) 原子性

原子性是拒绝多线程操作的，不论是多核还是单核，具有原子性的量，同一时刻只能有一个线程来对它进行操作。简而言之，在整个操作过程中不会被线程调度器中断的操作，都可认为是原子性。例如 a=1是原子性操作，但是a++和a +=1就不是原子性操作。在java中提供了两个高级的字节码指令**monitorenter和monitorexit**，在Java中对应的Synchronized来保证代码块内的操作是原子的。

实例1：论证原子性

```java
package com.train.thread01;

import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * @author lqd
 * @DATE 2018/11/16
 * @Description 原子性
 */
public class VolatileAtomicityDemo
{
     // static volatile AtomicInteger atomicInteger = new AtomicInteger() ;
     static volatile int  count = 0 ;
     private static Object object = new Object();
     public  static void inc()
     {
         try {
             Thread.sleep(1);
         } catch (InterruptedException e) {
             e.printStackTrace();
         }
       /*  synchronized (object)
         {*/
            count++;
        /* }*/
        // atomicInteger.getAndIncrement();
     }

    public static void main(String[] args) throws InterruptedException {

        for(int j=0; j<1000;j++)
        {
            new Thread(()->{
                    inc();
            }).start();
        }
        TimeUnit.SECONDS.sleep(5);
       // System.out.println(atomicInteger.get());
        System.out.println(count);
    }
}

```

实例2：查看字节码，证明monitorenter和monitorexit

```java
package com.train.thread01;

/**
 * @author lqd
 * @DATE 2018/11/16
 * @Description xxxxx
 */
public class SynchronizedDemo
{
    public void getInstance()
    {
        synchronized (this) {
            System.out.printf("ok \\ getInstance");
        }
    }

    public static void main(String[] args) {

        new SynchronizedDemo().getInstance();
    }
}

```

> ```
> 输入命令：javap -p -v SynchronizedDemo.class > SynchronizedDemo.txt
> 查看字节码，如下：
> 
> Classfile /E:/workspace_train/thread/target/classes/com/train/thread01/SynchronizedDemo.class
>   Last modified 2018-11-16; size 849 bytes
>   MD5 checksum c2670be7cfec6eb50ecd5beb7aa69b5f
>   Compiled from "SynchronizedDemo.java"
> public class com.train.thread01.SynchronizedDemo
>   minor version: 0
>   major version: 52
>   flags: ACC_PUBLIC, ACC_SUPER
> Constant pool:
>    #1 = Methodref          #4.#27         // java/lang/Object."<init>":()V
>    #2 = Fieldref           #28.#29        // java/lang/System.out:Ljava/io/PrintStream;
>    #3 = String             #30            // ok \ getInstance
>    #4 = Class              #31            // java/lang/Object
>    #5 = Methodref          #32.#33        // java/io/PrintStream.printf:(Ljava/lang/String;[Ljava/lang/Object;)Ljava/io/PrintStream;
>    #6 = Class              #34            // com/train/thread01/SynchronizedDemo
>    #7 = Methodref          #6.#27         // com/train/thread01/SynchronizedDemo."<init>":()V
>    #8 = Methodref          #6.#35         // com/train/thread01/SynchronizedDemo.getInstance:()V
>    #9 = Utf8               <init>
>   #10 = Utf8               ()V
>   #11 = Utf8               Code
>   #12 = Utf8               LineNumberTable
>   #13 = Utf8               LocalVariableTable
>   #14 = Utf8               this
>   #15 = Utf8               Lcom/train/thread01/SynchronizedDemo;
>   #16 = Utf8               getInstance
>   #17 = Utf8               StackMapTable
>   #18 = Class              #34            // com/train/thread01/SynchronizedDemo
>   #19 = Class              #31            // java/lang/Object
>   #20 = Class              #36            // java/lang/Throwable
>   #21 = Utf8               main
>   #22 = Utf8               ([Ljava/lang/String;)V
>   #23 = Utf8               args
>   #24 = Utf8               [Ljava/lang/String;
>   #25 = Utf8               SourceFile
>   #26 = Utf8               SynchronizedDemo.java
>   #27 = NameAndType        #9:#10         // "<init>":()V
>   #28 = Class              #37            // java/lang/System
>   #29 = NameAndType        #38:#39        // out:Ljava/io/PrintStream;
>   #30 = Utf8               ok \ getInstance
>   #31 = Utf8               java/lang/Object
>   #32 = Class              #40            // java/io/PrintStream
>   #33 = NameAndType        #41:#42        // printf:(Ljava/lang/String;[Ljava/lang/Object;)Ljava/io/PrintStream;
>   #34 = Utf8               com/train/thread01/SynchronizedDemo
>   #35 = NameAndType        #16:#10        // getInstance:()V
>   #36 = Utf8               java/lang/Throwable
>   #37 = Utf8               java/lang/System
>   #38 = Utf8               out
>   #39 = Utf8               Ljava/io/PrintStream;
>   #40 = Utf8               java/io/PrintStream
>   #41 = Utf8               printf
>   #42 = Utf8               (Ljava/lang/String;[Ljava/lang/Object;)Ljava/io/PrintStream;
> {
>   public com.train.thread01.SynchronizedDemo();
>     descriptor: ()V
>     flags: ACC_PUBLIC
>     Code:
>       stack=1, locals=1, args_size=1
>          0: aload_0
>          1: invokespecial #1                  // Method java/lang/Object."<init>":()V
>          4: return
>       LineNumberTable:
>         line 8: 0
>       LocalVariableTable:
>         Start  Length  Slot  Name   Signature
>             0       5     0  this   Lcom/train/thread01/SynchronizedDemo;
> 
>   public void getInstance();
>     descriptor: ()V
>     flags: ACC_PUBLIC
>     Code:
>       stack=3, locals=3, args_size=1
>          0: aload_0
>          1: dup
>          2: astore_1
>          3: monitorenter
>          4: getstatic     #2                  // Field java/lang/System.out:Ljava/io/PrintStream;
>          7: ldc           #3                  // String ok \ getInstance
>          9: iconst_0
>         10: anewarray     #4                  // class java/lang/Object
>         13: invokevirtual #5                  // Method java/io/PrintStream.printf:(Ljava/lang/String;[Ljava/lang/Object;)Ljava/io/PrintStream;
>         16: pop
>         17: aload_1
>         18: monitorexit
>         19: goto          27
>         22: astore_2
>         23: aload_1
>         24: monitorexit
>         25: aload_2
>         26: athrow
>         27: return
>       Exception table:
>          from    to  target type
>              4    19    22   any
>             22    25    22   any
>       LineNumberTable:
>         line 12: 0
>         line 13: 4
>         line 14: 17
>         line 15: 27
>       LocalVariableTable:
>         Start  Length  Slot  Name   Signature
>             0      28     0  this   Lcom/train/thread01/SynchronizedDemo;
>       StackMapTable: number_of_entries = 2
>         frame_type = 255 /* full_frame */
>           offset_delta = 22
>           locals = [ class com/train/thread01/SynchronizedDemo, class java/lang/Object ]
>           stack = [ class java/lang/Throwable ]
>         frame_type = 250 /* chop */
>           offset_delta = 4
> 
>   public static void main(java.lang.String[]);
>     descriptor: ([Ljava/lang/String;)V
>     flags: ACC_PUBLIC, ACC_STATIC
>     Code:
>       stack=2, locals=1, args_size=1
>          0: new           #6                  // class com/train/thread01/SynchronizedDemo
>          3: dup
>          4: invokespecial #7                  // Method "<init>":()V
>          7: invokevirtual #8                  // Method getInstance:()V
>         10: return
>       LineNumberTable:
>         line 19: 0
>         line 20: 10
>       LocalVariableTable:
>         Start  Length  Slot  Name   Signature
>             0      11     0  args   [Ljava/lang/String;
> }
> SourceFile: "SynchronizedDemo.java"
> 
> ```

#### 2) 可见性

Java中的volatile关键字提供了一个功能，那就是被其修饰的变量在被修改后可以立即同步到主内存，被其修饰的变量在每次是用之前都从主内存刷新。因此，可以使用volatile来保证多线程操作时变量的可见性。除了volatile，Java中的synchronized和final两个关键字也可以实现可见性。

```java
package com.train.thread01;

import java.util.concurrent.TimeUnit;

/**
 * @author lqd
 * @DATE 2018/11/15
 * @Description 可见性
 */
public class VolatileVisibilityDemo
{
    //没有设置volatile,main线程与子线程的变量不可见
    volatile static boolean bol = false ;
    public static void main(String[] args) throws InterruptedException {
        Thread thread = new Thread(()->{
            while (!bol)
            {

            }
        });
        thread.start();
        TimeUnit.SECONDS.sleep(1L);
       // bol = true;
    }
}

```

#### 3) 有序性

在Java中，可以使用synchronized和volatile来保证多线程之间操作的有序性。实现方式有所区别：volatile关键字会禁止指令重排。synchronized关键字保证同一时刻只允许一条线程操作。

```java
package com.train.thread01;

/**
 * @author lqd
 * @DATE 2018/11/15
 * @Description 有序性
 */
public class VolatileOrderDemo
{
    private static int x = 0, y = 0;
    private static int a = 0, b = 0;

    public static void main(String[] args) throws InterruptedException
    {
        Thread t1 = new Thread(() -> {
            a = 1;
            x = b;
        });
        Thread t2 = new Thread(() -> {
            b = 1;
            y = a;
        });
        t1.start();
        t2.start();
        t1.join();
        t2.join();
        System.out.println("x=" + x + "->y =" + y );
    }
}

```

#### 4) volatile如何保证可见性？

volatile变量修饰的共享变量，**在进行写操作的时候会多出一个lock前缀的汇编令**，这个指令在前面我们讲解CPU高速缓存的时候提到过，会触发总线锁或者缓存锁，通过缓存一致性协议来解决可见性问题对于声明了volatile的变量进行写操作，JVM就会向处理器发送一条Lock前缀的指令，把这个变量所在的缓存行的数据写回到系统内存，再根据我们前面提到过的MESI的缓存一致性协议，来保证多CPU下的各个高速缓存中的数据的一致性。举例示范：查看汇编 关键字LOCK

查看以下代码的汇编代码指令

```java
package com.train.thread01;

/**
 * @author lqd
 * @DATE 2018/11/15
 * @Description 汇编
 */
public class VolatileDemo
{
    private volatile static int number = 0 ;

    public static int getNumber()
    {
       return number++;
    }

    public static void main(String[] args) {
        getNumber();
    }
}

```

下载hsdis工具 ，https://sourceforge.net/projects/fcml/files/fcml-1.1.1/hsdis-1.1.1-win32-amd64.zip/download
解压后存放到jre目录的server路径下
然后跑main函数，跑main函数之前，加入如下虚拟机参数：
-server -Xcomp -XX:+UnlockDiagnosticVMOptions -XX:+PrintAssembly -XX:CompileCommand=compileonly,*VolatileDemo.getNumber（替换成实际运行的代码）

汇编内容

> ```
> "C:\Program Files\Java\jre1.8.0_92\bin\java" -server -Xcomp -XX:+UnlockDiagnosticVMOptions -XX:+PrintAssembly -XX:CompileCommand=compileonly,*VolatileDemo.getNumber "-javaagent:C:\Program Files\JetBrains\IntelliJ IDEA 2017.1.1\lib\idea_rt.jar=53569:C:\Program Files\JetBrains\IntelliJ IDEA 2017.1.1\bin" -Dfile.encoding=UTF-8 -classpath "C:\Program Files\Java\jre1.8.0_92\lib\charsets.jar;C:\Program Files\Java\jre1.8.0_92\lib\deploy.jar;C:\Program Files\Java\jre1.8.0_92\lib\ext\access-bridge-64.jar;C:\Program Files\Java\jre1.8.0_92\lib\ext\cldrdata.jar;C:\Program Files\Java\jre1.8.0_92\lib\ext\dnsns.jar;C:\Program Files\Java\jre1.8.0_92\lib\ext\jaccess.jar;C:\Program Files\Java\jre1.8.0_92\lib\ext\jfxrt.jar;C:\Program Files\Java\jre1.8.0_92\lib\ext\localedata.jar;C:\Program Files\Java\jre1.8.0_92\lib\ext\nashorn.jar;C:\Program Files\Java\jre1.8.0_92\lib\ext\sunec.jar;C:\Program Files\Java\jre1.8.0_92\lib\ext\sunjce_provider.jar;C:\Program Files\Java\jre1.8.0_92\lib\ext\sunmscapi.jar;C:\Program Files\Java\jre1.8.0_92\lib\ext\sunpkcs11.jar;C:\Program Files\Java\jre1.8.0_92\lib\ext\zipfs.jar;C:\Program Files\Java\jre1.8.0_92\lib\javaws.jar;C:\Program Files\Java\jre1.8.0_92\lib\jce.jar;C:\Program Files\Java\jre1.8.0_92\lib\jfr.jar;C:\Program Files\Java\jre1.8.0_92\lib\jfxswt.jar;C:\Program Files\Java\jre1.8.0_92\lib\jsse.jar;C:\Program Files\Java\jre1.8.0_92\lib\management-agent.jar;C:\Program Files\Java\jre1.8.0_92\lib\plugin.jar;C:\Program Files\Java\jre1.8.0_92\lib\resources.jar;C:\Program Files\Java\jre1.8.0_92\lib\rt.jar;E:\workspace_train\thread\target\classes" com.train.thread01.VolatileDemo
> CompilerOracle: compileonly *VolatileDemo.getNumber
> Loaded disassembler from C:\Program Files\Java\jre1.8.0_92\bin\server\hsdis-amd64.dll
> Decoding compiled method 0x00000000037cb6d0:
> Code:
> Argument 0 is unknown.RIP: 0x37cb820 Code size: 0x00000150
> [Disassembling for mach='amd64']
> [Entry Point]
> [Verified Entry Point]
> [Constants]
>   # {method} {0x0000000018083288} 'getNumber' '()I' in 'com/train/thread01/VolatileDemo'
>   #           [sp+0x40]  (sp of caller)
>   0x00000000037cb820: mov     dword ptr [rsp+0ffffffffffffa000h],eax
>   0x00000000037cb827: push    rbp
>   0x00000000037cb828: sub     rsp,30h
>   0x00000000037cb82c: mov     rax,180834e0h     ;   {metadata(method data for {method} {0x0000000018083288} 'getNumber' '()I' in 'com/train/thread01/VolatileDemo')}
>   0x00000000037cb836: mov     esi,dword ptr [rax+0dch]
>   0x00000000037cb83c: add     esi,8h
>   0x00000000037cb83f: mov     dword ptr [rax+0dch],esi
>   0x00000000037cb845: mov     rax,18083280h     ;   {metadata({method} {0x0000000018083288} 'getNumber' '()I' in 'com/train/thread01/VolatileDemo')}
>   0x00000000037cb84f: and     esi,0h
>   0x00000000037cb852: cmp     esi,0h
>   0x00000000037cb855: je      37cb884h
>   0x00000000037cb85b: mov     rax,0d5efcad0h    ;   {oop(a 'java/lang/Class' = 'com/train/thread01/VolatileDemo')}
>   0x00000000037cb865: mov     esi,dword ptr [rax+68h]  ;*getstatic number
>                                                 ; - com.train.thread01.VolatileDemo::getNumber@0 (line 14)
> 
>   0x00000000037cb868: mov     rdi,rsi
>   0x00000000037cb86b: inc     edi
>   0x00000000037cb86d: mov     dword ptr [rax+68h],edi
>   0x00000000037cb870: lock add dword ptr [rsp],0h  ;*putstatic number
>                                                 ; - com.train.thread01.VolatileDemo::getNumber@6 (line 14)
> 
>   0x00000000037cb875: mov     rax,rsi
>   0x00000000037cb878: add     rsp,30h
>   0x00000000037cb87c: pop     rbp
>   0x00000000037cb87d: test    dword ptr [0df0100h],eax
>                                                 ;   {poll_return}
>   0x00000000037cb883: ret
>   0x00000000037cb884: mov     qword ptr [rsp+8h],rax
>   0x00000000037cb889: mov     qword ptr [rsp],0ffffffffffffffffh
>   0x00000000037cb891: call    37c13e0h          ; OopMap{off=118}
>                                                 ;*synchronization entry
>                                                 ; - com.train.thread01.VolatileDemo::getNumber@-1 (line 14)
>                                                 ;   {runtime_call}
>   0x00000000037cb896: jmp     37cb85bh
>   0x00000000037cb898: nop
>   0x00000000037cb899: nop
>   0x00000000037cb89a: mov     rax,qword ptr [r15+2a8h]
>   0x00000000037cb8a1: mov     r10,0h
>   0x00000000037cb8ab: mov     qword ptr [r15+2a8h],r10
>   0x00000000037cb8b2: mov     r10,0h
>   0x00000000037cb8bc: mov     qword ptr [r15+2b0h],r10
>   0x00000000037cb8c3: add     rsp,30h
>   0x00000000037cb8c7: pop     rbp
>   0x00000000037cb8c8: jmp     37bc8e0h          ;   {runtime_call}
>   0x00000000037cb8cd: hlt
>   0x00000000037cb8ce: hlt
>   0x00000000037cb8cf: hlt
>   0x00000000037cb8d0: hlt
>   0x00000000037cb8d1: hlt
>   0x00000000037cb8d2: hlt
>   0x00000000037cb8d3: hlt
>   0x00000000037cb8d4: hlt
>   0x00000000037cb8d5: hlt
>   0x00000000037cb8d6: hlt
>   0x00000000037cb8d7: hlt
>   0x00000000037cb8d8: hlt
>   0x00000000037cb8d9: hlt
>   0x00000000037cb8da: hlt
>   0x00000000037cb8db: hlt
>   0x00000000037cb8dc: hlt
>   0x00000000037cb8dd: hlt
>   0x00000000037cb8de: hlt
>   0x00000000037cb8df: hlt
> [Exception Handler]
> [Stub Code]
>   0x00000000037cb8e0: call    37beba0h          ;   {no_reloc}
>   0x00000000037cb8e5: mov     qword ptr [rsp+0ffffffffffffffd8h],rsp
>   0x00000000037cb8ea: sub     rsp,80h
>   0x00000000037cb8f1: mov     qword ptr [rsp+78h],rax
>   0x00000000037cb8f6: mov     qword ptr [rsp+70h],rcx
>   0x00000000037cb8fb: mov     qword ptr [rsp+68h],rdx
>   0x00000000037cb900: mov     qword ptr [rsp+60h],rbx
>   0x00000000037cb905: mov     qword ptr [rsp+50h],rbp
>   0x00000000037cb90a: mov     qword ptr [rsp+48h],rsi
>   0x00000000037cb90f: mov     qword ptr [rsp+40h],rdi
>   0x00000000037cb914: mov     qword ptr [rsp+38h],r8
>   0x00000000037cb919: mov     qword ptr [rsp+30h],r9
>   0x00000000037cb91e: mov     qword ptr [rsp+28h],r10
>   0x00000000037cb923: mov     qword ptr [rsp+20h],r11
>   0x00000000037cb928: mov     qword ptr [rsp+18h],r12
>   0x00000000037cb92d: mov     qword ptr [rsp+10h],r13
>   0x00000000037cb932: mov     qword ptr [rsp+8h],r14
>   0x00000000037cb937: mov     qword ptr [rsp],r15
>   0x00000000037cb93b: mov     rcx,59b83510h     ;   {external_word}
>   0x00000000037cb945: mov     rdx,37cb8e5h      ;   {internal_word}
>   0x00000000037cb94f: mov     r8,rsp
>   0x00000000037cb952: and     rsp,0fffffffffffffff0h
>   0x00000000037cb956: call    59840390h         ;   {runtime_call}
>   0x00000000037cb95b: hlt
> [Deopt Handler Code]
>   0x00000000037cb95c: mov     r10,37cb95ch      ;   {section_word}
>   0x00000000037cb966: push    r10
>   0x00000000037cb968: jmp     3707600h          ;   {runtime_call}
>   0x00000000037cb96d: hlt
>   0x00000000037cb96e: hlt
>   0x00000000037cb96f: hlt
> Decoding compiled method 0x00000000037cd510:
> Code:
> Argument 0 is unknown.RIP: 0x37cd660 Code size: 0x00000110
> [Entry Point]
> [Verified Entry Point]
> [Constants]
>   # {method} {0x0000000018083288} 'getNumber' '()I' in 'com/train/thread01/VolatileDemo'
>   #           [sp+0x40]  (sp of caller)
>   0x00000000037cd660: mov     dword ptr [rsp+0ffffffffffffa000h],eax
>   0x00000000037cd667: push    rbp
>   0x00000000037cd668: sub     rsp,30h
>   0x00000000037cd66c: mov     rax,0d5efcad0h    ;   {oop(a 'java/lang/Class' = 'com/train/thread01/VolatileDemo')}
>   0x00000000037cd676: mov     esi,dword ptr [rax+68h]  ;*getstatic number
>                                                 ; - com.train.thread01.VolatileDemo::getNumber@0 (line 14)
> 
>   0x00000000037cd679: mov     rdi,rsi
>   0x00000000037cd67c: inc     edi
>   0x00000000037cd67e: mov     dword ptr [rax+68h],edi
>   0x00000000037cd681: lock add dword ptr [rsp],0h  ;*putstatic number
>                                                 ; - com.train.thread01.VolatileDemo::getNumber@6 (line 14)
> 
>   0x00000000037cd686: mov     rax,rsi
>   0x00000000037cd689: add     rsp,30h
>   0x00000000037cd68d: pop     rbp
>   0x00000000037cd68e: test    dword ptr [0df0100h],eax
>                                                 ;   {poll_return}
>   0x00000000037cd694: ret
>   0x00000000037cd695: nop
>   0x00000000037cd696: nop
>   0x00000000037cd697: mov     rax,qword ptr [r15+2a8h]
>   0x00000000037cd69e: mov     r10,0h
>   0x00000000037cd6a8: mov     qword ptr [r15+2a8h],r10
>   0x00000000037cd6af: mov     r10,0h
>   0x00000000037cd6b9: mov     qword ptr [r15+2b0h],r10
>   0x00000000037cd6c0: add     rsp,30h
>   0x00000000037cd6c4: pop     rbp
>   0x00000000037cd6c5: jmp     37bc8e0h          ;   {runtime_call}
>   0x00000000037cd6ca: hlt
>   0x00000000037cd6cb: hlt
>   0x00000000037cd6cc: hlt
>   0x00000000037cd6cd: hlt
>   0x00000000037cd6ce: hlt
>   0x00000000037cd6cf: hlt
>   0x00000000037cd6d0: hlt
>   0x00000000037cd6d1: hlt
>   0x00000000037cd6d2: hlt
>   0x00000000037cd6d3: hlt
>   0x00000000037cd6d4: hlt
>   0x00000000037cd6d5: hlt
>   0x00000000037cd6d6: hlt
>   0x00000000037cd6d7: hlt
>   0x00000000037cd6d8: hlt
>   0x00000000037cd6d9: hlt
>   0x00000000037cd6da: hlt
>   0x00000000037cd6db: hlt
>   0x00000000037cd6dc: hlt
>   0x00000000037cd6dd: hlt
>   0x00000000037cd6de: hlt
>   0x00000000037cd6df: hlt
> [Exception Handler]
> [Stub Code]
>   0x00000000037cd6e0: call    37beba0h          ;   {no_reloc}
>   0x00000000037cd6e5: mov     qword ptr [rsp+0ffffffffffffffd8h],rsp
>   0x00000000037cd6ea: sub     rsp,80h
>   0x00000000037cd6f1: mov     qword ptr [rsp+78h],rax
>   0x00000000037cd6f6: mov     qword ptr [rsp+70h],rcx
>   0x00000000037cd6fb: mov     qword ptr [rsp+68h],rdx
>   0x00000000037cd700: mov     qword ptr [rsp+60h],rbx
>   0x00000000037cd705: mov     qword ptr [rsp+50h],rbp
>   0x00000000037cd70a: mov     qword ptr [rsp+48h],rsi
>   0x00000000037cd70f: mov     qword ptr [rsp+40h],rdi
>   0x00000000037cd714: mov     qword ptr [rsp+38h],r8
>   0x00000000037cd719: mov     qword ptr [rsp+30h],r9
>   0x00000000037cd71e: mov     qword ptr [rsp+28h],r10
>   0x00000000037cd723: mov     qword ptr [rsp+20h],r11
>   0x00000000037cd728: mov     qword ptr [rsp+18h],r12
>   0x00000000037cd72d: mov     qword ptr [rsp+10h],r13
>   0x00000000037cd732: mov     qword ptr [rsp+8h],r14
>   0x00000000037cd737: mov     qword ptr [rsp],r15
>   0x00000000037cd73b: mov     rcx,59b83510h     ;   {external_word}
>   0x00000000037cd745: mov     rdx,37cd6e5h      ;   {internal_word}
>   0x00000000037cd74f: mov     r8,rsp
>   0x00000000037cd752: and     rsp,0fffffffffffffff0h
>   0x00000000037cd756: call    59840390h         ;   {runtime_call}
>   0x00000000037cd75b: hlt
> [Deopt Handler Code]
>   0x00000000037cd75c: mov     r10,37cd75ch      ;   {section_word}
>   0x00000000037cd766: push    r10
>   0x00000000037cd768: jmp     3707600h          ;   {runtime_call}
>   0x00000000037cd76d: hlt
>   0x00000000037cd76e: hlt
>   0x00000000037cd76f: hlt
> Java HotSpot(TM) 64-Bit Server VM warning: PrintAssembly is enabled; turning on DebugNonSafepoints to gain additional output
> 
> Process finished with exit code 0
> 
> ```



#### 5) volatile防止指令重排序？

> 指令重排的目的是为了最大化的提高CPU利用率以及性能，CPU的乱序执优化在单核时代并不影响正确性，但是在多核时代的多线程能够在不同的核心上实现真正的并行，**一旦线程之间共享数据**，就可能会出现一些不可预料的问题。指令重排序必须要遵循的原则是，不影响代码执行的最终结果，编译器和处理器不会改变存在数据依赖关系的两个操作的执行顺序，(这里所说的数据依赖性仅仅是针对单个处理器中执行的指令和单个线程中执行的操作.)这个语义，实际上就是as-if-serial语义，不管怎么重排序，单线程程序的执行结果不会改变，编译器、处理器都必须遵守as-if-serial语义。
>

##### 扩展 - CPU内存屏障 以及 JMM中把内存屏障

> 内存屏障需要解决我们前面提到的两个问题，一个是编译器的优化乱序和CPU的执行乱序，我们可以分别使用优化屏障和内存屏障这两个机制来解决。
>
> 从CPU层面来了解一下什么是内存屏障？
>
> CPU的乱序执行，本质还是，由于在多CPU的机器上，每个CPU都	存在cache，当一个特定数据第一次被特定一个CPU获取时，由于在该CPU缓存中不存在，就会从内存中去获取，被加载到CPU高速缓存中后就能从缓存中快速访问。当某个CPU进行写操作时，它必须确保其他的CPU已经将这个数据从他们的缓存中移除，这样才能让其他CPU安全的修改数据。显然，存在多个cache时，我们必须通过一个cache一致性协议来避免数据不一致的问题，而这个通讯的过程就可能导致乱序访问的问题，也就是运行时的内存乱序访问。
>
> 现在的CPU架构都提供了内存屏障功能，在x86的cpu中，实现了相应的内存屏障。写屏障(store barrier)、读屏障(load barrier)和全屏障(Full 	Barrier)，主要的作用是
>
> ​		Ø 防止指令之间的重排序
>
> ​		Ø 保证数据的可见性
>
> 总结：内存屏障只是解决顺序一致性问题，不解决缓存一致性问题，	缓存一致性是由cpu的缓存锁以及MESI协议来完成的。在编译器层面，通过volatile关键字，取消编译器层面的缓存和重排序。保证编译程序时在优化屏障之前的指令不会在优化屏障之后执行。这就保证了编译时期的优化不会影响到实际代码逻辑顺序。
>
> JMM中把内存屏障指令分为4类:
>
> LoadLoad Barriers, load1 ; LoadLoad; load2 , 确保load1数据的装载优先于load2及所有后续装载指令的装载
>
> StoreStore Barriers，store1; storestore;store2 , 确保store1数据对其他处理器可见优先于store2及所有后续存储指令的存储
>
> LoadStore Barries， load1;loadstore;store2, 确保load1数据装载优先于store2以及后续的存储指令刷新到内存
>
> StoreLoad Barries， store1; storeload;load2, 确保store1数据对其他处理器变得可见， 优先于load2及所有后续装载指令的装载；这条内存屏障指令是一个全能型的屏障，在前面讲cpu层面的内存屏障的时候有提到。它同时具有其他3条屏障的效果
>

# 四，synchronized的使用

在多线程并发编程中synchronized一直是元老级角色，很多人都会称呼它为重量级锁。但是，随着Java SE 1.6对
synchronized进行了各种优化之后，有些情况下它就并不那么重了，Java SE 1.6中为了减少获得锁和释放锁带来的性能消耗而引入的偏向锁和轻量级锁，以及锁的存储结构和升级过程。我们仍然沿用前面使用的案例，然后通过
synchronized关键字来修饰在inc的方法上。再看看执行结果。

```java
public class Demo{
  private static int count=0;
  public static void inc(){
    synchronized (Demo.class) {
      try {
        Thread.sleep(1);
     } catch (InterruptedException e) {
        e.printStackTrace();
     }
      count++;
   }
 }
  public static void main(String[] args) throws InterruptedException {
    for(int i=0;i<1000;i++){
      new Thread(()->Demo.inc()).start();
   }
    Thread.sleep(3000);
    System.out.println("运行结果"+count);
 }
}
```

## synchronized的三种应用方式

> ```
> synchronized有三种方式来加锁，分别是
> \1. 修饰实例方法，作用于当前实例加锁，进入同步代码前要获得当前实例的锁	
> \2. 静态方法，作用于当前类对象加锁，进入同步代码前要获得当前类对象的锁
> \3. 修饰代码块，指定加锁对象，对给定对象加锁，进入同步代码库前要获得给定对象的锁。
> ```

### synchronized括号后面的对象

> synchronized扩后后面的对象是一把锁，在java中任意一个对象都可以成为锁，简单来说，我们把object比喻是一个key，拥有这个key的线程才能执行这个方法，拿到这个key以后在执行方法过程中，这个key是随身携带的，并且只有一把。
>
> 如果后续的线程想访问当前方法，因为没有key所以不能访问只能在门口等着，等之前的线程把key放回去。所以，synchronized锁定的对象必须是同一个，如果是不同对象，就意味着是不同的房间的钥匙，对于访问者来说是没有任何影响的。

### synchronized的字节码指令

> 通过javap -v 来查看对应代码的字节码指令，对于同步块的实现使用了monitorenter和monitorexit指令，前面我们在讲JMM的时候，提到过这两个指令，他们隐式的执行了Lock和UnLock操作，用于提供原子性保证。
> monitorenter指令插入到同步代码块开始的位置、monitorexit指令插入到同步代码块结束位置，jvm需要保证每个monitorenter都有一个monitorexit对应。
> 这两个指令，本质上都是对一个对象的监视器(monitor)进行获取，这个过程是排他的，也就是说同一时刻只能有一个线程获取到由synchronized所保护对象的监视器线程执行到monitorenter指令时，会尝试获取对象所对应的monitor所有权，也就是尝试获取对象的锁；而执行monitorexit，就是释放monitor的所有权。

## synchronized的锁的原理

jdk1.6以后对synchronized锁进行了优化，包含偏向锁、轻量级锁、重量级锁; 在了解synchronized锁之前，我们
需要了解两个重要的概念，一个是对象头、另一个是monitor

### Java对象头

在Hotspot虚拟机中，对象在内存中的布局分为三块区域：对象头、实例数据和对齐填充；Java对象头是实现
synchronized的锁对象的基础，一般而言，synchronized使用的锁对象是存储在Java对象头里。它是轻量级锁和偏向锁的关键

### Mark Word

Mark Word用于存储对象自身的运行时数据，如哈希码（HashCode）、GC分代年龄、锁状态标志、线程持有的
锁、偏向线程 ID、偏向时间戳等等。Java对象头一般占有两个机器码（在32位虚拟机中，1个机器码等于4字节，
也就是32bit）

![1542512989510](C:\Users\lqd\AppData\Roaming\Typora\typora-user-images\1542512989510.png)

在源码中的体现:

如果想更深入了解对象头在JVM源码中的定义，需要关心几个文件，oop.hpp/markOop.hpp
oop.hpp，每个 Java Object 在 JVM 内部都有一个 native 的 C++ 对象 oop/oopDesc 与之对应。先在oop.hpp中看oopDesc的定义.

```c
class oopDesc {
  friend class VMStructs;
 private:
  volatile markOop  _mark;
  union _metadata {
    Klass*      _klass;
    narrowKlass _compressed_klass;
  } _metadata;

  // Fast access to barrier set.  Must be initialized.
  static BarrierSet* _bs;
```

_mark 被声明在 oopDesc 类的顶部，所以这个 _mark 可以认为是一个 头部, 前面我们讲过头部保存了一些重要的
状态和标识信息，在markOop.hpp文件中有一些注释说明markOop的内存布局.

### Monitor

什么是Monitor？我们可以把它理解为一个同步工具，也可以描述为一种同步机制。所有的Java对象是天生的
Monitor，每个object的对象里 markOop->monitor() 里可以保存ObjectMonitor的对象。从源码层面分析一下
monitor对象.
Ø oop.hpp下的oopDesc类是JVM对象的顶级基类，所以每个object对象都包含markOop
Ø markOop.hpp**中** markOopDesc继承自oopDesc，并扩展了自己的monitor方法，这个方法返回一个ObjectMonitor指针对象
Ø objectMonitor.hpp,在hotspot虚拟机中，采用ObjectMonitor类来实现monitor.

## synchronized的锁升级和获取过程

> 了解了对象头以及monitor以后，接下来去分析synchronized的锁的实现，就会非常简单了。
>
> 前面讲过synchronized的锁是进行过优化的，引入了偏向锁、轻量级锁；
>
> 锁的级别从低到高逐步升级， 无锁->偏向锁->轻量级锁->重量级锁.

### 自旋锁（CAS）

> 自旋锁就是让不满足条件的线程等待一段时间，而不是立即挂起。看持有锁的线程是否能够很快释放锁。
>
> 怎么自旋呢？其实就是一段没有任何意义的循环。
>
> 虽然它通过占用处理器的时间来避免线程切换带来的开销，但是如果持有锁的线程不能在很快释放锁，那么自旋的线程就会浪费处理器的资源，因为它不会做任何有意义的工作。所以，自旋等待的时间或者次数是有一个限度的，如果自旋超过了定义的时间仍然没有获取到锁，则该线程应该被挂起.

### 偏向锁

> 大多数情况下，锁不仅不存在多线程竞争，而且总是由同一线程多次获得，为了让线程获得锁的代价更低而引入了偏向锁。
>
> 当一个线程访问同步块并获取锁时，会在对象头和栈帧中的锁记录里存储锁偏向的线程ID，以后该线程在进入和退出同步块时不需要进行CAS操作来加锁和解锁，只需简单地测试一下对象头的Mark Word里是否存储着指向当前线程的偏向锁。
>
> 如果测试成功，表示线程已经获得了锁。如果测试失败，则需要再测试一下Mark Word中偏向锁的标识是否设置成1（表示当前是偏向锁）：如果没有设置，则使用CAS竞争锁；如果设置了，则尝试使用CAS将对象头的偏向锁指向当前线程.

### 轻量级锁

> 引入轻量级锁的主要目的是在多没有多线程竞争的前提下，减少传统的重量级锁使用操作系统互斥量产生的性能消耗。
>
> 当关闭偏向锁功能或者多个线程竞争偏向锁导致偏向锁升级为轻量级锁，则会尝试获取轻量级锁.

### 重量级锁

> 重量级锁通过对象内部的监视器（monitor）实现，其中monitor的本质是依赖于底层操作系统的Mutex Lock实现，操作系统实现线程之间的切换需要从用户态到内核态的切换，切换成本非常高。
>
> 前面我们在讲Java对象头的时候，讲到了monitor这个对象，在hotspot虚拟机中，通过ObjectMonitor类来实现monitor。他的锁的获取过程的体现会简单很多

![1542513861141](C:\Users\lqd\AppData\Roaming\Typora\typora-user-images\1542513861141.png)

### 总结

> 重量级锁会阻塞、唤醒请求加锁的线程。它针对的是多个线程同时竞争同一把锁的情况。Java 虚拟机采取了自适应自旋，来避免线程在面对非常小的 synchronized 代码块时，仍会被阻塞、唤醒的情况。
>
> 轻量级锁采用 CAS 操作，将锁对象的标记字段替换为一个指针，指向当前线程栈上的一块空间，存储着锁对象原本的标记字段。它针对的是多个线程在不同时间段申请同一把锁的情况。
>
> 偏向锁只会在第一次请求时采用 CAS 操作，在锁对象的标记字段中记录下当前线程的地址。在之后的运行过程中，持有该偏向锁的线程的加锁操作将直接返回。它针对的是锁仅会被同一线程持有的情况。

### wait和notify

*wait和notify是用来让线程进入等待状态以及使得线程唤醒的两个操作*

```java
package com.train.thread02;

/**
 * @author lqd
 * @DATE 2018/11/18
 * @Description xxxxx
 */
public class ThreadWait extends Thread {
    private Object lock;

    public ThreadWait(Object lock) {
        this.lock = lock;
    }

    @Override
    public void run() {
        synchronized (lock) {
            System.out.println("开始执行 thread wait");
            try {
                lock.wait();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            System.out.println("执行结束 thread wait");
        }
    }
}

```

```java
package com.train.thread02;

/**
 * @author lqd
 * @DATE 2018/11/18
 * @Description xxxxx
 */
public class ThreadNotify implements  Runnable{

    private Object lock;

    public ThreadNotify(Object lock) {
        this.lock = lock;
    }

    @Override
    public void run() {
        synchronized (lock) {
            System.out.println("开始执行 thread notify");
            lock.notify();
            System.out.println("执行结束 thread notify");
        }
    }
}

```

### wait和notify的原理

调用wait方法，首先会获取监视器锁，获得成功以后，会让当前线程进入等待状态进入等待队列并且释放锁；

然后当其他线程调用notify或者notifyall以后，会选择从等待队列中唤醒任意一个线程，而执行完notify方法以后，并不会立马唤醒线程，原因是当前的线程仍然持有这把锁，处于等待状态的线程无法获得锁。

必须要等到当前的线程执行完按monitorexit指令以后，也就是锁被释放以后，处于等待队列中的线程就可以开始竞争锁了.

![1542519962625](C:\Users\lqd\AppData\Roaming\Typora\typora-user-images\1542519962625.png)

### wait和notify为什么需要在synchronized里面？

wait方法的语义有两个，一个是释放当前的对象锁、另一个是使得当前线程进入阻塞队列， 而这些操作都和监视器是相关的，所以wait必须要获得一个监视器锁。
而对于notify来说也是一样，它是唤醒一个线程，既然要去唤醒，首先得知道它在哪里？所以就必须要找到这个对
象获取到这个对象的锁，然后到这个对象的等待队列中去唤醒一个线程。

# 五，同步锁

我们知道，锁是用来控制多个线程访问共享资源的方式，一般来说，一个锁能够防止多个线程同时访问共享资源，
在Lock接口出现之前，Java应用程序只能依靠synchronized关键字来实现同步锁的功能，

在java5以后，增加了JUC的并发包且提供了Lock接口用来实现锁的功能，它提供了与synchroinzed关键字类似的同步功能，只是它比synchronized更灵活，能够显示的获取和释放锁。

## Lock的初步使用

Lock是一个接口，核心的两个方法lock和unlock，它有很多的实现，比如ReentrantLock、
ReentrantReadWriteLock;

### ReentrantLock

重入锁，表示支持重新进入的锁，也就是说，如果当前线程t1通过调用lock方法获取了锁之后，再次调用lock，是
不会再阻塞去获取锁的，直接增加重试次数就行了。

```java
package com.train.thread02;

import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

/**
 * @author lqd
 * @DATE 2018/11/18
 * @Description xxxxx
 */
public class AtomicDemo {
    static Lock lock = new ReentrantLock();
    private static int count = 0;

    public static void inc() {
        lock.lock();
        try {
            Thread.sleep(1);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        count++;
        System.out.printf("当前线程【%s】",Thread.currentThread().getName());
        lock.unlock();
    }

    public static void main(String[] args) throws InterruptedException {
        for (int i = 0; i < 1000; i++) {
            new Thread(() -> {
                AtomicDemo.inc();
            }).start();
        }
        Thread.sleep(3000);
        System.out.println("result:" + count);
    }
}

```

### ReentrantReadWriteLock

我们以前理解的锁，基本都是排他锁，也就是这些锁在同一时刻只允许一个线程进行访问，而读写所在同一时刻可
以允许多个线程访问，但是在写线程访问时，所有的读线程和其他写线程都会被阻塞。读写锁维护了一对锁，一个
读锁、一个写锁;

 一般情况下，读写锁的性能都会比排它锁好，因为大多数场景读是多于写的。在读多于写的情况下，读写锁能够提供比排它锁更好的并发性和吞吐量.

```java
package com.train.thread02;

import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantReadWriteLock;

/**
 * @author lqd
 * @DATE 2018/11/18
 * @Description xxxxx
 */
public class LockDemo
{
    static Map<String, Object> cacheMap = new HashMap<>();
    static ReentrantReadWriteLock rwl = new ReentrantReadWriteLock();
    static Lock read = rwl.readLock();
    static Lock write = rwl.writeLock();

    public static final Object get(String key) {
        System.out.println("开始读取数据");
        read.lock(); //读锁
        try {
            return cacheMap.get(key);
        } finally {
            read.unlock();
        }
    }

    public static final Object put(String key, Object value) {
        write.lock();
        System.out.println("开始写数据");
        try {
            return cacheMap.put(key, value);
        } finally {
            write.unlock();
        }
    }
}
```

在这个案例中，通过hashmap来模拟了一个内存缓存，然后使用读写所来保证这个内存缓存的线程安全性。

当执行读操作的时候，需要获取读锁，在并发访问的时候，读锁不会被阻塞，因为读操作不会影响执行结果。
在执行写操作是，线程必须要获取写锁，当已经有线程持有写锁的情况下，当前线程会被阻塞，只有当写锁释放以
后，其他读写操作才能继续执行。使用读写锁提升读操作的并发性，也保证每次写操作对所有的读写操作的可见性。
l 读锁与读锁可以共享
l 读锁与写锁不可以共享（排他）
l 写锁与写锁不可以共享（排他）

## Lock和synchronized的简单对比

通过我们对Lock的使用以及对synchronized的了解，基本上可以对比出这两种锁的区别了。因为这个也是在面试
过程中比较常见的问题：

```properties
Ø 从层次上，一个是关键字、一个是类， 这是最直观的差异
Ø 从使用上，lock具备更大的灵活性，可以控制锁的释放和获取； 而synchronized的锁的释放是被动的，当出现
异常或者同步代码块执行完以后，才会释放锁
Ø lock可以判断锁的状态、而synchronized无法做到
Ø lock可以实现公平锁、非公平锁； 而synchronized只有非公平锁
```

## AQS

> Lock之所以能实现线程安全的锁，主要的核心是AQS(AbstractQueuedSynchronizer),AbstractQueuedSynchronizer提供了一个FIFO队列，可以看做是一个用来实现锁以及其他需要同步功能的框架。这里简称该类为AQS。
>
> AQS的使用依靠继承来完成，子类通过继承自AQS并实现所需的方法来管理同步状态。例如常见ReentrantLock，CountDownLatch等AQS的两种功能。
>
> 从使用上来说，AQS的功能可以分为两种：独占和共享。
> 独占锁模式下，每次只能有一个线程持有锁，比如前面给大家演示的ReentrantLock就是以独占方式实现的互斥锁。共享锁模式下，允许多个线程同时获取锁，并发访问共享资源，比如ReentrantReadWriteLock。
>
> 很显然，独占锁是一种悲观保守的加锁策略，它限制了读/读冲突，如果某个只读线程获取锁，则其他读线程都只能等待，这种情况下就限制了不必要的并发性，因为读操作并不会影响数据的一致性。共享锁则是一种乐观锁，它放宽了加锁策略，允许多个执行读操作的线程同时访问共享资源

### AQS的内部实现

同步器依赖内部的同步队列（一个FIFO双向队列）来完成同步状态的管理，当前线程获取同步状态失败时，同步器会将当前线程以及等待状态等信息构造成为一个节点（Node）并将其加入同步队列，同时会阻塞当前线程，当同步状态释放时，会把首节点中的线程唤醒，使其再次尝试获取同步状态。

AbstractQueuedSynchronizer类内容如下：

```java
/*
 * ORACLE PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.
 * Written by Doug Lea with assistance from members of JCP JSR-166
 * Expert Group and released to the public domain, as explained at
 * http://creativecommons.org/publicdomain/zero/1.0/
 */

package java.util.concurrent.locks;
import java.util.concurrent.TimeUnit;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Date;
import sun.misc.Unsafe;

/**
 * Provides a framework for implementing blocking locks and related
 * synchronizers (semaphores, events, etc) that rely on
 * first-in-first-out (FIFO) wait queues.  This class is designed to
 * be a useful basis for most kinds of synchronizers that rely on a
 * single atomic {@code int} value to represent state. Subclasses
 * must define the protected methods that change this state, and which
 * define what that state means in terms of this object being acquired
 * or released.  Given these, the other methods in this class carry
 * out all queuing and blocking mechanics. Subclasses can maintain
 * other state fields, but only the atomically updated {@code int}
 * value manipulated using methods {@link #getState}, {@link
 * #setState} and {@link #compareAndSetState} is tracked with respect
 * to synchronization.
 *
 * <p>Subclasses should be defined as non-public internal helper
 * classes that are used to implement the synchronization properties
 * of their enclosing class.  Class
 * {@code AbstractQueuedSynchronizer} does not implement any
 * synchronization interface.  Instead it defines methods such as
 * {@link #acquireInterruptibly} that can be invoked as
 * appropriate by concrete locks and related synchronizers to
 * implement their public methods.
 *
 * <p>This class supports either or both a default <em>exclusive</em>
 * mode and a <em>shared</em> mode. When acquired in exclusive mode,
 * attempted acquires by other threads cannot succeed. Shared mode
 * acquires by multiple threads may (but need not) succeed. This class
 * does not &quot;understand&quot; these differences except in the
 * mechanical sense that when a shared mode acquire succeeds, the next
 * waiting thread (if one exists) must also determine whether it can
 * acquire as well. Threads waiting in the different modes share the
 * same FIFO queue. Usually, implementation subclasses support only
 * one of these modes, but both can come into play for example in a
 * {@link ReadWriteLock}. Subclasses that support only exclusive or
 * only shared modes need not define the methods supporting the unused mode.
 *
 * <p>This class defines a nested {@link ConditionObject} class that
 * can be used as a {@link Condition} implementation by subclasses
 * supporting exclusive mode for which method {@link
 * #isHeldExclusively} reports whether synchronization is exclusively
 * held with respect to the current thread, method {@link #release}
 * invoked with the current {@link #getState} value fully releases
 * this object, and {@link #acquire}, given this saved state value,
 * eventually restores this object to its previous acquired state.  No
 * {@code AbstractQueuedSynchronizer} method otherwise creates such a
 * condition, so if this constraint cannot be met, do not use it.  The
 * behavior of {@link ConditionObject} depends of course on the
 * semantics of its synchronizer implementation.
 *
 * <p>This class provides inspection, instrumentation, and monitoring
 * methods for the internal queue, as well as similar methods for
 * condition objects. These can be exported as desired into classes
 * using an {@code AbstractQueuedSynchronizer} for their
 * synchronization mechanics.
 *
 * <p>Serialization of this class stores only the underlying atomic
 * integer maintaining state, so deserialized objects have empty
 * thread queues. Typical subclasses requiring serializability will
 * define a {@code readObject} method that restores this to a known
 * initial state upon deserialization.
 *
 * <h3>Usage</h3>
 *
 * <p>To use this class as the basis of a synchronizer, redefine the
 * following methods, as applicable, by inspecting and/or modifying
 * the synchronization state using {@link #getState}, {@link
 * #setState} and/or {@link #compareAndSetState}:
 *
 * <ul>
 * <li> {@link #tryAcquire}
 * <li> {@link #tryRelease}
 * <li> {@link #tryAcquireShared}
 * <li> {@link #tryReleaseShared}
 * <li> {@link #isHeldExclusively}
 * </ul>
 *
 * Each of these methods by default throws {@link
 * UnsupportedOperationException}.  Implementations of these methods
 * must be internally thread-safe, and should in general be short and
 * not block. Defining these methods is the <em>only</em> supported
 * means of using this class. All other methods are declared
 * {@code final} because they cannot be independently varied.
 *
 * <p>You may also find the inherited methods from {@link
 * AbstractOwnableSynchronizer} useful to keep track of the thread
 * owning an exclusive synchronizer.  You are encouraged to use them
 * -- this enables monitoring and diagnostic tools to assist users in
 * determining which threads hold locks.
 *
 * <p>Even though this class is based on an internal FIFO queue, it
 * does not automatically enforce FIFO acquisition policies.  The core
 * of exclusive synchronization takes the form:
 *
 * <pre>
 * Acquire:
 *     while (!tryAcquire(arg)) {
 *        <em>enqueue thread if it is not already queued</em>;
 *        <em>possibly block current thread</em>;
 *     }
 *
 * Release:
 *     if (tryRelease(arg))
 *        <em>unblock the first queued thread</em>;
 * </pre>
 *
 * (Shared mode is similar but may involve cascading signals.)
 *
 * <p id="barging">Because checks in acquire are invoked before
 * enqueuing, a newly acquiring thread may <em>barge</em> ahead of
 * others that are blocked and queued.  However, you can, if desired,
 * define {@code tryAcquire} and/or {@code tryAcquireShared} to
 * disable barging by internally invoking one or more of the inspection
 * methods, thereby providing a <em>fair</em> FIFO acquisition order.
 * In particular, most fair synchronizers can define {@code tryAcquire}
 * to return {@code false} if {@link #hasQueuedPredecessors} (a method
 * specifically designed to be used by fair synchronizers) returns
 * {@code true}.  Other variations are possible.
 *
 * <p>Throughput and scalability are generally highest for the
 * default barging (also known as <em>greedy</em>,
 * <em>renouncement</em>, and <em>convoy-avoidance</em>) strategy.
 * While this is not guaranteed to be fair or starvation-free, earlier
 * queued threads are allowed to recontend before later queued
 * threads, and each recontention has an unbiased chance to succeed
 * against incoming threads.  Also, while acquires do not
 * &quot;spin&quot; in the usual sense, they may perform multiple
 * invocations of {@code tryAcquire} interspersed with other
 * computations before blocking.  This gives most of the benefits of
 * spins when exclusive synchronization is only briefly held, without
 * most of the liabilities when it isn't. If so desired, you can
 * augment this by preceding calls to acquire methods with
 * "fast-path" checks, possibly prechecking {@link #hasContended}
 * and/or {@link #hasQueuedThreads} to only do so if the synchronizer
 * is likely not to be contended.
 *
 * <p>This class provides an efficient and scalable basis for
 * synchronization in part by specializing its range of use to
 * synchronizers that can rely on {@code int} state, acquire, and
 * release parameters, and an internal FIFO wait queue. When this does
 * not suffice, you can build synchronizers from a lower level using
 * {@link java.util.concurrent.atomic atomic} classes, your own custom
 * {@link java.util.Queue} classes, and {@link LockSupport} blocking
 * support.
 *
 * <h3>Usage Examples</h3>
 *
 * <p>Here is a non-reentrant mutual exclusion lock class that uses
 * the value zero to represent the unlocked state, and one to
 * represent the locked state. While a non-reentrant lock
 * does not strictly require recording of the current owner
 * thread, this class does so anyway to make usage easier to monitor.
 * It also supports conditions and exposes
 * one of the instrumentation methods:
 *
 *  <pre> {@code
 * class Mutex implements Lock, java.io.Serializable {
 *
 *   // Our internal helper class
 *   private static class Sync extends AbstractQueuedSynchronizer {
 *     // Reports whether in locked state
 *     protected boolean isHeldExclusively() {
 *       return getState() == 1;
 *     }
 *
 *     // Acquires the lock if state is zero
 *     public boolean tryAcquire(int acquires) {
 *       assert acquires == 1; // Otherwise unused
 *       if (compareAndSetState(0, 1)) {
 *         setExclusiveOwnerThread(Thread.currentThread());
 *         return true;
 *       }
 *       return false;
 *     }
 *
 *     // Releases the lock by setting state to zero
 *     protected boolean tryRelease(int releases) {
 *       assert releases == 1; // Otherwise unused
 *       if (getState() == 0) throw new IllegalMonitorStateException();
 *       setExclusiveOwnerThread(null);
 *       setState(0);
 *       return true;
 *     }
 *
 *     // Provides a Condition
 *     Condition newCondition() { return new ConditionObject(); }
 *
 *     // Deserializes properly
 *     private void readObject(ObjectInputStream s)
 *         throws IOException, ClassNotFoundException {
 *       s.defaultReadObject();
 *       setState(0); // reset to unlocked state
 *     }
 *   }
 *
 *   // The sync object does all the hard work. We just forward to it.
 *   private final Sync sync = new Sync();
 *
 *   public void lock()                { sync.acquire(1); }
 *   public boolean tryLock()          { return sync.tryAcquire(1); }
 *   public void unlock()              { sync.release(1); }
 *   public Condition newCondition()   { return sync.newCondition(); }
 *   public boolean isLocked()         { return sync.isHeldExclusively(); }
 *   public boolean hasQueuedThreads() { return sync.hasQueuedThreads(); }
 *   public void lockInterruptibly() throws InterruptedException {
 *     sync.acquireInterruptibly(1);
 *   }
 *   public boolean tryLock(long timeout, TimeUnit unit)
 *       throws InterruptedException {
 *     return sync.tryAcquireNanos(1, unit.toNanos(timeout));
 *   }
 * }}</pre>
 *
 * <p>Here is a latch class that is like a
 * {@link java.util.concurrent.CountDownLatch CountDownLatch}
 * except that it only requires a single {@code signal} to
 * fire. Because a latch is non-exclusive, it uses the {@code shared}
 * acquire and release methods.
 *
 *  <pre> {@code
 * class BooleanLatch {
 *
 *   private static class Sync extends AbstractQueuedSynchronizer {
 *     boolean isSignalled() { return getState() != 0; }
 *
 *     protected int tryAcquireShared(int ignore) {
 *       return isSignalled() ? 1 : -1;
 *     }
 *
 *     protected boolean tryReleaseShared(int ignore) {
 *       setState(1);
 *       return true;
 *     }
 *   }
 *
 *   private final Sync sync = new Sync();
 *   public boolean isSignalled() { return sync.isSignalled(); }
 *   public void signal()         { sync.releaseShared(1); }
 *   public void await() throws InterruptedException {
 *     sync.acquireSharedInterruptibly(1);
 *   }
 * }}</pre>
 *
 * @since 1.5
 * @author Doug Lea
 */
public abstract class AbstractQueuedSynchronizer
    extends AbstractOwnableSynchronizer
    implements java.io.Serializable {

    private static final long serialVersionUID = 7373984972572414691L;

    /**
     * Creates a new {@code AbstractQueuedSynchronizer} instance
     * with initial synchronization state of zero.
     */
    protected AbstractQueuedSynchronizer() { }

```

Node的主要属性如下：

```java
static final class Node {
  int waitStatus; //表示节点的状态，包含cancelled（取消）；condition 表示节点在等待condition
也就是在condition队列中
  Node prev; //前继节点
  Node next; //后继节点
  Node nextWaiter; //存储在condition队列中的后继节点
  Thread thread; //当前线程
}
```

AQS类底层的数据结构是使用双向链表，是队列的一种实现。包括一个head节点和一个tail节点，分别表示头结点
和尾节点，其中头结点不存储Thread，仅保存next结点的引用。

![1542522642091](C:\Users\lqd\AppData\Roaming\Typora\typora-user-images\1542522642091.png)

当一个线程成功地获取了同步状态（或者锁），其他线程将无法获取到同步状态，转而被构造成为节点并加入到同
步队列中，而这个加入队列的过程必须要保证线程安全，因此同步器提供了一个基于CAS的设置**尾节点**的方法：compareAndSetTail(Node expect,Nodeupdate)，它需要传递当前线程“认为”的尾节点和当前节点，只有设置成功后，当前节点才正式与之前的尾节点建立关联。

![1542522658681](C:\Users\lqd\AppData\Roaming\Typora\typora-user-images\1542522658681.png)

同步队列遵循FIFO，首节点是获取同步状态成功的节点，首节点的线程在释放同步状态时，将会唤醒后继节点，而后继节点将会在获取同步状态成功时将自己设置为首节点。

![1542522687263](C:\Users\lqd\AppData\Roaming\Typora\typora-user-images\1542522687263.png)

设置首节点是通过获取同步状态成功的线程来完成的，由于只有一个线程能够成功获取到同步状态，因此设置头节
点的方法并不需要使用CAS来保证，它只需要将首节点设置成为原首节点的后继节点并断开原首节点的next引用即
可。

### compareAndSet

AQS中，除了本身的链表结构以外，还有一个很关键的功能，就是CAS，这个是保证在多线程并发的情况下保证线
程安全的前提下去把线程加入到AQS中的方法,可以简单理解为乐观锁

```java
private final boolean compareAndSetHead(Node update) {
  return unsafe.compareAndSwapObject(this, headOffset, null, update);
}
```

这个方法里面，首先，用到了unsafe类，(Unsafe类是在sun.misc包下，不属于Java标准。但是很多Java的基础类库，包括一些被广泛使用的高性能开发库都是基于Unsafe类开发的，比如Netty、Hadoop、Kafka等；Unsafe可认为是Java中留下的后门，提供了一些低层次操作，如直接内存访问、线程调度等)，然后调用了compareAndSwapObject这个方法。

```java
public final native boolean compareAndSwapObject(Object var1, long var2, Object var4,
Object var5);
```

这个是一个native方法，第一个参数为需要改变的对象，第二个为偏移量(即之前求出来的headOffset的值)，第三个参数为期待的值，第四个为更新后的值。

整个方法的作用是如果当前时刻的值等于预期值var4相等，则更新为新的期望值 var5，如果更新成功，则返回true，否则返回false；

这里传入了一个headOffset，这个headOffset是什么呢？在下面的代码中，通过unsafe.objectFieldOffset 。headOffset这个是指类中相应字段在该类的偏移量，在这里具体即是指head这个字段在AQS类的内存中相对于该类首地址的偏移量。

一个Java对象可以看成是一段内存，每个字段都得按照一定的顺序放在这段内存里，通过这个方法可以准确地告诉
你某个字段相对于对象的起始内存地址的字节偏移。用于在后面的compareAndSwapObject中，去根据偏移量找
到对象在内存中的具体位置.

这个方法在unsafe.cpp文件中，代码如下:

```c
UNSAFE_ENTRY(jboolean, Unsafe_CompareAndSwapObject(JNIEnv *env, jobject unsafe, jobject
obj, jlong offset, jobject e_h, jobject x_h))
 UnsafeWrapper("Unsafe_CompareAndSwapObject");
 oop x = JNIHandles::resolve(x_h); // 新值
 oop e = JNIHandles::resolve(e_h); // 预期值
 oop p = JNIHandles::resolve(obj);
 HeapWord* addr = (HeapWord *)index_oop_from_field_offset_long(p, offset);// 在内存中的
具体位置
 oop res = oopDesc::atomic_compare_exchange_oop(x, addr, e, true);// 调用了另一个方法，实
际上就是通过cas操作来替换内存中的值是否成功
 jboolean success  = (res == e);  // 如果返回的res等于e，则判定满足compare条件（说明res应该为
内存中的当前值），但实际上会有ABA的问题
 if (success) // success为true时，说明此时已经交换成功（调用的是最底层的cmpxchg指令）
  update_barrier_set((void*)addr, x); // 每次Reference类型数据写操作时，都会产生一个Write
Barrier暂时中断操作，配合垃圾收集器
 return success;
UNSAFE_END
```

所以其实compareAndSet这个方法，最终调用的是unsafe类的compareAndSwap，这个指令会对内存中的共享数据做原子的读写操作。
1. 首先， cpu会把内存中将要被更改的数据与期望值做比较
2. 然后，当两个值相等时，cpu才会将内存中的对象替换为新的值。否则，不做变更操作
3. 最后，返回操作执行结果
    很显然，这是一种乐观锁的实现思路。

## ReentrantLock的实现原理分析

之所以叫重入锁是因为同一个线程如果已经获得了锁，那么后续该线程调用lock方法时不需要再次获取锁，也就是
不会阻塞；重入锁提供了两种实现，一种是非公平的重入锁，另一种是公平的重入锁。

怎么理解公平和非公平呢？
如果在绝对时间上，先对锁进行获取的请求一定先被满足获得锁，那么这个锁就是公平锁，反之，就是不公平的。
简单来说公平锁就是等待时间最长的线程最优先获取锁。

![1542525400921](C:\Users\lqd\AppData\Roaming\Typora\typora-user-images\1542525400921.png)

### ReentrantLock.lock

这个是获取锁的入口，调用了sync.lock； sync是一个实现了AQS的抽象类，这个类的主要作用是用来实现同步控
制的，并且sync有两个实现，一个是NonfairSync(非公平锁)、另一个是FailSync(公平锁)； 我们先来分析一下非公
平锁的实现

### NonfairSync.lock

```java
final void lock() 
{
  if (compareAndSetState(0, 1)) //这是跟公平锁的主要区别,一上来就试探锁是否空闲,如果可以插队，
则设置获得锁的线程为当前线程
//exclusiveOwnerThread属性是AQS从父类AbstractOwnableSynchronizer中继承的属性，用来保存当前占用
同步状态的线程
    setExclusiveOwnerThread(Thread.currentThread());
  else
    acquire(1); //尝试去获取锁
}
```

compareAndSetState，这个方法在前面提到过了，再简单讲解一下，通过cas算法去改变state的值，而这个state
是什么呢？ 在AQS中存在一个变量state，对于ReentrantLock来说，如果state=0表示无锁状态、如果state>0表示有锁状态。所以在这里，是表示当前的state如果等于0，则替换为1，如果替换成功表示获取锁成功了。

由于ReentrantLock是可重入锁，所以持有锁的线程可以多次加锁，经过判断加锁线程就是当前持有锁的线程时
（即exclusiveOwnerThread==Thread.currentThread()），即可加锁，每次加锁都会将state的值+1，state等于几，就代表当前持有锁的线程加了几次锁;解锁时每解一次锁就会将state减1，state减到0后，锁就被释放掉，这时其它线程可以加锁；

### AbstractQueuedSynchronizer.acquire

如果CAS操作未能成功，说明state已经不为0，此时继续acquire(1)操作,acquire是AQS中的方法 当多个线程同时进入这个方法时，首先通过cas去修改state的状态，如果修改成功表示竞争锁成功，竞争失败的，tryAcquire会返回false。

```java
public final void acquire(int arg) {
        if (!tryAcquire(arg) &&
            acquireQueued(addWaiter(Node.EXCLUSIVE), arg))
            selfInterrupt();
    }
```

这个方法的主要作用是
Ø 尝试获取独占锁，获取成功则返回，否则
Ø 自旋获取锁，并且判断中断标识，如果中断标识为true，则设置线程中断
Ø addWaiter方法把当前线程封装成Node，并添加到队列的尾部

### NonfairSync.tryAcquire

tryAcquire方法尝试获取锁，如果成功就返回，如果不成功，则把当前线程和等待状态信息构适成一个Node节
点，并将结点放入同步队列的尾部。然后为同步队列中的当前节点循环等待获取锁，直到成功.

这里可以看非公平锁的涵义，即获取锁并不会严格根据争用锁的先后顺序决定。

这里的实现逻辑类似synchroized关键字的偏向锁的做法，即可重入而不用进一步进行锁的竞争，也解释了ReentrantLock中Reentrant的意义.

```java
final boolean nonfairTryAcquire(int acquires) {
  final Thread current = Thread.currentThread();
  int c = getState(); //获取当前的状态，前面讲过，默认情况下是0表示无锁状态
  if (c == 0) {
    if (compareAndSetState(0, acquires)) { //通过cas来改变state状态的值，如果更新成功，表示获取锁成功, 这个操作外部方法lock()就做过一次，这里再做只是为了再尝试一次，尽量以最简单的方式获取锁。
      setExclusiveOwnerThread(current);
      return true;
   }
 }
  else if (current == getExclusiveOwnerThread()) {//如果当前线程等于获取锁的线程，表示重入，直接累加重入次数
    int nextc = c + acquires;
    if (nextc < 0) // overflow 如果这个状态值越界，抛出异常；如果没有越界，则设置后返回true
      throw new Error("Maximum lock count exceeded");
    setState(nextc);
    return true;
 }
//如果状态不为0，且当前线程不是owner，则返回false。
  return false; //获取锁失败，返回false
}
```

### addWaiter

当前锁如果已经被其他线程锁持有，那么当前线程来去请求锁的时候，会进入这个方法,这个方法主要是把当前线程封装成node，添加到AQS的链表中.

```java
private Node addWaiter(Node mode) {
  Node node = new Node(Thread.currentThread(), mode); //创建一个独占的Node节点,mode为排他模式
 // 尝试快速入队,如果失败则降级至full enq
  Node pred = tail; // tail是AQS的中表示同步队列队尾的属性，刚开始为null，所以进行enq(node)方法
  if (pred != null) {
    node.prev = pred;
     if (compareAndSetTail(pred, node)) { //防止有其他线程修改tail,使用CAS进行修改,如果失败则降级至full enq
      pred.next = node; // 如果成功之后旧的tail的next指针再指向新的tail,成为双向链表
      return node;
   }
 }
  enq(node); // 如果队列为null或者CAS设置新的tail失败
  return node;
}
```

### enq

enq就是通过自旋操作把当前节点加入到队列中

```java
private Node enq(final Node node) {
  for (;;) {  //无效的循环，为什么采用for(;;)，是因为它执行的指令少，不占用寄存器
    Node t = tail;// 此时head, tail都为null
    if (t == null) { // Must initialize// 如果tail为null则说明队列首次使用,需要进行初始化
      if (compareAndSetHead(new Node()))// 设置头节点,如果失败则存在竞争,留至下一轮循环
        tail = head; // 用CAS的方式创建一个空的Node作为头结点，因为此时队列中只一个头结点，所以tail也指向head，第一次循环执行结束
   } else {
//进行第二次循环时，tail不为null，进入else区域。将当前线程的Node结点的prev指向tail，然后使用CAS将tail指向Node
//这部分代码和addWaiter代码一样，将当前节点添加到队列
      node.prev = t;
      if (compareAndSetTail(t, node)) {
        t.next = node; //t此时指向tail,所以可以CAS成功，将tail重新指向CNode。此时t为更新前的tail的值，即指向空的头结点，t.next=node，就将头结点的后续结点指向Node，返回头结点
        return t;
     }
   }
 }
}
```

代码运行到这里，aqs队列的结构就是这样一个表现:

![1542528125709](C:\Users\lqd\AppData\Roaming\Typora\typora-user-images\1542528125709.png)

### acquireQueued

addWaiter返回了插入的节点，作为acquireQueued方法的入参,这个方法主要用于争抢锁.

```java
final boolean acquireQueued(final Node node, int arg) {
  boolean failed = true;
  try {
    boolean interrupted = false;
    for (;;) {
      final Node p = node.predecessor();// 获取prev节点,若为null即刻抛出NullPointException
      if (p == head && tryAcquire(arg)) {// 如果前驱为head才有资格进行锁的抢夺
        setHead(node); // 获取锁成功后就不需要再进行同步操作了,获取锁成功的线程作为新的head节点
//凡是head节点,head.thread与head.prev永远为null, 但是head.next不为null
        p.next = null; // help GC
        failed = false; //获取锁成功
        return interrupted;
     }
//如果获取锁失败，则根据节点的waitStatus决定是否需要挂起线程
      if (shouldParkAfterFailedAcquire(p, node) &&
        parkAndCheckInterrupt())// 若前面为true,则执行挂起,待下次唤醒的时候检测中断的标志
        interrupted = true;
   }
 } finally {
    if (failed) // 如果抛出异常则取消锁的获取,进行出队(sync queue)操作
      cancelAcquire(node);
 }
}
```

原来的head节点释放锁以后，会从队列中移除，原来head节点的next节点会成为head节点

![1542529620432](C:\Users\lqd\AppData\Roaming\Typora\typora-user-images\1542529620432.png)

### shouldParkAfterFailedAcquire

从上面的分析可以看出，只有队列的第二个节点可以有机会争用锁，如果成功获取锁，则此节点晋升为头节点。对
于第三个及以后的节点，if (p == head)条件不成立，首先进行shouldParkAfterFailedAcquire(p, node)操作。shouldParkAfterFailedAcquire方法是**判断一个争用锁的线程是否应该被阻塞**。

它首先判断一个节点的前置节点的状态是否为Node.SIGNAL，如果是，是说明此节点已经将状态设置-如果锁释放，则应当通知它，所以它可以安全的阻塞了，返回true。

```java
private static boolean shouldParkAfterFailedAcquire(Node pred, Node node) {
  int ws = pred.waitStatus; //前继节点的状态
  if (ws == Node.SIGNAL)//如果是SIGNAL状态，意味着当前线程需要被unpark唤醒
       return true;
//如果前节点的状态大于0，即为CANCELLED状态时，则会从前节点开始逐步循环找到一个没有被“CANCELLED”节点设置为当前节点的前节点，返回false。在下次循环执行shouldParkAfterFailedAcquire时，返回true。这个操作实际是把队列中CANCELLED的节点剔除掉。
  if (ws > 0) {// 如果前继节点是“取消”状态，则设置 “当前节点”的 “当前前继节点” 为 “‘原前继节点'的前继节点”。
    do {
      node.prev = pred = pred.prev;
   } while (pred.waitStatus > 0);
    pred.next = node;
 } else { // 如果前继节点为“0”或者“共享锁”状态，则设置前继节点为SIGNAL状态。
    /*
    * waitStatus must be 0 or PROPAGATE. Indicate that we
    * need a signal, but don't park yet. Caller will need to
    * retry to make sure it cannot acquire before parking.
    */
    compareAndSetWaitStatus(pred, ws, Node.SIGNAL);
 }
  return false;
}
```

> 解读：假如有t1,t2两个线程都加入到了链表中
> 如果head节点位置的线程一直持有锁，那么t1和t2就是挂起状态，而HEAD以及Thread1的的awaitStatus都是:
> SIGNAL，在多次尝试获取锁失败以后，就会通过下面的方法进行挂起（这个地方就是避免了惊群效应，每个节点只需要关心上一个节点的状态即可）
> SIGNAL：值为-1，表示当前节点的的后继节点将要或者已经被阻塞，在当前节点释放的时候需要unpark后继节点；
> CONDITION：值为-2，表示当前节点在等待condition，即在condition队列中；
> PROPAGATE：值为-3，表示releaseShared需要被传播给后续节点（仅在共享模式下使用）；

### parkAndCheckInterrupt

如果shouldParkAfterFailedAcquire返回了true，则会执行：“parkAndCheckInterrupt()”方法，它是通过LockSupport.park(this)将当前线程挂起到WATING状态，它需要等待一个中断、unpark方法来唤醒它，通过这样
一种FIFO的机制的等待，来实现了Lock的操作.

```java
private final boolean parkAndCheckInterrupt() {
  LockSupport.park(this);// LockSupport提供park()和unpark()方法实现阻塞线程和解除线程阻塞
  return Thread.interrupted();
}
```

### ReentrantLock.unlock

加锁的过程分析完以后，再来分析一下释放锁的过程，调用release方法，这个方法里面做两件事，

1，释放锁 ；

2，唤醒park的线程

```java
public final boolean release(int arg) {
        if (tryRelease(arg)) {
            Node h = head;
            if (h != null && h.waitStatus != 0)
                unparkSuccessor(h);
            return true;
        }
        return false;
    }
```

### tryRelease

这个动作可以认为就是一个设置锁状态的操作，而且是将状态减掉传入的参数值（参数是1），如果结果状态为0，就将排它锁的Owner设置为null，以使得其它的线程有机会进行执行。 

在排它锁中，加锁的时候状态会增加1（当然可以自己修改这个值），在解锁的时候减掉1，同一个锁，在可以重入后，可能会被叠加为2、3、4这些值，只有unlock()的次数与lock()的次数对应才会将Owner线程设置为空，而且也只有这种情况下才会返回true。

```java
protected final boolean tryRelease(int releases) {
  int c = getState() - releases; // 这里是将锁的数量减1
  if (Thread.currentThread() != getExclusiveOwnerThread())// 如果释放的线程和获取锁的线程不是同一个，抛出非法监视器状态异常
 throw new IllegalMonitorStateException();
  boolean free = false;
  if (c == 0) {
// 由于重入的关系，不是每次释放锁c都等于0，
  // 直到最后一次释放锁时，才会把当前线程释放
    free = true;
    setExclusiveOwnerThread(null);
 }
  setState(c);
  return free;
}
```

### LockSupport

LockSupport类是Java6引入的一个类，提供了基本的线程同步原语。LockSupport实际上是调用了Unsafe类里的
函数，归结到Unsafe里，只有两个函数：

```java
public native void unpark(Thread jthread); 
public native void park(boolean isAbsolute, long time); 
```

unpark函数为线程提供“许可(permit)”，线程调用park函数则等待“许可”。这个有点像信号量，但是这个“许可”是不能叠加的，“许可”是一次性的。

permit相当于0/1的开关，默认是0，调用一次unpark就加1变成了1.调用一次park会消费permit，又会变成0。

如果再调用一次park会阻塞，因为permit已经是0了。直到permit变成1.这时调用unpark会把permit设置为1.

每个线程都有一个相关的permit，permit最多只有一个，重复调用unpark不会累积。

在使用LockSupport之前，我们对线程做同步，只能使用wait和notify，但是wait和notify其实不是很灵活，并且耦合性很高，调用notify必须要确保某个线程处于wait状态，而park/unpark模型真正解耦了线程之间的同步，先后顺序没有没有直接关联，同时线程之间不再需要一个Object或者其它变量来存储状态，不再需要关心对方的状态。

### 总结

分析了独占式同步状态获取和释放过程后，做个简单的总结：

在获取同步状态时，同步器维护一个同步队列，获取状态失败的线程都会被加入到队列中并在队列中进行自旋；

移出队列（或停止自旋）的条件是前驱节点为头节点且成功获取了同步状态。在释放同步状态时，同步器调用tryRelease(int arg)方法释放同步状态，然后唤醒头节点的后继节点。

## 公平锁和非公平锁的区别

锁的公平性是相对于获取锁的顺序而言的，如果是一个公平锁，那么锁的获取顺序就应该符合请求的绝对时间顺
序，也就是FIFO。 在上面分析的例子来说，只要CAS设置同步状态成功，则表示当前线程获取了锁，而公平锁则不一样，差异点有两个。

# 六、Condition

通过前面的课程学习，我们知道任意一个Java对象，都拥有一组监视器方法（定义在java.lang.Object上），主要包括wait()、notify()以及notifyAll()方法，这些方法与synchronized同步关键字配合，可以实现等待/通知模式。
JUC包提供了Condition来对锁进行精准控制，Condition是一个多线程协调通信的工具类，可以让某些线程一起等
待某个条件（condition），只有满足条件时，线程才会被唤醒。

## condition使用案例

```java
public class ConditionDemoWait implements  Runnable{
  private Lock lock;
  private Condition condition;
  public ConditionDemoWait(Lock lock, Condition condition){
    this.lock=lock;
    this.condition=condition;
  }
  @Override
  public void run() {
    System.out.println("begin -ConditionDemoWait");
    try {
      lock.lock();
      condition.await();
      System.out.println("end - ConditionDemoWait");
    } catch (InterruptedException e) {
      e.printStackTrace();
    }finally {
      lock.unlock();
    }
  }
}
```

```java
public class ConditionDemoSignal implements  Runnable{
  private Lock lock;
  private Condition condition;
  public ConditionDemoSignal(Lock lock, Condition condition){
    this.lock=lock;
    this.condition=condition;
  }
  @Override
  public void run() {
    System.out.println("begin -ConditionDemoSignal");
    try {
      lock.lock();
      condition.signal();
      System.out.println("end - ConditionDemoSignal");
    }finally {
         lock.unlock();
    }
  }
}
```

通过这个案例简单实现了wait和notify的功能，当调用await方法后，当前线程会释放锁并等待，而其他线程调用
condition对象的signal或者signalall方法通知并被阻塞的线程，然后自己执行unlock释放锁，被唤醒的线程获得之
前的锁继续执行，最后释放锁。所以，condition中两个最重要的方法，一个是await，一个是signal方法
await:把当前线程阻塞挂起
signal:唤醒阻塞的线程

### await方法

调用Condition的await()方法（或者以await开头的方法），会使当前线程进入等待队列并释放锁，同时线程状态变为等待状态。当从await()方法返回时，当前线程一定获取了Condition相关联的锁。

### signal方法

调用Condition的signal()方法，将会唤醒在等待队列中等待时间最长的节点（首节点），在唤醒节点之前，会将节
点移到同步队列中。

# 七、并发框架

JUC中提供了几个比较常用的并发工具类，比如CountDownLatch、CyclicBarrier、Semaphore。 接下来我们会带大家去深入研究一些常用的api。

## CountDownLatch

countdownlatch是一个同步工具类，它允许一个或多个线程一直等待，直到其他线程的操作执行完毕再执行。从
命名可以解读到countdown是倒数的意思，类似于我们倒计时的概念。
countdownlatch提供了两个方法，一个是countDown，一个是await， countdownlatch初始化的时候需要传入一个整数，在这个整数倒数到0之前，调用了await方法的程序都必须要等待，然后通过countDown来倒数。

```java
public static void main(String[] args) throws InterruptedException {
  CountDownLatch countDownLatch=new CountDownLatch(3);
  new Thread(()->{
    countDownLatch.countDown();
   
 },"t1").start();
  new Thread(()->{
    countDownLatch.countDown();
  
 },"t2").start();
  new Thread(()->{
  
    countDownLatch.countDown();
 },"t3").start();
    countDownLatch.await();
  System.out.println("所有线程执行完毕");
}
```

![1542532432710](C:\Users\lqd\AppData\Roaming\Typora\typora-user-images\1542532432710.png)

使用场景：

```
\1. 通过countdownlatch实现最大的并行请求，也就是可以让N个线程同时执行，这个我也是在课堂上写得比较多
的。
\2. 比如应用程序启动之前，需要确保相应的服务已经启动，比如我们之前在讲zookeeper的时候，通过原生api连
接的地方有用到countDownLatch。
```

## Semaphore

semaphore也就是我们常说的信号灯，semaphore可以控制同时访问的线程个数，通过acquire获取一个许可，如果没有就等待，通过release释放一个许可。有点类似限流的作用。叫信号灯的原因也和他的用处有关，比如某商场就5个停车位，每个停车位只能停一辆车，如果这个时候来了10辆车，必须要等前面有空的车位才能进入。

```java
public class Test {
public static void main(String[] args) {
    Semaphore semaphore=new Semaphore(5);
    for(int i=0;i<10;i++){
      new Car(i,semaphore).start();
   }
 }
  static class Car extends Thread{
    private int num;
    private Semaphore semaphore;
    public Car(int num, Semaphore semaphore) {
      this.num = num;
      this.semaphore = semaphore;
   }
    public void run(){
      try {
        semaphore.acquire();//获取一个许可
        System.out.println("第"+num+"占用一个停车位");
        TimeUnit.SECONDS.sleep(2);
        System.out.println("第"+num+"俩车走喽");
        semaphore.release();
     } catch (InterruptedException e) {
        e.printStackTrace();
     }
   }
 }
 }
```

使用场景：

可以实现对某些接口访问的限流

## 原子操作

当在多线程情况下，同时更新一个共享变量，由于我们前面讲过的原子性问题，可能得不到预期的结果。如果要达
到期望的结果，可以通过synchronized来加锁解决，因为synchronized会保证多线程对共享变量的访问进行排
队。

在Java5以后，提供了原子操作类，这些原子操作类提供了一种简单、高效以及线程安全的更新操作。而由于变量
的类型很多，所以Atomic一共提供了12个类分别对应四种类型的原子更新操作，基本类型、数组类型、引用类
型、属性类型

```
基本类型对应：AtomicBoolean、AtomicInteger、AtomicLong
数组类型对应：AtomicIntegerArray、AtomicLongArray、AtomicReferenceArray
引用类型对应：AtomicReference、AtomicReferenceFieldUpdater、AtomicMarkableReference
字段类型对应：AtomicIntegerFieldUpdater、AtomicLongFieldUpdater、AtomicStampedReference
```

Atomic原子操作的使用：

```java
private static AtomicInteger count=new AtomicInteger(0);
public static synchronized void inc() {
  try {
    Thread.sleep(1);
 } catch (InterruptedException e) {
    e.printStackTrace();
 }
  count.getAndIncrement();
}
public static void main(String[] args) throws InterruptedException {
  for(int i=0;i<1000;i++){
    new Thread(()-> {
      SafeDemo.inc();
   }).start();
 }
  Thread.sleep(4000);
  System.out.println(count.get());
}
```

## 线程池

Java中的线程池是运用场景最多的并发框架，几乎所有需要异步或并发执行任务的程序都可以使用线程池。线程池
就像数据库连接池的作用类似，只是线程池是用来重复管理线程避免创建大量线程增加开销。所以合理的使用线程
池可以。

```
\1. 降低创建线程和销毁线程的性能开销
\2. 合理的设置线程池大小可以避免因为线程数超出硬件资源瓶颈带来的问题，类似起到了限流的作用；线程是稀
缺资源，如果无线创建，会造成系统稳定性问题
```

### 线程池的使用

JDK 为我们内置了几种常见线程池的实现，均可以使用 Executors 工厂类创建
为了更好的控制多线程，JDK提供了一套线程框架Executor，帮助开发人员有效的进行线程控制。它们都在
java.util.concurrent包中，是JDK并发包的核心。
其中有一个比较重要的类:Executors，他扮演着线程工厂的角色，我们通过Executors可以创建特定功能的线程池

```
newFixedThreadPool：**该方法返回一个固定数量的线程池，线程数不变，当有一个任务提交时，若线程池
中空闲，则立即执行，若没有，则会被暂缓在一个任务队列中，等待有空闲的线程去执行。
newSingleThreadExecutor: 创建一个线程的线程池，若空闲则执行，若没有空闲线程则暂缓在任务队列中。
newCachedThreadPool：**返回一个可根据实际情况调整线程个数的线程池，不限制最大线程数量，若用空
闲的线程则执行任务，若无任务则不创建线程。并且每一个空闲线程会在60秒后自动回收
newScheduledThreadPool: 创建一个可以指定线程的数量的线程池，但是这个线程池还带有延迟和周期性执行
任务的功能，类似定时器。
```

```java
public class Test implements Runnable{
  @Override
  public void run() {
    try {
      Thread.sleep(10);
   } catch (InterruptedException e) {
      e.printStackTrace();
   }
    System.out.println(Thread.currentThread().getName());
 }
  static ExecutorService service=Executors.newFixedThreadPool(3);
  public static void main(String[] args) {
    for(int i=0;i<100;i++) {
      service.execute(new Test());
   }
    service.shutdown();
 }
}
```

![1542532907815](C:\Users\lqd\AppData\Roaming\Typora\typora-user-images\1542532907815.png)

### 线程池监控 --- 数据监控日志上报

![1542532990480](C:\Users\lqd\AppData\Roaming\Typora\typora-user-images\1542532990480.png)

![1542532999233](C:\Users\lqd\AppData\Roaming\Typora\typora-user-images\1542532999233.png)

![1542533016395](C:\Users\lqd\AppData\Roaming\Typora\typora-user-images\1542533016395.png)

### 自定义线程池名称

```java
private static final ThreadFactory unzipThreadFactory = new ThreadFactoryBuilder()
.setNameFormat("unzip-pool-%d").build();
private static final ExecutorService unzipThreadPool = new ThreadPoolExecutor(3, Integer.parseInt(maximumPoolSize),
60L, TimeUnit.SECONDS,
new LinkedBlockingQueue<>(1024), unzipThreadFactory, new ThreadPoolExecutor.AbortPolicy());
```

## Future 

```java
package study.java8.concurrent;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
public class FutureDemo {
    public static void main(String[] args) throws ExecutionException, InterruptedException {
        ExecutorService executorService = Executors.newFixedThreadPool(2);
        Future<?> future  = executorService.submit(()->{
            System.out.println("Hello,World");
        });
        while(!future.isDone()){
        }
        executorService.shutdown();
    }
}
```

## Fork/Join（java7引入）

编程模型

```
ForkJoinPool
ForkJoinTask
RecursiveAction -- 继承了ForkJoinTask<Void>
```

Future的限制

```
无法手动完成
阻塞式返回结果
无法链式多个future
无法合并多个future
缺少异常处理
```

演示代码：

```java
import java.util.Arrays;
import java.util.List;
import java.util.concurrent.ForkJoinPool;
import java.util.concurrent.RecursiveAction;
import java.util.concurrent.atomic.LongAccumulator;
public class ForkJoinDemo {
    public static void main(String[] args) {
        ForkJoinPool forkJoinPool = new ForkJoinPool();
        LongAccumulator accumulator = new LongAccumulator((left, right) -> {
            return left+right;
        },0);
        List<Long> params = Arrays.asList(1L,2L,3L,4L,5L,6L,7L,8L,9L);
        forkJoinPool.invoke(new LongSumTask(params,accumulator));
        System.out.println(accumulator.get());
    }
    static class LongSumTask extends RecursiveAction {
        private final List<Long> elements;
        private final LongAccumulator accumulator;
        LongSumTask(List<Long> elements, LongAccumulator accumulator) {
            this.elements = elements;
            this.accumulator = accumulator;
        }
        @Override
        public void compute() {
            int size = elements.size();
            int parts = size / 2;
            if(size > 1){
                List<Long> left = elements.subList(0,parts);
                List<Long> right = elements.subList(parts,size);
                new LongSumTask(left,accumulator).fork().join();
                new LongSumTask(right,accumulator).fork().join();
            }else{
                if(elements.isEmpty()){
                    return;
                }
                Long num = elements.get(0);
                accumulator.accumulate(num);
            }
        }
    }
}
```

## Fork/Join 异步并行框架（java8引入）

编程模型

```
CompletionStage
CompletableFuture
```

代码实例1

```java
package study.java8.concurrent;
import java.util.concurrent.CountedCompleter;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.LongAccumulator;
public class CountedCompleterDemo {
    public static void main(String[] args) {
        Integer[] data = new Integer[]{0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
        LongAccumulator longAccumulator = new LongAccumulator((a, b) -> a + b, 0);
        ForEach.forEach(data, new MyOperation<Integer>() {
            @Override
            public void apply(Integer value, ForEach<Integer> forEach) {
                longAccumulator.accumulate(value);
                System.out.printf("Current CountedCompleter[%d] applied value is %d on Thread[%s]!\n",
                        forEach.id,
                        value,
                        Thread.currentThread().getName());
            }
        });
        System.out.println(longAccumulator.get());
    }
    static interface MyOperation<E> {
        default void apply(E e, ForEach<E> forEach) {
            System.out.println(e);
        }
    }
    static class ForEach<E> extends CountedCompleter<Void> {
        private static final AtomicInteger sequence = new AtomicInteger(0);
        final E[] array;
        final MyOperation<E> op;
        final int lo, hi;
        final private int id;
        ForEach(CountedCompleter<?> p, E[] array, MyOperation<E> op, int lo, int hi) {
            super(p);
            this.array = array;
            this.op = op;
            this.lo = lo;
            this.hi = hi;
            this.id = sequence.incrementAndGet();
        }
        public static <E> void forEach(E[] array, MyOperation<E> op) {
            new ForEach<E>(null, array, op, 0, array.length).invoke();
        }
        public void compute() { // version 1
            if (hi - lo >= 2) {
                int mid = (lo + hi) >>> 1;
                setPendingCount(2); // must set pending count before fork
                new ForEach(this, array, op, mid, hi).fork(); // right child
                new ForEach(this, array, op, lo, mid).fork(); // left child
            } else if (hi > lo)
                op.apply(array[lo], this);
            tryComplete();
        }
        public void onCompletion(CountedCompleter countedCompleter) {
            System.out.printf("Current CountedCompleter[ ID : %d , ] is completion on Thread[%s]!\n", ((ForEach) countedCompleter).id,
                    Thread.currentThread().getName());
        }
    }
}
```

代码实例2

```java
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ForkJoinPool;
import java.util.concurrent.RecursiveAction;
import java.util.function.Supplier;
/**
 * @author lqd
 * @DATE 2018/9/13
 * @Description xxxxx
 */
public class Test
{
    public static void main(String[] args) throws InterruptedException, ExecutionException {
        /**完成操作**/
        CompletableFuture<String> completableFuture = new CompletableFuture<>();
        completableFuture.complete("Hello world");
        String value = completableFuture.get();
        System.out.println(value);
        /**异步执行，阻塞操作**/
        CompletableFuture completableFuture1 = CompletableFuture.runAsync(()->{
            System.out.println("-111");
        });
        completableFuture1.get();
        System.out.println("-222");
        /**异步操作**/
        CompletableFuture<String> completableFuture2 = CompletableFuture.supplyAsync(()->{
           return String.format("Thread[%s] ,execute \n" ,Thread.currentThread().getName() );
        });
        String value1 = completableFuture2.get() ;
        System.out.printf("Thread ,%s"  ,value1);
        System.out.printf("Thread ,%s stop"  ,Thread.currentThread().getName());
        /**合并操作 reactive**/
         CompletableFuture.supplyAsync(()->{
            return String.format("Thread[%s]A ,execute " ,Thread.currentThread().getName() );
        }).thenApply(v->{
            return  v + String.format("- 来自Thread[%s]B " ,Thread.currentThread().getName());
        }).thenApply(v->{
            return  v + String.format("- 来自Thread[%s]C \n " ,Thread.currentThread().getName());
        }).thenApply(v->{
            System.out.println(v);
            return v ;
        }).thenRun(()->{
            System.out.println("over");
        });
       // String value2 = completableFuture3.get() ;
        //System.out.printf("Thread ,%s"  ,value2);
       // System.out.printf("Thread ,%s stop"  ,Thread.currentThread().getName());
       /* ForkJoinPool forkJoinPool = new ForkJoinPool();
        forkJoinPool.invoke(new RecursiveAction() {
            @Override
            protected void compute() {
                System.out.printf("Thread[%s]" ,Thread.currentThread().getName());
            }
        }) ;
        forkJoinPool.shutdown();*/
       /* boolean completable = false;
        SubThread runnable = new SubThread(completable);
        System.out.printf("【Thread %s】" , Thread.currentThread().getName() + " start!");
        Thread resultThread = new Thread(runnable);
        resultThread.start();
        resultThread.join();
        System.out.printf("【Thread %s】" , Thread.currentThread().getName() + " complete:" + runnable.isCompletable());*/
    }
    private static class SubThread implements Runnable
    {
        private boolean completable ;
        SubThread(boolean completable)
        {
            this.completable = completable ;
        }
        @Override
        public void run() {
            System.out.printf("【Thread %s】" , Thread.currentThread().getName() + " execute!");
            this.completable = true ;
        }
        public boolean isCompletable() {
            return completable;
        }
        public void setCompletable(boolean completable) {
            this.completable = completable;
        }
    }
}
```

# 八、异步事件驱动 之 Reactive

## 介绍

In computing, reactive programming is a declarative programming paradigm concerned with data streams and the propagation of change.

## 异步与同步操作

### servlet

```java
package com.gupao.asyncweb.servlet;
import javax.servlet.AsyncContext;
import javax.servlet.AsyncEvent;
import javax.servlet.AsyncListener;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.PrintWriter;
/**
 * 访问 "/simple/async"
 */
@WebServlet(value = "/simple/async", asyncSupported = true)
public class SimpleAsyncServlet extends HttpServlet {
    @Override
    public void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        request.setCharacterEncoding("UTF-8");
        response.setCharacterEncoding("UTF-8");
        response.setContentType("text/html; charset=utf-8");
        PrintWriter writer = response.getWriter();
        writer.println(Thread.currentThread().getName() + " 开始执行！");
        // 启动异步上下文
        AsyncContext asyncContext = request.startAsync();
        asyncContext.addListener(new AsyncListener() {
            @Override
            public void onComplete(AsyncEvent event) throws IOException {
                writer.println(Thread.currentThread().getName() + " 请求完成了！");
            }
            @Override
            public void onTimeout(AsyncEvent event) throws IOException {
                writer.println(Thread.currentThread().getName() + " 请求超时了！");
            }
            @Override
            public void onError(AsyncEvent event) throws IOException {
                writer.println(Thread.currentThread().getName() + " 请求错误了！");
            }
            @Override
            public void onStartAsync(AsyncEvent event) throws IOException {
                writer.println(Thread.currentThread().getName() + " 异步请求开始！");
            }
        });
        //同步方式
         asyncContext.complete();
        // 异步方式
     /*   asyncContext.start(()->{
            writer.println(Thread.currentThread().getName() + " 执行中！");
            asyncContext.complete();
        });*/
    }
}
```

### CometProcessor

```
Comet技术被称为下一代Ajax技术，主要通过实现server push来解决ajax需要定时频繁发送请求的问题。
```

### 参考

[](https://en.wikipedia.org/wiki/Reactive_programming)

# 九，Reactive Streams 并发编程之Reactor、JAVA9

## 时代局限性

阻塞编程

```
无法并行计算
资源低效使用
```

传统的CallBack/Future不足

1，不知道什么时候结束，ListenableFutureCallback帮助增加成功的回调（spring 4.0后提供的）

```java
AsyncListenableTaskExecutor executor = new SimpleAsyncTaskExecutor("SimpleAsyncTaskExecutor-") ;
ListenableFuture<Integer> handler = executor.submitListenable(new Callable<Integer>() {
    @Override
    public Integer call() throws Exception {
        return 1;
    }
});
handler.addCallback(new ListenableFutureCallback<Integer>() {
    @Override
    public void onFailure(Throwable ex) {
        System.out.printf("[Thread %s] " + ex.getMessage(),Thread.currentThread().getName());
    }
    @Override
    public void onSuccess(Integer result) {
        System.out.printf("[Thread %s] " + result,Thread.currentThread().getName());
    }
});
try {
    handler.get() ;
} catch (Exception e) {
    e.printStackTrace();
}
```

2，future之间没有相互管理

## Reactive Streams 编程

Reactive Streams规范

```
信号
onSubscribe():订阅事件
onNext()
```

Reactive Streams框架、实现 - Reactor 、Rxjava、Java 9 Flow API

## 了解Reactor基本使用

```
核心接口
	Mono（异步0-1元素序列）
	Flux（异步0-N元素序列）
编程方式
	接口编程
	函数式编程（Lambda）
```

### 实操

引入maven依赖

```xml
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>io.projectreactor</groupId>
            <artifactId>reactor-bom</artifactId>
            <version>Bismuth-RELEASE</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
<dependencies>
    <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-core</artifactId>
        <version>5.0.1.RELEASE</version>
    </dependency>
    <dependency>
        <groupId>io.projectreactor</groupId>
        <artifactId>reactor-core</artifactId>
    </dependency>
    <dependency>
        <groupId>io.projectreactor</groupId>
        <artifactId>reactor-test</artifactId>
        <scope>test</scope>
    </dependency>
</dependencies>
```

一般情况

```java
package com.gupao.reactor;
import com.gupao.util.Utils;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import java.util.Arrays;
import java.util.IntSummaryStatistics;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
/**
 * @author lqd
 * @DATE 2018/9/11
 * @Description xxxxx
 */
public class FluxDemo
{
    public static void main(String[] args)
    {
//        /**
//         * Flux
//         */
//        Flux<String> flux = Flux.just("1","3","2") ;
//        flux.subscribe(Utils::println);
//
//        /**
//         * Mono
//         */
//        Mono<String> mono = Mono.just("00000");
//        mono.subscribe(Utils::println);
//
        /*Flux<Integer> numbers = Flux.range(5,3) ;
        numbers.subscribe(Utils::println) ;*/
//        List<String> strings = Arrays.asList("abc", "", "bc", "efg", "abcd","", "jkl");
//        List<String> filtered = strings.stream().
//                filter(string -> !string.isEmpty()).collect(Collectors.toList());
//        filtered.forEach(Utils::println);
//        List<Integer> numbers = Arrays.asList(3, 2, 2, 3, 7, 3, 5);
//
//        IntSummaryStatistics stats = numbers.stream().mapToInt((x) -> x).summaryStatistics();
//
//        System.out.println("列表中最大的数 : " + stats.getMax());
//        System.out.println("列表中最小的数 : " + stats.getMin());
//        System.out.println("所有数之和 : " + stats.getSum());
//        System.out.println("平均数 : " + stats.getAverage());
      /*  FluxDemo java8Tester = new FluxDemo();
        Integer value1 = null;
        Integer value2 = new Integer(10);
        // Optional.ofNullable - 允许传递为 null 参数
        Optional<Integer> a = Optional.ofNullable(value1);
        // Optional.of - 如果传递的参数是 null，抛出异常 NullPointerException
        Optional<Integer> b = Optional.of(value2);
        System.out.println(java8Tester.sum(a,b));*/
        Flux<String> flux = Flux.generate(
                () -> 2,
                (state, sink) -> {
                    sink.next("3 x " + state + " = " + 3*state);
                    if (state == 10) sink.complete();
                    return state + 1;
                });
        flux.subscribe(Utils::println,Utils::println,()->{
                    Utils.println("ok");                }
                );
    }
    public Integer sum(Optional<Integer> a, Optional<Integer> b){
        // Optional.isPresent - 判断值是否存在
        System.out.println("第一个参数值存在: " + a.isPresent());
        System.out.println("第二个参数值存在: " + b.isPresent());
        // Optional.orElse - 如果值存在，返回它，否则返回默认值
        Integer value1 = a.orElse(new Integer(0));
        //Optional.get - 获取值，值需要存在
        Integer value2 = b.get();
        return value1 + value2;
    }
}
```

并发情况

```java
package com.gupao.reactor;
import com.gupao.util.Utils;
import reactor.core.publisher.Flux;
import reactor.core.scheduler.Schedulers;
/**
 * {@link Flux} 异步操作
 *
 * @author mercyblitz
 * @email mercyblitz@gmail.com
 * @date 2017-10-26
 **/
public class FluxAsyncDemo {
    public static void main(String[] args) throws InterruptedException {
        // 当前线程执行
//        Flux.range(0,10)
//                .publishOn(Schedulers.immediate())
//                .subscribe(Utils::println);
        // 单线程异步执行
//        Flux.range(0, 10)
//                .publishOn(Schedulers.single())
//                .subscribe(Utils::println);
        // 弹性线程池异步执行
        Flux.range(0, 10)
                .publishOn(Schedulers.elastic())
                .subscribe(Utils::println);
        // 并行线程池异步执行
//        Flux.range(0, 10)
//                .publishOn(Schedulers.parallel())
//                .subscribe(Utils::println);
//        // 强制让主线程执行完毕
        Thread.currentThread().join(1 * 1000L);
    }
}
```

## 参考

CPU密集型和IO密集型 <https://blog.csdn.net/youanyyou/article/details/78990156>

reactor <http://projectreactor.io/docs/core/release/reference/>

# 十，Vert.x异步编程

# 十一，理解WebFlux

# 十二，Rxjava

