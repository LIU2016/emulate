### 跨浏览器、终端适配问题

```
1，转时间戳safari浏览器不兼容，要采用以下方式(用.replace(/-/g,"/")处理下字符串即可)：
let startDate = new Date(param.startTime.replace(/-/g,"/"));
let time = Date.parse(startDate);

```

### js下载

```
 async download (url, name) {
      var xhr = new XMLHttpRequest()
      xhr.open('GET', url, true)
      xhr.responseType = 'blob'
      xhr.onload = function (e) {
        if (this.status === 200) {
          var myBlob = this.response
          var aLink = document.createElement('a')
          aLink.download = name
          aLink.href = URL.createObjectURL(myBlob)
          aLink.click()
          // myBlob is now the blob that the object URL pointed to.
        }
      }
      xhr.send()
    },
```

