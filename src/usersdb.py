import mysql.connector
from hashfunction import encrypt_password

# connect to the MySQL server using the given host, username, password, port, and database name
mydb = mysql.connector.connect(host='127.0.0.1', user='root', password='1351996', port='3306', database='users_db')
# create a cursor object to execute the database operations
mycursor = mydb.cursor()

def CreateUser(username,pw,email):
    try:
        # query to check if the username or email already exists in the database
        checkRegistrationQuery = f"SELECT username, email FROM users WHERE username = '{username}' OR email = '{email}'"
        mycursor.execute(checkRegistrationQuery)
        # fetch the result of the query
        result = mycursor.fetchall()
        # iterate through the result to check if the username or email already exists
        for user in result:
            if user[0] == f'{username}' and user[1] == f'{email}':
                print("User already exists")
                break
            if user[0] == f'{username}':
                print("Username already exists")
                break
            if user[1] == f'{email}':
                print("Email already exists")
                break
        # insert the new user into the database
        query = f"INSERT INTO users (username,pw,email) VALUES ('{username}','{encrypt_password(pw)}','{email}')"
        mycursor.execute(query)
        mydb.commit()
        print("User successfully created")
    except Exception as e:
        print(e)

def chooseRetrieveUser():
    # print the options for the user to retrieve a single user or all users
    print("Press S to retrieve a single user")
    print("Press A to retrieve all users")
    while True:
        option = input("Enter either 'S' or 'A': ")
        if option in ['S', 'A']:
            break
        else:
            print("Invalid input. Please enter either 'S' or 'A'.")
    
    return option
    
def RetrieveUsers():
    try:
        option = chooseRetrieveUser() # call the chooseRetrieverUser function to retrieve the option selected by the user
        if option == 'A': # query to retrieve all users from the database
            query = "SELECT * FROM users"
            mycursor.execute(query)
        elif option == 'S': # query to retrieve a single user based on the username
            username = input("Select a user to retrieve by passing username: ")
            query = f"SELECT * FROM users WHERE username = '{username}'"
            mycursor.execute(query)

        listOfUsers = mycursor.fetchall()
        # print the retrieved user information
        if len(listOfUsers) == 0:
            print("User not found")
        else:
            for user in listOfUsers:
                print(f"User ID: {user[0]}, Username: {user[1]}, Password: {user[2]}, Email: {user[3]}")
    except Exception as e:
        print(e)

def chooseUpdateUser():
    # print the options for the user to modify username, password, or email
    print("Press U to modify the username")
    print("Press P to modify the password")
    print("Press E to modify the email")
    while True:
        option = input("Enter either 'U' or 'P' or 'E': ")
        if option in ['U', 'P', 'E']:
            break
        else:
            print("Invalid input. Please enter either 'U' or 'P' or 'E'.")

    return option

def verifyUser(user_id):
    # check if the provided user_id exists in the database
    query = f"SELECT username FROM users WHERE user_id = '{user_id}'"
    mycursor.execute(query)
    # fetch the result of the query
    result = mycursor.fetchone()
    currentUsername = input("Submit your current username: ")
    # return True if the input username matches the username in the result
    return currentUsername == result[0]

def verifyUserId(user_id):
    # count the number of rows in the 'users' table
    query = "SELECT COUNT(*) FROM users"
    mycursor.execute(query)
    maxUserId = mycursor.fetchone()
     # return True if the provided user_id is within the range [1, maxUserId]
    return (user_id >=1 and user_id <= maxUserId[0])


def UpdateUser(user_id):
    try:
        option = chooseUpdateUser() # calls the chooseUpdateUser function to retrieve the option selected by user
        if option == 'U':
            username = input("Select a new username: ")
            query = f"UPDATE users SET username = '{username}' WHERE user_id = {user_id}" # update the username in database
            mycursor.execute(query) 
        elif option == 'P':
            password = input("Select a new password: ")
            query = f"UPDATE users SET pw = '{encrypt_password(password)}' WHERE user_id = {user_id}" # update the password in database
            mycursor.execute(query) 
        elif option == 'E':
            email = input("Select a new email: ")
            query = f"UPDATE users SET email = '{email}' WHERE user_id = {user_id}" # update the email in database
            mycursor.execute(query)
        mydb.commit() 
        print("User updated successfully")
    except Exception as e:
        print(e)

def DeleteUser(username):
    try:
        query = f"SELECT COUNT(*) FROM users WHERE username = '{username}'" # check if the user with the specified username exists in the database
        mycursor.execute(query)
        # fetch the result of the query
        result = mycursor.fetchone()
        if result[0] == 1: # if the result count is 1, the user exists and can be deleted
            query = f"DELETE FROM users WHERE username = '{username}'" # delete the user from database with specified username
            mycursor.execute(query) 
            mydb.commit() 
            print("User deleted successfully")
        else:
            print("Error: User does not exist, hence can't removed.")
    except Exception as e:
        print(e)

def resetCounter():
    try:
        mycursor.execute("SET SQL_SAFE_UPDATES = 0") # set safe updates to 0
        mycursor.execute("SET @num := 0") # set num to 0
        mycursor.execute("UPDATE users SET user_id = @num := (@num+1)") # update the user_id to start from 1
        mycursor.execute("ALTER TABLE users AUTO_INCREMENT = 1") # set auto increment to 1
        mydb.commit() 
    except Exception as e:
        print(e)

def LoginUser(username,pw):
    # check if the provided username and encrypted password match with the database
    checkAuthenticationQuery = f"SELECT COUNT(*) FROM users WHERE username = '{username}' AND pw = '{encrypt_password(pw)}'"
    mycursor.execute(checkAuthenticationQuery)
    # fetch the result of the query
    result = mycursor.fetchone()
    if result[0] == 1: # check if the number of rows returned is 1, meaning the username and password match
        print("You have successfully logged in")
    else:
        print("Error: The username or password is incorrect")

def closeConnection():
    # close the cursor
    mycursor.close()
    # close the database connection
    mydb.close()