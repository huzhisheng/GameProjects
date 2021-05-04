import pygame
import pygame.sprite
import random
from pygame.locals import *
import pygame.font
import sys
from Base import Protocol
import socket
from threading import Thread
import threading
from Map import *
import ctypes
import MatchVoice
import Server
from AI import AI
from Model import Model
from Bullet import Bullet
from Wall import Wall

root = '.'
#----------------------------------------------------------------------------------------添加skillChosen，time，distance
class Scene(object):
	def __init__(self, is_window,map = 1, IP = '10.13.87.19', port = 7777, skillChosen = 0, time = 0, distance = 0,hostIP = '10.13.87.19',maxVolume = 20000):
		pygame.init()
		pygame.mixer.init()	
		pygame.font.init()
		self.is_online = 1
		self.size = [1200, 900]
		self.skillChosen = skillChosen
		self.maxVolume = maxVolume*1.5
		self.voice_thread = None
		print(self.maxVolume)
		print('4')
		print(time)
		print(distance)
		print(hostIP)
		if is_window:
			self.scene = pygame.display.set_mode(self.size,flags=pygame.RESIZABLE)
		else:
			self.scene = pygame.display.set_mode(self.size,flags=pygame.FULLSCREEN,depth = 32)
		#置于最上层 from ctypes import windll http://www.itkeyword.com/doc/5239207061455695x393/how-to-make-python-window-run-as-always-on-top
		SetWindowPos = ctypes.windll.user32.SetWindowPos
		SetWindowPos(pygame.display.get_wm_info()['window'], -1, 300, 0, 0, 0, 0x0001)
		#self.scene = pygame.display.set_mode([self.size[0], self.size[1]])
		pygame.display.set_caption("输出全靠吼")
		#***************************************************实例化map 接口成功
		self.map = Map()
		self.map_order = map
		if map == 1:
			backgroundPath = self.map.generateMapOne()
		elif map == 2:
			backgroundPath = self.map.generateMapTwo()
		elif map == 3:
			backgroundPath = self.map.generateMapThree()
		elif map == 4:
			backgroundPath = self.map.generateMapFour()
		elif map == 5:
			backgroundPath = self.map.generateMapFive()
		elif map == 6:
			backgroundPath = self.map.generateMapSix()
		elif map == 7:
			backgroundPath = self.map.generateMapSeven()
		elif map == 8:
			backgroundPath = self.map.generateMapEight()
		elif map == 9:
			backgroundPath = self.map.generateMapNine()
		elif map == 10:
			backgroundPath = self.map.generateMapTen()
		#************************************************************
		self.bgImage = pygame.image.load(backgroundPath).convert()
		self.bgm=pygame.mixer.Sound(root+"/TestPic/bgm1.wav")
		self.bgm.play()
		self.bgImage = pygame.transform.scale(self.bgImage, (self.size[0], self.size[1]))
		self.scene.blit(self.bgImage,(0,0))
		self.clock = pygame.time.Clock()
		self.charList=[]#[Model(self,random.randint(0,1000),200,200)]#,Model(self,1,900,100),Model(self,2,400,100)]
		self.player=None#self.charList[0]
		'''
		for i in range(len(self.charList[1:])):
			self.charList[i+1].enemy=self.player
		'''
		self.voiceTime=time
		self.voiceDistance=distance

		self.lastA=0
		self.lastD=0
		
		self.bullets=pygame.sprite.Group()
		self.walls=pygame.sprite.Group()
		self.heartFull=pygame.image.load(root+"/TestPic/heartFull.png").convert_alpha()
		self.heartHalf=pygame.image.load(root+"/TestPic/heartHalf.png").convert_alpha()
		self.heartEmpty=pygame.image.load(root+"/TestPic/heartEmpty.png").convert_alpha()
		self.loadingImage=pygame.image.load(root+"/TestPic/loading.png").convert_alpha()
		self.loadingImage=pygame.transform.scale(self.loadingImage,(532,48))
		#*************************************************
		#****************网络数据包用到的属性*****************
		self.netPlayerMove=0
		self.netPlayerNew=1
		self.netPlayerOff=2
		self.netBulletNew=3
		self.netAnimationNew=4
		self.netWallNew=5
		#*************************************************
		self.g_client = socket.socket()
		self.IP=IP
		self.ADDRESS = (self.IP,port)
		#****************进入界面属性***********************
		self.breakFlag=False
		self.playerName=''
		self.mouseX=0
		self.mouseY=0
		self.p1front=None
		self.p2front=None
		self.p3front=None
		self.pSelect=1
		self.pSelectImage=pygame.image.load(root+"/TestPic/pSelect.png").convert_alpha()
		#****************暂停界面属性***********************
		self.pauseImage=pygame.image.load(root+"/TestPic/pauseBg.png").convert()
		#*****************声音识别的标志********************
		self.attackBool=False
		self.skillBool=False
		self.voiceVolume=0
		self.voice_thread=None
		self.voice_volume_thread=None
		#*****************线程中止的标志********************
		self.voice_life=True
		self.volume_life=True
		self.net_life=True
	def drawHeart(self):
		if self.player.life<=0:
			self.player.life=0
		fullNum=self.player.life//2
		halfNum=self.player.life-fullNum*2
		emptyNum=3-fullNum-halfNum
		num=0
		for i in range(fullNum):
			self.scene.blit(self.heartFull,(20+num*60,20))
			num+=1
		for i in range(halfNum):
			self.scene.blit(self.heartHalf,(20+num*60,20))
			num+=1
		for i in range(emptyNum):
			self.scene.blit(self.heartEmpty,(20+num*60,20))
			num+=1
			
	def charTrigger(self,trigger,charId):
		for r in self.charList:
			if r.charId == charId:
				if trigger==0:
					r.attackCount=0
					r.imageState=r.attackState
					r.stateFree=False
				elif trigger==1:
					if r.stateFree:
						r.imageState=r.walkState
					r.direct=1
				elif trigger==2:
					if r.stateFree:
						r.imageState=r.walkState
					r.direct=-1
				elif trigger==3:
					r.imageState=r.runState
					r.direct=1
				elif trigger==4:
					r.imageState=r.runState
					r.direct=-1
				elif trigger==5:
					r.rushCount=0
					r.stateFree=False
					r.imageState=r.rushState
				elif trigger==6:
					pass
				elif trigger==7:
					r.movingRight=0
					r.imageState=r.standState
				elif trigger==8:
					r.movingLeft=0
					r.imageState=r.standState
				elif trigger==9:
					r.jumpCount=0
					r.imageState=r.jumpState
					r.jumping=True
				elif trigger==10:
					r.dropBool=True
					r.dropTimeCount=20
				elif trigger==11:
					r.flyBool=True
					r.flyTimeCount=300
				elif trigger==12:
					r.hiding=True
					r.hideTimeCount=500
				elif trigger==13:
					r.shelding=True
					r.sheldTimeCount=500	
	def drawHandle(self):
		self.scene.blit(self.bgImage,(0,0))
		self.drawHeart()
		for i in range(len(self.charList)):
			self.charList[i].draw()
		self.bullets.draw(self.scene)
		self.walls.draw(self.scene)
		 #**********************************************************draw map
		self.map.map.draw(self.scene)
		#pygame.draw.rect(self.scene,(0,0,255),self.player.rect,1)
		#pygame.draw.rect(self.scene,(0,0,255),self.land1.rect,1)
		#pygame.draw.rect(self.scene,(0,0,255),self.land2.topRect,1)
	def actionHandle(self):
		for bullet in self.bullets:
			bullet.action()
		for wall in self.walls:
			wall.action()
		for i in range(len(self.charList)):
			self.charList[i].action()
		
	def landCollision(self):
		for i in range(len(self.charList)):
			self.charList[i].onLand=False
		for platform in self.map.map:
			for i in range(len(self.charList)):
				if platform.topRect.collidepoint(self.charList[i].rect.midbottom) and self.charList[i].speedY>=0 and not self.charList[i].dropBool:
					if self.charList[i].imageState==self.charList[i].jumpState :
						self.charList[i].imageState=self.charList[i].standState
					self.charList[i].onLand=True
		for i in range(len(self.charList)):
			if not self.charList[i].onLand:
				self.charList[i].jumping=False
	def bulletCollision(self):
		for bullet in self.bullets:
			bullet.collision()
	def wallCollision(self):
		
		self.player.leftWall=False
		self.player.rightWall=False
		for wall in self.walls:
			wall.collision()
	def eventHandle(self):
		'''
		for i in range(len(self.charList[1:])):
			self.charList[i+1].AI()
		'''
		self.lastA+=1
		self.lastD+=1
		eventList = pygame.event.get()
		
		for event in eventList:
			if event.type == pygame.QUIT:
				print('exit')
				#stopper = Server.ThreadStopper()
				#stopper.stop_thread(self.voice_thread)
				#stopper.stop_thread(self.voice_volume_thread)
				self.voice_life=False
				self.volume_life=False
				self.net_life=False
				pygame.quit()
				return True
				#exit()

			if event.type == pygame.KEYDOWN:
				if event.key==pygame.K_d:
					if self.lastD>=20:
						self.player.walkRight()
					else:
						self.player.runRight()
					self.lastD=0
				if event.key==pygame.K_a:
					if self.lastA>=20:
						self.player.walkLeft()
					else:
						self.player.runLeft()
					self.lastA=0
				if event.key==pygame.K_s:
					self.player.drop()
				if event.key==pygame.K_j:
					self.player.attack()
				if event.key==pygame.K_w:
					self.player.jump()
				if event.key==pygame.K_r :
					self.player.reset()
				if event.key==pygame.K_LSHIFT:
					self.player.rush()
				if event.key==pygame.K_SPACE:
					self.player.fly()
				if event.key==pygame.K_u:
					self.player.skill()
				if event.key==pygame.K_ESCAPE:
					flag = self.pause()
					return flag
			if event.type == pygame.KEYUP:
				if event.key==pygame.K_d:
					self.player.stopMovingRight()
				if event.key==pygame.K_a:
					self.player.stopMovingLeft()
				if event.key==pygame.K_w:
					self.player.stopFly()

			if event.type==pygame.MOUSEBUTTONDOWN:
				mouseX,mouseY=pygame.mouse.get_pos()
		if self.attackBool:
			self.attackBool=False
			self.player.attack()
		if self.skillBool:
			self.skillBool=False
			self.player.skill()	
		return False
	def collisionHandle(self):
		self.landCollision()
		self.bulletCollision()
		self.wallCollision()
	def run(self):
		self.collisionHandle()
		self.actionHandle()
		self.drawHandle()
		self.send_role_move()
		exitFlag = self.eventHandle()
		if not exitFlag:
			pygame.display.update()
			self.clock.tick(60)
		return exitFlag
	#*********************网络模块***************************************************************************
	def send_role_move(self):

		#发送角色的坐标给服务端

		# 构建数据包
		p = Protocol()
		p.add_int32(0)
		p.add_int32(self.player.rect[0])
		p.add_int32(self.player.rect[1])
		data = p.get_pck_has_head()
		# 发送数据包
		self.g_client.sendall(data)
	def send_role_animation(self,trigger):
		#发送角色的动画状态给服务端

		# 构建数据包
		p = Protocol()
		p.add_int32(4)
		p.add_int32(trigger)
		p.add_int32(self.player.charId)
		data = p.get_pck_has_head()
		# 发送数据包
		self.g_client.sendall(data)
	def send_new_bullet(self,x,y,direct,power,createrId):
		#告诉服务端有新子弹

		# 构建数据包
		p = Protocol()
		p.add_int32(3)
		p.add_int32(x)
		p.add_int32(y)
		p.add_int32(direct)
		p.add_int32(power)
		p.add_int32(createrId)
		data = p.get_pck_has_head()
		# 发送数据包
		self.g_client.sendall(data)
	def send_new_wall(self,x,y,direct):
		#告诉服务端有新墙

		# 构建数据包
		p=Protocol()
		p.add_int32(5)
		p.add_int32(x)
		p.add_int32(y)
		p.add_int32(direct)
		data = p.get_pck_has_head()
		# 发送数据包
		self.g_client.sendall(data)
	def send_new_role(self):

		#告诉服务端有新玩家加入

		# 构建数据包
		p = Protocol()
		p.add_int32(1)
		p.add_str(self.playerName)
		p.add_int32(self.player.rect[0])
		p.add_int32(self.player.rect[1])
		p.add_int32(self.player.charId)
		p.add_int32(self.player.charType)
		data = p.get_pck_has_head()
		# 发送数据包
		self.g_client.sendall(data)
	def send_exit_game(self):
		#告诉服务端玩家下线
		
		#构建数据包
		p = Protocol()
		p.add_int32(6)
		data = p.get_pck_has_head()
		# 发送数据包
		self.g_client.sendall(data)
	def pck_handler(self,pck):
		p = Protocol(pck)
		pck_type = p.get_int32()

		if pck_type == self.netPlayerMove:  # 玩家移动的数据包
			x = p.get_int32()
			y = p.get_int32()
			charId = p.get_int32()
			for r in self.charList:
				if r.charId == charId:
					r.rect[0] = x
					r.rect[1] = y
					break
		elif pck_type == self.netPlayerNew:  # 新玩家数据包
			playerName=p.get_str()
			x = p.get_int32()
			y = p.get_int32()
			charId = p.get_int32()
			charType=p.get_int32()
			r = Model(self,charId,x,y,charType,self.is_online)
			r.playerName=playerName
			self.charList.append(r)
		elif pck_type == self.netPlayerOff:  # 玩家掉线
			charId = p.get_int32()
			for r in self.charList:
				if r.charId == charId:
					self.charList.remove(r)
					break
		elif pck_type == self.netBulletNew:  # 新子弹
			x = p.get_int32()
			y = p.get_int32()
			direct = p.get_int32()
			if direct==0:
				direct=-1
			power = p.get_int32()
			createrId = p.get_int32()
			bullet=Bullet(self,[x,y],direct,power,createrId)
			self.bullets.add(bullet)
		elif pck_type == self.netAnimationNew:
			trigger=p.get_int32()
			charId=p.get_int32()
			self.charTrigger(trigger,charId)
		elif pck_type == self.netWallNew:	# 新墙
			x = p.get_int32()
			y = p.get_int32()
			direct = p.get_int32()
			if direct==0:
				direct=-1
			wall=Wall(self,(x,y),direct)
			self.walls.add(wall)
		else:
			return
	
	def msg_handler(self):

		#处理服务端返回的消息

		while True:
			if not self.net_life:
				break
			try:
				bytes = self.g_client.recv(1024)
				# 以包长度切割封包
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
			except:
				pass
	def send_connect_request(self):

		#发送搜索服务器请求

		# 构建数据包
		p = Protocol()
		p.add_int32(8)
		data = p.get_pck_has_head()
		# 发送数据包
		self.g_client.sendall(data)

	def net_init(self):
		# 与服务器建立连接
		self.g_client.connect(self.ADDRESS)
		self.send_connect_request()
		# 开始接受服务端消息
		thead = Thread(target=self.msg_handler)
		thead.setDaemon(True)
		thead.start()
		# 告诉服务端有新玩家
		self.player_enter()
		self.player=Model(self,random.randint(0,1000),200,200,self.pSelect,self.is_online)
		self.player.skillChosen = self.skillChosen
		self.charList.append(self.player)
		self.player.playerName=self.playerName
		self.send_new_role()
		#self.voice_init()

	def enter_input_handle(self):
		eventList = pygame.event.get()
		
		for event in eventList:
			if event.type == pygame.QUIT:
				print('exit')
				#stopper = Server.ThreadStopper()
				#stopper.stop_thread(self.voice_thread)
				#stopper.stop_thread(self.voice_volume_thread)
				self.send_exit_game()
				self.g_client.shutdown(2)
				self.g_client.close()
				self.voice_life=False
				self.volume_life=False
				self.net_life=False
				pygame.quit()
				return True
				#self.voice_thread.join()
				#exit()

			if event.type == pygame.KEYDOWN:
				if event.key==pygame.K_0:
					self.playerName=self.playerName+'0'
				elif event.key==pygame.K_1:
					self.playerName=self.playerName+'1'
				elif event.key==pygame.K_2:
					self.playerName=self.playerName+'2'
				elif event.key==pygame.K_3:
					self.playerName=self.playerName+'3'
				elif event.key==pygame.K_4:
					self.playerName=self.playerName+'4'
				elif event.key==pygame.K_5:
					self.playerName=self.playerName+'5'
				elif event.key==pygame.K_6:
					self.playerName=self.playerName+'6'
				elif event.key==pygame.K_7:
					self.playerName=self.playerName+'7'
				elif event.key==pygame.K_8:
					self.playerName=self.playerName+'8'
				elif event.key==pygame.K_9:
					self.playerName=self.playerName+'9'
				elif event.key==pygame.K_a:
					self.playerName=self.playerName+'A'
				elif event.key==pygame.K_b:
					self.playerName=self.playerName+'B'
				elif event.key==pygame.K_c:
					self.playerName=self.playerName+'C'
				elif event.key==pygame.K_d:
					self.playerName=self.playerName+'D'
				elif event.key==pygame.K_e:
					self.playerName=self.playerName+'E'
				elif event.key==pygame.K_f:
					self.playerName=self.playerName+'F'
				elif event.key==pygame.K_g:
					self.playerName=self.playerName+'G'
				elif event.key==pygame.K_h:
					self.playerName=self.playerName+'H'
				elif event.key==pygame.K_i:
					self.playerName=self.playerName+'I'
				elif event.key==pygame.K_j:
					self.playerName=self.playerName+'J'
				elif event.key==pygame.K_k:
					self.playerName=self.playerName+'K'
				elif event.key==pygame.K_l:
					self.playerName=self.playerName+'L'
				elif event.key==pygame.K_m:
					self.playerName=self.playerName+'M'
				elif event.key==pygame.K_n:
					self.playerName=self.playerName+'N'
				elif event.key==pygame.K_o:
					self.playerName=self.playerName+'O'
				elif event.key==pygame.K_p:
					self.playerName=self.playerName+'P'
				elif event.key==pygame.K_q:
					self.playerName=self.playerName+'Q'
				elif event.key==pygame.K_r:
					self.playerName=self.playerName+'R'
				elif event.key==pygame.K_s:
					self.playerName=self.playerName+'S'
				elif event.key==pygame.K_t:
					self.playerName=self.playerName+'T'
				elif event.key==pygame.K_u:
					self.playerName=self.playerName+'U'
				elif event.key==pygame.K_v:
					self.playerName=self.playerName+'V'
				elif event.key==pygame.K_w:
					self.playerName=self.playerName+'W'
				elif event.key==pygame.K_x:
					self.playerName=self.playerName+'X'
				elif event.key==pygame.K_y:
					self.playerName=self.playerName+'Y'
				elif event.key==pygame.K_z:
					self.playerName=self.playerName+'Z'
			if event.type==pygame.MOUSEBUTTONDOWN:
				self.mouseX,self.mouseY=pygame.mouse.get_pos()
	def enter_action_handle(self):
		if self.mouseX>300 and self.mouseX<500 and self.mouseY>570 and self.mouseY<700:
			self.pSelect=1
		if self.mouseX>500 and self.mouseX<700 and self.mouseY>570 and self.mouseY<700:
			self.pSelect=2
		if self.mouseX>700 and self.mouseX<900 and self.mouseY>570 and self.mouseY<700:
			self.pSelect=3
		if self.mouseX>508 and self.mouseX<688 and self.mouseY>778 and self.mouseY<848:
			self.breakFlag=True
	def player_enter(self):
		enterImage=pygame.image.load(root+'/TestPic/EnterImage.png').convert()
		self.p1front=pygame.image.load(root+'/TestPic/p1_front.png').convert_alpha()
		self.p2front=pygame.image.load(root+'/TestPic/p2_front.png').convert_alpha()
		self.p3front=pygame.image.load(root+'/TestPic/p3_front.png').convert_alpha()
		enterImage = pygame.transform.scale(enterImage, (self.size[0], self.size[1]))
		font =  pygame.font.SysFont('arial',60)
		textip=font.render(self.IP,False,(255,200,10))
		playerName=font.render(self.playerName,False,(255,200,10))
		threadCount=0
		while True:
			if threadCount<700:
				threadCount += 1
			if threadCount == 500:
				self.voice_init_voice()
				#pass
			if threadCount == 200:
				self.voice_init_volume()

			self.scene.blit(enterImage,(0,0))
			self.scene.blit(textip,(555,257))
			self.scene.blit(playerName,(475,414))
			self.scene.blit(self.p1front,(300,580))
			self.scene.blit(self.p2front,(545,580))
			self.scene.blit(self.p3front,(790,580))
			if self.pSelect==1:
				self.scene.blit(self.pSelectImage,(300,680))
			elif self.pSelect==2:
				self.scene.blit(self.pSelectImage,(545,680))
			else:
				self.scene.blit(self.pSelectImage,(790,680))
			self.enter_input_handle()
			self.enter_action_handle()
			playerName=font.render(self.playerName,False,(255,200,10))
			if self.breakFlag:
				if threadCount<690:
					self.scene.blit(self.loadingImage,(350,406))
				else:
					return
			pygame.display.update()
	def pause(self):
		while True:
			self.scene.blit(self.pauseImage,(0,0))
			eventList = pygame.event.get()
			for event in eventList:
				if event.type==pygame.MOUSEBUTTONDOWN:
					self.mouseX,self.mouseY=pygame.mouse.get_pos()
					if self.mouseX>500 and self.mouseX<700 and self.mouseY>190 and self.mouseY<250:
						return False
					if self.mouseX>500 and self.mouseX<700 and self.mouseY>335 and self.mouseY<395:
						print('exit')
						self.send_exit_game()
						self.g_client.shutdown(2)
						self.g_client.close()
						#stopper = Server.ThreadStopper()
						#stopper.stop_thread(self.voice_thread)
						#stopper.stop_thread(self.voice_volume_thread)
						self.voice_life=False
						self.volume_life=False
						self.net_life=False
						pygame.quit()
						return True
						
			pygame.display.update()

	def voice_init_voice(self):
		self.voice_thread = Thread(target=self.voice_handler)
		self.voice_thread.setDaemon(True)
		self.voice_thread.start()
		#self.voice_volume_thread.start()
	
	def voice_init_volume(self):
		self.voice_volume_thread = Thread(target=self.voice_volume_handler)
		self.voice_volume_thread.setDaemon(True)
		self.voice_volume_thread.start()

	def voice_handler(self):
		while True:
			print("voice_handler")
			try:
				newDistance,maxVolume = MatchVoice.GetMicrophoneData(root+'/Voice/TemplateOutput.wav',root+'/Voice/Feature.npy',root+'/Voice/InGameOutput.wav',5000,self.voiceTime,1)
				skillLevel = 5 
				tempDistance = self.voiceDistance
				if tempDistance*1.05>newDistance:
					print('ok')
					if skillLevel<=7:
						tempDistance = tempDistance - 0.15*self.voiceDistance
						skillLevel = skillLevel + 1
					#print(self.voice_thread)
					self.skillBool=True
				else:
					print('no')
					if skillLevel >= 3:
						tempDistance = tempDistance + 0.15*self.voiceDistance
						skillLevel = skillLevel - 1
					#print(self.voice_thread)
					#self.attackBool=True	
				if not self.voice_life:
					break
			except:
				pass
		while True:
			time.sleep(1000)


	def voice_volume_handler(self):
		while True:
			print("voice_volume_handler")
			try:
				self.voiceVolume=MatchVoice.MonitorMicrophone()
				print("volume:",self.voiceVolume)
				if self.voiceVolume>self.maxVolume*0.18:
					self.attackBool=True
				if not self.volume_life:
					break
			except:
				pass	
		while True:
			time.sleep(1000)

#scene=Scene()

#if __name__ == '__main__':
	# 初始化
#	scene.net_init()
	# 游戏循环
	
	#while True:
		#scene.run()

