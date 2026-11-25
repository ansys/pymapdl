# Download examples through `ansys-tools-common` into PyMAPDL's persistent cache

`examples/downloads.py` delegates the actual download, with retries and caching, to the shared `ansys-tools-common` example downloader (`download_manager.download_file`). It passes `destination=pymapdl.EXAMPLES_PATH`, PyMAPDL's own persistent cache directory, instead of the library's default temporary directory. Before downloading, it returns an already present (and decompressed) file from `EXAMPLES_PATH` to avoid hitting the network again.

## Consequences

- Downloaded examples survive between sessions.
- Retry and download logic is maintained in `ansys-tools-common`, not PyMAPDL.
