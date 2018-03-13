import itchat


def main():
	if itchat.load_login_status('../php/itchat.pkl'):
		print(200)
	else:
		print(400)
	

if __name__ == '__main__':
	main()