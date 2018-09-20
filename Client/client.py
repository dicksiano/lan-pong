"""Class that handle client connections"""
import socket
from threading import Thread, Event
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

    self.available_servers = []

    self.timeout_handle = Event()

  def wait_servers_response(self):
    while True:
      data, _ = self.udp.recvfrom(1024)
      print("received", data)

      if self.timeout_handle.is_set():
        break

  def search_servers(self):
    """Send udp broadcast to search for servers"""
    self.udp.sendto(b"MANDANDO BROADCAST", ('<broadcast>', UDP_PORT))
    wait_response = Thread(target=self.wait_servers_response)
    wait_response.start()
    wait_response.join(timeout=1)
    self.timeout_handle.set()
