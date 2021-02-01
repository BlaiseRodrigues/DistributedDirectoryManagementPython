#Blaise Rodrigues
#1001759552
import socket
import sys
import tkinter as tk
import re


#WORKING ON DISPLAY
#FUNCTION TO PRINT ON UI
def PRINT_LABEL(VALUE):
    label1 = tk.Label(frame, text = VALUE)
    label1.pack()

#FUNCTION TO HANDLE UI INPUTS
def UI_INPUT(Button, IntVal):
    Button.wait_variable(IntVal)
    INPUT = Entry1.get()
    Entry1.delete(0,'end')
    return INPUT


#FUNCTION TO HANDLE QUIT
def QUIT(top):
    myclient.send(str.encode('x'))

    USERNAME_STATUS = False
    top.destroy()
    sys.exit(0)


def validate_string(username):
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if(regex.search(username) == None):
        return False
    else:
        return True



#FUNCTION TO GET USERNAME UI
def GET_USERNAME():
    USERNAME_STATUS = False
    while not USERNAME_STATUS:
        PRINT_LABEL("Enter Your Username")  #INPUT TO PRINT LABEL FUNCTION ABOVE
        username = UI_INPUT(Button1,int_var)
        if len(username)==0 or validate_string(username):
            PRINT_LABEL("Enter Valid Username")
        while len(username)==0 or validate_string(username):#INPUT TO PRINT LABEL FUNCTION ABOVE
            username = UI_INPUT(Button1,int_var)

        myclient.send(str.encode(username))  #UI SEND 1 CLIENTNAME
        response = str(myclient.recv(1024),'utf-8') #UI RECV 1 USERNAME CHECK
        while response == 'please enter a valid username':
            Label1 = tk.Label(frame, text='Enter valid username')
            Label1.pack()
            Message = UI_INPUT(Button1, int_var)
            myclient.send(str.encode(Message))
            response = str(myclient.recv(1024),'utf-8')


        if response == 'Username Exists and is Active': #If username exists and active
            Label1 = tk.Label(frame, text='Username Taken & Active.')
            Label1.pack()
            continue
        if response == 'Username Exists and is assigned a directory':
            Label1 = tk.Label(frame, text='Username Exists and is assigned a directory.')
            Label1.pack()

        if response == 'directory exists':
            Label1 = tk.Label(frame, text='Username Taken & directory exists.')
            Label1.pack()
            PRINT_LABEL('Welcome back, Directory has been assigned.')
            continue

        USERNAME_STATUS = True
    return USERNAME_STATUS, username



def setup():
    #https://realpython.com/python-sockets/
    myclient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    myclient.connect((HOST, PORT))
    return myclient, HOST, PORT

if __name__ == "__main__":

    HOST = '127.0.0.1'
    PORT = 1396

    #ADDING CODE FOR DISPLAY
    ##https://www.python-course.eu/tkinter_labels.php
    top = tk.Tk()
    top.title("Client")
    int_var = tk.IntVar() #TO STORE INTEGER VAR
    main = tk.Canvas(top, height = 1000, width = 600)
    main.pack()

    frame = tk.Frame(main) #BUILD FRAME
    frame.place(relwidth = 1, relheight = 0.9)
    myclient, HOST, PORT = setup()  #GETTING SETUP DETAILS
    Entry1 = tk.Entry(frame)
    Entry1.pack()
    Button1 = tk.Button(frame, text = 'Enter', command = lambda: int_var.set(1))
    Button1.pack()
    Button2 = tk.Button(frame, text = 'Quit', command = lambda: QUIT(top))
    Button2.pack()
    USERNAME_STATUS, username  = GET_USERNAME() #CHECK ABOVE SEND AND RECV 1 UI
    if USERNAME_STATUS:
        PRINT_LABEL(str("Client "+username+" Has been connected"))
        # PRINT_LABEL(str("Current Directory :" + curr_dir))

        #MAKE CHOICE LOOP. User makes a choice

        PRINT_LABEL("Enter 1: Create Directory. 2: Delete Directory. 3: Move Directory. 4: Rename Directory. 5. List directory ")
        PRINT_LABEL("'X' To Quit ")


        while USERNAME_STATUS != False:
            Choice = UI_INPUT(Button1, int_var)  #Get Numerical Choice
            if len(Choice)==0:  #checks if valid choice is made
                PRINT_LABEL('Enter valid choice')
            while len(Choice)==0: #Loops until user makes a valid choice
                Choice = UI_INPUT(Button1, int_var)
            SERVER_RESPONSE = myclient.send(str.encode(Choice))  #UI SEND 2. CHOICE

            #QUIT HANDLING
            if Choice == 'X' or Choice == 'x':
                QUIT(top)


            #1. Create Directory
            # if Choice == '1':
            #     PRINT_LABEL("Enter Directory Name")
            #     new_dir = UI_INPUT(Button1, int_var)
            #     myclient.send(str.encode(new_dir))
            #     ACK = str(myclient.recv(1024),'utf-8')
            #     PRINT_LABEL(ACK)


            #1. Create a new directory
            if Choice == '1':
                list_dir = str(myclient.recv(1024),'utf-8')
                PRINT_LABEL('Select a directory to create the new directory in') #Initial -  Receives list of directories available in Homer directory
                PRINT_LABEL("Directories-> 'Home' OR , "+ list_dir.strip('[]') if len(list_dir)!=2 else "Directory-> 'Home'")
                # PRINT_LABEL("Enter Directory Name")
                new_dir = UI_INPUT(Button1, int_var) # selects directory name form [Current , dir_, dir_]
                myclient.send(str.encode(new_dir)) #1 - Sends directory name to server

                message_recv = str(myclient.recv(1024),'utf-8') #2 - Message asking user for new directory name
                #we get a message prompting to enter new_dir name for creating it

                if message_recv == 'Enter new directory name to create':
                    PRINT_LABEL("Enter new direcory name")
                    new_dir = UI_INPUT(Button1, int_var) #User eneters directory name
                    myclient.send(str.encode(new_dir)) #3- client send directory name to server

                    new_message = str(myclient.recv(1024),'utf-8') #4 - Receives message from server
                    while new_message != 'Directory Created': #if the directory not created prompt user to enter anotehr name
                        PRINT_LABEL("Enter unique and valid direcory name")
                        new_dir = UI_INPUT(Button1, int_var) #User eneters directory name agin
                        myclient.send(str.encode(new_dir)) #5- send to server
                        new_message = str(myclient.recv(1024),'utf-8')#6 - receives message from server


                    PRINT_LABEL(new_message) #prints the new message 'Directory created on the client side'


                elif message_recv == 'Such directory Doest exists': #if directory doesnt exists then user can start over
                    PRINT_LABEL(message_recv) #Displays the received message on the client screen


            #2. Delete Directory
            elif Choice == '2':
                list_dir = str(myclient.recv(1024),'utf-8') #receives a list of directories present in the current folder
                if len(list_dir)==2:
                    PRINT_LABEL(list_dir)                        #prints the directory list on client side
                    PRINT_LABEL('No directory available to delete')
                    myclient.send(b'False')
                else:
                    PRINT_LABEL(list_dir) #prints the received message from the server
                    PRINT_LABEL("Enter Directory to Delete")
                    Message = UI_INPUT(Button1, int_var) #takes the input from user for directory name
                    myclient.send(str.encode(Message)) #send the input over to server
                    while str(myclient.recv(1024),'utf-8') == 'Directory Doesnt exists': #receives the message from server and loops until correct directory name is specifies
                        PRINT_LABEL("Enter correct Directory to Delete")
                        Message = UI_INPUT(Button1, int_var)#Takes input - directory name(to be deleted) from the user.
                        myclient.send(str.encode(Message))#sends it over to the client
                    PRINT_LABEL('Deleted') #once the directory is deleted, the loop is ended and 'Deleted' message is prinetd


            #3. Move Directory
            elif Choice == '3':

                PRINT_LABEL(str(myclient.recv(1024),'utf-8'))
                s_dir = UI_INPUT(Button1, int_var)
                myclient.send(str.encode(s_dir))

                r_mess = str(myclient.recv(1024),'utf-8') #receives message from the server
                while r_mess == 'Directory Doesnt exists':
                    PRINT_LABEL("Enter correct Directory to Move")
                    s_dir = UI_INPUT(Button1, int_var)#takes the input as directory name which is to be moved
                    myclient.send(str.encode(s_dir))
                    r_mess =str(myclient.recv(1024),'utf-8')

                # PRINT_LABEL(str(myclient.recv(1024),'utf-8'))
                PRINT_LABEL("Enter destination Directory")
                d_dir = UI_INPUT(Button1, int_var) #takes the destination of directory to move as input
                myclient.send(str.encode(d_dir))#send the informations to the server

                r_mess = str(myclient.recv(1024),'utf-8')
                while r_mess == 'Directory Doesnt exists': #checks if the Directory exists or not, if not the loops
                    PRINT_LABEL("Enter correct Directory to Move")
                    d_dir = UI_INPUT(Button1, int_var) #takes a new directory name
                    myclient.send(str.encode(d_dir))
                    r_mess =str(myclient.recv(1024),'utf-8')

                PRINT_LABEL(r_mess)#prints the message if its not equal to 'Directory doesnt exists'



            #4. Rename Directory
            elif Choice == '4':
                list_dir = str(myclient.recv(1024),'utf-8') #receives a list of directories present in the current folder
                if len(list_dir)==2:
                    PRINT_LABEL(list_dir)                        #prints the directory list on client side
                    PRINT_LABEL('No directory available')
                    myclient.send(b'False')

                else:
                    PRINT_LABEL(list_dir)                        #prints the directory list on client side
                    PRINT_LABEL("Select directory to rename")
                    dir_name = UI_INPUT(Button1, int_var)          #client enters a directory name from above list
                    myclient.send(str.encode(dir_name))
                    while str(myclient.recv(1024),'utf-8') == 'Directory Doesnt exists': #if such directory doesnt exists then we loop until correct name is entered
                        PRINT_LABEL("Enter correct Directory name")
                        Message = UI_INPUT(Button1, int_var)          #takes the directory name
                        myclient.send(str.encode(Message))

                    PRINT_LABEL("Enter New Directory name")
                    new_name = UI_INPUT(Button1, int_var) #takes the new name for that directory
                    myclient.send(str.encode(new_name)) #sends over to the client
                    PRINT_LABEL(str(myclient.recv(1024),'utf-8')) #prints the final message received from the server


            #5. List Directories
            elif Choice == '5':
                list_dir = str(myclient.recv(1024),'utf-8') #receives list of directories present in the current folder from the server
                PRINT_LABEL('Select a directory of which you want to list subdirectories of') #Initial -  Receives list of directories available in Homer directory
                PRINT_LABEL("Directories-> 'Home' OR, "+ list_dir.strip('[]') if len(list_dir)!=2 else "Directory-> 'Home'")
                new_dir = UI_INPUT(Button1, int_var) #User eneters directory name
                myclient.send(str.encode(new_dir)) #3- client send directory name to server
                all_dir = str(myclient.recv(1024),'utf-8')
                PRINT_LABEL(all_dir if len(all_dir)!=2 else 'No sub directories.')

            # Button2 = tk.Button(frame, text = 'Quit', command = lambda: QUIT(top))
            # Button2.pack()


        PRINT_LABEL("Client Disconnected")
        top.mainloop()

# https://github.com/isiddheshrao/Distributed-Systems/blob/master/Client.py
