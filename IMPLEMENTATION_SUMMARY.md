# Summary of Changes: add_instance and remove_instance Methods

## Overview
Added two new methods to the `MapdlPool` class to enable dynamic management of MAPDL instances:
- `add_instance()`: Add a new MAPDL instance to the pool
- `remove_instance()`: Remove an existing MAPDL instance from the pool

## Files Modified

### 1. `/workspaces/pymapdl/src/ansys/mapdl/core/pool.py`
Added two new public methods to the `MapdlPool` class:

#### `add_instance()` method (lines 849-957)
- **Purpose**: Dynamically add a new MAPDL instance to an existing pool
- **Parameters**:
  - `ip` (optional): IP address for the instance (defaults to LOCALHOST)
  - `port` (optional): Port number (auto-selected if not provided)
  - `name` (optional): Custom name for the instance
  - `exec_file` (optional): Path to MAPDL executable
  - `**kwargs`: Additional arguments passed to `launch_mapdl`
- **Returns**: Index of the newly added instance
- **Features**:
  - Automatically finds available ports when `start_instance=True`
  - Validates IP addresses
  - Creates isolated working directory for the instance
  - Updates internal instance count (`_n_instances`)
  - Verifies successful instance creation
  - Comprehensive error handling with cleanup on failure

#### `remove_instance()` method (lines 959-1030)
- **Purpose**: Remove a MAPDL instance from the pool
- **Parameters**:
  - `index` (required): Index of the instance to remove
  - `force` (optional, default=False): Force removal even if locked/busy
- **Raises**:
  - `IndexError`: If index is out of range
  - `MapdlRuntimeError`: If instance is locked/busy and `force=False`
- **Features**:
  - Checks if instance is locked or busy (unless `force=True`)
  - Properly exits the MAPDL instance
  - Updates internal instance count
  - Handles None instances gracefully
  - Thread-safe exit counter management

### 2. `/workspaces/pymapdl/tests/test_pool.py`
Added comprehensive unit tests:

#### Updated imports (line 42)
- Added `MapdlRuntimeError` to imports for testing error conditions

#### `test_add_remove_instance()` method
- Tests basic add and remove functionality
- Verifies instance counts are correctly updated
- Confirms new instances are functional (can execute MAPDL commands)
- Tests adding multiple instances
- Validates cleanup after removal

#### `test_remove_instance_locked()` method
- Tests error handling when removing locked instances
- Verifies `force=True` parameter works correctly
- Ensures proper error messages are raised

### 3. `/workspaces/pymapdl/doc/source/user_guide/pool.rst`
Added new documentation section:

#### "Dynamically add or remove instances" section
- Explains when and why to use these methods
- Provides practical examples for both methods
- Documents the `force` parameter for removing locked instances
- Includes code examples showing:
  - Basic instance addition
  - Adding with custom parameters
  - Basic instance removal
  - Force removal of busy/locked instances

## Key Implementation Details

### Thread Safety
- Both methods properly manage internal counters (`_spawning_i`, `_exiting_i`)
- Compatible with pool monitoring thread
- Safe to call during pool operation

### Resource Management
- Automatic directory creation for new instances
- Proper cleanup on failure
- Exit handling for removed instances

### Compatibility
- Works with both local and remote MAPDL instances
- Respects pool's `start_instance` setting
- Uses pool's default `exec_file` unless overridden
- Maintains pool healing functionality

### Validation
- IP address validation using existing `check_valid_ip()`
- Port availability checking via `available_ports()`
- Instance creation verification
- Index bounds checking

## Testing
Created test script: `/workspaces/pymapdl/test_add_remove_instance.py`
- Demonstrates practical usage
- Tests basic add/remove operations
- Verifies instance functionality
- Tests multiple additions

## Documentation
- Added comprehensive docstrings with parameter descriptions
- Included usage examples in docstrings
- Updated user guide with dedicated section
- Follows existing PyMAPDL documentation style

## Benefits
1. **Dynamic Scaling**: Users can scale pool size up or down based on workload
2. **Resource Optimization**: Remove idle instances to free system resources
3. **Flexibility**: Add instances with custom configurations
4. **Safety**: Protected removal with lock/busy checks
5. **Robustness**: Comprehensive error handling and cleanup

## Usage Examples

### Adding an instance
```python
pool = MapdlPool(2)
new_idx = pool.add_instance()
# Use pool[new_idx] for work
```

### Removing an instance
```python
pool.remove_instance(2)  # Remove by index
```

### Force remove busy instance
```python
pool.remove_instance(1, force=True)
```

### Custom instance configuration
```python
idx = pool.add_instance(port=50055, name="CustomWorker")
```
