from vk_api import *
from vk_api.exceptions import ApiError
from vk_api.longpoll import *

actions = 0
ACTION_LIMIT = 190


def menu():
	""" show text menu """
	print()
	for index, paragraph in enumerate(["Exit", "Get subs", "Add all subs", "Be bitch"], 0):
		print("[{0}] {1}".format(index, paragraph), "\n")

def getMe():
	""" receives information about the authorized user """
	info = vk.users.get(fields="nickname")
	return info

def auth(token):
	""" authentication """
	try:
		v = VkApi(token=token)
		lp = VkLongPoll(v)
		global vk
		vk = v.get_api()

		first_name = getMe()[0]["first_name"]
		last_name = getMe()[0]["last_name"]
		name = first_name + " " + last_name
		print("{0}: Authorization completed successfully".format(name))
	except ApiError:
		print("ERROR: Invalid token")
		auth(token=input("Try again: "))

def get_id_followers(user_id=None):
	""" receives id of subscribers """
	subs = vk.users.getFollowers()["items"]
	if len (subs) > 0:
		for index, user_id in enumerate(subs, 1):
			print("{0}. {1}".format(index, user_id))
		return subs
	else:
		print("Not found")
		return None

def take_in_frends(user_id, follow=0):
	""" adds to friends """
	user_id = int(user_id)
	if follow == 0 or follow == 1:
		vk.friends.add(user_id=user_id, follow=follow)
		global actions
		actions += 1
	else:
		return "ERROR: follow must be 1 or 0"
	if follow == 0:
		print("Add this user: {}".format(user_id))
		print("Actions today:", actions, "\n")
	elif follow == 1:
		print("Rejected this user's request: {}".format(user_id), "\n")

if __name__ == "__main__":
	print("-"*13, " SocialBitch_bot by davy1ex ", "-"*13)
	auth(token=input("Token: "))
	menu()
	choice = ""
	while choice != "0":
		choice = input()
		if choice == "1":
			get_id_followers()
		elif choice == "2":
			ids = get_id_followers()
			if ids != None:
				for user_id in ids:
					take_in_frends(user_id=user_id)
		elif choice == "3":
			print("Coming soon")
		print("")
