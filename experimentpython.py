users = {
    'dhanu1': {'following': [], 'followers': [], 'blocked': [], 'private': False, 'req': []},
    'amrit1': {'following': [], 'followers': [], 'blocked': [], 'private': False, 'req': []},
    'aadit1': {'following': [], 'followers': [], 'blocked': [], 'private': False, 'req': []}
}

print('''1. Add Follower
2. Remove Follower
3. Accept or Reject Request
4. Block Users
5. View Followers
6. View Mutual Followers
7. Get Number of Followers
8. Suggest Users to Follow
9. Exit''')

def add():
    user1 = input('User: ')
    f = input('Follow: ')
    if user1 in users and f in users:
        if f in users[user1]['blocked']:
            print(f"You cannot follow {f} because they have blocked you.")
            return
        if users[f]['private']:
            users[f]['req'].append(user1)
            print(f"Follow request sent to {f}.")
        elif f not in users[user1]['following']:
            users[user1]['following'].append(f)
            users[f]['followers'].append(user1)
            print(f"{user1} is now following {f}.")
        else:
            print(f"{user1} is already following {f}.")
    else:
        print("Invalid users.")

def remove():
    user1 = input('User: ')
    f = input('Remove: ')
    if user1 in users and f in users and f in users[user1]['following']:
        users[user1]['following'].remove(f)
        users[f]['followers'].remove(user1)
        print(f"{user1} has unfollowed {f}.")
    else:
        print("Invalid operation.")

def accept():
    user1 = input('User: ')
    if user1 in users and users[user1]['req']:
        for i in users[user1]['req'][:]:
            ch = input(f'{i} wants to follow you. Accept? (y/n): ')
            if ch.lower() == 'y':
                users[i]['following'].append(user1)
                users[user1]['followers'].append(i)
            users[user1]['req'].remove(i)
        print(f"Follow requests for {user1} processed.")
    else:
        print("No follow requests or invalid user.")

def block():
    user1 = input('User: ')
    bl = input('Block: ')
    if user1 in users and bl in users:
        if bl not in users[user1]['blocked']:
            users[user1]['blocked'].append(bl)
            users[bl]['following'] = [f for f in users[bl]['following'] if f != user1]
            users[user1]['followers'] = [f for f in users[user1]['followers'] if f != bl]
            print(f"{bl} has been blocked by {user1}.")
        else:
            print(f"{bl} is already blocked by {user1}.")
    else:
        print("Invalid users.")

def follower():
    user1 = input('User: ')
    if user1 in users:
        print(f"Followers of {user1}: {users[user1]['followers']}")
    else:
        print("Invalid user.")

def mutual():
    u1 = input('User 1: ')
    u2 = input('User 2: ')
    if u1 in users and u2 in users:
        mutual_followers = list(set(users[u1]['followers']) & set(users[u2]['followers']))
        print(f"Mutual followers of {u1} and {u2}: {mutual_followers}")
    else:
        print("Invalid users.")

def number_followers():
    user1 = input('User: ')
    if user1 in users:
        print(f"Number of followers for {user1}: {len(users[user1]['followers'])}")
    else:
        print("Invalid user.")

def suggest():
    user1 = input('User: ')
    if user1 in users:
        suggestions = {u3 for u2 in users[user1]['following'] for u3 in users[u2]['following'] 
                       if u3 != user1 and u3 not in users[user1]['following']}
        print(f"Suggestions for {user1}: {list(suggestions)}")
    else:
        print("Invalid user.")

while True:
    print("\n")
    choice = input("Enter choice: ")
    if choice.isdigit():
        choice = int(choice)
        if choice == 1:
            add()
        elif choice == 2:
            remove()
        elif choice == 3:
            accept()
        elif choice == 4:
            block()
        elif choice == 5:
            follower()
        elif choice == 6:
            mutual()
        elif choice == 7:
            number_followers()
        elif choice == 8:
            suggest()
        elif choice == 9:
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
    else:
        print("Invalid input. Please enter a number.")
