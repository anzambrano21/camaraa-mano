import sys

if sys.platform.startswith('win'):
    print("Es Windows")
elif sys.platform.startswith('linux'):
    print("Es Linux")
    
elif sys.platform.startswith('darwin'):
    print("Es macOS")