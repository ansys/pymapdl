# Launch MAPDL Docker Action

> Reusable GitHub Action for launching MAPDL instances in Docker containers with automatic cleanup

A comprehensive, production-ready action that consolidates MAPDL Docker launch scripts into a single reusable component with type-safe inputs, structured outputs, and built-in service readiness checks.

## Features

- ✅ **Automatic cleanup** - Containers stopped/removed when workflow completes
- ✅ **Configurable inputs** with smart defaults
- ✅ **7 structured outputs** for downstream steps
- ✅ **Automatic image detection** (Ubuntu/CentOS/CICD/Student)
- ✅ **Built-in service checks** - waits for MAPDL and DPF to be ready
- ✅ **Multi-instance support** - run multiple MAPDL containers in parallel
- ✅ **SMP and DMP modes** with configurable processors
- ✅ **Optional DPF server** for data processing
- ✅ **Cross-repository reusable** - use from any GitHub repo

## Quick Start

### Minimal Examples

**Option 1: Using version number (simpler, defaults to ubuntu-cicd)**

```yaml
steps:
  - uses: actions/checkout@v4

  - name: Login to registry
    uses: docker/login-action@v3
    with:
      registry: ghcr.io
      username: ${{ github.actor }}
      password: ${{ secrets.GITHUB_TOKEN }}

  - name: Launch MAPDL
    uses: ./.github/actions/launch-mapdl-docker
    with:
      mapdl-version: '25.2'  # Automatically uses v25.2-ubuntu-cicd
      license-server: ${{ secrets.LICENSE_SERVER }}
```

**Option 2: Using full image reference (for custom variants)**

```yaml
steps:
  - uses: actions/checkout@v4

  - name: Login to registry
    uses: docker/login-action@v3
    with:
      registry: ghcr.io
      username: ${{ github.actor }}
      password: ${{ secrets.GITHUB_TOKEN }}

  - name: Launch MAPDL
    uses: ./.github/actions/launch-mapdl-docker
    with:
      mapdl-image: 'ghcr.io/ansys/mapdl:v25.2-ubuntu'  # Full image reference
      license-server: ${{ secrets.LICENSE_SERVER }}
```

**Note:** Use either `mapdl-version` OR `mapdl-image`, not both. Cleanup is automatic.

### Common Configurations

#### With DPF Server (using version number)

```yaml
- name: Launch MAPDL with DPF
  uses: ./.github/actions/launch-mapdl-docker
  with:
    mapdl-version: '25.2'  # Automatically uses v25.2-ubuntu-cicd
    license-server: ${{ secrets.LICENSE_SERVER }}
    enable-dpf-server: 'true'
```

#### High Performance (DMP, 4 CPUs)

```yaml
- name: Launch MAPDL
  uses: ./.github/actions/launch-mapdl-docker
  with:
    mapdl-version: '25.2'
    license-server: ${{ secrets.LICENSE_SERVER }}
    distributed-mode: 'dmp'
    num-processors: '4'
    memory-mb: '8192'
    mpi-type: 'openmpi'
```

#### Using Full Image Reference

```yaml
- name: Launch MAPDL with custom image
  uses: ./.github/actions/launch-mapdl-docker
  with:
    mapdl-image: 'ghcr.io/ansys/mapdl:v25.1-centos'
    license-server: ${{ secrets.LICENSE_SERVER }}
```

#### Multiple Instances

```yaml
- name: Instance 0
  uses: ./.github/actions/launch-mapdl-docker
  with:
    instance-name: 'MAPDL_0'
    mapdl-version: '25.2'
    license-server: ${{ secrets.LICENSE_SERVER }}
    pymapdl-port: '21000'

- name: Instance 1
  uses: ./.github/actions/launch-mapdl-docker
  with:
    instance-name: 'MAPDL_1'
    mapdl-version: '25.2'
    license-server: ${{ secrets.LICENSE_SERVER }}
    pymapdl-port: '21001'
```

#### Using Outputs

```yaml
- id: mapdl
  uses: ./.github/actions/launch-mapdl-docker
  with:
    mapdl-version: '25.2'
    license-server: ${{ secrets.LICENSE_SERVER }}

- name: Use outputs
  run: |
    echo "Container: ${{ steps.mapdl.outputs.container-id }}"
    echo "Port: ${{ steps.mapdl.outputs.pymapdl-port }}"
    docker logs ${{ steps.mapdl.outputs.container-name }}
```


## API Reference

### Required Inputs

| Input           | Description                                        | Example                      |
|-----------------|------------------------------------------------|---------------------------:|
| `license-server` | License server address (port@host)              | `1055@license.example.com` |

### Input Options (Choose One)

Provide **exactly one** of the following:

| Input           | Description                                    | Example                      |
|-----------------|------------------------------------------------|---------------------------:|
| `mapdl-version` | MAPDL version number (simpler, recommended)    | `25.2`, `25.1`, `24.2`     |
| `mapdl-image`   | Full Docker image reference (for custom tags)  | `ghcr.io/ansys/mapdl:v25.2-ubuntu` |

**Important:** Providing both or neither will cause an error. The action will fail with a clear message if this requirement isn't met.

#### `mapdl-version` Details

- Format: `25.2`, `25.1`, `24.2` (version number only, no prefix or tag)
- Automatically expands to: `ghcr.io/ansys/mapdl:v{version}-ubuntu-cicd`
- Use this for most cases—it's simpler and defaults to the recommended ubuntu-cicd variant
- Cannot be used together with `mapdl-image`

#### `mapdl-image` Details

- Format: `ghcr.io/ansys/mapdl:v25.2-ubuntu-cicd` (full image reference with tag)
- Use this only when you need a non-default variant (e.g., CentOS, specific tag, different registry)
- Cannot be used together with `mapdl-version`

### Optional Inputs

| Input                  | Default             | Description                                |
|------------------------|---------------------|--------------------------------------------|
| `instance-name`        | `MAPDL_0`           | Container name                             |
| `pymapdl-port`         | `50052`             | PyMAPDL gRPC port                          |
| `pymapdl-db-port`      | `50055`             | PyMAPDL database port                      |
| `dpf-port`             | `50056`             | DPF service port                           |
| `enable-dpf-server`    | `false`             | Start DPF server (`true`/`false`)          |
| `distributed-mode`     | `smp`               | Execution mode (`smp` or `dmp`)            |
| `num-processors`       | `2`                 | Number of processors                       |
| `mpi-type`             | `auto`              | MPI type (`auto`, `openmpi`, `intelmpi`)   |
| `memory-mb`            | `6656`              | Container memory limit (MB)                |
| `memory-swap-mb`       | `16896`             | Container swap limit (MB)                  |
| `memory-db-mb`         | `6000`              | MAPDL database memory (MB)                 |
| `memory-workspace-mb`  | `6000`              | MAPDL workspace memory (MB)                |
| `transport`            | `insecure`          | gRPC transport mode                        |
| `student-version`      | `auto`              | Student version flag (`auto`, `true`, `false`) |
| `timeout`              | `60`                | Startup timeout (seconds)                  |

### Outputs

| Output                 | Description              | Example        |
|------------------------|--------------------------|----------------|
| `container-id`         | Docker container ID      | `a1b2c3d4e5f6` |
| `container-name`       | Container name           | `MAPDL_0`      |
| `pymapdl-port`         | PyMAPDL port used        | `50052`        |
| `dpf-port`             | DPF port used            | `50056`        |
| `pymapdl-db-port`      | Database port used       | `50055`        |
| `mapdl-version-number` | Numeric version          | `252`          |
| `log-file`             | Launch log file path     | `/tmp/mapdl_launch.log` |

## Automatic Detection

The action intelligently configures itself based on the `mapdl-version` string:

| Version Pattern    | Detection       | Configuration                                   |
|--------------------|-----------------|------------------------------------------------|
| Contains `ubuntu`  | Ubuntu image    | Uses `/ansys_inc/v{VERSION}/ansys/bin/mapdl`   |
| Contains `latest-ubuntu` | Latest Ubuntu | Uses simplified `ansys` command            |
| Contains `cicd`    | CI/CD image     | Forces DMP, enables DPF port binding           |
| Contains `student` | Student version | Auto-detects student mode                      |
| Other              | CentOS/Rocky    | Uses `/ansys_inc/ansys/bin/mapdl`              |

**MPI Auto-Selection:**

- CICD versions → OpenMPI
- Other versions → Based on `mpi-type` input

## Usage from Other Repositories

### By Branch

```yaml
- uses: ansys/pymapdl/.github/actions/launch-mapdl-docker@main
  with:
    mapdl-version: '25.2'
    license-server: ${{ secrets.LICENSE_SERVER }}
```

### By Tag/Version

```yaml
- uses: ansys/pymapdl/.github/actions/launch-mapdl-docker@v0.69.0
  with:
    mapdl-version: '25.2'
    license-server: ${{ secrets.LICENSE_SERVER }}
```

### Copy to Your Repository

Simply copy the entire `.github/actions/launch-mapdl-docker/` directory to your repository.

## Migration from Shell Scripts

**Old approach** (using `.ci/start_mapdl.sh`):

```yaml
- name: Launch MAPDL
  env:
    LICENSE_SERVER: ${{ secrets.license-server }}
    MAPDL_VERSION: v25.2-ubuntu-cicd
    DISTRIBUTED_MODE: dmp
    INSTANCE_NAME: MAPDL_0
    PYMAPDL_PORT: 50052
  run: .ci/start_mapdl.sh

- name: Wait for services
  env:
    PYMAPDL_PORT: 50052
  run: .ci/waiting_services.sh
```

**New approach** (using this action):

```yaml
- name: Launch MAPDL
  uses: ./.github/actions/launch-mapdl-docker
  with:
    mapdl-version: '25.2'
    instance-name: 'MAPDL_0'
    license-server: ${{ secrets.license-server }}
    distributed-mode: 'dmp'
    pymapdl-port: '50052'
```

**Benefits:**

- ✅ Service waiting is built-in
- ✅ Type-safe inputs with validation
- ✅ Structured outputs for downstream steps
- ✅ Better error messages
- ✅ Centralized maintenance
- ✅ Automatic cleanup

### Environment Variable Mapping

| Old Variable       | New Input             |
|--------------------|-----------------------|
| `MAPDL_VERSION`    | `mapdl-version`       |
| `MAPDL_PACKAGE`    | `mapdl-image`         |
| `INSTANCE_NAME`    | `instance-name`       |
| `LICENSE_SERVER`   | `license-server`      |
| `PYMAPDL_PORT`     | `pymapdl-port`        |
| `PYMAPDL_DB_PORT`  | `pymapdl-db-port`     |
| `DPF_PORT`         | `dpf-port`            |
| `RUN_DPF_SERVER`   | `enable-dpf-server`   |
| `DISTRIBUTED_MODE` | `distributed-mode`    |

## Requirements

- Docker installed and running
- **Docker registry authentication** (use `docker/login-action` before this action)
- Valid ANSYS license server
- `netcat` (`nc`) utility (pre-installed on GitHub runners)

**Important:** Always authenticate to the Docker registry first:

```yaml
- name: Login to GitHub Container Registry
  uses: docker/login-action@v3
  with:
    registry: ghcr.io
    username: ${{ github.actor }}
    password: ${{ secrets.GITHUB_TOKEN }}
```

## Troubleshooting

### Container Fails to Start

Check logs:
```yaml
- name: Launch MAPDL
  id: mapdl
  uses: ./.github/actions/launch-mapdl-docker
  with:
    mapdl-version: '25.2'
    license-server: ${{ secrets.LICENSE_SERVER }}

- name: Debug on failure
  if: failure()
  run: |
    cat ${{ steps.mapdl.outputs.log-file }}
    docker logs ${{ steps.mapdl.outputs.container-name }}
```

### Port Conflicts

Use unique ports for each instance:
```yaml
pymapdl-port: '21000'  # Not 50052
dpf-port: '21014'       # Not 50056
```

### Memory Issues

Increase limits:
```yaml
memory-mb: '8192'
memory-workspace-mb: '8000'
memory-db-mb: '8000'
```

### License Server Format

Correct format: `port@hostname`
```yaml
license-server: '1055@license.example.com'  # ✅ Correct
license-server: 'license.example.com:1055'  # ❌ Wrong
```

### Service Not Ready

The action waits up to 60 seconds by default. Increase if needed:
```yaml
timeout: '120'  # 2 minutes
```

### DPF Not Starting

Ensure you're using a CICD version:
```yaml
mapdl-version: 'v25.2-ubuntu-cicd'  # ✅ Has DPF
mapdl-version: 'v25.2-ubuntu'       # ❌ No DPF
enable-dpf-server: 'true'
```

## Cleanup

**Automatic cleanup is built-in!** Containers are stopped and removed when the workflow completes.

For manual cleanup before job ends (optional):
```yaml
- name: Manual cleanup
  run: |
    docker stop ${{ steps.mapdl.outputs.container-name }}
    docker rm ${{ steps.mapdl.outputs.container-name }}
```

## Complete Example

```yaml
name: Test with MAPDL

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Login to registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Launch MAPDL
        id: mapdl
        uses: ./.github/actions/launch-mapdl-docker
        with:
          mapdl-version: '25.2'
          license-server: ${{ secrets.LICENSE_SERVER }}
          enable-dpf-server: 'true'
          distributed-mode: 'dmp'
          num-processors: '4'
          memory-mb: '8192'

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -e .
          pip install pytest

      - name: Run tests
        env:
          PYMAPDL_PORT: ${{ steps.mapdl.outputs.pymapdl-port }}
          PYMAPDL_START_INSTANCE: false
        run: pytest tests/

      - name: Show logs on failure
        if: failure()
        run: |
          docker logs ${{ steps.mapdl.outputs.container-name }}
          cat ${{ steps.mapdl.outputs.log-file }}
```

## Development

### Building the Action

This GitHub Action uses bundled JavaScript files to reduce dependencies and improve execution speed. The action requires building after any changes to the main source files.

#### Prerequisites

- Node.js 20 or later
- npm (comes with Node.js)

#### Source Files

- **`index.js`** - Main entry point for the action (runs during workflow step)
- **`post.js`** - Post-action entry point for cleanup (runs after workflow completes)
- **`package.json`** - Dependencies and build configuration
- **`action.yml`** - Action metadata and input/output definitions

#### Build Process

The action uses `@vercel/ncc` (Node.js Compiler Collection) to bundle all JavaScript code, dependencies, and assets into single executable files.

**To build:**

```bash
cd .github/actions/launch-mapdl-docker
npm install          # Install dependencies (only needed once)
npm run build        # Compile source files into dist/ directories
```

**Output:**

- `dist/index.js` - Bundled main action code
- `dist-post/index.js` - Bundled post-action cleanup code
- `.gitignore` - Should include `dist/`, `dist-post/`, and `node_modules/`

#### After Making Changes

Any modifications to source files require rebuilding:

```bash
npm run build
```

Then commit the new `dist/` and `dist-post/` directories along with your source changes:

```bash
git add index.js post.js package.json action.yml
git add dist/ dist-post/
git commit -m "feat: update action logic"
```

#### CI/CD Integration

The `prepare` script in `package.json` runs automatically when installing npm packages:

```bash
npm install  # This automatically runs 'npm run build'
```

This ensures the distribution files are always up-to-date when dependencies change.

## Related Documentation

- **Example workflows**: `.github/workflows/example-launch-mapdl-action.yml`
- **Updated test workflow**: `.github/workflows/test-remote-with-action.yml`
- **Original scripts** (for reference): `.ci/start_mapdl.sh`, `.ci/entrypoint.sh`

## Support

- **Documentation**: [PyMAPDL Docs](https://mapdl.docs.pyansys.com/)
- **Issues**: [GitHub Issues](https://github.com/ansys/pymapdl/issues)
- **License**: See repository root
