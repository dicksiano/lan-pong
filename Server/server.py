"""Class that handle server connections"""
import socket

UDP_PORT = 13702
TCP_PORT = 13703

class Server:
  """Class that handle server connections"""
  def __init__(self, **kwargs):
    ip_addr = kwargs.get('ip', '')

    self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    udp_src = (ip_addr, UDP_PORT)
    self.udp.bind(udp_src)

    tcp_src = (ip_addr, TCP_PORT)
    self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.tcp.bind(tcp_src)

  def wait_broad(self):
    """Wait broadcast"""
    while True:
      data, addr = self.udp.recvfrom(1024)
      print("received", data)
      self.udp.sendto(b"RESPONDENDO BROADCAST", addr)
