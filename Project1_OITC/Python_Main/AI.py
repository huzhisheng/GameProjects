from Model import Model
import math
import random

class AI(Model):
	def __init__(self,scene,charId,x,y,charType,is_online):
		super().__init__(scene,charId, x, y, charType,is_online)
		#*********************AI角色属性******************
		self.enemy=None
		self.pos_record=0
		self.path=[]
		self.current_path=[]
		self.inDanger = False
		self.attackGap = 0
		self.pathChoice = 1
		self.jumpTwiceCountAI = 0
		self.jumpTwiceFlagAI = 0
		self.rushFlagAI = 0
		self.rushCountAI = 0
		print('online')
		print(self.is_online)

	def AI(self, shortest_path_record, y_map_table,point_map_table):
		#寻找路径
		min_distance_AI = 1000000
		point_AI = None
		min_distance_AItoDestination = 1000000
		point_destination = None
		y_destination = 1000000
		y_point_sets = []
		for point in point_map_table:
			_point = point.point
			_position = point.position
			dis = self.getDistance(_position,(self.rect.centerx,self.rect.centery))
			if dis < min_distance_AI:
				min_distance_AI = dis
				point_AI = _point
		
		for y in y_map_table:
			##print(abs(self.enemy.rect.bottom - y.y))
			if abs(self.enemy.rect.bottom - y.y) < y_destination:
				y_destination = abs(self.enemy.rect.bottom - y.y)
				y_point_sets = y.sets.copy()

		#*******************************************************************目的点寻址方法1——找寻两人离两人中点最近的点
		#*******************************************************************目的点寻址方法2——找寻两人离自己最近的点
		#*******************************************************************目的点寻址方法3——找寻两人离两人1/3最近的点
		#*******************************************************************目的点寻址方法4——找寻两人离两人2/3最近的点
		for point in y_point_sets:
			if self.pathChoice == 1:
				dis = self.getDistance(point.position,((self.rect.centerx + self.enemy.rect.centerx)/2,(self.rect.centery + self.enemy.rect.centery)/2))
			elif self.pathChoice == 2:
				dis = self.getDistance(point.position,(self.rect.centerx, self.rect.centery))
			elif self.pathChoice == 3:
				dis = self.getDistance(point.position,((self.rect.centerx + self.enemy.rect.centerx)/3,(self.rect.centery + self.enemy.rect.centery)/3))
			elif self.pathChoice == 4:
				dis = self.getDistance(point.position,((self.rect.centerx + self.enemy.rect.centerx)*2/3,(self.rect.centery + self.enemy.rect.centery)*2/3))
			if dis < min_distance_AItoDestination:
				min_distance_AItoDestination = dis
				point_destination = point.point

		self.path = shortest_path_record[point_AI][point_destination]
		if self.pos_record == 0 or self.current_path != self.path:
			#更换路径，重新选择寻路方案
			self.pathChoice = random.randint(1,4)
			self.pos_record = 0
			self.current_path =self.path.copy()

		#AI行为
		self.arrivePoint(self.current_path,point_map_table,len(self.path))
		
		if abs(self.enemy.rect.centery-self.rect.centery)<= 50:
			if self.attackGap == 30:
				if self.enemy.hiding:
					if self.enemy.imageState==self.attackState or self.enemy.imageState==self.hurtState:
						self.attack()
				else:
					print('attack')
					self.attack()
				self.attackGap = 0
			else:
				self.attackGap += 1
	
	def getDistance(self,point1,point2):
		return math.sqrt(math.pow(point1[0] - point2[0],2) + math.pow(point1[1] - point2[1],2))

	def arrivePoint(self, path, point_map_table,len):
		#print(self.pos_record)
		#print(len)
		point = path[self.pos_record]
		point = point_map_table[point]
		dest_x = point.position[0]
		dest_y = point.position[1]
		self_x = self.rect.centerx
		self_y = self.rect.bottom
		
		
		#print(self.imageState)
		if self.getDistance((dest_x, dest_y),(self_x, self_y)) >= 100 and self.imageState!=self.rushState:
			if 50<dest_x-self_x:
				self.movingLeft=0
				if self.getDistance((dest_x, dest_y),(self_x, self_y)) >= 200:
					#print('run')
					
					self.runRight()
				else:
					#print('walk1')
					self.walkRight()
			elif self_x - dest_x>50:
				self.movingRight=0
				if self.getDistance((dest_x, dest_y),(self_x, self_y)) >= 200:
					#print('run')
					self.runLeft()
				else:
					self.walkLeft()
			else:
				self.movingLeft = 0
				self.movingRight = 0
				self.imageState = self.standState

			

			if (self_y - dest_y) >= 50 or self.jumpTwiceFlagAI == 1:
				if(self.onLand or self.jumpTwiceFlagAI == 1):
					if(self_y - dest_y >= 150  or self.jumpTwiceFlagAI == 1):
						self.jumpTwiceAI()
						#self.jump()
					else:
						self.jump()

			elif dest_y -self_y >= 10 and self.onLand:
				self.drop()
				#print('drop')

			self.inDanger = True
			if self.onLand:
				self.inDanger=False

			for platform in self.scene.map.map:
				if self.rect.centery < platform.rect.centery:
					if abs(self.rect.centerx - platform.rect.centerx)<=15:
						self.inDanger=False

			if self.inDanger:
				#print('danger')
				self.avoidDanger()	

		else:
			#self.attack()
			self.movingLeft = 0
			self.movingRight = 0
			if len - 1 == self.pos_record:
				self.movingLeft = 0
				self.movingRight = 0
				self.pos_record = 0
				#走完后，重新选择寻路方案
				self.pathChoice = random.randint(1,4)
			else:
				self.pos_record += 1

		if self.enemy.rect.centerx < self.rect.centerx:
			self.direct = -1
		else:
			self.direct = 1

	def avoidDanger(self):
		jump_random = random.randint(0,1)
		if self.onLand == False:
			if jump_random == 0:
				self.jump()
			else:
				self.jumpTwiceAI()

		if self.direct == 1:
			#self.runRight()
			self.rushAI()
		elif self.direct == -1:
			#self.runLeft()
			self.rushAI()

	def jumpTwiceAI(self,count = 20):
		#print('danger')
		if self.jumpTwiceFlagAI == 0:
			#print('jumpone')
			self.jump()
			self.jumpTwiceFlagAI = 1
		else:
			self.jumpTwiceCountAI += 1
			if self.jumpTwiceCountAI == count:
				#print('jumpTwice')
				self.jump()
				#冲刺？
				self.jumpTwiceCount = 0
				self.jumpTwiceFlag = 0

	def rushAI(self,count = 10):
		if self.rushFlagAI == 0:
			self.rushFlagAI = 1

		elif self.rushFlagAI == 1: 
			self.rushCountAI += 1
			if self.rushCountAI == count:
				#print('rush')
				self.rush()
				self.rushCountAI = 0
				self.rushFlagAI = 0