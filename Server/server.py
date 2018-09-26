"""Class that handle server connections"""
import socket
import json
import select
import logging
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

    self.engine = Engine()

  def gen_bc_response(self):
    """Return model to broadcast response"""
    return {
        'tcp_addr': self.tcp.getsockname()
    }

  def respond_bc(self):
    """Responds udp broadcast"""
    # while True:
    #   readable, _, _ = select.select([self.udp], [], [], 1)
    #   if readable:
    #     data, addr = self.udp.recvfrom(1024)
    #     print("Server: received", data, "from", addr)
    #     self.udp.sendto(json.dumps(self.bc_response).encode(), addr)
    #   if self.num_conn >= 2:
    #     print("Server: Fechando receptor Broadcast")
    #     break
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
    self.num_conn += 1
    # while True:
    #   msg = conn.recv(1024).decode()
    #   if not msg:
    #     break
    #   print(client, msg)
    # print('CABOU')

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
          data, addr = s.recvfrom(1024)
          print("Server: tcp received", data)
          if data:
            # data = json.loads(data)
            # Process received data
            self.msg_queue[s].append(self.engine.get_state())
            if s not in self.outputs:
              self.outputs.append(s)
          # else:
          #   if s in self.outputs:
          #     self.outputs.remove(s)
          #   self.inputs.remove(s)
          #   s.close()
          #   del self.msg_queue[s]

      for s in writable:
        if self.msg_queue[s]:
          next_msg = json.dumps(self.msg_queue[s].pop(0)).encode()
          s.sendall(next_msg)

      # for s in exceptional:
      #   print("Exceptional")
      #   self.inputs.remove(s)
      #   if s in self.outputs:
      #     self.outputs.remove(s)
      #   s.close()
      #   del self.msg_queue[s]

      if self.quit:
        print("Server: end")
        break

  def wait_conn(self):
    """Wait connections from two players"""
    server = Thread(target=self.running_server)
    server.start()
    # udp_conn = Thread(target=self.respond_bc)
    # udp_conn.start()
    # tcp_conn1 = Thread(target=self.tcp_conn)
    # tcp_conn1.start()
    # tcp_conn2 = Thread(target=self.tcp_conn)
    # tcp_conn2.start()
