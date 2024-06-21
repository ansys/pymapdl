from ansys.mapdl.core.mapdl import MapdlBase
from typing import Optional, Protocol

class _Backend(Protocol):
    def run_command(self) -> str: ...

class MapdlInProcess(MapdlBase):
    def __init__(self, backend: _Backend):
        super().__init__(
            loglevel="WARNING",
            use_vtk=False,
            log_apdl=None,
            print_com=False
        )
        self._backend = backend
        self._cleanup: bool = True
        self._name: str = "MapdlInProcess"
        self._session_id: Optional[str] = None
        self._mute: bool = False

    def _run(self, command: str, verbose: bool=False, mute: bool=False) -> str:
        if not command.strip():
            raise ValueError("Empty commands not allowed")

        if len(command) > 639:
            raise ValueError("Maximum command length mut be less than 640 characters")

        return self._backend.run_command(command, verbose, mute).strip()

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name) -> None:
        self._name = name

    def _check_session_id() -> None:
        pass

    def __repr__(self):
        info = super().__repr__()
        return info
