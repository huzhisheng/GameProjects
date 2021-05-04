import socketserver
import socket
import threading
from time import sleep

from base import Protocol
server_ip = '127.0.0.1'
server_port = 7777

ADDRESS = (server_ip, server_port)  # 绑定地址


g_conn_pool = []  # 连接池


class Conn:
	def __init__(self, conn):
		self.conn = conn
		self.playerName=''
		self.x = None
		self.y = None
		self.charId=None
		self.mouseX=0
		self.mouseY=0
class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

	
	def setup(self):
		self.request.sendall("连接服务器成功!".encode(encoding='utf8'))
		# 加入连接池
		conn = Conn(self.request)
		g_conn_pool.append(conn)

	def handle(self):
		while True:
			try:
				# 读取数据包
				bytes = self.request.recv(1024)
				# 切割数据包
				while True:
					# 读取包长度
					length_pck = int.from_bytes(bytes[:4], byteorder='little')
					# 截取封包
					pck = bytes[4:4 + length_pck]
					# 删除已经读取的字节
					bytes = bytes[4 + length_pck:]
					# 把封包交给处理函数
					self.pck_handler(pck)
					# 如果bytes没数据了，就跳出循环
					if len(bytes) == 0:
						break
					# print("客户端消息：", bytes.decode(encoding="utf8"))
			except Exception as e:  # 意外掉线
				print("---------------------------")
				print("玩家：【%s】掉线啦。" % self.get_conn().playerName)
				self.remove()
				break

	def finish(self):
		pass
	def get_conn(self):
		for conn in g_conn_pool:
			if conn.conn == self.request:
				return conn

	def new_role(self):
		# 告诉各个客户端有新玩家加入
		ret = Protocol()
		ret.add_int32(1)
		ret.add_str(self.get_conn().playerName)
		ret.add_int32(self.get_conn().x)
		ret.add_int32(self.get_conn().y)
		ret.add_int32(self.get_conn().charId)
		for r in g_conn_pool:
			if r != self.get_conn():
				r.conn.sendall(ret.get_pck_has_head())

	def other_role(self):
		# 告诉当前玩家，其他玩家的信息
		for conn in g_conn_pool:
			if conn != self.get_conn():
				ret = Protocol()
				ret.add_int32(1)
				ret.add_str(conn.playerName)
				ret.add_int32(conn.x)
				ret.add_int32(conn.y)
				ret.add_int32(conn.charId)
				self.request.sendall(ret.get_pck_has_head())

	def move_role(self):
		# 告诉各个客户端有玩家移动了
		ret = Protocol()
		ret.add_int32(0)
		ret.add_int32(self.get_conn().x)
		ret.add_int32(self.get_conn().y)
		ret.add_int32(self.get_conn().charId)
		for r in g_conn_pool:
			if r != self.get_conn():
				r.conn.sendall(ret.get_pck_has_head())
	
	
	def new_animation(self,trigger,charId):
		ani=Protocol()
		ani.add_int32(4)
		ani.add_int32(trigger)
		ani.add_int32(charId)
		for r in g_conn_pool:
			if r != self.get_conn():
				r.conn.sendall(ani.get_pck_has_head())
	def new_mouse(self):
		p=Protocol()
		p.add_int32(3)
		p.add_int32(self.get_conn().mouseX)
		p.add_int32(self.get_conn().mouseY)
		p.add_int32(self.get_conn().charId)
		for r in g_conn_pool:
			if r != self.get_conn():
				r.conn.sendall(p.get_pck_has_head())
	def pck_handler(self, pck):
		"""
		解析数据包
		"""
		p = Protocol(pck)
		pck_type = p.get_int32()

		if pck_type == 1:
			self.get_conn().playerName=p.get_str()
			self.get_conn().x = p.get_int32()
			self.get_conn().y = p.get_int32()
			self.get_conn().charId = p.get_int32()
			self.new_role()  # 告诉当前服务器的其他玩家，有新玩家加入
			self.other_role()  # 告诉新加入的玩家，当前服务器的其他玩家信息

		elif pck_type == 0:
			self.get_conn().x = p.get_int32()
			self.get_conn().y = p.get_int32()
			self.move_role()
		elif pck_type == 3:
			
			self.get_conn().mouseX=p.get_int32()
			self.get_conn().mouseY=p.get_int32()
			self.get_conn().charId=p.get_int32()
			self.new_mouse()
		elif pck_type == 4:
			trigger=p.get_int32()
			charId=p.get_int32()
			self.new_animation(trigger,charId)
			
	def remove(self):
		# 告诉各个客户端有玩家离线
		ret = Protocol()
		ret.add_int32(2)
		ret.add_int32(self.get_conn().charId)
		for r in g_conn_pool:
			if r != self.get_conn():
				r.conn.sendall(ret.get_pck_has_head())
		g_conn_pool.remove(self.get_conn())

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
	pass


if __name__ == '__main__':
	server = ThreadedTCPServer(ADDRESS, ThreadedTCPRequestHandler)
	# 新开一个线程运行服务端
	server_thread = threading.Thread(target=server.serve_forever)
	server_thread.daemon = True
	server_thread.start()

	# 主线程逻辑
	while True:
		sleep(3)
