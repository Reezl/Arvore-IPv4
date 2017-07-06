# CLIENTE SOCKET
import socket, pickle

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dest = ('192.168.1.252', 65025)
while True:
	ip = input("Informe o seu IP: ")
	m = int(input("Informe a máscara que sua rede está configurada (Ex: /24):  "))
	d = int(input("Informe quantos dispositivos estão/serão alocados em sua rede: "))

	
	
	msg = (m, d, ip)
	msg = pickle.dumps(msg)
	udp.sendto(msg, dest)
	sizeb = 0
	sizeb,cliente = udp.recvfrom(1024)
	print("Aguardando o tamanho do pacote")
	sizeb = int(sizeb.decode('utf8'))
	if sizeb != 0:
	
		msg_t,cliente = udp.recvfrom(sizeb)
		print("Criando o arquivo com os IPs")
		msg_r = open('ips_recebido.txt','w')
		msg_r.write(pickle.loads(msg_t))
		msg_r = open('ips_recebido.txt','rt')

		print("Um arquivo com IP's foi gerado!")
		
		for w in msg_r:
			print(w)
	
	
