from bill import Bill

def billme():	
	my_bill = Bill("origin", ["gas"])
	result = my_bill.all()
	print(result)

if __name__ == '__main__':
	billme()