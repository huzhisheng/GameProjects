import socket
import threading

from Base import Protocol
class ScanIP(object):
	# 创建接收路由列表
	def __init__(self,host_ip,port_list):
		self.routers = []

		# 创建互斥锁
		self.lock = threading.Lock()

		# 设置需要扫描的端口号列表
		self.port_list = port_list
		self.map_orders = []
		self.room_player_counts=[]
		self.room_names = []
	# 定义查询路由函数
	def search_routers(self):
		# 获取本地ip地址列表
		local_ips = socket.gethostbyname_ex(socket.gethostname())[2]
		print(local_ips)
		# 存放线程列表池
		all_threads = []
		# 循环本地网卡IP列表
		for ip in local_ips:
			for i in range(1, 255):
				# 把网卡IP"."进行分割,生成每一个可用地址的列表
				array = ip.split('.')
				# 获取分割后的第四位数字，生成该网段所有可用IP地址
				array[3] = str(i)
				# 把分割后的每一可用地址列表，用"."连接起来，生成新的ip
				new_ip = '.'.join(array)
				# print(new_ip)
				# 遍历需要扫描的端口号列表
				if new_ip == ip:
					pass
				else:
					for port in self.port_list:
						dst_port = int(port)
						#self.check_ip(new_ip,dst_port)
						# 循环创建线程去链接该地址
						t = threading.Thread(target=self.check_ip, args=(new_ip, dst_port) )
						t.start()
						# 把新建的线程放到线程池
						all_threads.append(t)
		# 循环阻塞主线程，等待每一字子线程执行完，程序再退出
		for t in all_threads:
			t.join()
		print(self.routers)
		return self.routers

# 创建访问IP列表方法
	def check_ip(self,new_ip, port):
		# 创建TCP套接字，链接新的ip列表
		scan_link = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# 设置链接超时时间
		scan_link.settimeout(2)
		# 链接地址(通过指定我们 构造的主机地址，和扫描指定端口)
		result = scan_link.connect_ex((new_ip, port))
		# print(result)
		

		# 判断链接结果
		if result == 0:
			self.send_search_request(scan_link)
			flag=0
			while True:
				bytes = scan_link.recv(1024)
				while True:
					# 读取包长度
					length_pck = int.from_bytes(bytes[:4], byteorder='little')
					# 截取封包
					pck = bytes[4:4 + length_pck]
					# 删除已经读取的字节
					bytes = bytes[4 + length_pck:]
					# 把封包交给处理函数
					flag=self.pck_handler(pck)
					# 如果bytes没数据了，就跳出循环

					if len(bytes) == 0:
						break
				if flag==1:
					break

			# 加锁
			self.lock.acquire()
			print(new_ip, '\t\t端口号%s开放' % port)
			#self.send_exit_game(scan_link)
			#scan_link.shutdown(2)
			#scan_link.close()
			
			self.routers.append((new_ip, port))
			# 释放锁
			self.lock.release()
		#else:
			#scan_link.close()
		# print(routers)
	def get_info(self):
		return self.map_orders,self.room_player_counts,self.room_names

	def pck_handler(self, pck):
		"""
		解析数据包
		"""
		p = Protocol(pck)
		pck_type = p.get_int32()
		#_map=p.get_int32()
		#_count=p.get_int32()
		#print(_map,_count)
		#print(pck_type)
		#print(len(pck))
		if pck_type == 1:
			_map=p.get_int32()
			_count=p.get_int32()
			_room_name = p.get_str()
			#print('www')
			print(_map,_count,_room_name)
			self.map_orders.append(_map)
			self.room_player_counts.append(_count)
			self.room_names.append(_room_name)
			return 1
		return 0
	def send_search_request(self,g_client):

		#发送搜索服务器请求

		# 构建数据包
		p = Protocol()
		p.add_int32(7)
		data = p.get_pck_has_head()
		# 发送数据包
		g_client.sendall(data)