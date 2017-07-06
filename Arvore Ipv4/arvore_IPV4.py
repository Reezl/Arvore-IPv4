import socket, pickle, os

def decimalToBinary(x):
	y = bin(x)[2:]
	if len(y) < 8:
		for i in range(8-len(y)):
			y = '0' + y
	#print(y)
	return y
	
def binaryToDecimal(x):
	y = int(x, 2)
	return int(y)
	
def concatMat(m):
	k = []
	s = ''
	for i in range(len(m)):
		for j in range(len(m[i])):
			s += str(m[i][j])
		k.append(int(s))
		s = ''
	#print(k)
	return k

def genMask(mask):
	m = []
	c = 0
	for i in range(32):
		if i == 0:
			m.append([])
		elif i % 8 == 0:
			m.append([])
			c += 1
		if i <= mask:
			m[c].append(1)
		else:
			m[c].append(0)
	return m
	
def vlsm(ip, maskblc):
	
	msc = {8:2**24,9:2**23,10:2**22,11:2**21,12:2**20,13:2**19,14:2**18,15:2**17,16:2**16,17:2**15,18:2**14,19:2**13,20:2**12,21:2**11,22:2**10,23:2**9,24:2**8,25:2**7,26:2**6,27:2**5,28:2**4,29:2**3,30:2**2}

	n = {}
	
	ips = []
	

	for i in range(8, 30):
		if maskblc == i:
			qntd = msc[i]
			indc = i
		
	for i in range(indc, 31):
		somaqntd = 0
		subqntd = msc[i]
	
		if indc==i:
			#print("Esse é o tamanho do seu bloco:",qntd,"hosts")
			with open('ips.txt', 'w') as f:
				f.write('\nEsse é o tamanho do seu bloco %d hosts\n'%(qntd))
		else:
			#print("Subrede de",subqntd,":")
			while (somaqntd < qntd):
				#print(subqntd, end=" | ")
				somaqntd+=subqntd
				if subqntd not in n:
					n[subqntd] = 0
				n[subqntd] += 1
	#print('\n')
	#print(n)
	
	mm = ip[0]
	g = ip[3]
	h = ip[2]
	f = ip[1]
	index = 0	
	actual_msk = maskblc
	for i in n:		
		actual_msk += 1
		g = 0		
		ips.append([])		
		for _ in range(n[i]):									
			ips[index].append([mm, f, h, (g+i)])						
			g += i						
			if g >= 255:
				g = 0
				h += 1			
			if h >= 255:
				h = 0
				f += 1			
		index += 1
		h = ip[2]
		f = ip[1]			
	i1 = 80
	i2 = 0
	
					
	for i in range(len(ips)):
		#print('-------------------------------------------------')
		with open ('ips.txt','a')as f:
			f.write('-------------------------------------------------\n')
		for j in range(len(ips[i])):		
			#print('%i.%i.%i.%i - %i.%i.%i.%i' % (ips[i][j][0] , ips[i][j][1], ips[i][j][2] ,(ips[i][j][3]-ips[i][0][3]), ips[i][j][0],ips[i][j][1], ips[i][j][2],(ips[i][j][3])-1))	
			with open('ips.txt', 'a') as f:
				
				f.write('%i.%i.%i.%i - %i.%i.%i.%i \n' % (ips[i][j][0] , ips[i][j][1], ips[i][j][2] ,(ips[i][j][3]-ips[i][0][3]), ips[i][j][0],ips[i][j][1], ips[i][j][2],(ips[i][j][3])-1))
				

def ipv4(mascara,dispositivos,ip):
	
	msc = {8:2**24,9:2**23,10:2**22,11:2**21,12:2**20,13:2**19,14:2**18,15:2**17,16:2**16,17:2**15,18:2**14,19:2**13,20:2**12,21:2**11,22:2**10,23:2**9,24:2**8,25:2**7,26:2**6,27:2**5,28:2**4,29:2**3,30:2**2}
	
	for i in msc:
		if (dispositivos+5 <= msc[i]):
			indc=i
	masc=msc[indc]
	if (mascara > masc):
		mascsub = mascara-masc
	else:
		mascsub = masc-mascara

	ipl = ip.split('.')
	for i in range(len(ipl)):
		ipl[i] = int(ipl[i])
		
	ipb = []	
		
	for i in range(len(ipl)):
		binary = decimalToBinary(ipl[i])
		ipb.append([])
		for j in range(len(binary)):
			ipb[i].append(int(binary[j]))
	
	mask = genMask(mascara)
	mip = []
	
	for i in range(len(ipb)):
		mip.append([])
		for j in range(len(ipb[i])):
			if ipb[i][j] == 1 and mask[i][j] == 1:
				mip[i].append(1)
			else:
				mip[i].append(0)
	

	mpb = []
	mipc = concatMat(mip)
	for i in range(len(mipc)):
		mpb.append(binaryToDecimal(str(mipc[i])))
	return mpb

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind(('192.168.1.251',65025))

while True:
	
	msg, cliente = udp.recvfrom(1024)
	m, d, ip = pickle.loads(msg)
	print('Aguarde ...')
	vlsm(ipv4(m, d, ip), m)
	
	
	
	arq = open('ips.txt','rt')
	arqb = arq.read()
	info = str(os.stat('ips.txt').st_size).encode()
	udp.sendto(info, cliente)

	arqb = pickle.dumps(arqb)
	udp.sendto(arqb, cliente)
