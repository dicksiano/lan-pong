"""Class that handle client connections"""
import socket
import json
import select
from random import randint
from threading import Thread, Event

import sys
from .constants import *

UDP_PORT = 13702
TCP_PORT = 13703

class Client:
  """Class that handle client connections"""
  def __init__(self):
    # ip_addr = kwargs.get('ip', '')

    self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    self.udp.setblocking(0)
    udp_src = ('', randint(10000, 20000))
    self.udp.bind(udp_src)
    # self.udp.setblocking(False)

    self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # self.tcp.setblocking(False)

    self.available_servers = []

    self.updated_state = False
    self.timeout_handle = Event()

  def wait_servers_response(self):
    """Function that handles servers response to broadcast"""
    while True:
      readable, _, _ = select.select([self.udp], [], [], 1)
      if readable:
        data, _ = self.udp.recvfrom(1024)
        self.available_servers.append(json.loads(data.decode()))
      else:
        print("Client: Servers Responses received", self.available_servers)
        break
    self.updated_state = True

  def tcp_connect(self, addr):
    """Connect to TCP addr"""
    self.tcp.connect(addr)
    print("Client: Conectado com servidor", addr)
    # msg = input()
    # while msg != 'exit':
    #   self.tcp.send(msg.encode())
    #   msg = input()
    # self.tcp.close()

  def search_servers(self):
    """Send udp broadcast to search for servers"""
    self.available_servers = []
    self.udp.sendto(b"Client: Searching servers", ('<broadcast>', UDP_PORT))
    wait_response = Thread(target=self.wait_servers_response)
    wait_response.start()
    # wait_response.join(timeout=1)
    # self.timeout_handle.set()
