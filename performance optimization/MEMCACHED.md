- 参考文档：<https://github.com/memcached/memcached/wiki>

- 参数：
  memcached 1.5.6
  -p, --port=<num>          TCP port to listen on (default: 11211)
  -U, --udp-port=<num>      UDP port to listen on (default: 11211, 0 is off)
  -s, --unix-socket=<file>  UNIX socket to listen on (disables network support)
  -A, --enable-shutdown     enable ascii "shutdown" command
  -a, --unix-mask=<mask>    access mask for UNIX socket, in octal (default: 0700)
  -l, --listen=<addr>       interface to listen on (default: INADDR_ANY)
  -d, --daemon              run as a daemon
  -r, --enable-coredumps    maximize core file limit
  -u, --user=<user>         assume identity of <username> (only when run as root)
  -m, --memory-limit=<num>  item memory in megabytes (default: 64 MB)
  -M, --disable-evictions   return error on memory exhausted instead of evicting
  -c, --conn-limit=<num>    max simultaneous connections (default: 1024)
  -k, --lock-memory         lock down all paged memory
  -v, --verbose             verbose (print errors/warnings while in event loop)
  -vv                       very verbose (also print client commands/responses)
  -vvv                      extremely verbose (internal state transitions)
  -h, --help                print this help and exit
  -i, --license             print memcached and libevent license
  -V, --version             print version and exit
  -P, --pidfile=<file>      save PID in <file>, only used with -d option
  -f, --slab-growth-factor=<num> chunk size growth factor (default: 1.25)
  -n, --slab-min-size=<bytes> min space used for key+value+flags (default: 48)
  -L, --enable-largepages  try to use large memory pages (if available)
  -D <char>     Use <char> as the delimiter between key prefixes and IDs.
  ​              This is used for per-prefix stats reporting. The default is
  ​              ":" (colon). If this option is specified, stats collection
  ​              is turned on automatically; if not, then it may be turned on
  ​              by sending the "stats detail on" command to the server.
  -t, --threads=<num>       number of threads to use (default: 4)
  -R, --max-reqs-per-event  maximum number of requests per event, limits the
  ​                          requests processed per connection to prevent 
  ​                          starvation (default: 20)
  -C, --disable-cas         disable use of CAS
  -b, --listen-backlog=<num> set the backlog queue limit (default: 1024)
  -B, --protocol=<name>     protocol - one of ascii, binary, or auto (default)
  -I, --max-item-size=<num> adjusts max item size
  ​                          (default: 1mb, min: 1k, max: 128m)
  -F, --disable-flush-all   disable flush_all command
  -X, --disable-dumping     disable stats cachedump and lru_crawler metadump
  -o, --extended            comma separated list of extended options
  ​                          most options have a 'no_' prefix to disable
     \- maxconns_fast:       immediately close new connections after limit
     \- hashpower:           an integer multiplier for how large the hash
  ​                          table should be. normally grows at runtime.
  ​                          set based on "STAT hash_power_level"
     \- tail_repair_time:    time in seconds for how long to wait before
  ​                          forcefully killing LRU tail item.
  ​                          disabled by default; very dangerous option.
     \- hash_algorithm:      the hash table algorithm
  ​                          default is murmur3 hash. options: jenkins, murmur3
     \- lru_crawler:         enable LRU Crawler background thread
     \- lru_crawler_sleep:   microseconds to sleep between items
  ​                          default is 100.
     \- lru_crawler_tocrawl: max items to crawl per slab per run
  ​                          default is 0 (unlimited)
     \- lru_maintainer:      enable new LRU system + background thread
     \- hot_lru_pct:         pct of slab memory to reserve for hot lru.
  ​                          (requires lru_maintainer)
     \- warm_lru_pct:        pct of slab memory to reserve for warm lru.
  ​                          (requires lru_maintainer)
     \- hot_max_factor:      items idle > cold lru age * drop from hot lru.
     \- warm_max_factor:     items idle > cold lru age * this drop from warm.
     \- temporary_ttl:       TTL's below get separate LRU, can't be evicted.
  ​                          (requires lru_maintainer)
     \- idle_timeout:        timeout for idle connections
     \- slab_chunk_max:      (EXPERIMENTAL) maximum slab size. use extreme care.
     \- watcher_logbuf_size: size in kilobytes of per-watcher write buffer.
     \- worker_logbuf_size:  size in kilobytes of per-worker-thread buffer
  ​                          read by background thread, then written to watchers.
     \- track_sizes:         enable dynamic reports for 'stats sizes' command.
     \- no_inline_ascii_resp: save up to 24 bytes per item.
  ​                           small perf hit in ASCII, no perf difference in
  ​                           binary protocol. speeds up all sets.
     \- no_hashexpand:       disables hash table expansion (dangerous)
     \- modern:              enables options which will be default in future.
  ​             currently: nothing
     \- no_modern:           uses defaults of previous major version (1.4.x)

- stats统计项

  - ① 命中率 ：stats命令

    ![img](https://img.mubu.com/document_image/f365e8f1-26e2-4ef3-bd8e-30892d549a4d-862021.jpg)

    get_hits表示读取cache命中的次数，get_misses是读取失败的次数，即尝试读取不存在的缓存数据。即：命中率=get_hits / (get_hits + get_misses) 
    命中率越高说明cache起到的缓存作用越大。但是在实际使用中，这个命中率不是有效数据的命中率，有些时候get操作可能只是检查一个key存在不存在，这个时候miss也是正确的，这个命中率是从memcached启动开始所有的请求的综合值，不能反映一个时间段内的情况，所以要排查memcached的性能问题，还需要更详细的数值。但是高的命中率还是能够反映出memcached良好的使用情况，突然下跌的命中率能够反映大量cache丢失的发生。

  - 观察各slab的items的情况：Stats items命令

    ![img](https://img.mubu.com/document_image/5b171b67-108b-4f90-b3d1-d69249f22789-862021.jpg)

    outofmemoryslab class为新item分配空间失败的次数。这意味着你运行时带上了-M或者移除操作失败
    ​number存放的数据总数
    ​age存放的数据中存放时间最久的数据已经存在的时间，以秒为单位
    ​evicted不得不从LRU中移除未过期item的次数 
    ​evicted_time自最后一次清除过期item起所经历的秒数，即最后被移除缓存的时间，0表示当前就有被移除，用这个来判断数据被移除的最近时间
    ​evicted_nonzero没有设置过期时间（默认30天），但不得不从LRU中称除该未过期的item的次数
    ​
    ​​​因为memcached的内存分配策略导致一旦memcached的总内存达到了设置的最大内存，表示所有的slab能够使用的page都已经固定，这时如果还有数据放入，将导致memcached使用LRU策略剔除数据。而LRU策略不是针对所有的slabs，而是只针对新数据应该被放入的slab，例如有一个新的数据要被放入slab 3，则LRU只对slab 3进行，通过stats items就可以观察到这些剔除的情况。
    注意evicted_time：并不是发生了LRU就代表memcached负载过载了，因为有些时候在使用cache时会设置过期时间为0，这样缓存将被存放30天，如果内存满了还持续放入数据，而这些为过期的数据很久没有被使用，则可能被剔除。把evicted_time换算成标准时间看下是否已经达到了你可以接受的时间，例如：你认为数据被缓存了2天是你可以接受的，而最后被剔除的数据已经存放了3天以上，则可以认为这个slab的压力其实可以接受的；但是如果最后被剔除的数据只被缓存了20秒，不用考虑，这个slab已经负载过重了。
    ​
    通过上面的说明可以看到当前的memcache的slab1的状态：
    items有305816个，有效时间最久的是21529秒，通过LRU移除未过期的items有95336839个，通过LRU移除没有设置过期时间的未过期items有95312220个，当前就有被清除的items，启动时没有带-M参数。

  - ③ 观察各slabs的情况：stats slabs命令

    ![img](https://img.mubu.com/document_image/af7ae8f0-b2a4-47d3-82bb-17550ddba872-862021.jpg)

    从Stats items中如果发现有异常的slab，则可以通过stats slabs查看下该slab是不是内存分配的确有问题。
    chunk_size当前slab每个chunk的大小
    ​chunk_per_page每个page能够存放的chunk数
    ​total_pages分配给当前slab的page总数，默认1个page大小1M，可以计算出该slab的大小
    ​total_chunks当前slab最多能够存放的chunk数，应该等于chunck_per_page * total_page
    ​used_chunks已经被占用的chunks总数
    ​free_chunks过期数据空出的chunk但还没有被使用的chunk数
    ​free_chunks_end新分配的但是还没有被使用的chunk数 
     
    这里需要注意：total_pages 这个是当前slab总共分配大的page总数，如果没有修改page的默认大小的情况下，这个数值就是当前slab能够缓存的数据的总大小（单位为M）。如果这个slab的剔除非常严重，一定要注意这个slab的page数是不是太少了。还有一个公式：
    total_chunks = used_chunks + free_chunks + free_chunks_end
    另外stats slabs还有2个属性：
    属性名称属性说明
    ​active_slabs活动的slab总数
    ​total_malloced实际已经分配的总内存数，单位为byte，
    ​这个数值决定了memcached实际还能申请多少内存，如果这个值已经达到设定的上限(和stats settings中的maxbytes对比)，则不会有新的page被分配。​

  - ④ 对象数量的统计：stats sizes
    该命令会锁定服务，暂停处理请求。该命令展示了固定chunk大小中的items的数量。也可以看出slab1(96byte)中有多少个chunks。

  - ⑤ 查看、导出key：stats cachedump
    在进入memcache中，大家都想查看cache里的key，类似redis中的keys *命令，在memcache里也可以查看，但是需要2步完成。
    一是先列出items:
    stats items --命令
    ...
    ...
    STAT items:29:number 228
    STAT items:29:age 34935
    ...
    END
    二是通过itemid取key，上面的id是29，再加上一个参数：为列出的长度，0为全部列出。
    stats cachedump 29 0 --命令
    ITEM 26457202 [49440 b; 1467262309 s]
    ...
    ITEM 30017977 [45992 b; 1467425702 s]
    ITEM 26634739 [48405 b; 1467437677 s]
    END --总共228个key
    get 26634739 取value
    如何导出key呢？这里就需要通过 echo ... nc 来完成了
    echo "stats cachedump 29 0" | nc 10.211.55.9 11212 >/home/zhoujy/memcache.log
    在导出的时候需要注意的是：cachedump命令每次返回的数据大小只有2M，这个是memcached的代码中写死的一个数值，除非在编译前修改。

  - ⑥ 另一个监控工具：memcached-tool（<https://github.com/memcached/memcached/blob/master/scripts/memcached-tool>），一个perl写的工具：[memcache_tool.pl](http://memcache_tool.pl)。
    列含义
    ​#slab class编号Item_Size　　　
    ​chunk大小
    ​Max_ageLRU内最旧的记录的生存时间
    ​pages分配给Slab的页数
    ​countSlab内的记录数、chunks数、items数、keys数
    ​Full?Slab内是否含有空闲​chunk
    ​Evicted从LRU中移除未过期item的次数
    ​Evict_Time最后被移除缓存的时间，0表示当前就有被移除
    ​OOM-M参数？