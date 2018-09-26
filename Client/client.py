"""Class that handle client connections"""
import socket
import json
import select
from random import randint
from threading import Thread

UDP_PORT = 13702
TCP_PORT = 13703

class Client:
  """Class that handle client connections"""
  def __init__(self):
    self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    self.udp.setblocking(0)
    udp_src = ('', randint(10000, 20000))
    self.udp.bind(udp_src)

    self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    self.inputs = []
    self.outputs = []
    self.msg_queue = []

    self.available_servers = []
    self.connected = False
    self.updated_state = False
    self.game_state = [[0, 0], [0, 0], [0, 0], 0, 0]

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
    self.inputs.append(self.tcp)
    self.outputs.append(self.tcp)
    self.tcp.setblocking(False)
    self.connected = True
    print("Client: Conectado com servidor", addr)

  def handle_msg_errors(self, msg):
    """Handle msg errors, when two messages are received \
    from server and read like one: [[3, 140], [797, 300],\
    [215, 299], 0, 0][[3, 140], [797, 300], [216, 300], 0, 0] -> \
    [[3, 140], [797, 300], [216, 300], 0, 0]"""
    idx = len(msg) - 1
    open_bracket_count = 0
    while idx >= 0:
      if msg[idx] == '[':
        open_bracket_count += 1
        if open_bracket_count == 4:
          return msg[idx:]
      idx -= 1
    return msg

  def handle_tcp(self, msg):
    """Handles tcp connection"""
    self.msg_queue.append(msg)
    readable, writable, exceptional = select.select(\
    self.inputs, self.outputs, self.inputs, 0.5)
    for s in readable:
      data, _ = s.recvfrom(1024)
      if data:
        print("Client tcp:", data)
        msg_filtered = self.handle_msg_errors(data.decode())
        self.game_state = json.loads(msg_filtered)

    for s in writable:
      if self.msg_queue:
        next_msg = json.dumps(self.msg_queue.pop(0)).encode()
        s.sendall(next_msg)

    for s in exceptional:
      self.inputs.remove(s)
      if s in self.outputs:
        self.outputs.remove(s)
      s.close()
      del self.msg_queue[s]


  def search_servers(self):
    """Send udp broadcast to search for servers"""
    self.available_servers = []
    self.udp.sendto(b"Client: Searching servers", ('<broadcast>', UDP_PORT))
    wait_response = Thread(target=self.wait_servers_response)
    wait_response.start()
