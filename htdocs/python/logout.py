import itchat


def main():
	itchat.auto_login(hotReload=True)
	itchat.logout()
	

if __name__ == '__main__':
	main()