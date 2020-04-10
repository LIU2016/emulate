## 虚拟机参数

```
-Xmx512m 
-Xms512m 
-XX:+UseG1GC ：开启G1
-XX:MaxGCPauseMills=20：最大GC停顿时间，这是个软目标，JVM将尽可能（但不保证）停顿小于这个时间(暂停时间目标50ms，默认200ms) 
-XX:InitiatingHeapOccupancyPercent=35：堆占用了多少比例的时候触发GC，就即触发标记周期的 Java 堆占用率阈值。默认占用率是整个 Java 堆的 45%
-XX:G1HeapRegionSize=16M：#设置的 G1 区域的大小。值是2的幂，范围是1 MB 到32 MB。目标是根据最小的 Java 堆大小划分出约 2048 个区域
-verbose:gc : 在控制台输出GC情况 
-XX:+PrintGCDetails : 在控制台输出详细的GC情况 
-XX:+PrintGCTimeStamps : jvm启动时间为起点的相对时间
-XX:+PrintGCDateStamps : 记录的是系统时间
-Xloggc : 将GC日志输出到指定文件中
```

