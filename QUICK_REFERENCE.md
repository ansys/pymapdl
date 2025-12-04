# Quick Reference: add_instance and remove_instance Methods

## Method Signatures

### add_instance()
```python
def add_instance(
    self,
    ip: Optional[str] = None,
    port: Optional[int] = None,
    name: Optional[str] = None,
    exec_file: Optional[str] = None,
    **kwargs,
) -> int
```

**Returns**: Index of the newly added instance

### remove_instance()
```python
def remove_instance(
    self,
    index: int,
    force: bool = False
) -> None
```

## Quick Examples

### Basic Usage
```python
from ansys.mapdl.core import MapdlPool

# Create a pool with 2 instances
pool = MapdlPool(2)

# Add a new instance
new_idx = pool.add_instance()
print(f"Pool now has {len(pool)} instances")

# Remove an instance
pool.remove_instance(new_idx)
print(f"Pool now has {len(pool)} instances")
```

### Advanced Usage
```python
# Add instance with specific configuration
idx = pool.add_instance(
    port=50055,
    name="HighPriorityWorker",
)

# Force remove a busy instance
pool.remove_instance(1, force=True)
```

## Key Features

✓ Dynamic pool sizing
✓ Automatic port selection
✓ Thread-safe operations
✓ Comprehensive error handling
✓ Lock/busy state protection
✓ Automatic cleanup on failure

## Common Use Cases

1. **Scale up during peak load**
   ```python
   for _ in range(5):
       pool.add_instance()
   ```

2. **Scale down to free resources**
   ```python
   while len(pool) > 2:
       pool.remove_instance(len(pool._instances) - 1)
   ```

3. **Replace failed instance**
   ```python
   pool.remove_instance(failed_idx, force=True)
   new_idx = pool.add_instance()
   ```

## Error Handling

### add_instance errors
- `MapdlRuntimeError`: Failed to create instance
- Port/IP validation errors

### remove_instance errors
- `IndexError`: Invalid index
- `MapdlRuntimeError`: Instance is locked/busy (without force=True)

## Testing

Run the test suite:
```bash
pytest tests/test_pool.py::TestMapdlPool::test_add_remove_instance -v
pytest tests/test_pool.py::TestMapdlPool::test_remove_instance_locked -v
```

## Documentation
- User Guide: `doc/source/user_guide/pool.rst` (lines 215-245)
- API Reference: Automatically generated from docstrings
