import random
from time import sleep

from vk_api import *
from vk_api.exceptions import ApiError
from vk_api.longpoll import *

actions = 0
REQUESTS_PER_DAY = 10


def menu():
    """ show text menu """
    print()
    for index, paragraph in enumerate(["Exit", "Add all subs", "Be bitch"], 0):
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
        print("ERROR: Invalid token", "\n")
        auth(token=input("Try again: "))

def get_id_followers(user_id=None):
    """ receives id of subscribers """
    subs = vk.users.getFollowers()["items"]
    if len (subs) > 0:
        for index, user_id in enumerate(subs, 1):
            print("{0}. {1}".format(index, user_id))
        return subs
    else:
        print("Subscribers not found :(")
        return None

def take_in_frends(user_id, follow=0, text=None):
    """ adds to friends """
    user_id = int(user_id)
    if follow == 0 or follow == 1:
        try:
            vk.friends.add(user_id=user_id, follow=follow, text=text)
            global actions
            actions += 1
        except ApiError:
             pass
        except Captcha:
            print("Oops, it seems to have finished. Suddenly there was a capcha, wait a little...\nTry:\n\t1. Wait a bit;\n\t2. Follow the link: https://vk.com/dev/friends.add and try it manually.")
        
    else:
        return "ERROR: follow must be 1 or 0"
    if follow == 0:
        print("Add this user: {}".format(user_id))
        print("Actions today:", actions, "\n")
    elif follow == 1:
        print("Rejected this user's request: {}".format(user_id), "\n")

if __name__ == "__main__":
    print("-"*13, " SocialBitch_bot by davy1ex ", "-"*13, "\n")
    auth(token=input("Token: "))
    menu()
    choice = ""
    while choice != "0":
        choice = input()
        if choice == "1":
            ids = get_id_followers()            
            if ids != None and actions < REQUESTS_PER_DAY:
                for user_id in ids:
                    take_in_frends(user_id=user_id)
            elif actions >= REQUESTS_PER_DAY:
                print("Exhausted action limit from this account, come back tomorrow")
        elif choice == "2":
            print("actions", actions)
            print("actions limit", REQUESTS_PER_DAY)
            MY_FRIENDS_0 = vk.friends.get()["items"]
            my_friends = vk.friends.get()["items"]
            my_friends_count = vk.friends.get()["count"]
            suckers = vk.friends.getRequests(out=1)["items"]
            print("Found:", my_friends)
            for i in range(random.randint(1, my_friends_count + 1)):
                friend = random.choice(my_friends)
                try:
                    friends_friend = vk.friends.get(user_id=friend)["items"]
                except ApiError:
                    continue
                for friend_f in friends_friend:
                    if friend_f not in MY_FRIENDS_0 and actions < REQUESTS_PER_DAY and friend_f not in suckers:
                        take_in_frends(user_id=friend_f)
                        sleep(3)
                    elif actions >= REQUESTS_PER_DAY:
                        print("Exhausted action limit from this account, come back tomorrow")
                        exit()
                my_friends.remove(friend)
        print("")
    print("Good bye.")
