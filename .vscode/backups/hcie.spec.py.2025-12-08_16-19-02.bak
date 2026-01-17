# -*- mode: python ; coding: utf-8 -*-

import os
import sys

block_cipher = None

# Qt plugin yolunu kontrol et
try:
    import PySide6
    qt_plugin_path = os.path.join(os.path.dirname(PySide6.__file__), "plugins")
    print(f"Qt plugin path found: {qt_plugin_path}")
    
    # Platformlar dizinini kontrol et
    platforms_path = os.path.join(qt_plugin_path, "platforms")
    if os.path.exists(platforms_path):
        print(f"Platforms directory exists: {platforms_path}")
    else:
        print(f"Warning: Platforms directory not found at: {platforms_path}")
        # Alternatif yol
        qt_plugin_path = os.path.join(sys.prefix, "lib", "python3.12", "site-packages", "PySide6", "plugins")
        print(f"Trying alternative path: {qt_plugin_path}")
        
except ImportError:
    print("PySide6 not found, using default paths")
    qt_plugin_path = ""

a = Analysis(
    ['main.py'],
    pathex=['/home/mint/Desktop/ie_qt'],
    binaries=[],
    datas=[
        ('resources', 'resources'),
        # Qt plugin'lerini ekle (eğer varsa)
        # (qt_plugin_path, 'PySide6/plugins'),
    ],
    hiddenimports=[
        'PySide6',
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtWidgets',
        'shiboken6',
    ],
    hookspath=[],
    hooksconfig={
        'PySide6': {
            'QtNetwork': False
        }
    },
    runtime_hooks=[],
    excludes=['PySide6.QtNetwork'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Qt plugin'leri manuel olarak ekle (eğer varsa)
if os.path.exists(qt_plugin_path):
    for item in os.listdir(qt_plugin_path):
        plugin_dir = os.path.join(qt_plugin_path, item)
        if os.path.isdir(plugin_dir):
            a.datas.append((plugin_dir, f'PySide6/plugins/{item}'))
            print(f"Added plugin directory: {plugin_dir} -> PySide6/plugins/{item}")

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='hcie2.9.2-alpha-mint-test',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
 # ONE FILE için bu satırları ekleyin:
    onefile=True,  # Bu en önemlisi!
    icon='icon.ico',  # İkon dosyası yolu (varsa
)
