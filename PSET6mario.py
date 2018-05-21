'''This program draws a Mario pyramid, with a user stated height'''

# initilise height for while loop to run
height = -1

while int(height) < 0 or int(height) > 22:
	height = input('Please entere a height for the pyramid: ')

#total number of chars in row
total = int(height) + 1

for row in range(total):
	# create variables for spaces and hashes
	spaces = total - (row + 1)
	hashes = total - (row + 1)
	
	# print spaces
	while spaces > 0:
		print(' ', end = '')
		spaces -= 1
	
	# print hashes
	while hashes < total:
		print('#', end = '')
		hashes += 1

	print('')
