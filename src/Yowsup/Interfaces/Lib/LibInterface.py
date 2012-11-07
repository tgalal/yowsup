import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)


from Interface import SignalInterfaceBase, MethodInterfaceBase

class LibSignalInterface(SignalInterfaceBase):
	def __init__(self):
		super(LibSignalInterface,self).__init__();
		
class LibMethodInterface(MethodInterfaceBase):
	def __init__(self):
		super(LibMethodInterface,self).__init__();

