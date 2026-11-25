# Use counters and explicit ordering for state touched by several threads

Two components update shared state from multiple threads. `MapdlPool` spawns and exits instances on several threads concurrently, so it tracks them with the integer counters `_spawning_i` and `_exiting_i` instead of booleans; the `_spawning` and `_exiting` properties report busy while the counter is non-zero. In `MeshGrpc._update_cache`, `_update_cache_elem` is not guarded by `_thread_lock_grpc`, so it runs first and alone, and must finish before `_update_cache_element_desc`, `_update_cache_nnum` and `_update_node_coord` start; otherwise it could race with them.

## Consequences

- One thread finishing a spawn or exit does not clear the busy state while others are still running.
- The call order in `MeshGrpc._update_cache` is load-bearing; parallelising or reordering it requires guarding `_update_cache_elem` first.
