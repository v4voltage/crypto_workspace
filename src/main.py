import usersdb

def menu():
    print()
    print("Hello")
    print("Welcome to this program")
    print()
    print("Press 1 to create a user")
    print("Press 2 to retrieve a user")
    print("Press 3 to update a user")
    print("Press 4 to delete a user")
    print("Press 5 to login to your account")
    print("Press 0 to exit the program")
    print()

menu()

option = int(input("Enter your option: "))
print()
# Keep looping until option 0 is selected
while option != 0:
    if option == 1:
        username = input("Select a username: ")
        pw = input("Select a password: ")
        email = input("Select an email: ")
        usersdb.CreateUser(username,pw,email)
        usersdb.resetCounter()
    elif option == 2:
        usersdb.RetrieveUsers()
    elif option == 3:
        user_id = int(input("Select a user id: "))
        if (usersdb.verifyUserId(user_id)):
            if (usersdb.verifyUser(user_id)):
                usersdb.UpdateUser(user_id)
            else:
                print("Error: Wrong credentials")
        else:
            print("Error: User id does not exist")
    elif option == 4:
        username = input("Select a username: ")
        usersdb.DeleteUser(username)
        usersdb.resetCounter()
    elif option == 5:
        username = input("Enter your username: ")
        pw = input("Enter your password: ")
        usersdb.LoginUser(username,pw)
    else:
        print()
        print("Invalid option. Please try another option")

    print()
    option = int(input("Enter your option: "))

print()
print("Thanks for using this program. Goodbye")
usersdb.closeConnection()