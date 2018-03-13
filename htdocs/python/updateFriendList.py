import itchat
import sys

def main():

	reload(sys)
	sys.setdefaultencoding('utf8')
	itchat.auto_login(hotReload=True)
	
	for friend in itchat.get_friends(update=True):
		print(friend["NickName"])




if __name__ == '__main__':
    main()