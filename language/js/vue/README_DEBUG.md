##### windows调试iphone的前端

1，https://www.cnblogs.com/xust14521/p/10332292.html

```
安装scoop的时候注意在cmd下 ，再进入powershell进行安装
下载过程有点长！！~~ ，保证翻了墙
```

2，https://blog.csdn.net/yanzhitaipi/article/details/79446772

```
注意：Couldn't find manifest for的时候根据以下文档调整。
https://www.jianshu.com/p/bb0ba62b519c
https://github.com/google/ios-webkit-debug-proxy/issues/242
https://blog.csdn.net/yanzhitaipi/article/details/79446772

安装的ios-webkit-debug-proxy的过程相当的让人蛋疼，可能要重启powershell、要等待、要换个心情

```

```
PS C:\Users\lqd> scoop bucket add extras
Checking repo... ok
The extras bucket was added successfully.
PS C:\Users\lqd> scoop install ios-webkit-debug-proxy
Updating Scoop...
Updating 'extras' bucket...
 * 497963a1 zotero: Update to version 5.0.71                             7 minutes ago
 * 3b5344b0 azure-functions-core-tools: Update to version 2.7.1471       67 minutes ago
 * 02aa1b37 testcentric: Update to version 1.0.0-beta4                   2 hours ago
 * e170c89b gitahead: Update to version 2.5.8                            3 hours ago
 * b6713f0a wireshark: Update to version 3.0.3                           5 hours ago
 * 33509d5a ueli: Update to version 7.2.8                                5 hours ago
 * 74454a88 steam-library-manager: Update to version 1.5.1.10            5 hours ago
 * 8a4feb7d now-cli: Update to version 15.8.1                            6 hours ago
 * eda726ee mpc-hc-fork: Update to version 1.8.7                         6 hours ago
 * 244b5c2f winsshterm: Update to version 2.6.2                          8 hours ago
 * c0e854a3 terminus: Update to version 1.0.86                           8 hours ago
 * 7763195c mediainfo-gui: Update to version 19.07                       9 hours ago
 * 4e73cca5 conemu-color-themes: Update to version 191972a               10 hours ago
 * 7200da5c conemu-color-themes: Update to version ec8de87               11 hours ago
 * fa820354 krita: Update to version 4.2.3                               15 hours ago
 * 418bfaf8 googlechrome-canary: Update to version 77.0.3854.3           16 hours ago
 * 6037f429 steamcmd: Update to version 1563313966                       18 hours ago
Updating 'main' bucket...
Checking repo... ok
The main bucket was added successfully.
 * ee7eed0b sass: Update to version 1.22.6                               9 minutes ago
 * 427ae364 minio: Update to version 2019-07-17T22-54-12Z                9 minutes ago
 * 750bf40d jx: Update to version 2.0.483                                9 minutes ago
 * 5c823d06 dig: Update to version 9.14.4                                9 minutes ago
 * c5b1d4e4 Yarn: Re-Add Prefix Global Directory Argument (#232)         44 minutes ago
 * f0bdeeb9 vim: Update to version 8.1.1711                              69 minutes ago
 * abd2843e minio-client: Update to version 2019-07-17T22-13-42Z         69 minutes ago
 * 55d90efb jx: Update to version 2.0.482                                69 minutes ago
 * acb97ec6 git-annex: fix checkver and au.hash (#246)                   3 hours ago
 * 22f93f87 doctl: Fix hashes (#250)                                     3 hours ago
 * 61770eb7 aws: Update to version 1.16.199                              5 hours ago
 * 4fe75876 jx: Update to version 2.0.480                                7 hours ago
 * be17e7b7 cmake: Update to version 3.15.0                              8 hours ago
 * 86b4a56b cake: Update to version 0.34.1                               8 hours ago
 * 71d560e5 openssl: Fix license, add desc (#251)                        9 hours ago
 * 07666891 nim: Update to version 0.20.2
```

##### windows调试android

```
chrome://inspect/#devices

```

