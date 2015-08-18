# -*- mode: python -*-
a = Analysis(['M2Spice.py'],
             pathex=['C:\Users\Minjie\Dropbox (Personal)\Research\M2Spice\Python'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)

for d in a.datas:
    if 'pyconfig' in d[0]: 
        a.datas.remove(d)
        break
		
import platform
if platform.system().find("Windows")>= 0:
    a.datas = [i for i in a.datas if i[0].find('Include') < 0]
	
a.datas = list({tuple(map(str.upper, t)) for t in a.datas})

a.datas += [('multiwinding.gif', 'C:\\Users\\Minjie\\Dropbox (Personal)\\Research\\M2Spice\\Python\\multiwinding.gif','DATA'),('icon.ico','C:\\Users\\Minjie\\Dropbox (Personal)\\Research\\M2Spice\\Python\\icon.ico','DATA')]

import ctypes
myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('M2Spice-win.exe'),
          debug=False,
          strip=None,
		  icon='icon.ico',
          upx=True,
          console=False )
app = BUNDLE(exe,
             name='M2Spice-osx.app',
             icon='icon.ico')
