'''Implements a Vigenere cipher with user defined key like so "./python PSET6vigenere ABC". Accept key after correct usage, add it to plaintext ascii, If the ciphered letter is above wrap around, minus so it is offset correct'''

import sys

def main():
	'''Requests code from user and returns coded output'''

	# ensure proper usage
	if len(sys.argv) != 2 or len(sys.argv) > 2:
		sys.exit()

	# start only if passed correctly
	else:	
		counter = 0

		plaintext = input('plaintext: ')

		print('ciphertext:', end = '')

		for i in plaintext:
			
			if i.isalpha() == 0:
				print(i, end = '')		

			if i.isalpha():
				
				# restore key's initial value, based on counter
				key = sys.argv[1][counter % len(sys.argv[1])]
				counter += 1

				# only way to assign, otherwise, can't assign to function call
				key = ord(key)

				if i.isupper():
					# key for upper

					key -= 65

					#65 == A, 91 == Z

					# wrap around if needed
					if ((ord(i) - 65) + key) % 26 > 26:
						print(chr(((ord(i) - 91) + key) % 26 + 65), end = '')
					# or print normally if not
					else:
						print(chr(((ord(i) - 65) + key) % 26 + 65), end = '')

				else:
					# key for lower

					key -= 97

					#97 == a, 123 == z
					# wrap around if needed
					if ((ord(i) - 97) + key) % 26 > 26:
						print(chr(((ord(i) - 123) + key) % 26 + 97), end = '')
					# or print normally if not
					else:
						print(chr(((ord(i) - 97) + key) % 26 + 97), end = '')

	print()
	sys.exit()

if __name__ == '__main__':
	main()