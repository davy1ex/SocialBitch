# import random

from vk_api import *
from vk_api.exceptions import ApiError
from vk_api.longpoll import *

actions = 0
ACTION_LIMIT = 190


def menu():
	print()
	for index, paragraph in enumerate(["Exit", "Get subs", "Add all subs", "Be bitch"], 0):
		print("[{0}] {1}".format(index, paragraph), "\n")
	#print("\n")

def getMe():
	# global vk
	info = vk.users.get(fields="nickname")
	return info

def auth(token=""):
	""" authentication """
	token = "670b31862e15c59168dcae17c978ff19f622d3183f1d21b650a9852e95a3c0eaf7007f360a448b210c7f4"
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
	subs = vk.users.getFollowers()["items"]
	# print(subs)
	if len (subs) > 0:
		for index, user_id in enumerate(subs, 1):
			print("{0}. {1}".format(index, user_id))
			# take_in_frends(user_id=id)
		return subs
	else:
		print("Not found")
		return None

def take_in_frends(user_id, follow=0):
	user_id = int(user_id)
	if follow == 0 or follow == 1:
		vk.friends.add(user_id=user_id, follow=follow)
		global actions
		actions += 1
		# vk.messages.send(user_id=user_id, message="жопа")
	else:
		return "ERROR: follow must be 1 or 0"
	if follow == 0:
		print("Add this user: {}".format(user_id))
		print("Actions today:", actions, "\n")
	elif follow == 1:
		print("Rejected this user's request: {}".format(user_id), "\n")

# 154597302
if __name__ == "__main__":
	print("-"*13, " SocialBlyad_bot by davy1ex ", "-"*13)
	auth(token=input("Token: "))
	# getMe()
	# get_id_followers()
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
	# take_in_frends(user_id=input(""))
	#print(vk.users.getFollowers())
	#print(get_id_followers())