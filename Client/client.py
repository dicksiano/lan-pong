"""Class that handle client connections"""
import socket

UDP_PORT = 13702
TCP_PORT = 13703

class Client:
  """Class that handle client connections"""
  def __init__(self, **kwargs):
    ip_addr = kwargs.get('ip', '')

    self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    udp_src = (ip_addr, 10001)
    self.udp.bind(udp_src)

    tcp_src = (ip_addr, 10002)
    self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.tcp.bind(tcp_src)

  def search_servers(self):
    """Send udp broadcast to search for servers"""
    self.udp.sendto(b"MANDANDO BROADCAST", ('<broadcast>', UDP_PORT))
