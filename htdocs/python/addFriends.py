import itchat
import sys

friendList = set()

def main():
	reload(sys)
	sys.setdefaultencoding('utf8')

	itchat.auto_login(hotReload=True)

	chatroom = sys.argv[1]

	for friend in itchat.get_friends(update=True):
		friendList.add(friend["UserName"])

	for user in itchat.update_chatroom((itchat.search_chatrooms(name=chatroom))[0]['UserName'], detailedMember=True)['MemberList']:
		if not (user["UserName"] in friendList):
			itchat.add_friend(user['UserName'])


if __name__ == '__main__':
	main()