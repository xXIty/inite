#!/usr/bin/python2

import socket
import time
from functions import Registre_IPs
from dnsQuery import DNSQuery
import signal
import os

IP_SERVIDOR='192.168.43.48'
IP_DNS='8.8.8.8'
DOMAINS = [ 'duniakato.org.',]

#db = Registre_IPs('u_dks', 'NTExMmZhMmU3', 'localhost', '5432', 'db_dks', 'portal_registre')
#p = None

def capture(req, domains, addr, loggedAddrs):
  return (addr[0] not in loggedAddrs) or (req in domains)


def handler(nombre, frame):
  db.actualitza()
  print("[*]\tIp list updated:\n"+", ".join(db.getIPs()))  
  

if __name__ == '__main__':
  global p
  global db
  
  db = Registre_IPs('u_dks', 'NTExMmZhMmU3', 'localhost', '5432', 'db_dks', 'portal_registre') 

  with open("/tmp/fakeDNS.pid","w") as pid_file:
    pid_file.write(str(os.getpid()))
  
  udps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  #udps.settimeout(5)
  try:
    udps.bind(('',53))
    print('[*]\tDns listening on port 53')
  except Exception as e:
    print('Error while port binding: ',e)
  signal.signal(signal.SIGUSR1, handler)
  print('[*]\tCapturing SIGUSR1...\n')


  try:
    while 1:
      try:
              data, addr = udps.recvfrom(1024)
              p=DNSQuery(data, IP_DNS ,IP_SERVIDOR)
              print('[***] Dns request from {}:\t{}'.format(addr[0],p.dominio))
              tocapture = capture(p.dominio, DOMAINS, addr, db.getIPs())
              response = p.respuesta(tocapture)
              chars = response[-4:]
              resolved = str(ord(chars[0])) + '.'
              resolved += str(ord(chars[1])) + '.'
              resolved += str(ord(chars[2])) + '.'
              resolved += str(ord(chars[3]))
              print('\t[*] Dns respone: {}\n'.format(resolved))
              udps.sendto(response, addr)
      except Exception as e:
                            print("Hi ha hagut un error %s" % e)
                            pass
      #print("surto del socket 1")
# #print 'Respuesta: %s -> %s' % (p.dominio, ip)
  except KeyboardInterrupt:
    #print ('Finalizando')
    udps.close()