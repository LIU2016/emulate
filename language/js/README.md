### 跨浏览器、终端适配问题

```
1，转时间戳safari浏览器不兼容，要采用以下方式(用.replace(/-/g,"/")处理下字符串即可)：
let startDate = new Date(param.startTime.replace(/-/g,"/"));
let time = Date.parse(startDate);

```

