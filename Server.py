#Blaise Rodrigues
#1001759552

import datetime
from queue import Queue
import socket
import tkinter as tk
import sys
import threading
from _thread import *
import os
from os import path
import dill
import shutil
import re

# https://github.com/isiddheshrao/Distributed-Systems/blob/master/Server.py

#CREATING CODE FOR UI

#FUNCTION TO HANDLE QUIT
def QUIT(top):

    top.destroy()
    #https://www.datacamp.com/community/tutorials/pickle-python-tutorial
    dill.dump(USER_QUEUES,open('USERNAME_QUEUES.pkl','wb'))  #DUMP A FILE ON CURRENT PATH IF SERVER IS QUIT (For Persistency) AND LOAD IT WHEN SERVER STARTS
    sys.exit(1)

#STATUS OF CLIENTS ON UI
#https://www.python-course.eu/tkinter_labels.php
def MAIN_DISPLAY(NULL):
    top = tk.Tk()
    top.title("Server")
    main = tk.Canvas(top, height= 500,width= 600)
    main.pack()
    frame = tk.Frame(main)
    frame.place(relwidth = 1, relheight= 0.9)
    Label1 = tk.Label(frame)
    Label1.pack()
    title_label1 = tk.Label(frame, justify=tk.LEFT, padx = 10)
    title_label1.pack(side = "left")
    title_label1.config(text = "Total Usernames in this Session ->")
    title_label2 = tk.Label(frame, justify=tk.RIGHT, padx = 10)
    title_label2.pack(side = "right")
    title_label2.config(text = "<- Active Usernames in this Session")
    Label2 = tk.Label(frame, justify=tk.LEFT, padx = 10)
    Label2.pack(side ="left")
    Label3 = tk.Label(frame, justify=tk.RIGHT, padx = 10)
    Label3.pack(side ="right")
    UPDATE(Label1,top)
    SHOW_LIST(top, Label2, Label3)
    Button1 = tk.Button(frame, text = 'Quit', command = lambda: QUIT(top))
    Button1.pack()
    top.mainloop()

#CODE TO UPDATE CLIENT STATUS UI IN EVERY 1000MS
def UPDATE(Label1,top):
    global USER_STATUS
    global count
    if USER_STATUS == True:
        PRINT_UI = str(str(count) + " Client(s) Connected in directory" + str(os.path))
        Label1.config(text = PRINT_UI)
    else:
        Label1.config(text = "No Client Connected")
    top.after(1000, lambda: UPDATE(Label1, top))

#CODE TO UPDATE USERNAMES AND ACTIVE USERNAMES AND UPDATE EVERY 1000MS
def SHOW_LIST(top, label2, Label3):
    label2.config(text = USERNAMES)
    Label3.config(text = ACTIVE_USERNAMES)
    top.after(1000, lambda: SHOW_LIST(top, label2, Label3))


#CODE FOR THREAD DELETION
def THREAD_DEL():
    global STOP_CLIENT_THREAD
    global count
    STOP_CLIENT_THREAD = True
    count -=1 #UI UPDATE
    newclientthread.join()  #TO CHECK AND DELETE THREAD CONTEXT



#CODE TO MAKE QUEUE FOR NEW USERNAMES AND NOT FOR EXISTING ONES
def MAKE_QUEUE(userdata):
    if userdata in USERNAMES:
        if USER_QUEUES.get(userdata):
            Client_Queue = USER_QUEUES.get(userdata)
        else:
            Client_Queue = Queue()
            USER_QUEUES[userdata] = Client_Queue
    return Client_Queue



#---------------MAIN CODE---------------------------------#



class ClientThread(threading.Thread):
    def __init__(self, ClientAddr, ClientSock):
        threading.Thread.__init__(self)
        self.csocket = ClientSock
        print("New Client Connection Added from address: ", ClientAddr)


    def validate_string(self, name):
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        if(regex.search(name.decode()) == None):
            return False
        else:

            return True


    def createDirectory(self, username): #Function to create a home directory for a new client
        print(str(os.listdir(str(os.getcwd()+'\\'))))
        if username.lower() not in str(os.listdir(str(os.getcwd()+'\\'))): #checks if directory already exists or not
            os.mkdir(username.lower())                                     #Creates the directory with its username
        # os.chdir(str(os.getcwd())+'\\'+username)
        else:
            print('Directory Exists')
            pass





#Saved ->>>
    # def createNewDirectory(self, username):
    #     dir_name = self.csocket.recv(2048)
    #     # os.chdir(str(os.getcwd())+'\\'+username)
    #     # os.chdir(str(os.())+'\\'+username)
    #     os.mkdir(username + '\\' +dir_name.decode())
    #
    #     message = b'Directory Created'
    #     self.csocket.sendall(message)

#For experiment ->>

    def createNewDirectory(self, username): #Function to create a new directory within the home directory of the client
        selectd_directory = self.csocket.recv(2048) #1 - receives selected directory.

        #if the user selects Current direcory, we create the new direcory in the current direcory(parent) of  the client
        if selectd_directory.decode() == 'Home' or selectd_directory.decode() == 'home': # if the client selects current directory
            message = b'Enter new directory name to create'
            self.csocket.sendall(message)          #2- send a message to user prompting it to enter new directory Name

            new_dir = self.csocket.recv(2048)     # 3 - receives the directory name
            while new_dir.decode() in str(os.listdir(str(os.getcwd()+'\\'+username))) or self.validate_string(new_dir): #check if there already exists a directory with that name
                message = b'A directory already exists'
                self.csocket.sendall(message)  #4- sends message to server
                new_dir = self.csocket.recv(2048) #5 - server receives the directory name from client


            os.mkdir(username + '\\' +new_dir.decode())
            message = b'Directory Created'
            self.csocket.sendall(message) #6 - send message to client that the directory is succesfully created



        #if the client selects another direcory, the we create the new directory in this directory
        elif selectd_directory.decode() in str(os.listdir(str(os.getcwd()+'\\'+username))): # checks if the selectd_directory is present in the parent directory of the client
            message = b'Enter new directory name to create'
            self.csocket.sendall(message) # 2- Sends message to user to enter new_dir name for creation
            new_dir = self.csocket.recv(2048)     # 3 - receives the directory name
            while new_dir.decode() in str(os.listdir(str(os.getcwd()+'\\'+username+'\\'+selectd_directory.decode()))) or self.validate_string(new_dir): #check if there already exists a directory with that name
                message = b'A directory already exists'
                self.csocket.sendall(message)  #4- sends message to server
                new_dir = self.csocket.recv(2048) #5 - server receives the directory name from client


            os.mkdir(username + '\\' +selectd_directory.decode()+'\\'+new_dir.decode())
            message = b'Directory Created'
            self.csocket.sendall(message) #6 - send message to client that the directory is succesfully created


        else:                #if the entered directory is not present the below message is sent
            message = b"Such directory Doest exists"
            self.csocket.sendall(message)



    def deleteDirectory(self, username): #function to delete directory
        dir_name = self.csocket.recv(2048) #receives the directory name to be deleted
        if dir_name.decode() != 'False': #checks if there exixts a directory or not based on response from clent
            while dir_name.decode() not in str(os.listdir(str(os.getcwd()+'\\'+username))) or self.validate_string(dir_name): #checks if such a directory exists or not AND loops until correct directory name is enetered
                message = b'Directory Doesnt exists'
                self.csocket.sendall(message) #send the message 'Directory d'Doesnt exists to the client
                dir_name = self.csocket.recv(2048) #receives new directory name from user



            os.rmdir(username +'\\'+dir_name.decode()) #if directory exixts then it removes it.
            message = b'Directory deleted'
            self.csocket.sendall(message) #sends message directory deleted to the client
        else:
            pass


    def moveDirectory(self, username): #Function to move directory
        s_dir = self.csocket.recv(2048) #reciebes source directory name

        while s_dir.decode() not in str(os.listdir(str(os.getcwd()+'\\'+username))): #checks if such dir exists or not, and loops until correct source is entered
            message = b'Directory Doest exists'
            self.csocket.sendall(message) #sends message to the client
            s_dir = self.csocket.recv(2048) #receives new source name
        message = b'Enter destination directory'
        self.csocket.sendall(message) #sends message to client and prompts for name of destination directory

        d_dir = self.csocket.recv(2048) #recceives the name of destination directory
        while d_dir.decode() not in str(os.listdir(str(os.getcwd()+'\\'+username))): #checks if such dir exists or not, and loops until correct source is entered
            message = b'Directory Doest exists'
            self.csocket.sendall(message) #sends message to client
            d_dir = self.csocket.recv(2048) #receives new destination directory name

        shutil.move(str(os.getcwd()+'\\'+username+'\\' + s_dir.decode()), str(os.getcwd()+'\\'+username+'\\' +d_dir.decode()+'\\'+s_dir.decode())) #Moves the directpry to destination folder
        message = b'Directory moved'
        self.csocket.sendall(message) #sends message to client



    def renameDirectory(self, username): #function to rename a directory
        dir_name = self.csocket.recv(2048) #receives directory name to be renamed
        if dir_name.decode() != 'False': #checks if there exixts a directory or not based on response from clent
            while dir_name.decode() not in str(os.listdir(str(os.getcwd()+'\\'+username))): #loops until correct directory is entered
                message = b'Directory Doesnt exists'
                self.csocket.sendall(message) #sends message to the client
                dir_name = self.csocket.recv(2048) #receives directory name

            message = b'Enter new name'
            self.csocket.sendall(message) #asks the client to enter new name for that directory
            new_name = self.csocket.recv(2048) #receives the new name from the client
            os.rename(str(os.getcwd()+'\\'+username) +'\\'+dir_name.decode(),str(os.getcwd()+'\\'+username)+'\\'+new_name.decode()) #renames the files
            self.csocket.sendall(str(os.listdir(str(os.getcwd()+'\\'+username))).encode('utf-8')) #send the list of files to the client
        else: #stops the execution if there is no file in the home directory of the client
            pass


    def listDirectory(self, username):
        dir_name = self.csocket.recv(2048)
        if dir_name.decode() == 'Home' or dir_name.decode()=='home':
            self.csocket.sendall(str(os.listdir(str(os.getcwd()+'\\'+username))).encode('utf-8')) #sends list of available drectories to the client

        elif dir_name.decode() in str(os.listdir(str(os.getcwd()+'\\'+username))):
            self.csocket.sendall(str(os.listdir(str(os.getcwd()+'\\'+username+'\\'+dir_name.decode()))).encode('utf-8'))
        else:                #if the entered directory is not present the below message is sent
            message = b"Such directory Doest exists"
            self.csocket.sendall(message)




    #FUNCTION TO GET AND CHECK USERNAME
    def USERNAME_CHECK(self):
        USER_FLAG = False
        while not USER_FLAG:
            username = str(self.csocket.recv(4096),'utf-8')   #USERNAME CHECK RECV 1

            if len(username)==0:
                message = b'please enter a valid username'
                self.csocket.sendall(message)

            if (username in USERNAMES) and (username in ACTIVE_USERNAMES):
                message = b"Username Exists and is Active"
                self.csocket.sendall(message)  #SEND 1 USERNAME EXISTS
                continue
            #
            # Username Exists but not ACTIVE Code
            #


            # elif os.path.exists(str(os.getcwd()+'\\'+username)):
            #     print(os.path.exists(str(os.getcwd()+'\\'+username)))
            #     print('FFFFF')
            #     message = b'directory exists'
            #     self.csocket.sendall(message)

            elif (username in USERNAMES) and (username not in ACTIVE_USERNAMES):
                message = b"Username Exists and is assigned a directory"
                self.csocket.sendall(message)  #SEND 1 USERNAME EXISTS

                ACTIVE_USERNAMES.append(username)


                message = b'Welcome'
                print("Welcome back", username)
                self.csocket.sendall(message) #SEND 1 USERNAME NEW
                return username


            else:

                self.createDirectory(username)


            USER_FLAG = True

        #CHECK IF USERNAME NOT ALREADY IN USERNAME LIST
        if username not in USERNAMES:
            USERNAMES.append(username)
        #GET USER QUEUE BASED ON USERNAME
        MAKE_QUEUE(username)
        ACTIVE_USERNAMES.append(username)
        global USER_STATUS  #FOR UI UPDATE
        USER_STATUS = True  #FOR UI UPDATE
        global count
        count +=1 #FOR UI UPDATE
        message = b'Welcome'
        print("Welcome", username)
        self.csocket.sendall(message) #SEND 1 USERNAME NEW
        return username






    def run(self):
        global STOP_CLIENT_THREAD
        userdata = self.USERNAME_CHECK() #USERNAME FUNCTION CALL 1

        while True:

#
#             Inside the home directory, the client will have the ability to:
# • Create directories;
# • Delete directories;
# • Move directories;
# • Rename directories; and,
# • List the contents of directories.


            choice = self.csocket.recv(2048) #RECV 2 CLIENT CHAT CHOICE
            choice = choice.decode()

            if choice.lower() == 'x':
                ACTIVE_USERNAMES.remove(userdata)  #REMOVING ACTIVE USERNAME FROM LIST
                THREAD_DEL()
                if STOP_CLIENT_THREAD:
                    break

            #1. Create Directory
            if choice == '1':
                self.csocket.sendall(str(os.listdir(str(os.getcwd()+'\\'+userdata))).encode('utf-8')) #1 - send list of directory to user to select from
                self.createNewDirectory(userdata)  #Calls function createNewDirectory and passes userdata to it.

            #2. Delete directory
            if choice == '2':
                self.csocket.sendall(str(os.listdir(str(os.getcwd()+'\\'+userdata))).encode('utf-8')) #sends list of available drectories to the client
                self.deleteDirectory(userdata) #Calls function deleteDirectory and passes userdata to it.


            #3. Move directory
            if choice == '3':
                # self.csocket.sendall(str(os.walk(str(os.getcwd()+'\\'))).encode('utf-8')
                message = b'Enter Source directory'
                self.csocket.sendall(message + str(os.listdir(str(os.getcwd()+'\\'+userdata))).encode('utf-8'))#sends list of available drectories to the client
                self.moveDirectory(userdata) #Calls function moveDirectory and passes userdata to it.



            #4. Rename Directory
            if choice == '4':
                self.csocket.sendall(str(os.listdir(str(os.getcwd()+'\\'+userdata))).encode('utf-8'))#sends list of available drectories to the client
                self.renameDirectory(userdata) #Calls function renameDirectory and passes userdata to it.

            #5. List directory
            if choice == '5':
                self.csocket.sendall(str(os.listdir(str(os.getcwd()+'\\'+userdata))).encode('utf-8')) #sends list of available drectories to the client
                self.listDirectory(userdata)


if __name__ == "__main__":
    STOP_CLIENT_THREAD = False
    USER_STATUS = False
    count = 0
    userdata = ''
    USERNAMES = []
    ACTIVE_USERNAMES = []
    USER_QUEUES = {} #TO HANDLE USERNAMES AND QUEUES
    #CHECK IF DUMP FILE EXISTS, IF YES, LOAD FILE INTO DICTIONARY FOR PERSISTENCy
    if path.exists('USERNAME_QUEUES.pkl') == True:
        with (open('USERNAME_QUEUES.pkl', "rb")) as openfile:
            while True:
                try:
                    #https://dill.readthedocs.io/en/latest/dill.html
                    USER_QUEUES.update(dill.load(openfile))
                except EOFError:
                    break
    HOST = '127.0.0.1'
    PORT = 1396

    NULL = ''
    #http://net-informations.com/python/net/thread.htm
    try:
        myserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        myserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        myserver.bind((HOST,PORT))
        print("Starting Server at HOST: "+ HOST + " and PORT: ", PORT)
        start_new_thread(MAIN_DISPLAY,(NULL,))
        while True:
            myserver.listen(3)
            conn, addr = myserver.accept()
            newclientthread = ClientThread(addr, conn)
            newclientthread.start()
    except Exception:
        #https://dill.readthedocs.io/en/latest/dill.html
        dill.dump(USER_QUEUES,open('USERNAME_QUEUES.pkl','wb'))
    finally:
        myserver.close()


