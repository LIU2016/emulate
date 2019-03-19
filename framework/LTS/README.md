# LTS分布式任务调度文档

参考文档：

https://www.cnblogs.com/dion-90/articles/8674591.html

https://gitee.com/hugui/light-task-scheduler

https://qq254963746.gitbooks.io/lts/content/

## LTS介绍

> LTS(light-task-scheduler)主要用于解决分布式任务调度问题，支持实时任务，定时任务，Cron任务，Repeat任务。有较好的伸缩性，扩展性，健壮稳定性而被多家公司使用，同时也希望开源爱好者一起贡献。

#### 主要功能

- 1. 支持分布式，解决多点故障，支持动态扩容，容错重试等
- 1. Spring扩展支持，SpringBoot支持，Spring Quartz Cron任务的无缝接入支持
- 1. 节点监控支持，任务执行监控支持，JVM监控支持
- 1. 后台运维操作支持, 可以动态提交，更改，停止 任务

## LTS技术架构

> LTS 着力于解决分布式任务调度问题，将任务的提交者和执行者解耦，解决任务执行的单点故障，支持动态扩容，出错重试等机制。代码程序设计上，参考了优秀开源项目Dubbo，Hadoop的部分思想。

#### LTS目前支持四种任务

- 实时任务：提交了之后立即就要执行的任务。
- 定时任务：在指定时间点执行的任务，譬如 今天3点执行（单次）。
- Cron任务：CronExpression，和quartz类似（但是不是使用quartz实现的）譬如 0 0/1 * ?
- Repeat任务：譬如每隔5分钟执行一次，重复50次就停止。

#### 架构设计上，LTS框架中包含以下五种类型的节点

- JobClient :主要负责提交任务, 并接收任务执行反馈结果。
- JobTracker :负责任务调度，接收并分配任务。
- TaskTracker :负责执行任务，执行完反馈给JobTracker。
- LTS-Monitor :主要负责收集各个节点的监控信息，包括任务监控信息，节点JVM监控信息
- LTS-Admin :管理后台）主要负责节点管理，任务队列管理，监控管理等。