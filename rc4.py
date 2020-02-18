import fileinput

def ksa(key):
	"""
	Función para Key Scheduling Algorithm, genera permutaciones a partir de la llave
	key : llave base
	"""
	S = []
	k = [ord(c) for c in key]
	for i in range(0,256):
		S.append(i)
	j = 0
	for i in range(0,256):
		j = (j + S[i] + k[i % len(k)]) % 256
		aux = S[i]
		S[i] = S[j]
		S[j] = aux
	return S

def prga(S,size):
	"""
	Función para Pseudo-Random Generation Algorithm, genera el "keystream" para el cifrado
	S : arreglo resultante del KSA
	size : tamaño del mensaje (plaintext)
	"""
	i,j = 0,0
	for s in range (0,size):
		i = (i + 1) % 256
		j = (j + S[i]) % 256
		aux = S[i]
		S[i] = S[j]
		S[j] = aux
		K = S[(S[i] + S[j]) % 256]
		yield K

def hexa(number):
	"""
	Convierte un número decimal a uno hexadecimal de 2 dígitos 
	number : número a convertir
	"""
	h = hex(number).split('x')[1]
	if len(h) < 2:
		h = "0" + h
	return h.upper()

def rc4(key,text):
	"""
	Realiza el algoritmo RC4, una operación XOR del mensaje con el keystram
	key : llave a utilizar
	text : mensaje a cifrar
	"""
	c = 0
	result = ''
	keystream = prga(ksa(key),len(text))
	for k in keystream:
		result = result + hexa(ord(text[c]) ^ k)
		c = c + 1
	return result

lines = []

for line in fileinput.input():
	line = line.replace('\n','')
	lines.append(line)

print(rc4(lines[0],lines[1]))
