# PyInstaller build spec for LensAnywhere.
#
# Deliberately built as a one-folder (--onedir) app with UPX compression
# disabled (--noupx). --onefile + UPX packs the interpreter and all
# dependencies into a single, high-entropy, self-extracting binary, which is
# a strong heuristic signature for antivirus/SmartScreen engines and drives
# false-positive detections. A plain folder with the DLLs laid out flat is
# far less suspicious to static analysis, at the cost of a slightly less
# "single file" distribution (ship the whole output folder / a zip of it).
#
# Build with:
#   pyinstaller LensAnywhere.spec
#
# Note: even with these flags, unsigned Windows binaries will still trigger
# SmartScreen reputation warnings. The most effective additional steps are
# (1) signing the executable with a code-signing certificate, and
# (2) submitting the built binary to https://www.microsoft.com/en-us/wdsi/filesubmission
# so Defender/SmartScreen can build reputation for it. Both are manual,
# account/cost-bound steps that can't be scripted here.

# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

datas = [
    ("logo.png", "."),
    ("rect.svg", "."),
    ("cancel.svg", "."),
    ("settings.svg", "."),
]

a = Analysis(
    ["main3.py"],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="LensAnywhere",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # never UPX-pack the bootloader/exe
    console=False,
    icon="logo.png",
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,  # never UPX-pack the collected DLLs/pyds either
    upx_exclude=[],
    name="LensAnywhere",
)
