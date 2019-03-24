#!/usr/bin/python

import os, sys
import re
import pexpect
import subprocess
import tempfile
import time

SSHError = [" ",\
            "ok",\
            "SSH connection exited: ",\
            "SSH connection to timed out: ",\
            "No results return on executing", \
            "Failed to access as admin"]
myhost = "10.205.47.1"
myJumpHostUser = "userrw"
myJumpHostPwd = "Pass@1234"
command = "header login info ^ "
text = "______________ FOR STARHUB AUTHORIZED USERS ONLY __________________ \r If you are not authorized to access this equipment of network \r please disconnect immediately. \r\r Please note that StarHub takes a serious view of any unauthorized \r or illegal access, and violators will be subject to prosecution. \r\r Please be informed that all login attempts will be logged. \r-------------------------------------------------------------------"


def connectPERouter(myhost, myJumpHostUser, myJumpHostPwd):
    #ssh_newkey = 'Are you sure you want to continue connecting (yes/no)?'
    #ssh_cmd = "ssh " + myJumpHostUser + "@" + myhost
    telnet_cmd = "telnet " + myhost
    child = pexpect.spawn(telnet_cmd)
    i = child.expect(['sername:',pexpect.EOF,pexpect.TIMEOUT])
   
    if i == 0:
      #Start of Debug print
      #print 'Debug: Prompt(yes/no)
      #End of Debug print
      child.sendline(myJumpHostUser)
      i=child.expect(['assword:',pexpect.EOF,pexpect.TIMEOUT])
      
      if i == 0:
              child.sendline(myJumpHostPwd)      
              child.expect_exact("[Y/N]:")             
              child.sendline('n')              
              child.expect(">")
      #Start of Debug print
      #print 'Connected and Page Off!'
      #End of Debug print
              return (0, child, "connected")
      elif i == 1:
              return (1, child, "Failed")
      elif i == 2:
              return (2, child, "Timed out")

def disconnectPERouter(ssh):

    """Disconnect connection"""
    ssh.close()


'''def exeCmdnotAdmin(ssh, mycmd, PROMPT):
    """Execute the command NOT as the admin and take the second arg as an indicator"""
    /try:
        ssh.sendline("term len 0")
        ssh.expect(PROMPT)
        ssh.sendline(mycmd)
        ssh.expect(PROMPT)
        return 1, ssh.before.split("\n")
    except Exception:
        return 4'''

def exeCmd(ssh, mycmd, text):
      
   # try:  
      ssh.sendline('system-view')
      ssh.expect_exact(']')
      ssh.sendline(mycmd)
      #ssh.expect(PROMPT, timeout=120)
      ssh.expect_exact(' ')
      ssh.sendline(text)
      ssh.expect_exact(' ')
      #ssh.sendline(text2)
      #ssh.expect_exact(' ')
      ssh.sendline('^')
      ssh.expect_exact(']')
      ssh.sendline('commit')
      return 1, ssh.before.split("\n") 
   # except Exception:
   #   return 4

def main():

   # myJumpHostUser = input("Enter Username: ")
   # myJumpHostPwd = input("Enter Password: ") 
   # myhost = input("Enter Device: ")
    connect_pctn = connectPERouter(myhost, myJumpHostUser, myJumpHostPwd)
    print('connected to: ' + myhost)
    show_comm = exeCmd(connect_pctn[1],command,text)
   # print(show_comm[1][0])
    print(show_comm)
    disconn = disconnectPERouter(connect_pctn[1])
    print('successfully disconnected')
if __name__ == '__main__':
    main()

