**序列化工具****序列化速度序列化文件大小**编程模型复杂度社区活跃度jar包大小

kryo               极快  小          简单高132kb

fst-serializer 快      小          非常简单高246kb

protobuffer  快     较大        较复杂稳定329kb

fastjson         较快 较大        简单一般338kb

jackson         一般  较大        简单稳定1.1mb

gson              较慢  较大        简单稳定189kb



FST序列化方案[序列化]耗时：11305 ms
FastJson序列化方案[序列化]耗时：18973 ms
Jackson2Json序列化方案[序列化]耗时：12073 ms
GenericJackson2JsonRedis序列化方案[序列化]耗时：12902 ms
Jdk序列化方案[序列化]耗时：11323 ms
Stringjson序列化方案[序列化]耗时：12703 ms