#### 基础知识

##### 简介

```
Kubernetes利⽤容器的扩缩容机制解决了许多常见的问题，它将容器归类到⼀起，形成“容器集”（Pod），为分组的容器增加了⼀个抽象层，⽤于帮助⽤户调度⼯作负载（workload），并为这些容器提供所需的联⽹和存储等服务。Kubernetes的其他部分可帮助⽤户在这些Pod之间达成负载均衡，同时确保运⾏正确数量的容器，以充分⽀持实际的⼯作负载

借助于Kubernetes的编排功能，⽤户可以构建出跨多个容器的应⽤服务，并且可以实现跨集群调度、扩展容器，以及长期持续管理这些容器的健康状况等。使⽤中，Kubernetes还需要与⽹络、存储、安全性、监控及其他服务进⾏整合，以提供全⾯的容器基础架构.
```

##### 术语

```
从物理角度分析：master、worknode.

Kubernetes还有着众多的组件来⽀撑其内部的业务逻辑，包括运⾏应⽤、应⽤编排、服务暴露、应⽤恢复等，它们在Kubernetes中被抽象为Pod、Service、Controller等资源类型. 以下九种：

pod：
Kubernetes并不直接运⾏容器，⽽是使⽤⼀个抽象的资源对象来封装⼀个或者多个容器，这个抽象即为Pod，它也是Kubernetes的最⼩调度单元。同⼀Pod中的容器共享⽹络名称空间和存储资源，这些容器可经由本地回环节⼜lo直接通信，但彼此之间又在Mount、User及PID等名称空间上保持了隔离。尽管Pod中可以包含多个容器，但是作为最⼩调度单元，它应该尽可能地保持“⼩”，即通常只应该包含⼀个主容器，以及必要的辅助型容器（sidecar）。

Label：
是将资源进⾏分类的标识符，资源标签其实就是⼀个键值型（key/values）数据。标签旨在指定对象（如Pod等）辨识性的属性，这些属性仅对⽤户存在特定的意义，对Kubernetes集群来说并不直接表达核⼼系统语义。标签可以在对象创建时附加其上，并能够在创建后的任意时间进⾏添加和修改。⼀个对象可以拥有多个标签，⼀个标签也可以附加于多个对象（通常是同⼀类对象）之上。

Label Selector：
标签选择器（Selector）全称为“Label Selector”，它是⼀种根据Label来过滤符合条件的资源对象的机制。例如，将附有标签“role：backend”的所有Pod对象挑选出来归为⼀组就是标签选择器的⼀种应⽤，如图1-8所⽰。⽤户通常使⽤标签对资源对象进⾏分类，⽽后使⽤标签选择器挑选出它们。

Annotation：
Annotation（注解）是另⼀种附加在对象之上的键值类型的数据，但它拥有更⼤的数据容量。Annotation常⽤于将各种⾮标识型元数据（metadata）附加到对象上，但它不能⽤于标识和选择对象，通常也不会被Kubernetes直接使⽤，其主要⽬的是⽅便⼯具或⽤户的阅读及查找等。

Controller：
尽管Pod是Kubernetes的最⼩调度单元，但⽤户通常并不会直接部署及管理Pod对象，⽽是要借助于另⼀类抽象—控制器（Controller）对其进⾏管理。⽤于⼯作负载的控制器是⼀种管理Pod⽣命周期的资源抽象，它们是Kubernetes上的⼀类对象，⽽⾮单个资源对象，包括ReplicationController、ReplicaSet、Deployment、StatefulSet、Job等。

Service：
Service是建⽴在⼀组Pod对象之上的资源抽象，它通过标签选择器选定⼀组Pod对象，并为这组Pod对象定义⼀个统⼀的固定访问⼊⼜（通常是⼀个IP地址），若Kubernetes集群存在DNS附件，它就会在Service创建时为其⾃动配置⼀个DNS名称以便客户端进⾏服务发现。到达Service IP的请求将被负载均衡⾄其后的端点—各个Pod对象之上，因此Service从本质上来讲是⼀个四层代理服务。另外，Service还可以将集群外部流量引⼊到集群中来。

Ingress：
Kubernetes将Pod对象和外部⽹络环境进⾏了隔离，Pod和Service等对象间的通信都使⽤其内部专⽤地址进⾏，如若需要开放某些Pod对象提供给外部⽤户访问，则需要为其请求流量打开⼀个通往Kubernetes集群内部的通道，除了Service之外，Ingress也是这类通道的实现⽅式之⼀。

存储卷：
存储卷（Volume）是独⽴于容器⽂件系统之外的存储空间，常⽤于扩展容器的存储空间并为它提供持久存储能⼒。Kubernetes集群上的存储卷⼤体可分为临时卷、本地卷和⽹络卷。临时卷和本地卷都位于Node本地，⼀旦Pod被调度⾄其他Node，此种类型的存储卷将⽆法访问到，因此临时卷和本地卷通常⽤于数据缓存，持久化的数据则需要放置于持久卷（persistent volume）之上。

Name和Namespace：
名称（Name）是Kubernetes集群中资源对象的标识符，它们的作⽤域通常是名称空间（Namespace），因此名称空间是名称的额外的限定机制。在同⼀个名称空间中，同⼀类型资源对象的名称必须具有唯⼀性。名称空间通常⽤于实现租户或项⽬的资源隔离，从⽽形成逻辑分组，如图1-10所⽰。创建的Pod和Service等资源对象都属于名称空间级别，未指定时，它们都属于默认的名称空间“default”。

```

##### 集群组件

```
⼀个典型的Kubernetes集群由多个⼯作节点（worker node）和⼀个集群控制平⾯（control plane，即Master），以及⼀个集群状态存储系统（etcd）组成。其中Master节点负责整个集群的管理⼯作，为集群提供管理接⼜，并监控和编排集群中的各个⼯作节点。各节点负责以Pod的形式运⾏容器，因此，各节点需要事先配置好容器运⾏依赖到的所有服务和资源，如容器运⾏时环境等。Kubernetes的系统架构如图1-11所⽰。

Master节点主要由apiserver、controller-manager和scheduler三个组件，以及⼀个⽤于集群状态存储的etcd存储服务组成，⽽每个Node节点则主要包含kubelet、kube-proxy及容器引擎（Docker是最为常⽤的实现）等组件。此外，完整的集群服务还依赖于⼀些附加组件，如KubeDNS等。

Node负责提供运⾏容器的各种依赖环境，并接受Master的管理，Node的核⼼代理程序kubelet，每个Node都要提供⼀个容器运⾏时（Container Runtime）环境，它负责下载镜像并运⾏容器。Kubernetes⽀持的容器运⾏环境⾄少包括Docker、RKT、cri-o和Fraki等。每个⼯作节点都需要运⾏⼀个kube-proxy守护进程，它能够按需为
Service资源对象⽣成iptables或ipvs规则，从⽽捕获访问当前Service的ClusterIP的流量并将其转发⾄正确的后端Pod对象。

核⼼附件：Kubernetes集群还依赖于⼀组称为“附件”（add-ons）的组件以提供完整的功能，它们通常是由第三⽅提供的特定应⽤程序，且托管运⾏于Kubernetes集群之上

```

##### ⽹络模型

```
Kubernetes集群⾄少应该包含三个⽹络，如图1-13中的⽹络环境所⽰。

⼀个是各主机（Master、Node和etcd等）⾃⾝所属的⽹络，其地址配置于主机的⽹络接⼜，⽤于各主机之间的通信，例如，Master与各Node之间的通信。此地址配置于Kubernetes集群构建之前，它并不能由Kubernetes管理，管理员需要于集群构建之前⾃⾏确定其地址配置及管理⽅式。

第⼆个是Kubernetes集群上专⽤于Pod资源对象的⽹络，它是⼀个虚拟⽹络，⽤于为各Pod对象设定IP地址等⽹络参数，其地址配置于Pod中容器的⽹络接⼜之上。Pod⽹络需要借助kubenet插件或CNI插件实现，该插件可独⽴部署于Kubernetes集群之外，亦可托管于Kubernetes之上，它需要在构建Kubernetes集群时由管理员进⾏定义，⽽后在创建Pod对象时由其⾃动完成各⽹络参数的动态配置。

第三个是专⽤于Service资源对象的⽹络，它也是⼀个虚拟⽹络，⽤于为Kubernetes集群之中的Service配置IP地址，但此地址并不配置于任何主机或容器的⽹络接⼜之上，⽽是通过Node之上的kube-proxy配置为iptables或ipvs规则，从⽽将发往此地址的所有流量调度⾄其后端的各Pod对象之上。Service⽹络在Kubernetes集群创建时予以指定，⽽各Service的地址则在⽤户创建Service时予以动态配置。
```

#### 集群

##### 搭建

```shell
前提多台服务器：
a，一台master
b，多台node节点

1，添加k8s 的 yum repo
[root@master yum.repos.d]#cat <<EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64/
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg https://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
> EOF

2，添加docker-ce的 yum repo
[root@master yum.repos.d]#cd /etc/yum.repos.d/
[root@master yum.repos.d]#wget https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo

3，把yum repo拷贝到各个节点
[root@master yum.repos.d]#scp kubernetes.repo docker-ce.repo node1:/etc/yum.repos.d/
[root@master yum.repos.d]#scp kubernetes.repo docker-ce.repo nodeX:/etc/yum.repos.d/

4，安装master的k8s工具
[root@master yum.repos.d]#yum install -y docker-ce kubelet kubeadm kubectl

5，禁用swap
[root@master yum.repos.d]# cat /etc/sysconfig/kubelet
KUBELET_EXTRA_ARGS="--fail-swap-on=false"
[root@master yum.repos.d]# swapoff  -a

6，master服务器初始化master的kubelet
[root@master yum.repos.d]#systemctl enable kubelet.service
[root@master yum.repos.d]#kubeadm init --kubernetes-version=v1.14.2 --pod-network-cidr=10.244.0.0/16 --service-cidr=10.96.0.0/12 --ignore-preflight-errors=Swap
-----------报错 ，很多镜像下载失败，于是按以下步骤处理-----------------
[root@master yum.repos.d]#hostnamectl set-hostname k8s
[root@master yum.repos.d]docker pull mirrorgooglecontainers/kube-apiserver-amd64:v1.14.2
[root@master yum.repos.d]docker pull mirrorgooglecontainers/kube-controller-manager-amd64:v1.14.2
[root@master yum.repos.d]docker pull mirrorgooglecontainers/kube-scheduler-amd64:v1.14.2
[root@master yum.repos.d]docker pull mirrorgooglecontainers/kube-proxy-amd64:v1.14.2
[root@master yum.repos.d]docker pull mirrorgooglecontainers/pause:3.1
[root@master yum.repos.d]docker pull mirrorgooglecontainers/etcd:3.3.10
[root@master yum.repos.d] docker pull coredns/coredns:1.3.1
[root@master yum.repos.d]docker pull mirrorgooglecontainers/kube-apiserver:v1.14.2
[root@master yum.repos.d]docker pull mirrorgooglecontainers/kube-controller-manager:v1.14.2
[root@master yum.repos.d]docker pull mirrorgooglecontainers/kube-scheduler:v1.14.2
[root@master yum.repos.d]docker pull mirrorgooglecontainers/kube-proxy:v1.14.2
[root@master yum.repos.d]docker tag  mirrorgooglecontainers/kube-apiserver:v1.14.2 k8s.gcr.io/kube-apiserver:v1.14.2
[root@master yum.repos.d]docker tag  docker.io/mirrorgooglecontainers/kube-controller-manager:v1.14.2 k8s.gcr.io/kube-controller-manager:v1.14.2
[root@master yum.repos.d]docker tag  docker.io/mirrorgooglecontainers/kube-scheduler:v1.14.2 k8s.gcr.io/kube-scheduler:v1.14.2
[root@master yum.repos.d]docker tag  docker.io/mirrorgooglecontainers/kube-proxy:v1.14.2 k8s.gcr.io/kube-proxy:v1.14.2
[root@master yum.repos.d]docker tag  docker.io/mirrorgooglecontainers/pause:3.1 k8s.gcr.io/pause:3.1
[root@master yum.repos.d]docker tag  docker.io/mirrorgooglecontainers/etcd:3.3.10 k8s.gcr.io/etcd:3.3.10
[root@master yum.repos.d]docker tag  docker.io/coredns/coredns:1.3.1 k8s.gcr.io/coredns:1.3.1
[root@master yum.repos.d]kubeadm init --kubernetes-version=v1.14.2 --pod-network-cidr=10.244.0.0/16 --service-cidr=10.96.0.0/12 --ignore-preflight-errors=Swap
[root@master yum.repos.d]export KUBECONFIG=/etc/kubernetes/admin.conf
[root@master yum.repos.d]. /etc/profile
[root@master yum.repos.d]kubectl get cs
[root@master yum.repos.d]cat /proc/sys/net/bridge/bridge-nf-call-iptables
[root@master yum.repos.d]cat /proc/sys/net/bridge/bridge-nf-call-ip6tables
[root@master yum.repos.d]echo 1> /proc/sys/net/bridge/bridge-nf-call-ip6tables
[root@master yum.repos.d]echo 1 > /proc/sys/net/bridge/bridge-nf-call-ip6tables
[root@master yum.repos.d]cat /proc/sys/net/bridge/bridge-nf-call-ip6tables
[root@master yum.repos.d]kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/v0.10.0/Documentation/kube-flannel.yml
---------将 master 、node节点的ip和映射关系 添加上去
[root@master yum.repos.d]vi /etc/hosts
[root@master yum.repos.d]scp /etc/docker/daemon.json node1:/etc/docker/

---------去master的秘钥和token ，给node节点使用
[root@master yum.repos.d]openssl x509 -pubkey -in /etc/kubernetes/pki/ca.crt | openssl rsa -pubin -outform der 2>/dev/null | openssl dgst -sha256 -hex | sed 's/^.* //'
[root@master yum.repos.d]994  kubectl get nodes


7，node服务器
[root@master yum.repos.d]yum install -y docker kubeadm kubelet
[root@master yum.repos.d]systemctl enable kubelet.service
[root@master yum.repos.d]echo 1 > /proc/sys/net/bridge/bridge-nf-call-iptables
[root@master yum.repos.d]echo 1 > /proc/sys/net/ipv4/ip_forward
[root@master yum.repos.d]cat /etc/sysconfig/kubelet
[root@master yum.repos.d]swapoff -a
[root@master yum.repos.d]docker pull mirrorgooglecontainers/kube-proxy:v1.14.2
[root@master yum.repos.d]docker pull mirrorgooglecontainers/pause:3.1
[root@master yum.repos.d]docker tag  docker.io/mirrorgooglecontainers/kube-proxy:v1.14.2 k8s.gcr.io/kube-proxy:v1.14.2
[root@master yum.repos.d]docker tag  docker.io/mirrorgooglecontainers/pause:3.1 k8s.gcr.io/pause:3.1
[root@master yum.repos.d]docker pull xiyangxixia/k8s-flannel:v0.10.0
[root@master yum.repos.d]docker pull xiyangxixia/k8s-flannel:v0.10.0-amd64
[root@master yum.repos.d]docker tag xiyangxixia/k8s-flannel:v0.10.0-amd64 quay.io/coreos/flannel:v0.10.0-amd64
--------------------加入master ，k8s集群
[root@master yum.repos.d]kubeadm join 192.168.133.27:6443 --token h6xdko.ordisvdwxbnkpdwh --discovery-token-ca-cert-hash sha256:5fa4ec345f14b58c259267fcfaea6e46af000862aaf9ffed7dc869ef9c12e7ad
[root@master yum.repos.d]kubectl get nodes

```

##### 异常

```shell


```

