"""Class that handle client connections"""
import socket
import json
import select
from random import randint
from threading import Thread, Event

import sys
sys.path.append('../')
import constants

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

    self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    self.available_servers = []

    self.timeout_handle = Event()

  def wait_servers_response(self):
    """Function that handles servers response to broadcast"""
    while True:
      readable, _, _ = select.select([self.udp], [], [], 1)
      if readable:
        data, _ = self.udp.recvfrom(1024)
        self.available_servers.append(json.loads(data.decode()))
      if self.timeout_handle.is_set():
        print("ENCERRANDO ROLE")
        break

  def tcp_connect(self, addr):
    """Connect to TCP addr"""
    self.tcp.connect(addr)
    msg = input()
    while msg != 'exit':
      self.tcp.send(msg.encode())
      msg = input()
    self.tcp.close()

  def search_servers(self):
    """Send udp broadcast to search for servers"""
    self.available_servers = []
    self.udp.sendto(b"MANDANDO BROADCAST", ('<broadcast>', UDP_PORT))
    wait_response = Thread(target=self.wait_servers_response)
    wait_response.start()
    wait_response.join(timeout=1)
    self.timeout_handle.set()
    print("received", self.available_servers)


def draw(canvas, ball_pos, paddle1_pos, paddle2_pos):
  canvas.fill(BLACK)
  pygame.draw.line(canvas, WHITE, [WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1)
  pygame.draw.line(canvas, WHITE, [PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1)
  pygame.draw.line(canvas, WHITE, [WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1)
  pygame.draw.circle(canvas, WHITE, [WIDTH//2, HEIGHT//2], 70, 1)

  # Paddles and Ball
  pygame.draw.circle(canvas, RED, ball_pos, 20, 0)
  pygame.draw.polygon(canvas, GREEN, [[paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT], [paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT], [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT], [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT]], 0)
  pygame.draw.polygon(canvas, GREEN, [[paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT], [paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT], [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT], [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT]], 0)