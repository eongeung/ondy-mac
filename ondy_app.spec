# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['ondy_app.py'],
    pathex=[],
    binaries=[],
    datas=[('ondyicon', 'ondyicon')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ondy_app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['ondy.icns'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ondy_app',
)
app = BUNDLE(
    coll,
    name='ondy_app.app',
    icon='ondy.icns',
    bundle_identifier=None,
)
