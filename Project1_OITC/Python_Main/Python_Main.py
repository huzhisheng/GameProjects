# -- coding: utf-8 -- 
import Map
import MutiGame
import LocalGame
import AI
import Model
import Wall
import Bullet
import Base
import socket
import sys
import MatchVoice
import Server
import ScanIP
import socketserver
import threading
from time import sleep
import eel
#import pygame
#import pygame.sprite
import random
#from pygame.locals import *

server = None
server_thread = None

#暴露搜索服务器函数
@eel.expose
def searchServers(host_ip,port_list):
	scan = ScanIP.ScanIP(host_ip,port_list)
	routers = scan.search_routers()
	map_orders, room_player_counts,room_names = scan.get_info()
	print(map_orders)
	print(room_player_counts)
	print(room_names)
	return routers,map_orders,room_player_counts,room_names

#暴露测试函数
@eel.expose
def test(is_window,map = 1,IP = '10.13.87.19',port =7777, online = 0, skillChosen = 0, time = 0, distance = 0,hostIP = '10.13.87.19',maxVolume = 20000):
	print('start')
	print(time)
	print(distance)
	print(hostIP)
	print(online)
	global server
	global server_thread
	if time != None and distance != None:
		if online:
			scene = MutiGame.Scene(is_window,map,IP,port,skillChosen, time, distance,hostIP,maxVolume)
			scene.net_init()
			print('net')
		else:
			scene = LocalGame.Scene(is_window,map, skillChosen,time,distance,maxVolume)
			scene.local_init()
			print('local')

		threadCount = 0
		exitFlag = False
		

		#线程不能同时启动，否则出现ID 1002 错误
		while not exitFlag:
			#if threadCount<400:
				#threadCount += 1
			#print(threadCount)
			#lock = threading.Lock()
			#if threadCount == 300:
				#scene.voice_init_voice()
				#pass
			#if threadCount == 100:
				#scene.voice_init_volume()

			exitFlag = scene.run()

	else:
		print('exit')
		return 0

	

#暴露录音函数
@eel.expose
def setSkill():
	time = MatchVoice.GetMicrophoneData('Voice/TemplateOutput.wav','Voice/Feature.npy','Voice/InGameOutput.wav',1200,5,0)
	print(time)
	return time

#暴露确认录音函数
@eel.expose
def confirmSkill(time):
	print('$')
	print(time)
	distance,maxVolume = MatchVoice.GetMicrophoneData('Voice/TemplateOutput.wav','Voice/Feature.npy','Voice/InGameOutput.wav',1200,time,1)
	return distance,maxVolume

#暴露服务器函数
@eel.expose
def createServer(IP,port = 7777,map = 1,room_name = 'hzs'):
	#scan = Server.ScanIP()
	#scan.search_routers()
	print(room_name)
	host = IP
	ADDRESS = (host, port)  # 绑定地址
	global server
	global server_thread
	server = Server.ThreadedTCPServer(ADDRESS, Server.ThreadedTCPRequestHandler, map, room_name)
	server.allow_reuse_address = True
	# 新开一个线程运行服务端
	server_thread = threading.Thread(target=server.serve_forever)
	server_thread.setDaemon(True)
	server_thread.start()
	print('Server start')

	

#获取本机ip
@eel.expose
def getIP():
    #获取本机name
    myname = socket.getfqdn(socket.gethostname())
    #获取本机ip
    myaddr = socket.gethostbyname(myname) 
    return myaddr

def printObject(object):
    for name, value in vars(object).items():
        #try:
            #x = vars(value).items()
        if isinstance(value, list):
            for elem in value:
                printObject(elem)
        #except:
        else:
            print('%s=%s'%(name,value))

def begin():
    eel._start_args['size'] = (1200,900)
    eel._start_args['host'] = 'localhost'
    eel.init('./MainInterfaceByHtml')
    eel.start('OITC.html')

begin()