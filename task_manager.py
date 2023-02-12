#====importing libraries====
import datetime
import os.path
#====Define functions for task management system
def reg_user(username_input,username): #check if current user is admin and allow admin to register new user only
    if username_input != "admin":
            print("You are not allowed to register new user! Please contact admin instead!")
    else:
        username_new = input("Please enter username of the new user: ")
        while username_new in username:# check if new username is not same as any existing username
            print("The username has been used by the other, please enter again!")
            username_new = input("Please enter username of the new user: ")
        password_new = input("Please enter password of the new user: ")
        password_new_check = input("Please enter the password again: ")
        while password_new != password_new_check: # check if new user password is entered correctly
            print("You have entered a different password, please enter again!")
            password_new = input("Please enter password of the new user: ")
            password_new_check = input("Please enter the password again: ")
        user_data_new = "\n" + username_new + ", " + password_new # construct new user data line & write to 'user.txt' in correct format
        user_data_file = open('user.txt','a')
        user_data_file.write(user_data_new)
        print("New user has been registered successfully!")
        user_data_file.close()

def add_task(): #add a new task to 'tasks.txt' in correct format
    task_assigned_user_new = input("Please enter the username of the person the new task is assigned to: ")
    task_title_new = input("Please enter the title of the new task: ")
    task_description_new = input("Please enter the description of the new task: ")
    current_date = datetime.datetime.now()
    task_assign_date_new = current_date.strftime("%d") + " " + current_date.strftime("%b") + " " + current_date.strftime("%Y")
    task_due_date_new = input("Please enter the due date of the new task (in format of dd mmm yyyy e.g. 25 Oct 2022): ")
    task_completed_new = "No"
    task_new_list = [task_assigned_user_new, task_title_new, task_description_new, task_assign_date_new, 
    task_due_date_new, task_completed_new]
    task_new = ", ".join(task_new_list)
    task_data_file = open('tasks.txt', 'a')
    task_data_file.write("\n"+task_new)
    print(f"New task has been assigned to {task_assigned_user_new}")
    task_data_file.close()

def view_all(): #read each line of 'tasks.txt' and call function "print_task" to display rach and every task on screen
    task_data_file = open('tasks.txt','r')
    for task_data_line in task_data_file:
        task_data_line = task_data_line.strip("\n")
        task_data = task_data_line.split(", ")
        print_task(task_data)
    task_data_file.close()    

def print_task(task_data): #print task on screen in readable manner
    print(f"Task: {task_data[1]}")
    print(f"Assigned to: {task_data[0]}")
    print(f"Date assigned: {task_data[3]}")
    print(f"Due date: {task_data[4]}")
    print(f"Task Complete? {task_data[5]}")
    print(f"Task description: \n {task_data[2]} \n")

#below function is to check if current task is assigned to current user and display on screen accordingly
#return a string list containing each line from 'tasks.txt'
#return a tuple list containing each task of current user and corresponding line number in 'tasks.txt'
def get_my_data(username_input,task_num, line_num, task_data_file, task_string_list, task_key_list):
    for task_data_line in task_data_file:
        task_data_line = task_data_line.strip("\n")
        task_string_list.append(task_data_line)
        task_data = task_data_line.split(", ")
        if username_input == task_data[0]: # check if current user matches with user assigned to current task
            task_num += 1
            tuple = (task_num, line_num)
            task_key_list.append(tuple)
            print(f"Task number: {task_num}")
            print_task(task_data)
        line_num += 1
    return task_string_list, task_key_list

#allow current user to select action on his/her own tasks and amend the corresponding line accordingly
#return a string list containing each line to write to 'tasks.txt'
def select_action(select_task, my_task_to_line_dict, task_string_list):
    select_action = input("Please input m to mark the task as complete, or input e to edit the task: ")
    if select_action == "m":
        selected_task_data = task_string_list[my_task_to_line_dict[select_task]].split(", ")
        selected_task_data[5] = "Yes"
        task_string_list[my_task_to_line_dict[select_task]] = ", ".join(selected_task_data)
    if select_action == "e":
        selected_task_data = task_string_list[my_task_to_line_dict[select_task]].split(", ")
        if selected_task_data[5] == "No":
            data_to_edit = input('''Please input u if you want to edit the username of the person to whom the task is assigned, 
            or input d if you want to edit the due date of the task: ''')
            if data_to_edit == "u":
                selected_task_data[0] = input("Please enter the new username: ")
            if data_to_edit == "d":
                selected_task_data[4] = input("Please enter the new due date in the format of DD MMM YYYY: ")
            task_string_list[my_task_to_line_dict[select_task]] = ", ".join(selected_task_data)
        else:
            print("The task cannot be edited as it is completed!")
    return task_string_list


#allow current user to view his/her own tasks and select specific task for modification by calling "select_action" fucntion
def view_mine(username_input):
    task_data_file = open('tasks.txt','r')
    task_num, line_num = 0, 0
    task_string_list = [] # to store each line in correct line num for rewriting tasks.txt later
    task_key_list = [] # to store task num with respect to line num in txt file
    task_string_list, task_key_list = get_my_data(username_input,task_num, line_num, task_data_file, task_string_list, task_key_list)
    if len(task_key_list) != 0: # check one or more tasks have been assigned to current user
        my_task_to_line_dict = dict(task_key_list) # create a dict so that corresponding line num can be called when task is selected
        select_task = int(input("Please select a specific task by entering task number or input -1 to return to the main menu: "))
        if select_task != -1:
            task_string_list = select_action(select_task, my_task_to_line_dict, task_string_list)
    else:
        print("No tasks has been assigned to this user!")
    task_data_file = open('tasks.txt','w') 
    for i in range(0, len(task_string_list)):
        task_data_file.write(task_string_list[i]+"\n")           
    task_data_file.close()

def summarise_task(): #read 'tasks.txt' and return total number of tasks, completed tasks, uncompleted tasks, overdue tasks.
    task_data_file = open('tasks.txt','r')
    total_task_number, total_completed_task, total_uncompleted_task, total_overdue_task = 0, 0, 0, 0
    for task_data_line in task_data_file:
        task_data_line = task_data_line.strip("\n")
        task_data = task_data_line.split(", ")
        total_task_number += 1
        if task_data[5] == "Yes":
            total_completed_task += 1
        elif datetime.datetime.strptime(task_data[4], "%d %b %Y") < datetime.datetime.now():
            total_uncompleted_task += 1
            total_overdue_task += 1
        else:
            total_uncompleted_task += 1
    return total_task_number, total_completed_task, total_uncompleted_task, total_overdue_task


#below function read 'user.txt' to create a list of user
#and 'tasks.txt' to create lists of users corresponding to each task, completed task, uncompleted task and overdue task
#which is to be used in function "user_total_count" to create dictionaries accordingly for counting purposes
def summarise_user():
    task_data_file = open('tasks.txt','r')
    user_data_file = open('user.txt','r')
    user_count = [] # to count # of user
    user_task = [] # to count # of task of each user
    user_completed = [] # to count # of completed task of each user
    user_uncompleted = [] # to count # of uncompleted task of each user
    user_overdue = [] # to count # of overdue task of each user
    for task_data_line in task_data_file:
        task_data_line = task_data_line.strip("\n")
        task_data = task_data_line.split(", ")
        user_task.append(task_data[0])
        if task_data[5] == "Yes":
            user_completed.append(task_data[0])
        elif datetime.datetime.strptime(task_data[4], "%d %b %Y") < datetime.datetime.now():
            user_uncompleted.append(task_data[0])
            user_overdue.append(task_data[0])
        else:
            user_uncompleted.append(task_data[0])
    for user_data_line in user_data_file:
        user_data_line = user_data_line.strip("\n")
        user_data = user_data_line.split(", ")
        user_count.append(user_data[0])
    return user_count, user_task, user_completed, user_uncompleted, user_overdue


#below function use lists from function "summarise_user" to create dictionaries accordingly to count number of task
#number of completed, uncompleted and overdue tasks
def user_total_count(user_count, user_task, user_completed, user_uncompleted, user_overdue):
    user_task_dict = {}
    user_completed_dict = {}
    user_uncompleted_dict = {}
    user_overdue_dict = {}
    for user in user_count:
        if user in user_task:
            user_task_dict[user] = user_task.count(user)
        else:
            user_task_dict[user] = 0
        if user in user_completed:
            user_completed_dict[user] = user_completed.count(user)
        else:
            user_completed_dict[user] = 0
        if user in user_uncompleted:
            user_uncompleted_dict[user] = user_uncompleted.count(user)
        else:
            user_uncompleted_dict[user] = 0
        if user in user_overdue:
            user_overdue_dict[user] = user_overdue.count(user)
        else:
            user_overdue_dict[user] = 0
    return user_task_dict, user_completed_dict, user_uncompleted_dict, user_overdue_dict

#below function create (if not exists) and write to 'task_overview.txt' in correct format
def task_overview_write(total_task_number, total_completed_task, total_uncompleted_task,total_overdue_task):
    task_overview_file = open('task_overview.txt','w')
    percentage_incomplete_task = round(total_uncompleted_task/total_task_number*100,2)
    percentage_overdue_task = round(total_overdue_task/total_task_number*100,2)
    task_overview_file.write("Total number of tasks that have been generated and tracked using the task_manager.py: "+ 
    str(total_task_number)+"\n")
    task_overview_file.write("Total number of completed tasks: "+str(total_completed_task)+"\n")
    task_overview_file.write("Total number of uncompleted tasks: "+str(total_uncompleted_task)+"\n")
    task_overview_file.write("Total number of tasks that haven’t been completed and that are overdue: "+str(total_overdue_task)+"\n")
    task_overview_file.write("Percentage of tasks that are incomplete: "+str(percentage_incomplete_task)+"% \n")
    task_overview_file.write("Percentage of tasks that are overdue: "+str(percentage_overdue_task)+"% \n")
    task_overview_file.close()

#below function create (if not exists) and write to 'user_overview.txt' in correct format for each user
def user_overview_write(total_task_number, user_count, user_task_dict, user_completed_dict, user_uncompleted_dict, user_overdue_dict):
    user_overview_file = open('user_overview.txt','w')
    user_overview_file.write("Total number of users registered with task_manager.py: "+str(len(user_count))+"\n")
    user_overview_file.write("Total number of tasks that have been generated and tracked using the task_manager.py: "+
    str(total_task_number)+"\n")
    for user in user_count:
        user_overview_file.write("Username: "+user+"\n")
        user_overview_file.write("Total number of tasks assigned: "+str(user_task_dict[user])+"\n")
        percentage_user_task_to_total = round(user_task_dict[user]/total_task_number*100,2)
        user_overview_file.write("Percentage of the total number of tasks that have been assigned: "+
        str(percentage_user_task_to_total)+"% \n")
        if user_task_dict[user] != 0:
            percentage_user_task_completed = round(user_completed_dict[user]/user_task_dict[user]*100,2)
            percentage_user_task_uncompleted = round(user_uncompleted_dict[user]/user_task_dict[user]*100,2)
            percentage_user_task_overdue = round(user_overdue_dict[user]/user_task_dict[user]*100,2)
            user_overview_file.write("Percentage of completed assigned task: "+str(percentage_user_task_completed)+"% \n")
            user_overview_file.write("Percentage of uncompleted assigned task: "+str(percentage_user_task_uncompleted)+"% \n")
            user_overview_file.write("Percentage of uncompleted and overdue assigned task: "+str(percentage_user_task_overdue)+"% \n")
        else:
            user_overview_file.write("No tasks have been assigned to this user! \n")
    user_overview_file.close()

#below function call functions 'summarise_task', 'summarise_user', 'user_total_count' to get details
#and call functions 'task_overview_write' and 'user_overview_write' to create reports
def gen_rep():
    task_summary = summarise_task()
    total_task_number, total_completed_task, total_uncompleted_task = task_summary[0], task_summary[1], task_summary[2]
    total_overdue_task = task_summary[3]
    user_summary = summarise_user()
    user_count, user_task, user_completed, user_uncompleted = user_summary[0], user_summary[1], user_summary[2], user_summary[3]
    user_overdue = user_summary[4]
    user_total_summary = user_total_count(user_count, user_task, user_completed, user_uncompleted, user_overdue)
    user_task_dict, user_completed_dict, user_uncompleted_dict = user_total_summary[0], user_total_summary[1], user_total_summary[2]
    user_overdue_dict = user_total_summary[3]
    task_overview_write(total_task_number, total_completed_task, total_uncompleted_task,total_overdue_task)
    user_overview_write(total_task_number, user_count, user_task_dict, user_completed_dict, user_uncompleted_dict, user_overdue_dict)

#====File Input for login check====
user_data_file = open('user.txt','r')
username = []
password = []
for user_data_line in user_data_file:
    user_data_line = user_data_line.strip("\n")
    user_data = user_data_line.split(", ")
    username.append(user_data[0]) # Create a username list for login section to check
    password.append(user_data[1]) # Create a password list for login section to check
user_data_file.close()

#====Login Section====
login_success = False
password_invalid = False
username_invalid = False
while login_success == False:
    username_input = input("Please enter your username: ")
    password_input = input("Please enter your password: ")      
    for i in range(0,len(username)):
        #Check entered username is in existing username list and entered password is corresponding to that username
        #return 'login_success' as True to exit the login section and 'show_menu' as True to trigger start of menu selection section
        if username_input == username[i] and password_input == password[i]:
            login_success = True
            show_menu = True
        #Check entered username is in existing username list but entered password is not correspondin to that username
        elif username_input == username[i] and password_input != password[i]:
            password_invalid = True
        elif username_input != username[i]: # Check entered username is not in existing username list
            username_invalid = True
    if login_success == True:
        print("Login Succeeded!")
    elif password_invalid == True:
        print("Login Failed, you have entered valid username but invalid password, please try again!")
    elif username_invalid == True:
        print("Login failed, you have entered invalid username, please try again!")
    password_invalid = False
    username_invalid = False

#====Menu Selection Section====
while show_menu == True:
    #presenting the menu to the user and 
    # making sure that the user input is coneverted to lower case.
    if username_input != "admin": # Check the current user is admin or not
        menu = input('''Select one of the following Options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - view my task
    e - Exit
: ''').lower()
    else:
        menu = input('''Select one of the following Options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - view my task
    gr - generate reports
    ds - display statistics
    e - Exit
: ''').lower()

    if menu == 'r':
        reg_user(username_input,username)
    
    if menu == 'a':
        add_task()
    
    if menu == "va":
        view_all()
    
    if menu == "vm":
        view_mine(username_input)
    
    if username_input == "admin" and menu == "gr":
        gen_rep()
    
    if username_input == "admin" and menu == "ds":
        user_overview_path = './user_overview.txt'
        task_overview_path = './task_overview.txt'
        #check if 'user_overview.txt' and 'task_overview.txt' exist
        if os.path.isfile(user_overview_path) != True or os.path.isfile(task_overview_path) != True:
            gen_rep()
        user_data_file = open('user_overview.txt','r')
        task_data_file = open('task_overview.txt','r')
        print(user_data_file.readline().strip("\n"))
        print(task_data_file.readline().strip("\n"))
    
    if menu == 'e':
        show_menu = False
        print("The manager will now close!")
        