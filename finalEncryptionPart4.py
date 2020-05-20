# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 07:08:38 2020

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


	# plaintext is a 80-bit integer
	# key is a list of 10-bytes
	def encrypt(self, key):

		for round in range (1, 33):
			if (1 <= round <= 4) or (9 <= round <= 12) or (17 <= round <= 20) or (25 <= round <= 28):
				self.A(round, key)
				#self.printStatus(round)
			elif (5 <= round <= 8) or (13 <= round <= 16) or (21 <= round <= 24) or (29 <= round <= 32):
				self.B(round, key)
				#self.printStatus(round)

		return self.appendWords()



	def A(self, round, key):
		c1 = self.w1
		c2 = self.w2
		c3 = self.w3
		self.w1 = self.G(round, key, c1) ^ self.w4 ^ round
		self.w2 = self.G(round, key, c1)
		self.w3 = c2
		self.w4 = c3



	def B(self, round, key):
		c1 = self.w1
		c2 = self.w2
		c3 = self.w3
		self.w1 = self.w4
		self.w2 = self.G(round, key, c1)
		self.w3 = c1 ^ c2 ^ round
		self.w4 = c3



	# w is a 20-bit integer
	def G(self, round, key, w):
		g = [0] * 6
		g[0] = (w >> 10 ) & 0x3ff
		g[1] = w & 0x3ff
		j = (4 * (round - 1)) % 10
		for i in range(2, 6): # gives i = 2,3,4,5
			g[i] = self.F[(g[i - 1] ^ key[j]) & 0xff] ^ g[i - 2] 
			j = (j + 1) % 10

		return (g[4] << 10) | g[5] 



	# append the four 16-bit words w1,w2,w3,w4 to return a 64-bit word
	def appendWords(self):
		x1 = self.w1 << 3 * 20
		x2 = self.w2 << 2 * 20
		x3 = self.w3 << 1 * 20
		x4 = self.w4
		#print(self.w1,self.w2,self.w3,self.w4)
		return x1 | x2 | x3 | x4


	# w is a 64-bit word. This function splits w into 
	# four 16-bit words which are stored in w1, w2, w3, w4
	def splitWord(self, w):
		self.w1 = (w >> (20 * 3)) & 0xfffff
		self.w2 = (w >> (20 * 2)) & 0xfffff
		self.w3 = (w >> (20 * 1)) & 0xfffff
		self.w4 = w & 0xfffff
        

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

	def ApplyModFun(self,PT1,PT2,PT3,PT4):
		M = m1*m2*m3*m4
		M1 = int(M/m1)
		M2 = int(M/m2)
		M3 = int(M/m3)
		M4 = int(M/m4)
        
		X1 = self.modulo_multiplicative_inverse(m1,M1)
		X2 = self.modulo_multiplicative_inverse(m2,M2)
		X3 = self.modulo_multiplicative_inverse(m3,M3)
		X4 = self.modulo_multiplicative_inverse(m4,M4)

		x1= (PT1*X1) % M1
		x2= (PT2*X2) % M2
		x3= (PT3*X3) % M3
		x4= (PT4*X4) % M4

		#print("x1,x2,x3,x4")
		#print(x1,x2,x3,x4)
		self.w1= (x1*k) % M1
		self.w2= (x2*k) % M2
		self.w3= (x3*k) % M3
		self.w4= (x4*k) % M4
		#print("Cipher text after applying Mod Fun: %d %d %d %d" %(self.w1,self.w2,self.w3,self.w4))
    
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

xCT=""
finalCT=""
plaintext_file = open("Plaintext.txt", "r",encoding="utf-8")
s=plaintext_file.read()
plaintext_file.close()

b=[str(ord(x)).zfill(3) for x in s ]
#print(b)

b="".join([(x)for x in b if len(x)==3])
#print(b)

for i in range(0,len(b),24):          
    PT1=b[i:i+6]
    PT2=b[i+6:i+12]
    PT3=b[i+12:i+18]
    PT4=b[i+18:i+24]
    PT = PT1+PT2+PT3+PT4 
    #print(PT)
    PT1 = int(PT1)
    if(PT2 == ""):
        PT2=0
    else:
        PT2 = int(PT2)

    if(PT3 == ""):
        PT3=0
    else:
        PT3 = int(PT3)
   
    if(PT4 == ""):
        PT4=0
    else:
        PT4= int(PT4)
    
    sj = SkipJack()
    #print("\nPlain text block %s:%s" %(int((i/24)+1),PT))
    sj.ApplyModFun(PT1,PT2,PT3,PT4)

    CT = sj.encrypt(KEY)
    #print("Cipher text after applying Skipjack:" + str(CT))
    xCT=str(CT).zfill(25)
    PT=""
    #print(xCT)
    finalCT=finalCT+chr(int(xCT[0:4]))
    #print(xCT[0:4],chr(int(xCT[0:4])))
    #print(xCT[0:4])
    #print(chr(int(xCT[0:4])))
    #print(ord(chr(int(xCT[0:4]))))
    #print(xCT,len(xCT))
    for j in range(4,len(xCT),3):
        finalCT=finalCT+chr(int(xCT[j:j+3]))
        #print(xCT[j:j+3],chr(int(xCT[j:j+3])))


print("Sender Side\nOriginal Plain text :\n",s)
print("Final Cypher Text :\n",finalCT)

ciphertext_file = open("Ciphertext.txt", "w",encoding="utf-8")
ciphertext_file.write("%s" % finalCT)
ciphertext_file.close()
print (time.time()- start)