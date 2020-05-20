# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 07:08:53 2020

@author: deonv
"""
import time
start = time.time()

KEY = [99, 100, 101, 103, 223, 0x55, 0x44, 0x33, 0x22, 0x11]

m1= KEY[0] #99
m2= KEY[1] #100 
m3= KEY[2] #101
m4= KEY[3] #103
k = KEY[4] #223

class SkipJack:
	def __init__(self):
		# F is an 8-bit S-box
		self.F = []
		self.defineF()
		# w1, w2, w3, w4 are 20-bit integers
		self.w1 = 0
		self.w2 = 0
		self.w3 = 0
		self.w4 = 0



	# ciphertext is a 80-bit integer
	# key is a list of 10-bytes
	def decrypt(self, ciphertext, key):
		self.splitWord(ciphertext)

		for round in reversed(range(1, 33)):
			if (5 <= round <= 8) or (13 <= round <= 16) or (21 <= round <= 24) or (29 <= round <= 32):
				self.Binv(round, key)
			if (1 <= round <= 4) or (9 <= round <= 12) or (17 <= round <= 20) or (25 <= round <= 28):
				self.Ainv(round, key)


		return self.ApplyDemodFun()


	def Ainv(self, round, key):
		c1 = self.w1
		c2 = self.w2
		self.w1 = self.Ginv(round, key, c2)
		self.w2 = self.w3
		self.w3 = self.w4
		self.w4 = c1 ^ c2 ^ round



	def Binv(self, round, key):
		c1 = self.w1
		self.w1 = self.Ginv(round, key, self.w2)
		self.w2 = self.Ginv(round, key, self.w2) ^ self.w3 ^ round
		self.w3 = self.w4
		self.w4 = c1




	# w is a 20-bit integer
	def Ginv(self, round, key, w):
		g = [0] * 6
		g[4] = (w >> 10) & 0x3ff
		g[5] = w & 0x3ff
		j = (4 * (round - 1) + 3) % 10

		for i in reversed(range(4)): # gives i=3,2,1,0
			g[i] = self.F[(g[i + 1] ^ key[j]) & 0xff] ^ g[i + 2]
			j = (j - 1) % 10

		return (g[0] << 10) | g[1]


	# append the four 20-bit words w1,w2,w3,w4 to return a 80-bit word
	def appendWords(self):
		x1 = self.w1 << 3 * 20
		x2 = self.w2 << 2 * 20
		x3 = self.w3 << 1 * 20
		x4 = self.w4
		#print(self.w1,self.w2,self.w3,self.w4)
		return x1 | x2 | x3 | x4


	# w is a 80-bit word. This function splits w into 
	# four 20-bit words which are stored in w1, w2, w3, w4
	def splitWord(self, w):
		self.w1 = (w >> (20 * 3)) & 0xfffff
		self.w2 = (w >> (20 * 2)) & 0xfffff
		self.w3 = (w >> (20 * 1)) & 0xfffff
		self.w4 = w & 0xfffff
		#print("split")
		#print(self.w1,self.w2,self.w3,self.w4)


	# print the round number and the current values of w1,w2,w3,w4
	def printStatus(self, round):
		w = self.appendWords()
		print("round=" + str(round) + "  " + str(w))


	def defineF(self):
		self.F = [0xa3, 0xd7, 0x09, 0x83, 0xf8, 0x48, 0xf6, 0xf4, 0xb3, 0x21, 0x15, 0x78, 0x99, 0xb1, 0xaf, 0xf9,
			0xe7, 0x2d, 0x4d, 0x8a, 0xce, 0x4c, 0xca, 0x2e, 0x52, 0x95, 0xd9, 0x1e, 0x4e, 0x38, 0x44, 0x28,
			0x0a, 0xdf, 0x02, 0xa0, 0x17, 0xf1, 0x60, 0x68, 0x12, 0xb7, 0x7a, 0xc3, 0xc9, 0xfa, 0x3d, 0x53,
			0x96, 0x84, 0x6b, 0xba, 0xf2, 0x63, 0x9a, 0x19, 0x7c, 0xae, 0xe5, 0xf5, 0xf7, 0x16, 0x6a, 0xa2,
			0x39, 0xb6, 0x7b, 0x0f, 0xc1, 0x93, 0x81, 0x1b, 0xee, 0xb4, 0x1a, 0xea, 0xd0, 0x91, 0x2f, 0xb8,
			0x55, 0xb9, 0xda, 0x85, 0x3f, 0x41, 0xbf, 0xe0, 0x5a, 0x58, 0x80, 0x5f, 0x66, 0x0b, 0xd8, 0x90,
			0x35, 0xd5, 0xc0, 0xa7, 0x33, 0x06, 0x65, 0x69, 0x45, 0x00, 0x94, 0x56, 0x6d, 0x98, 0x9b, 0x76,
			0x97, 0xfc, 0xb2, 0xc2, 0xb0, 0xfe, 0xdb, 0x20, 0xe1, 0xeb, 0xd6, 0xe4, 0xdd, 0x47, 0x4a, 0x1d,
			0x42, 0xed, 0x9e, 0x6e, 0x49, 0x3c, 0xcd, 0x43, 0x27, 0xd2, 0x07, 0xd4, 0xde, 0xc7, 0x67, 0x18,
			0x89, 0xcb, 0x30, 0x1f, 0x8d, 0xc6, 0x8f, 0xaa, 0xc8, 0x74, 0xdc, 0xc9, 0x5d, 0x5c, 0x31, 0xa4,
			0x70, 0x88, 0x61, 0x2c, 0x9f, 0x0d, 0x2b, 0x87, 0x50, 0x82, 0x54, 0x64, 0x26, 0x7d, 0x03, 0x40,
			0x34, 0x4b, 0x1c, 0x73, 0xd1, 0xc4, 0xfd, 0x3b, 0xcc, 0xfb, 0x7f, 0xab, 0xe6, 0x3e, 0x5b, 0xa5,
			0xad, 0x04, 0x23, 0x9c, 0x14, 0x51, 0x22, 0xf0, 0x29, 0x79, 0x71, 0x7e, 0xff, 0x8c, 0x0e, 0xe2,
			0x0c, 0xef, 0xbc, 0x72, 0x75, 0x6f, 0x37, 0xa1, 0xec, 0xd3, 0x8e, 0x62, 0x8b, 0x86, 0x10, 0xe8,
			0x08, 0x77, 0x11, 0xbe, 0x92, 0x4f, 0x24, 0xc5, 0x32, 0x36, 0x9d, 0xcf, 0xf3, 0xa6, 0xbb, 0xac,
			0x5e, 0x6c, 0xa9, 0x13, 0x57, 0x25, 0xb5, 0xe3, 0xbd, 0xa8, 0x3a, 0x01, 0x05, 0x59, 0x2a, 0x46]

	def ApplyDemodFun(self):
		#print(self.w1,self.w2,self.w3,self.w4)
		M = m1*m2*m3*m4
		M1 = int(M/m1)
		M2 = int(M/m2)
		M3 = int(M/m3)
		M4 = int(M/m4)
        #find inverse of k wrt M1,M2,M3,M4
		kinv1 = self.modulo_multiplicative_inverse(k,M1)
		kinv2 = self.modulo_multiplicative_inverse(k,M2)
		kinv3 = self.modulo_multiplicative_inverse(k,M3)
		kinv4 = self.modulo_multiplicative_inverse(k,M4)
        
		x1= (self.w1*kinv1) % M1
		x2= (self.w2*kinv2) % M2
		x3= (self.w3*kinv3) % M3
		x4= (self.w4*kinv4) % M4
		#print(kinv1,kinv2,kinv3,kinv4)
		#print(x1,x2,x3,x4)
        
		PT1 = (x1*m1) % M1
		PT2 = (x2*m2) % M2
		PT3 = (x3*m3) % M3
		PT4 = (x4*m4) % M4	
		#print("Plain text: %d %d %d %d" %(PT1,PT2,PT3,PT4))
		return(str(PT1).zfill(6)+str(PT2).zfill(6)+str(PT3).zfill(6)+str(PT4).zfill(6))
        
        
	def modulo_multiplicative_inverse(self,A, M):
		"""
        Assumes that A and M are co-prime
        Returns multiplicative modulo inverse of A under M
        """
        # Find gcd using Extended Euclid's Algorithm
		gcd, x, y = self.extended_euclid_gcd(A, M)
    
        # In case x is negative, we handle it by adding extra M
        # Because we know that multiplicative inverse of A in range M lies
        # in the range [0, M-1]
		if x < 0:
		    x += M
        
		return x

	def extended_euclid_gcd(self,a, b):
		"""
        Returns a list `result` of size 3 where:
        Referring to the equation ax + by = gcd(a, b)
            result[0] is gcd(a, b)
            result[1] is x
            result[2] is y 
        """
		s = 0; old_s = 1
		t = 1; old_t = 0
		r = b; old_r = a
    
		while r != 0:
		    quotient = old_r//r # In Python, // operator performs integer or floored division
            # This is a pythonic way to swap numbers
            # See the same part in C++ implementation below to know more
		    old_r, r = r, old_r - quotient*r
		    old_s, s = s, old_s - quotient*s
		    old_t, t = t, old_t - quotient*t
		return [old_r, old_s, old_t]

        



# example
PT=""
ciphertext_file = open("Ciphertext.txt", "r",encoding="utf-8")
finalCT=ciphertext_file.read()
ciphertext_file.close()
#print(len(finalCT))
xCT=""
#print(len(finalCT))
for i in range(len(finalCT)):
    if(i%8==0):
        xCT=xCT+str(ord(finalCT[i])).zfill(4)
        #print("%s - %s" %(finalCT[i],ord(finalCT[i])))
    else:
        xCT=xCT+str(ord(finalCT[i])).zfill(3) 
        #print("%s - %s" %(finalCT[i],ord(finalCT[i])))

#print(xCT)
for i in range(0,len(xCT),25):
    CT=int(xCT[i:i+25])
    #print(CT)
    sj = SkipJack()
    DT = sj.decrypt(CT, KEY)
    #print(DT)
    for j in range(0,24,3):
        if(i+25==len(xCT) and DT[j:j+3]=="000"):
            continue
        #print(DT[j:j+3])
        PT+=chr(int(DT[j:j+3]))
    #print("\nCipher text block %s:%s" %(int((i/24)+1),CT))

 
print("Recerver Side\nDecrypted PT:\n" , PT)# should match the plain text
    
decrypted_file = open("Decryptedtext.txt", "w",encoding="utf-8")
decrypted_file.write("%s" % PT)
decrypted_file.close()
print (time.time()- start)