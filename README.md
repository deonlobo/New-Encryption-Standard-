# New-Encryption-Technique 
I created a new encryption standard using the concept of modulular multiplicative inerse and integrated it with skipjack encryption standard to make a powerful encryption technique 

#Here is how my Modular Multiplicative encryption technique works .

#check solved example.pdf for the worked out problem 

#for detailed information download report 

Encryption:

Steps Applied for the encipher mod function :

Step1: The plain text is 80 bit blocks divided into four 20 bit words say P1,P2,P3,P4

Step2: Find m1,m2,m3,m4 such that :

  (mi*mj*mk)≈ 2^20

  m1,m2,m3,m4 are pairwise co-prime

  Difference between each pair m1,m2,m3,m4 is minimum

Step 3: M=(m1*m2*m3*m4)
  
  Mi = M/mi        where (i=1,2,3,4)

Step 4: Xi = (mi*〖mi〗^(-1)) ≡ 1 mod Mi

  i.e. Xi is the modular multiplicative inverse of mi wrt Mi

Step 5: xi = (Pi*Xi) mod Mi

Step 6: wi = (xi*k) mod Mi        where (k*k^(-1)) ≡1 mod Mi


Step 7: Send w1,w2,w3,w4 to the skipjack algorithm .

  w1,w2,w3,w4 are 20 bit integers 

Step 8: The ciphertext produced is of 80 bits


Decryption:

Step 1: Apply Skipjack Algorithm to decipher and get w1,w2,w3,w4

Step 2 : Apply decipher Mod function on w1,w2,w3,w4 

   M=(m1*m2*m3*m4)
	
   Mi = M/mi        where (i=1,2,3,4)

Step 3 : xi = (wi*〖ki〗^(-1)) mod Mi         where 〖ki〗^(-1) is the inverse of k wrt Mi

Step 4: Pi = (xi*mi) mod Mi
