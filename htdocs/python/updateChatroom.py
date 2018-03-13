import itchat
import sys

def main():
	reload(sys)
	sys.setdefaultencoding('utf8')

	fd = open("../php/chatrooms.txt", "w");

	itchat.auto_login(hotReload=True)

	for room in itchat.get_chatrooms(update=True):
		fd.write(room.NickName.decode('utf-8') + "\n")

	fd.close();


if __name__ == '__main__':
	main()