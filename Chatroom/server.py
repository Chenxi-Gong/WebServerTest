# coding=gbk
from socket import *
from multiprocessing import Process
from urllib import parse
import time
import re

def send(file,client):
	response_header = "HTTP/1.1 200 OK\r\nServer: ChenxiGong\r\n\r\n"
	with open(file,"rb") as f:
		response_body = f.read()
	client.send(response_header.encode("gbk"))
	print("header sent")
	client.send(response_body)
	print("body sent")

def handle_client(client):
	print("\r\nwaiting for data")
	recv_data = client.recv(1024).decode("gbk")
	print("\r\nreceived")
	header = recv_data.splitlines()
	#防止请求头为空
	if [] == header:
		print("***nothing***")
		client.close()
		print("over3")
	else:
		print(header[0])
		if "GET / HTTP/1.1" == header[0]:
			file = "index.html"
			send(file,client)
			print("index sent")
		elif "GET /index.html HTTP/1.1" == header[0]:
			file = "index.html"
			send(file,client)
			print("index sent")
		elif "GET /chatroom.html HTTP/1.1" == header[0]:
			file = "chatroom.html"
			send(file,client)
			print("chatroom sent")
		elif "GET /moneygame.html HTTP/1.1" == header[0]:
			file = "moneygame.html"
			send(file,client)
			print("moneygame sent")
		elif "GET /favicon.ico HTTP/1.1" == header[0]:
			file = "wolf.jpg"
			send(file,client)
			print("favicon wolf sent")
		#ajax获取消息记录
		elif "GET /data.txt HTTP/1.1" == header[0]:
			file = "data.txt"
			#send(file,client)
			response_header = "HTTP/1.1 200 OK\r\nServer: ChenxiGong\r\n\r\n"
			with open(file,"rb") as f:
				response_body = f.read().decode("gbk")
			client.send(response_header.encode("gbk"))
			print("header sent")
			client.send(response_body.encode("utf-8"))
			print("body sent")
			print("data sent")
		#处理客户端在聊天栏发送的信息
		elif "POST /chatroom.html HTTP/1.1" == header[0]:
			#接收消息
			#print(header[-1])
			a = re.match(r"message=(.*)",header[-1]).group(1)
			#print(a)
			b = parse.unquote(a,encoding = "gbk")
			#print(b)
			with open("data.txt","rb") as f:
				c = f.read().decode("gbk")
			#print(c)
			ti = time.strftime("%m/%d %H:%M:%S",time.localtime())
			d = "[" + ti + "]" + "  " + b + "<br/><br/>" + c
			#print(d)
			#控制数据库消息数量
			m = 0
			e = ""
			for i in d:
				e = e + i
				#print(e)
				if ">" == i:
					m = m + 1
					#print(m)
				if m > 17:
					break
			#print(m)
			#print(e)
			#存入数据库
			with open("data.txt","w") as f:
				f.write(e)
			#刷新页面
			file = "chatroom.html"
			send(file,client)
			print("chatroom sent")
		#未知的请求头
		else:
			print("!!!!")
			print(header)
			print("!!!!")
			header404_1 = "HTTP/1.1 404 Not Found\r\n"
			header404_2 = "Server: ChenxiGong\r\n\r\n"
			body404 = "MISTAKE"
			response404 = header404_1 + header404_2 + body404
			client.send(response404.encode("gbk"))
			print("404 sent")
		client.close()
		print("over1")

#7秒不发请求报文就断开连接
def timer(client):
	clientProcess = Process(target = handle_client,args = (client,))
	clientProcess.daemon = True
	clientProcess.start()
	print("\r\nclientProcess started")
	client.close()
	time.sleep(7)
	print("***time out***")

def main():
	server_socket = socket(AF_INET, SOCK_STREAM)
	print("TCP socket")
	server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	print("setsockopt")
	server_socket.bind(('', 777))
	print("bind port")
	server_socket.listen(128)
	print("listen\r\n\r\n\r\n")
	while True:
		print("loop started")
		client, address = server_socket.accept()
		print("\r\n****************")
		print(client)
		print("****************")
		print(address)
		print("****************")
		timerProcess = Process(target = timer,args = (client,))
		timerProcess.start()
		print("timerProcess started")
		client.close()
		print("loop over\r\n\r\n")

if __name__ == "__main__":
	main()