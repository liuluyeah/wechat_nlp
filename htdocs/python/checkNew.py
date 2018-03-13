import itchat
import sys
import codecs

oldList = set()

def readOldList():
	old_fd = codecs.open("../php/friendList.txt", "r", "utf-8")

	while True:
		friend = old_fd.readline()
		if not friend:
			break
		friend = friend.strip("\n")
		oldList.add(friend)

def main():

	itchat.auto_login(hotReload=True)
	readOldList()

	new_fd = codecs.open("../php/newFriends.txt", "w", "utf-8")

	reload(sys)
	sys.setdefaultencoding('utf8')


	for friend in itchat.get_friends(update=True):
		if not (friend["NickName"] in oldList):
			new_fd.write(friend["NickName"] + "\n")

if __name__ == '__main__':
    main()