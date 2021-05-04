import socketserver
import socket
import threading
from time import sleep
import ctypes
import inspect
from ScanIP import ScanIP

from Base import Protocol
g_conn_pool = []  # 连接池
map = 1
room_name = ''
class Conn:
	def __init__(self, conn):
		self.conn = conn
		self.playerName=''
		self.x = None
		self.y = None
		self.charId=None
		self.charType=None
class Bullet:
	def __init__(self):
		self.x=None
		self.y=None
		self.direct=None
		self.power=None
		self.createrId=None
bullet=Bullet()
class Wall:
	def __init__(self):
		self.x=None
		self.y=None
		self.direct=None
wall=Wall()

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
	def setup(self):
		self.request.sendall("连接服务器成功!".encode(encoding='utf8'))
		print('1')
		
		bytes = self.request.recv(1024)
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
		# 加入连接池
		

	def handle(self):
		while True and self.get_conn():
			#print(g_conn_pool)
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
		ret.add_int32(self.get_conn().charType)
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
				ret.add_int32(conn.charType)
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
	def new_bullet(self):
		#告诉各个客户端有新的子弹生成
		bul=Protocol()
		bul.add_int32(3)
		bul.add_int32(bullet.x)
		bul.add_int32(bullet.y)
		bul.add_int32(bullet.direct)
		bul.add_int32(bullet.power)
		bul.add_int32(bullet.createrId)
		for r in g_conn_pool:
			if r != self.get_conn():
				r.conn.sendall(bul.get_pck_has_head())
	def new_wall(self):
		wal=Protocol()
		wal.add_int32(5)
		wal.add_int32(wall.x)
		wal.add_int32(wall.y)
		wal.add_int32(wall.direct)
		for r in g_conn_pool:
			if r != self.get_conn():
				r.conn.sendall(wal.get_pck_has_head())
	def new_animation(self,trigger,charId):
		ani=Protocol()
		ani.add_int32(4)
		ani.add_int32(trigger)
		ani.add_int32(charId)
		for r in g_conn_pool:
			if r != self.get_conn():
				r.conn.sendall(ani.get_pck_has_head())
	def send_back_info(self):
		p=Protocol()
		p.add_int32(1)
		p.add_int32(map)
		print(map)
		p.add_int32(len(g_conn_pool))
		p.add_str(room_name)		
		print(len(g_conn_pool))
		print(p.get_pck_has_head())
		print(len(p.get_pck_has_head()))
		self.request.sendall(p.get_pck_has_head())
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
			self.get_conn().charType = p.get_int32()
			self.new_role()  # 告诉当前服务器的其他玩家，有新玩家加入
			self.other_role()  # 告诉新加入的玩家，当前服务器的其他玩家信息

		elif pck_type == 0:
			self.get_conn().x = p.get_int32()
			self.get_conn().y = p.get_int32()
			self.move_role()

		elif pck_type == 3:
			bullet.x=p.get_int32()
			bullet.y=p.get_int32()
			bullet.direct=p.get_int32()
			bullet.power=p.get_int32()
			bullet.createrId=p.get_int32()
			self.new_bullet()
		elif pck_type == 4:
			trigger=p.get_int32()
			charId=p.get_int32()
			self.new_animation(trigger,charId)
		elif pck_type == 5:
			wall.x=p.get_int32()
			wall.y=p.get_int32()
			wall.direct=p.get_int32()
			self.new_wall()
		elif pck_type == 6:
			self.remove()
		elif pck_type == 7:
			self.send_back_info()
		elif pck_type == 8:
			conn = Conn(self.request)
			g_conn_pool.append(conn)

			
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
	def __init__(self, server_address, RequestHandlerClass,_map,_room_name,bind_and_activate=True):
		super().__init__(server_address, RequestHandlerClass, bind_and_activate)
		global map
		global room_name
		map = _map
		room_name = _room_name

class ThreadStopper(object):
	def __init__(self):
		pass
	def _async_raise(self,tid, exctype):
		print('tid')
		print(tid)
		tid = ctypes.c_long(tid)
		if not inspect.isclass(exctype):
			exctype = type(exctype)
		res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
		if res == 0:
			print("invalid thread id")
			raise ValueError("invalid thread id")
		elif res != 1:
			ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
			raise SystemError("PyThreadState_SetAsyncExc failed")
		elif res == 1:
			print('线程已关闭')

	def stop_thread(self,thread):
		try:
			print('thread.ident')
			print(thread.ident)
			self._async_raise(thread.ident, SystemExit)
		except:
			print('未开启线程')

if __name__ == '__main__':
	print(1)
	scan = ScanIP('10.13.77.57',['8080', '8000', '7777', '3389', '2425', '139'])
	#scan.search_routers()
	lock = threading.Lock()
	host = '10.13.77.57'
	ADDRESS = (host, 7777)  # 绑定地址
	server = ThreadedTCPServer(ADDRESS, ThreadedTCPRequestHandler)
	# 新开一个线程运行服务端
	server_thread = threading.Thread(target=server.serve_forever)
	#server_thread.daemon = True
	server_thread.start()
	print('seyr')
	# 主线程逻辑
	#while True:
	#scan_thread = threading.Thread(target = scan.search_routers)
	#scan_thread.daemon = True
	#scan_thread.start()
	scan.search_routers()