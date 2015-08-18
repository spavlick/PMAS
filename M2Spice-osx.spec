# -*- mode: python -*-
a = Analysis(['M2Spice.py'],
             pathex=['/Users/Minjie-MAC/Dropbox (Personal)/Research/PMAS/PMAS'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
a.datas += [('multiwinding.gif', '/Users/Minjie-MAC/Dropbox (Personal)/Research/M2Spice/Python/multiwinding.gif','DATA'),('icon.ico','/Users/Minjie-MAC/Dropbox (Personal)/Research/M2Spice/Python/icon.icns','DATA')]
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='M2Spice',
          debug=False,
          strip=None,
          upx=True,
          console=False )
app = BUNDLE(exe,
             name='M2Spice-osx.app',
             icon='icon.icns')
