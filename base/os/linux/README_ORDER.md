##### linux 命令集合

`*要求每日一练*`

20190328

```shell
uptime
~]#yum install -y stress
~]#yum install -y sysstat
~]#stress --cpu 8 --timeout 600 （模拟cpu负载）
~]#mpstat -P ALL 5 (查看CPU负载)
~]#stress -i 1 --timeout 600 （模拟io负载）
~]#mpstat -P ALL 5 (查看CPU负载)
~]#stress -c 10 --timeout 600
~]#mpstat -P ALL 5 (查看CPU负载)
~]#watch -d uptime (查看平均负载：可能是由于进程过多、cpu负载、IO负载)
```

20190402

```shell
top（每隔3秒监控）、pidstat（查看到进程和线程的切换次数以及命令）、vmstat（查看总的线程、进程、中断切换次数）、perf（实时监控性能）、proc（用户态到内核态的通道文件）
~]#yum install -y sysbench
~]#sysbench --threads=10 --max-time=300 threads run
~]#perf top -g -p 25894
```

