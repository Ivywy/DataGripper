# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['DataGripper.py', 'second_page.py'],
    pathex=['C:\\Users\\yanwen12\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages\\PyQt5\\Qt5\\bin\\', 'C:\\Users\\yanwen12\\python\\DataGripper\\'],
    binaries=[],
    datas=[('C:\\Users\\yanwen12\\python\\DataGripper\\gripper.ui', '.')],
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='DataGripper',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='amd.ico',
)
