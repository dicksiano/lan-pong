"""Class that handle server connections"""
import socket
import json
from threading import Thread
from .engine import Engine

UDP_PORT = 13702
TCP_PORT = 13703

class Server:
  """Class that handle server connections"""
  def __init__(self, **kwargs):
    ip_addr = kwargs.get('ip', '')

    self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    udp_src = ('', UDP_PORT)
    self.udp.bind(udp_src)

    tcp_src = (ip_addr, TCP_PORT)
    self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.tcp.bind(tcp_src)
    self.tcp.listen()

    self.bc_response = self.gen_bc_response()
    self.num_conn = 0
    self.engine = Engine()

  def gen_bc_response(self):
    """Return model to broadcast response"""
    return {
        'tcp_addr': self.tcp.getsockname()
    }

  def respond_bc(self):
    """Responds udp broadcast"""
    while True:
      data, addr = self.udp.recvfrom(1024)
      print("received", data, "from", addr)
      self.udp.sendto(json.dumps(self.bc_response).encode(), addr)
      if self.num_conn == 2:
        break

  def tcp_conn(self):
    """Waits TCPs connection"""
    conn, client = self.tcp.accept()
    print(conn, client)
    self.num_conn += 1
    while True:
      msg = conn.recv(1024).decode()
      if not msg:
        break
      print(client, msg)
    print('CABOU')

  def wait_conn(self):
    """Wait connections from two players"""
    udp_conn = Thread(target=self.respond_bc)
    udp_conn.start()
    tcp_conn1 = Thread(target=self.tcp_conn)
    tcp_conn1.start()
    tcp_conn2 = Thread(target=self.tcp_conn)
    tcp_conn2.start()
