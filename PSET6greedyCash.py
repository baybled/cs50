'''This program runs the greedy cash algorithm'''

def main():
	'''Gets the values of user spending and returns change'''
	
	cost = input('How much did the customer spend: ')

	paid = input('and how much did they pay with: ')

	owed = (float(paid) - float(cost)) * 100
	
	payQuarters = owed / 25

	owed = owed - int(payQuarters) * 25
	
	payTens = owed / 10

	owed = owed - int(payTens) * 10
	
	payFives = owed / 5

	owed = owed - int(payFives) * 5
	
	payPennies = owed

	print('Please give back {:.0f} quarters, {:.0f} tens, {:.0f} fives and {:.0f} cents'.format(payQuarters, payTens, payFives, payPennies))


if __name__ == '__main__':
	main()