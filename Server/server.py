"""Class that handle server connections"""
import socket
import json
import select
from threading import Thread
from .engine import Engine

UDP_PORT = 13702
TCP_PORT = 13703

class Server:
  """Class that handle server connections"""
  def __init__(self, **kwargs):
    ip_addr = kwargs.get('ip', '')
    self.quit = False

    self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    udp_src = ('', UDP_PORT)
    self.udp.bind(udp_src)
    self.udp.setblocking(False)

    tcp_src = (ip_addr, TCP_PORT)
    self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.tcp.bind(tcp_src)
    self.tcp.setblocking(False)
    self.tcp.listen()

    self.bc_response = self.gen_bc_response()
    self.num_conn = 0
    self.in_game = False

    self.inputs = [self.udp, self.tcp]
    self.outputs = []
    self.msg_queue = {}
    self.cli_num = {}

    self.engine = Engine()

  def gen_bc_response(self):
    """Return model to broadcast response"""
    return {
        'tcp_addr': self.tcp.getsockname()
    }

  def respond_bc(self):
    """Responds udp broadcast"""
    if not self.in_game or self.num_conn < 2:
      data, addr = self.udp.recvfrom(1024)
      print("Server: received", data, "from", addr)
      self.udp.sendto(json.dumps(self.bc_response).encode(), addr)

  def tcp_conn(self):
    """Waits TCPs connection"""
    if self.num_conn >= 2:
      return
    conn, client = self.tcp.accept()
    print("Server: conectado", conn, client)
    self.inputs.append(conn)
    self.msg_queue[conn] = []
    self.cli_num[conn] = self.num_conn
    self.num_conn += 1

  def process_events(self, data, conn):
    """Process received events from client to engine"""
    player_num = self.cli_num[conn]
    for event in data:
      if event[0] == "KEYUP":
        self.engine.keyup(player_num)
      elif event[0] == "KEYDOWN":
        self.engine.keydown(event[1], player_num)

  def filter_data(self, data):
    """Filter repeated data at server receiving"""
    result = []
    string = ''
    num_op_brack = 0
    for char in data:
      if char == '[':
        num_op_brack += 1
      elif char == ']':
        num_op_brack -= 1
      string += char
      if num_op_brack == 0:
        result.append(json.loads(string))
        string = ''
    return result

  def running_server(self):
    """Used to run server thread"""
    while True:
      readable, writable, exceptional = select.select(\
      self.inputs, self.outputs, self.inputs, 0.5)
      for s in readable:
        if s is self.udp:
          self.respond_bc()
        elif s is self.tcp:
          self.tcp_conn()
        else:
          data, _ = s.recvfrom(1024)
          # print("Server: tcp received", data)
          if data:
            self.filter_data(data.decode())
            data = json.loads(data.decode())
            self.process_events(data, s)
            self.engine.update()
            # Process received data
            self.msg_queue[s].append(self.engine.get_state())
            if s not in self.outputs:
              self.outputs.append(s)

      for s in writable:
        if self.msg_queue[s]:
          next_msg = json.dumps(self.msg_queue[s].pop(0)).encode()
          s.sendall(next_msg)

      for s in exceptional:
        print("Exceptional")
        self.inputs.remove(s)
        if s in self.outputs:
          self.outputs.remove(s)
        s.close()
        del self.msg_queue[s]

      if self.quit:
        print("Server: end")
        break

  def wait_conn(self):
    """Wait connections from two players"""
    server = Thread(target=self.running_server)
    server.start()
