# -*- mode: python ; coding: utf-8 -*-

import os
import importlib

root = os.path.dirname(importlib.import_module("ansys.api.mapdl").__file__)
# The ``files_to_add`` list contains tuples that define the mapping between the original file paths and their corresponding paths within the executable folder.
# Note: If you have chosen the ``onefile`` mode, the files in ``files_to_add`` are integrated into the executable file.
files_to_add = [
    (os.path.join(root, "VERSION"), os.path.join(".", "ansys", "api", "mapdl"))
]

block_cipher = None


a = Analysis(
    ['cli_rotor.py'],
    pathex=[],
    binaries=[],
    datas=files_to_add,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='cli_rotor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='cli_rotor',
)
