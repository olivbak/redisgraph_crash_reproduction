# redisgraph_crash_reproduction
Showcases a reproducible crash using redisgraph 2.12.10

## How to reproduce
1. `git clone https://github.com/olivbak/redisgraph_crash_reproduction`
2. `cd redis_crash_reprodside docker container: `python3 lib/reproduction.py`
uction`
3. Build service: `docker-compose run --use-aliases --rm crash-service`
4. Inside docker container: `python3 lib/reproduction.py`

Above steps will reproduce crash within ~1 second.

## What is the test doing?
See `redis_crash_report/lib/reproduction.py` for reproduction code.
1. Two clients spam a random query (from a set of two queries) in parallel. Both
two queries in the set might delete an edge (directly or indirectly).
2. IF both clients packs the random query into a transaction(MULTI/EXEC), nothing happens.
3. IF no clients packs the random query into a transaction(MULTI/EXEC), nothing happens.
4. BUT IF one client packs the random query into a transaction (MULTI/EXEC), redis crashes. I.e.
its seems like a race condition on edge deletion, between transactions and non transactions.


## CRASH REPORT
Getting logs from the `redis`-container yields following CRASH REPORT:
```
=== REDIS BUG REPORT START: Cut & paste starting from here ===
1:M 08 Nov 2023 12:28:10.501 # Redis 7.0.12 crashed by signal: 11, si_code: 1
1:M 08 Nov 2023 12:28:10.501 # Accessing address: (nil)
1:M 08 Nov 2023 12:28:10.501 # Crashed running the instruction at: 0x7f45ad85e2a1

------ STACK TRACE ------
EIP:
/usr/lib/redisgraph.so(UndoLog_DeleteEdge+0x41)[0x7f45ad85e2a1]

Backtrace:
/lib/x86_64-linux-gnu/libc.so.6(+0x3bfd0)[0x7f45afc93fd0]
/usr/lib/redisgraph.so(UndoLog_DeleteEdge+0x41)[0x7f45ad85e2a1]
/usr/lib/redisgraph.so(DeleteEdges+0x9a)[0x7f45ad83f1fa]
/usr/lib/redisgraph.so(+0x2bba74)[0x7f45ad828a74]
/usr/lib/redisgraph.so(+0x2be0e5)[0x7f45ad82b0e5]
/usr/lib/redisgraph.so(+0x2be0e5)[0x7f45ad82b0e5]
/usr/lib/redisgraph.so(+0x2c13cc)[0x7f45ad82e3cc]
/usr/lib/redisgraph.so(+0x2c1830)[0x7f45ad82e830]
/usr/lib/redisgraph.so(ExecutionPlan_Execute+0x48)[0x7f45ad81daa8]
/usr/lib/redisgraph.so(+0x2a5cf5)[0x7f45ad812cf5]
/usr/lib/redisgraph.so(CommandDispatch+0x462)[0x7f45ad812082]
redis-server *:6379(RedisModuleCommandDispatcher+0x3b)[0x559f1116ecfb]
redis-server *:6379(call+0xcb)[0x559f110d30eb]
redis-server *:6379(execCommand+0x22c)[0x559f1112fd3c]
redis-server *:6379(call+0xcb)[0x559f110d30eb]
redis-server *:6379(processCommand+0x96d)[0x559f110d59ed]
redis-server *:6379(processInputBuffer+0xe6)[0x559f110ec496]
redis-server *:6379(readQueryFromClient+0x2e8)[0x559f110efe18]
redis-server *:6379(+0x13f0fc)[0x559f111980fc]
redis-server *:6379(+0x71090)[0x559f110ca090]
redis-server *:6379(aeMain+0x1d)[0x559f110cab1d]
redis-server *:6379(main+0x2f9)[0x559f110c64f9]
/lib/x86_64-linux-gnu/libc.so.6(+0x271ca)[0x7f45afc7f1ca]
/lib/x86_64-linux-gnu/libc.so.6(__libc_start_main+0x85)[0x7f45afc7f285]
redis-server *:6379(_start+0x21)[0x559f110c6bd1]

------ REGISTERS ------
1:M 08 Nov 2023 12:28:10.504 #
RAX:0000000000000000 RBX:00007f45af82a88c
RCX:00007f45afe2ca80 RDX:0000000000000000
RDI:00007f45af80c958 RSI:0000000000000000
RBP:0000000000000000 RSP:00007ffebf22e390
R8 :0000000000000000 R9 :00007f45af82a880
R10:0000000000000001 R11:00007f45afc53fc0
R12:0000000000000001 R13:00007f45af80c958
R14:0000000000000000 R15:00007f45af86a1c0
RIP:00007f45ad85e2a1 EFL:0000000000010246
CSGSFS:002b000000000033
1:M 08 Nov 2023 12:28:10.504 # (00007ffebf22e39f) -> 0000000000000001
1:M 08 Nov 2023 12:28:10.504 # (00007ffebf22e39e) -> 0000000000000001
1:M 08 Nov 2023 12:28:10.504 # (00007ffebf22e39d) -> 00007f45af86a900
1:M 08 Nov 2023 12:28:10.504 # (00007ffebf22e39c) -> 00007f45af86a90c
1:M 08 Nov 2023 12:28:10.504 # (00007ffebf22e39b) -> 00007f45af849780
1:M 08 Nov 2023 12:28:10.504 # (00007ffebf22e39a) -> 0000000000000008
1:M 08 Nov 2023 12:28:10.504 # (00007ffebf22e399) -> 00000000ad851d0d
1:M 08 Nov 2023 12:28:10.504 # (00007ffebf22e398) -> 00007ffebf22e330
1:M 08 Nov 2023 12:28:10.504 # (00007ffebf22e397) -> 00007f45ad83f1fa
1:M 08 Nov 2023 12:28:10.504 # (00007ffebf22e396) -> 00007f45af80c958
1:M 08 Nov 2023 12:28:10.504 # (00007ffebf22e395) -> 00007f45af82a88c
1:M 08 Nov 2023 12:28:10.504 # (00007ffebf22e394) -> 0000000000000001
1:M 08 Nov 2023 12:28:10.504 # (00007ffebf22e393) -> 00007f45af82a88c
1:M 08 Nov 2023 12:28:10.504 # (00007ffebf22e392) -> 00007f45af849180
1:M 08 Nov 2023 12:28:10.504 # (00007ffebf22e391) -> 0000000000000003
1:M 08 Nov 2023 12:28:10.504 # (00007ffebf22e390) -> 0000000000000000

------ INFO OUTPUT ------
# Server
redis_version:7.0.12
redis_git_sha1:00000000
redis_git_dirty:0
redis_build_id:275d31c4087c801
redis_mode:standalone
os:Linux 6.2.0-36-generic x86_64
arch_bits:64
monotonic_clock:POSIX clock_gettime
multiplexing_api:epoll
atomicvar_api:c11-builtin
gcc_version:12.2.0
process_id:1
process_supervised:no
run_id:ee76604cea1564e92ed2912b473f79786b84b37b
tcp_port:6379
server_time_usec:1699446490501723
uptime_in_seconds:31
uptime_in_days:0
hz:10
configured_hz:10
lru_clock:4947674
executable:/data/redis-server
config_file:
io_threads_active:0

# Clients
connected_clients:2
cluster_connections:0
maxclients:10000
client_recent_max_input_buffer:0
client_recent_max_output_buffer:0
blocked_clients:1
tracking_clients:0
clients_in_timeout_table:0

# Memory
used_memory:3123816
used_memory_human:2.98M
used_memory_rss:17133568
used_memory_rss_human:16.34M
used_memory_peak:3123816
used_memory_peak_human:2.98M
used_memory_peak_perc:117.17%
used_memory_overhead:930808
used_memory_startup:930328
used_memory_dataset:2193008
used_memory_dataset_perc:99.98%
allocator_allocated:2694128
allocator_active:3002368
allocator_resident:7593984
total_system_memory:33296158720
total_system_memory_human:31.01G
used_memory_lua:31744
used_memory_vm_eval:31744
used_memory_lua_human:31.00K
used_memory_scripts_eval:0
number_of_cached_scripts:0
number_of_functions:0
number_of_libraries:0
used_memory_vm_functions:32768
used_memory_vm_total:64512
used_memory_vm_total_human:63.00K
used_memory_functions:184
used_memory_scripts:184
used_memory_scripts_human:184B
maxmemory:0
maxmemory_human:0B
maxmemory_policy:noeviction
allocator_frag_ratio:1.11
allocator_frag_bytes:308240
allocator_rss_ratio:2.53
allocator_rss_bytes:4591616
rss_overhead_ratio:2.26
rss_overhead_bytes:9539584
mem_fragmentation_ratio:7.34
mem_fragmentation_bytes:14799440
mem_not_counted_for_evict:0
mem_replication_backlog:0
mem_total_replication_buffers:0
mem_clients_slaves:0
mem_clients_normal:0
mem_cluster_links:0
mem_aof_buffer:0
mem_allocator:jemalloc-5.2.1
active_defrag_running:0
lazyfree_pending_objects:0
lazyfreed_objects:0

# Persistence
loading:0
async_loading:0
current_cow_peak:0
current_cow_size:0
current_cow_size_age:0
current_fork_perc:0.00
current_save_keys_processed:0
current_save_keys_total:0
rdb_changes_since_last_save:60
rdb_bgsave_in_progress:0
rdb_last_save_time:1699446459
rdb_last_bgsave_status:ok
rdb_last_bgsave_time_sec:-1
rdb_current_bgsave_time_sec:-1
rdb_saves:0
rdb_last_cow_size:0
rdb_last_load_keys_expired:0
rdb_last_load_keys_loaded:5
aof_enabled:0
aof_rewrite_in_progress:0
aof_rewrite_scheduled:0
aof_last_rewrite_time_sec:-1
aof_current_rewrite_time_sec:-1
aof_last_bgrewrite_status:ok
aof_rewrites:0
aof_rewrites_consecutive_failures:0
aof_last_write_status:ok
aof_last_cow_size:0
module_fork_in_progress:0
module_fork_last_cow_size:0

# Stats
total_connections_received:2
total_commands_processed:171
instantaneous_ops_per_sec:0
total_net_input_bytes:17671
total_net_output_bytes:17384
total_net_repl_input_bytes:0
total_net_repl_output_bytes:0
instantaneous_input_kbps:0.00
instantaneous_output_kbps:0.00
instantaneous_input_repl_kbps:0.00
instantaneous_output_repl_kbps:0.00
rejected_connections:0
sync_full:0
sync_partial_ok:0
sync_partial_err:0
expired_keys:0
expired_stale_perc:0.00
expired_time_cap_reached_count:0
expire_cycle_cpu_milliseconds:0
evicted_keys:0
evicted_clients:0
total_eviction_exceeded_time:0
current_eviction_exceeded_time:0
keyspace_hits:183
keyspace_misses:0
pubsub_channels:0
pubsub_patterns:0
pubsubshard_channels:0
latest_fork_usec:0
total_forks:0
migrate_cached_sockets:0
slave_expires_tracked_keys:0
active_defrag_hits:0
active_defrag_misses:0
active_defrag_key_hits:0
active_defrag_key_misses:0
total_active_defrag_time:0
current_active_defrag_time:0
tracking_total_keys:0
tracking_total_items:0
tracking_total_prefixes:0
unexpected_error_replies:0
total_error_replies:0
dump_payload_sanitizations:0
total_reads_processed:89
total_writes_processed:87
io_threaded_reads_processed:0
io_threaded_writes_processed:0
reply_buffer_shrinks:0
reply_buffer_expands:0

# Replication
role:master
connected_slaves:0
master_failover_state:no-failover
master_replid:9332bb1190fb857c29e45adf22eb7ff67fff4a6b
master_replid2:0000000000000000000000000000000000000000
master_repl_offset:0
second_repl_offset:-1
repl_backlog_active:0
repl_backlog_size:1048576
repl_backlog_first_byte_offset:0
repl_backlog_histlen:0

# CPU
used_cpu_sys:0.051652
used_cpu_user:0.051652
used_cpu_sys_children:0.000000
used_cpu_user_children:0.000743
used_cpu_sys_main_thread:0.049636
used_cpu_user_main_thread:0.045123

# Modules
module:name=graph,ver=21210,api=1,filters=0,usedby=[],using=[],options=[]

# Commandstats
cmdstat_multi:calls=42,usec=9,usec_per_call=0.21,rejected_calls=0,failed_calls=0
cmdstat_graph.QUERY:calls=88,usec=13200,usec_per_call=150.00,rejected_calls=0,failed_calls=0
cmdstat_exec:calls=41,usec=5108,usec_per_call=124.59,rejected_calls=0,failed_calls=0

# Errorstats

# Latencystats
latency_percentiles_usec_multi:p50=0.001,p99=1.003,p99.9=1.003
latency_percentiles_usec_graph.QUERY:p50=118.271,p99=524.287,p99.9=720.895
latency_percentiles_usec_exec:p50=107.007,p99=536.575,p99.9=536.575

# Cluster
cluster_enabled:0

# Keyspace
db0:keys=5,expires=0,avg_ttl=0

------ CLIENT LIST OUTPUT ------
id=19 addr=172.21.0.3:42014 laddr=172.21.0.2:6379 fd=8 name= age=0 idle=0 flags=x db=0 sub=0 psub=0 ssub=0 multi=1 qbuf=301 qbuf-free=20173 argv-mem=4 multi-mem=271 rbs=16384 rbp=16384 obl=18 oll=0 omem=0 tot-mem=37979 events=r cmd=exec user=default redir=-1 resp=2
id=20 addr=172.21.0.3:42000 laddr=172.21.0.2:6379 fd=9 name= age=0 idle=0 flags=b db=0 sub=0 psub=0 ssub=0 multi=-1 qbuf=0 qbuf-free=20474 argv-mem=83 multi-mem=0 rbs=16384 rbp=16384 obl=0 oll=0 omem=0 tot-mem=37739 events=r cmd=graph.QUERY user=default redir=-1 resp=2

------ CURRENT CLIENT INFO ------
id=19 addr=172.21.0.3:42014 laddr=172.21.0.2:6379 fd=8 name= age=0 idle=0 flags=x db=0 sub=0 psub=0 ssub=0 multi=1 qbuf=301 qbuf-free=20173 argv-mem=4 multi-mem=271 rbs=16384 rbp=16384 obl=18 oll=0 omem=0 tot-mem=37979 events=r cmd=exec user=default redir=-1 resp=2
argv[0]: '"GRAPH.QUERY"'
argv[1]: '"key"'
argv[2]: '"\nCYPHER actor_id=1 movie_id=2\n\nMERGE (actor:Actor {id: $actor_id})\nWITH actor\nOPTIONAL MATCH (actor)-[acts:STARS_IN]->(old_movie"'
1:M 08 Nov 2023 12:28:10.504 # key 'key' found in DB containing the following object:
1:M 08 Nov 2023 12:28:10.504 # Object type: 5
1:M 08 Nov 2023 12:28:10.504 # Object encoding: 0
1:M 08 Nov 2023 12:28:10.504 # Object refcount: 1

------ MODULES INFO OUTPUT ------
# graph_executing commands
graph_command:GRAPH.QUERY
CYPHER actor_id=1 movie_id=2

MERGE (actor:Actor {id: $actor_id})
WITH actor
OPTIONAL MATCH (actor)-[acts:STARS_IN]->(old_movie:Movie)
DELETE acts
MERGE (movie:Movie {id: $movie_id})
MERGE (actor)-[:STARS_IN]->(movie)

RETURN actor


------ CONFIG DEBUG OUTPUT ------
sanitize-dump-payload no
io-threads-do-reads no
activedefrag no
lazyfree-lazy-eviction no
repl-diskless-load disabled
lazyfree-lazy-user-flush no
proto-max-bulk-len 512mb
client-query-buffer-limit 1gb
list-compress-depth 0
io-threads 1
repl-diskless-sync yes
lazyfree-lazy-server-del no
lazyfree-lazy-expire no
replica-read-only yes
slave-read-only yes
lazyfree-lazy-user-del no

------ FAST MEMORY TEST ------
1:M 08 Nov 2023 12:28:10.504 # Bio thread for job type #0 terminated
1:M 08 Nov 2023 12:28:10.504 # Bio thread for job type #1 terminated
1:M 08 Nov 2023 12:28:10.504 # Bio thread for job type #2 terminated
*** Preparing to test memory region 559f11329000 (2301952 bytes)
*** Preparing to test memory region 559f12468000 (2502656 bytes)
*** Preparing to test memory region 7f4550000000 (2125824 bytes)
*** Preparing to test memory region 7f4554000000 (2125824 bytes)
*** Preparing to test memory region 7f4558000000 (2125824 bytes)
*** Preparing to test memory region 7f455c000000 (2125824 bytes)
*** Preparing to test memory region 7f4560000000 (2125824 bytes)
*** Preparing to test memory region 7f4564000000 (2125824 bytes)
*** Preparing to test memory region 7f4568000000 (2125824 bytes)
*** Preparing to test memory region 7f456de00000 (37777408 bytes)
*** Preparing to test memory region 7f4574000000 (2125824 bytes)
*** Preparing to test memory region 7f4578000000 (2125824 bytes)
*** Preparing to test memory region 7f457c000000 (2125824 bytes)
*** Preparing to test memory region 7f4580000000 (2125824 bytes)
*** Preparing to test memory region 7f4584000000 (2125824 bytes)
*** Preparing to test memory region 7f4588000000 (2125824 bytes)
*** Preparing to test memory region 7f458c000000 (2125824 bytes)
*** Preparing to test memory region 7f4590000000 (2125824 bytes)
*** Preparing to test memory region 7f4594000000 (135168 bytes)
*** Preparing to test memory region 7f4598000000 (135168 bytes)
*** Preparing to test memory region 7f459c000000 (33554432 bytes)
*** Preparing to test memory region 7f459e200000 (8388608 bytes)
*** Preparing to test memory region 7f459ea00000 (4194304 bytes)
*** Preparing to test memory region 7f459f000000 (8388608 bytes)
*** Preparing to test memory region 7f459f800000 (4194304 bytes)
*** Preparing to test memory region 7f459fd6b000 (2621440 bytes)
*** Preparing to test memory region 7f459ffec000 (8388608 bytes)
*** Preparing to test memory region 7f45a07ed000 (8388608 bytes)
*** Preparing to test memory region 7f45a0fee000 (8388608 bytes)
*** Preparing to test memory region 7f45a17ef000 (8388608 bytes)
*** Preparing to test memory region 7f45a1ff0000 (8388608 bytes)
*** Preparing to test memory region 7f45a27f1000 (8388608 bytes)
*** Preparing to test memory region 7f45a2ff2000 (8388608 bytes)
*** Preparing to test memory region 7f45a37f3000 (8388608 bytes)
*** Preparing to test memory region 7f45a3ff4000 (8388608 bytes)
*** Preparing to test memory region 7f45a47f5000 (8388608 bytes)
*** Preparing to test memory region 7f45a4ff6000 (8388608 bytes)
*** Preparing to test memory region 7f45a57f7000 (8388608 bytes)
*** Preparing to test memory region 7f45a5ff8000 (8388608 bytes)
*** Preparing to test memory region 7f45a67f9000 (8388608 bytes)
*** Preparing to test memory region 7f45a6ffa000 (8388608 bytes)
*** Preparing to test memory region 7f45a77fb000 (8388608 bytes)
*** Preparing to test memory region 7f45a7ffc000 (8388608 bytes)
*** Preparing to test memory region 7f45a87fd000 (8388608 bytes)
*** Preparing to test memory region 7f45a8ffe000 (8388608 bytes)
*** Preparing to test memory region 7f45a97ff000 (8388608 bytes)
*** Preparing to test memory region 7f45aa000000 (8388608 bytes)
*** Preparing to test memory region 7f45aa800000 (2097152 bytes)
*** Preparing to test memory region 7f45aab49000 (8388608 bytes)
*** Preparing to test memory region 7f45ab349000 (2097152 bytes)
*** Preparing to test memory region 7f45ab54a000 (8388608 bytes)
*** Preparing to test memory region 7f45abd4b000 (8388608 bytes)
*** Preparing to test memory region 7f45ac54c000 (8388608 bytes)
*** Preparing to test memory region 7f45acd4d000 (8388608 bytes)
*** Preparing to test memory region 7f45af3f8000 (32768 bytes)
*** Preparing to test memory region 7f45af400000 (8388608 bytes)
*** Preparing to test memory region 7f45afc52000 (24576 bytes)
*** Preparing to test memory region 7f45afe2c000 (53248 bytes)
*** Preparing to test memory region 7f45b02b7000 (12288 bytes)
*** Preparing to test memory region 7f45b0444000 (8192 bytes)
.O.O.O.O.O.O.O.O.O.O.O.O.O.O.O.O.O.O.O.O.O.O.O.O.O.O.O.O.O.O.O.O.O.O.O.O.O.O.O.O.O.O.O.O.O.O.O.O.O.O.O.O.O.O.O.O.O.O.O.O
Fast memory test PASSED, however your memory can still be broken. Please run a memory test for several hours if possible.

------ DUMPING CODE AROUND EIP ------
Symbol: UndoLog_DeleteEdge (base: 0x7f45ad85e260)
Module: /usr/lib/redisgraph.so (base 0x7f45ad56d000)
$ xxd -r -p /tmp/dump.hex /tmp/dump.bin
$ objdump --adjust-vma=0x7f45ad85e260 -D -b binary -m i386:x86-64 /tmp/dump.bin
------
1:M 08 Nov 2023 12:28:11.087 # dump of function (hexdump of 193 bytes):
415641554989fd4889f7415455534889f34883ec104c8b7608e8d2dcfdff4889df4889c5e8d7dcfdff4889df4889442408e8dadcfdff4c89ef31f64189c4488b03488b184889da480fbaea3f488910e8ec16000066480f6ec50f164424084c89304489600848895820c74040040000000f1140104883c4105b5d415c415d415ec366662e0f1f8400000000000f1f4000554889d55389cb4883ec5883f9017470f30f6f26f30f6f6e10f30f6f76200f1124240f116c24100f1174242031f6e87d16
Function at 0x7f45ad85f9a0 is DataBlock_AllocateItem

=== REDIS BUG REPORT END. Make sure to include from START to END. ===
```
