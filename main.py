import tkinter as tk
from tkinter import ttk                
import sqlite3
from content_based_system import get_ID, get_possible_searches,get_similar_animes,get_index_from_name
import AccountDB
import numpy as np
import string
import webbrowser
import random
import tkinter.messagebox
import os
import sys

# File paths
project_folder = os.getcwd()
IMAGES_FOLDER = project_folder+'/Images/'
PICTIONARY_FOLDER = project_folder+'/Pictionary/'
DATA_FOLDER = project_folder+'/Data/'

LARGE_FONT= ("Anime Ace Bold", 12)
NORM_FONT =("Anime Ace Bold", 10)
SMALL_FONT =("Anime Ace Bold", 8)



##
''' (STEP 1) CREATING THE INTERFACE CLASS - Instead of making a window for each of our screens, i decided to create just one window
and instead make multiple Tkinter Frame widgets which will represent the screens. I then plan to create an invisible Frame which will
act as a container to hold all the screens. So then if we want to change to a different screen we can do so by raising the screen
that we want to see to the top of the container.

I chose to do this in this way as creating multiple windows can be very inefficient on memory and cause cause delays and freezes in
runtime of the application.Whereas, the use of frames is much more generous on memory consumption.
'''
##
    

# Declaring the Interface class which inherits from Tkinter's Tk class
class interface(tk.Tk):

    # Declaring interface's constructor method and following convention by stating the default parameters
    def __init__(self, *args, **kwargs):
        # Initialising Tkinter (Creates the window)
        tk.Tk.__init__(self, *args, **kwargs)

        # Setting the title of the window
        tk.Tk.wm_title(self, "Anime Rec")

        # Creating a Tkinter Frame widget which will act as a container
        container = tk.Frame(self)

        # Displaying/putting the container onto the window and making it fill the entire window
        container.pack(side="top", fill="both", expand=True)

        # Giving the container priority over all other widgets
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Declaring a dictionary which will contain all the frames that we will make
        self.frames = {}

        # For loop which puts each frame in to the container and appends each container item to the self.frames dictionary
        for F in {home, register, menu, profile, get_rec, browse, pictionary}: # These are classes that are yet to be created
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Sets the Home screen to the top of the container by defualt (displays the home screen by default)
        self.show_frame(home)

        # Creating and displaying a navigation bar which will allow the user to logout and exit the app
        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff = 0)
        filemenu.add_command(label="Log out",command=self.logout )
        filemenu.add_separator()
        filemenu.add_command(label="Menu",command=lambda: self.show_frame(menu))
        menubar.add_cascade(label="File", menu=filemenu)
        tk.Tk.config(self, menu=menubar)

        # This function will be called whenever we want to change screens, it does this by taking the screen we want to change to
        # as a parameter and using Tkinters tkraise() we can raise that screen to the top of the container
        
    def show_frame(self, cont): 
        frame = self.frames[cont]
        frame.tkraise()

    def logout(self):
        os.execl(sys.executable, sys.executable, *sys.argv)

     
class home(tk.Frame): # Class Home inherits from Tkinter's Frame class (Creating a frame for the Home screen)
    def __init__(self, parent, controller): # Constructor method for home class
        tk.Frame.__init__(self, parent, bg = 'grey11') # Initialises the Frame class nad sets background colour to follow our colour scheme

        self.controller = controller # Assigns the controller variable to a variable of the class home

        ## CREATING AND DISPLAYING THE HOME TITLE ##
        self.title_img = tk.PhotoImage(file= IMAGES_FOLDER+"Home_Title.png") # Loads image
            # Creates Label widget containing the image
        self.title_label = tk.Label(self, width=392, image=self.title_img, relief='flat', background =  'grey11')
        self.title_label.place(relx=0.21, rely=0.02, height=108, width=392) # Places widget onto window

       
        self.ken = tk.PhotoImage(file= IMAGES_FOLDER+"Ken_Masked.png") 
        self.ken_label = tk.Label(self, width=392, image=self.ken, relief='flat', background =  'grey11')
        self.ken_label.place(relx=0, rely=0.2, height=450, width=180) 

        ## CREATING AND DISPLAYING THE LOGIN BUTTON ##
        login_img = tk.PhotoImage(file = IMAGES_FOLDER+"Login_button.png") # Loads image
            # Creates Button widget containing the image
        self.login_butt = tk.Button(self,image=login_img,command = self.login, borderwidth=0,background ='grey11', activebackground='grey11')
        self.login_butt.image=login_img # keeps a reference of the widgets image
        self.login_butt.place(relx=0.4, rely=0.46, height=35, width=120) # Places widget onto window

        ## CREATING AND DISPLAYING THE REGISTER BUTTON ##
        reg_img = tk.PhotoImage(file = IMAGES_FOLDER+"Reg_Button.png")
        self.register_butt = tk.Button(self, image=reg_img,command = lambda:controller.show_frame(register), borderwidth=0,background ='grey11', activebackground='grey11')
        self.register_butt.image = reg_img
        self.register_butt.place(relx=0.31, rely=0.74, height=45, width=250)

        ## CREATING AND DISPLAYING USERNAME ENTRY WIDGET ##
        self.username_entry = ttk.Entry(self) # Creates usenrmae entry widget
        self.username_entry.insert(0, 'Enter Username') # Sets placeholder text
        # Clears placeholder text when you click in the entry field
        self.username_entry.bind("<FocusIn>", lambda args: self.username_entry.delete('0', 'end'))
        self.username_entry.place(relx=0.35, rely=0.3, relheight=0.06, relwidth=0.34) # Places widget onto window
        
        ## CREATING AND DISPLAYING PASSWORD ENTRY WIDGET ##
        self.password_entry = ttk.Entry(self)                              
        
        self.password_entry.insert(0, 'Enter Password')
        self.password_entry.bind("<FocusIn>", lambda args: self.password_entry.delete('0', 'end'))
        self.password_entry.place(relx=0.35, rely=0.37, relheight=0.06, relwidth=0.34)

        
                
    def login(self): # Login function which is executed when the login button is clicked
        username = self.username_entry.get() # Gets the value from the username entry widget
        password = self.password_entry.get() # Gets the value from the password entry widget
  
        with sqlite3.connect(DATA_FOLDER+"Accounts.db") as  db:# Connects to the Accounts database and checks if the login credentials are valid
            cursor = db.cursor() # Creates a cursor object used to traverse the database
        find_user = ("SELECT * FROM user WHERE username = ? AND password =?") # runs a sql query on the database to check login validity
        cursor.execute(find_user,[(username),(password)])
        results = cursor.fetchall() # Stores the query results in variable called 'results'
        if results:
            for i in results:
                self.name=i[2]
            self.login_success(username) # if credentials are valid then the LoginSuccess() is executed
        else:
            self.login_fail() # if credentials are invalid then the LoginFail() is executed
        db.commit() # Makes changes made to the database permanent
        
    def login_success(self,username):# Executed if Login is succesful
        global usr_name
        usr_name = username
        self.popup = tk.Toplevel() # Creates a pop-up window
        self.popup.wm_title("Login Succesful")

        # Creates and displays a welcome message on the pop up window
        label = ttk.Label(self.popup,text=("Welcome\n\n     "+self.name), font =NORM_FONT, background='grey11', foreground='limegreen')
        label.pack(side='top', expand=True)

        # Creates and displays a continue button, which is binded to the LSMenu function
        con_img = tk.PhotoImage(file= IMAGES_FOLDER+"con_button.png")        
        c = tk.Button(self.popup, image= con_img, command=self.ls_menu, borderwidth=0,background ='grey11', activebackground='grey11')
        c.image = con_img
        c.pack(side='bottom', expand=True)

        # Sets the dimensions of the pop-up window
        width_of_window = 200
        height_of_window = 150
        screen_width = self.popup.winfo_screenwidth()
        screen_height = self.popup.winfo_screenheight()
        x_coordinate = (screen_width//2) - (width_of_window//2)
        y_coordinate = (screen_height//2) - (height_of_window//2)
        self.popup.geometry("%dx%d" % (width_of_window, height_of_window))
        self.popup.configure(bg='grey11')
        self.popup.mainloop() # ends the loop for the pop up window

    def ls_menu(self): 
        self.popup.destroy() # Closes the login sucessful pop up window
        self.username_entry.delete(0,'end') # Clears the username and password entry fields 
        self.password_entry.delete(0,'end')
        self.controller.show_frame(menu) # Displays the Menu screen

    def login_fail(self): #  Executed if user login fails
        self.popup = tk.Toplevel() # Creates a pop-up window
        self.popup.wm_title("Login Failed") # Sets windows title

        label = ttk.Label(self.popup,text=("Username and password not recognised"), font =NORM_FONT, background='grey11', foreground='limegreen')# Error message (Label widget) 
        label.pack(side='top', expand=True)

        try_img = tk.PhotoImage(file= IMAGES_FOLDER+"Try_Again_Button.png")        
        try_again = tk.Button(self.popup, image= try_img, command=self.lf_home, borderwidth=0,background ='grey11', activebackground='grey11')
        try_again.image = try_img
        try_again.pack(side='bottom', expand=True)

        # Sets the dimensions of the pop-up window
        width_of_window = 450
        height_of_window = 150
        screen_width = self.popup.winfo_screenwidth()
        screen_height = self.popup.winfo_screenheight()
        x_coordinate = (screen_width//2) - (width_of_window//2)
        y_coordinate = (screen_height//2) - (height_of_window//2)
        self.popup.geometry("%dx%d" % (width_of_window, height_of_window))
        self.popup.configure(bg='grey11')
        self.popup.mainloop()# ends the loop for the pop up window

    def lf_home(self):
        self.popup.destroy() # Closes the login failed pop up window
        self.controller.show_frame(home) # Displays the Menu screen
        
class register(tk.Frame): # Declaring register class which inherits from Tkinters Frame class (Creating Register screen)
    def __init__(self, parent, controller):# Constructor method for register class
        tk.Frame.__init__(self, parent, bg='grey11') # Initialising Tkinters Frame class
        self.controller = controller # Assigning controller as a variable of the register class    
        ## CREATING AND DISPLAYING REGISTER TITLE LABEL WIDET ##
        reg_title = tk.Label(self,text='Fill in details below to create an account', background='grey11', foreground='limegreen')
        reg_title.place(relx=0.21, rely=0.07, height=29, width=318)
        ## CREATING AND DISPLAYING THE USERNAME LABEL WIDGET ##
        reg_username = tk.Label(self, text='Username:' , background='grey11', foreground='limegreen')
        reg_username.place(relx=0.13, rely=0.35, height=29, width=87)        
        ## CREATING AND DISPLAYING THE FIRSTNAME LABEL WIDGET ##
        reg_firstname = tk.Label(self, text='Firstname:', background='grey11', foreground='limegreen')
        reg_firstname.place(relx=0.13, rely=0.17, height=29, width=85)
        ## CREATING AND DISPLAYING THE SURNAME LABEL WIDGET ##
        reg_surname = tk.Label(self, text='Surname:' , background='grey11', foreground='limegreen')
        reg_surname.place(relx=0.13, rely=0.26, height=29, width=78)
        ## CREATING AND DISPLAYING THE PASSWORD LABEL WIDGET ##
        reg_pass = tk.Label(self,text='Password:' , background='grey11', foreground='limegreen')
        reg_pass.place(relx=0.13, rely=0.45, height=29, width=84)        
        ## CREATING AND DISPLAYING THE RE-ENTER PASSWORD LABEL WIDGET ##
        reg_pass2 = tk.Label(self, text='Re-enter Password:' , background='grey11', foreground='limegreen')
        reg_pass2.place(relx=0.13, rely=0.54, height=29, width=156)
        ## CREATING AND DISPLAYING THE FIRSTNAME ENTRY WIDGET ##
        self.reg_firstname_entry = tk.Entry(self,cursor="ibeam")
        self.reg_firstname_entry.place(relx=0.31, rely=0.16, relheight=0.06, relwidth=0.34)
        ## CREATING AND DISPLAYING THE SURNAME ENTRY WIDGET ##
        self.reg_surname_entry = tk.Entry(self,cursor="ibeam")
        self.reg_surname_entry.place(relx=0.31, rely=0.26, relheight=0.06, relwidth=0.34)
        ## CREATING AND DISPLAYING THE USERNAME ENTRY WIDGET ##
        self.reg_username_entry = tk.Entry(self,cursor="ibeam")
        self.reg_username_entry.place(relx=0.31, rely=0.35, relheight=0.06, relwidth=0.34)
        ## CREATING AND DISPLAYING THE PASSWORD ENTRY WIDGET ##
        self.reg_pass_entry = ttk.Entry(self,show="*" ,cursor="ibeam")
        self.reg_pass_entry.place(relx=0.31, rely=0.44, relheight=0.06, relwidth=0.34)        
        ## CREATING AND DISPLAYING THE RE-ENTER PASSWORD ENTRY WIDGET ##
        self.reg_pass2_entry = tk.Entry(self,show="*" ,cursor="ibeam")
        self.reg_pass2_entry.place(relx=0.41, rely=0.54, relheight=0.06, relwidth=0.34)
        ## CREATING AND DISPLAYING THE REGISTER BUTTON ##
        reg_img = tk.PhotoImage(file= IMAGES_FOLDER+'register_button.png') # Adding image to register button
        self.reg_butt = tk.Button(self, image=reg_img, command = self.create, borderwidth=0,background ='grey11', activebackground='grey11', foreground='limegreen')
        self.reg_butt.image=reg_img # Keeping a reference of the image
        self.reg_butt.place(relx=0.36, rely=0.71, height=35, width=120)
   
    def create(self):
        # Gets the entered values for all entery widgets
        username=self.reg_username_entry.get() 
        firstname=self.reg_firstname_entry.get()
        surname=self.reg_surname_entry.get()
        password=self.reg_pass_entry.get()
        password1=self.reg_pass2_entry.get()
        values = [username, firstname, surname, password, password1]

        # Check to see if a entry widget is empty
        empty = True
        count = 0
            
        while empty == True and count != 5: # While loop that sets empty to True if a value is blank for an entry widget
            if len(values[count]) > 0:
                empty = False
            else:
                empty = True
                break
            count+=1

        if empty == True: # If one or more entry widgets are blank the appropriate prompt message is displayed
            self.fill_in_all_details()
        else: # Else if no entry widget is blank continue
            with sqlite3.connect(DATA_FOLDER+"Accounts.db") as  db: # Connects to the Accounts database
                cursor = db.cursor() #  Creates cursor object to traverse through the database
                findUser = ("SELECT * FROM user WHERE username = ?") # SQL query to check if that username already exists
                cursor.execute(findUser,[(username)])
            # If username exists execute userTaken() (pop-up window that prompts that the username is taken/ already exists)
            if cursor.fetchall(): 
                self.user_taken()
            # Else if username is not taken then gets all the values from the other entry widgets
            else:
                if password != password1: # VALIDATION - checks to see whether the initial password matches the re-entered password
                    self.pass_miss_match() # If they dont match then it executes passMissMatch function
                    self.controller.show_frame(register)
                ## SQL query to Write users account details to the Accounts database
                insertData = '''INSERT INTO user (username,firstname,surname,password) 
                VALUES(?,?,?,?)'''
                cursor.execute(insertData,[(username),(firstname), (surname), (password)])
                db.commit() # Makes changes made to the database permanent
                self.acc_created() # Executes the accCreated() function

    def r2_register(self): # Executed if the user wants to try again in creating an account
        self.popup.destroy()
        self.controller.show_frame(register)
    def r2_home(self): # Executed if the user wants to return to the home screen
        self.popup.destroy()
        self.controller.show_frame(home)
                
    def user_taken(self): # userTaken function, executed if the username already exists in the database
            self.popup = tk.Toplevel() #Creates user taken pop-up window
            self.popup.wm_title("!USER TAKEN!") # Window title
            ## CREATING AND DISPLAYING THE USER TAKEN MESSAGE LABEL WIDGET ##
            label = tk.Label(self.popup,text="User already exists!", font =NORM_FONT, borderwidth=0,background ='grey11',foreground='limegreen')
            label.pack(side='top', expand=True)
            ## CREATING AND DISPLAYING THE TRY AGAIN BUTTON WIDGET##
            try_img = tk.PhotoImage(file= IMAGES_FOLDER+"Try_Again_Button.png")        
            try_again = tk.Button(self.popup, image= try_img, command=self.r2_register, borderwidth=0,background ='grey11', activebackground='grey11')
            try_again.image = try_img
            try_again.pack(side='bottom', expand=True)
            ## CREATING AND DISPLAYING THE HOME BUTTON WIDGTET ##              #  Configure widgets to match colour scheme
            button1 = tk.Button(self.popup, text="Home", command=self.r2_home, borderwidth=0,background ='grey11', activebackground='grey11', foreground='limegreen')
            button1.pack(side='bottom', expand=True)

            ## CENTERING THE POP-UP WINDOW ##
            width_of_window = 250
            height_of_window = 150
            screen_width = self.popup.winfo_screenwidth()
            screen_height = self.popup.winfo_screenheight()
            x_coordinate = (screen_width//2) - (width_of_window//2)
            y_coordinate = (screen_height//2) - (height_of_window//2)
            self.popup.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x_coordinate, y_coordinate))
            self.popup.configure(bg='grey11') # Set windows background colour to match client requested colour scheme
            self.popup.mainloop() ## User taken pop-up window loop

    def pass_miss_match(self): # passMissMatch function, executed if the two entered passwords by the the user do not match
            self.popup = tk.Toplevel() #  Creates password mismatch pop-up window
            self.popup.wm_title("! PASSWORD ERROR !") # Window title
            
            ## CREATING AND DISPLAYING THE ERROR MESSAGE LABEL WIDGET ##
            label = tk.Label(self.popup,text="Passwords do not match!", font =NORM_FONT, borderwidth=0,background ='grey11',foreground='limegreen')
            label.pack(side='top', expand=True)
            ## CREATING AND DISPLAYING THE TRY AGIAN BUTTON WIDGET ##
            try_img = tk.PhotoImage(file= IMAGES_FOLDER+"Try_Again_Button.png")        
            try_again = tk.Button(self.popup, image= try_img, command=self.r2_register, borderwidth=0,background ='grey11', activebackground='grey11')
            try_again.image = try_img
            try_again.pack(side='bottom', expand=True)
            ## CREATING AND DISPLAYING THE HOME BUTTON WIDGET ##
            button1 = tk.Button(self.popup, text="Home", command=self.r2_home, borderwidth=0,background ='grey11', activebackground='grey11', foreground='limegreen')
            button1.pack(side='bottom', expand=True)
            ##  CENTERING THE POP-UP WINDOW ## 
            width_of_window = 400
            height_of_window = 150
            screen_width = self.popup.winfo_screenwidth()
            screen_height = self.popup.winfo_screenheight()
            x_coordinate = (screen_width//2) - (width_of_window//2)
            y_coordinate = (screen_height//2) - (height_of_window//2)
            self.popup.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x_coordinate, y_coordinate))
            self.popup.configure(bg='grey11')
            self.popup.mainloop() # Password mismatch pop-up window main loop

    def acc_created(self): # accCreated function, executed in the case when the account is succesfully created
            self.popup = tk.Toplevel() # Creates the account created pop up window
            self.popup.wm_title("!!") # Setting the windows title

            ## CREATING AND DISPLAYING THE SUCCESS MESSAGE, LABEL WIDGET ##
            label = tk.Label(self.popup,text="Account succesfully created", font =NORM_FONT, borderwidth=0,background ='grey11',foreground='limegreen')
            label.pack(side='top', expand=True)
            ## CREATING AND DISPLAYING THE SIGN IN BUTTON WIDGET ## 
    

            # Creates and displays a continue button, which is binded to the LSMenu function
            sign_img = tk.PhotoImage(file= IMAGES_FOLDER+"sign_in_button.png")        
            b = tk.Button(self.popup, image= sign_img, command=self.r2_home, borderwidth=0,background ='grey11', activebackground='grey11')
            b.image = sign_img
            b.pack(side='bottom', expand=True)

            ## CENTERING THE POP-UP WINDOW ##
            width_of_window = 400
            height_of_window = 150
            screen_width = self.popup.winfo_screenwidth()
            screen_height = self.popup.winfo_screenheight()
            x_coordinate = (screen_width//2) - (width_of_window//2)
            y_coordinate = (screen_height//2) - (height_of_window//2)
            self.popup.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x_coordinate, y_coordinate))
            self.popup.configure(bg='grey11')
            self.popup.mainloop() # Account created pop up window main loop

    def fill_in_all_details(self): # function that is executed in the case of one or more mepty entry fields
            self.popup = tk.Toplevel() # Creates the empty entry  pop up window
            self.popup.wm_title("!!") # Setting the windows title

            ## CREATING AND DISPLAYING THE ERROR MESSAGE, LABEL WIDGET ##
            label = tk.Label(self.popup,text="Please fill in all the fields", font =NORM_FONT, borderwidth=0,background ='grey11',foreground='limegreen')
            label.pack(side='top', expand=True)
            ## CREATING AND DISPLAYING THE SIGN IN BUTTON WIDGET ## 
            try_img = tk.PhotoImage(file= IMAGES_FOLDER+"Try_Again_Button.png")        
            try_again = tk.Button(self.popup, image= try_img, command=self.r2_register, borderwidth=0,background ='grey11', activebackground='grey11', foreground='limegreen')
            try_again.image = try_img
            try_again.pack(side='bottom', expand=True)
            ## CENTERING THE POP-UP WINDOW ##
            width_of_window = 400
            height_of_window = 150
            screen_width = self.popup.winfo_screenwidth()
            screen_height = self.popup.winfo_screenheight()
            x_coordinate = (screen_width//2) - (width_of_window//2)
            y_coordinate = (screen_height//2) - (height_of_window//2)
            self.popup.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x_coordinate, y_coordinate))
            self.popup.configure(bg='grey11')
            self.popup.mainloop() # fill_in_all_deatils pop up window main loop
            
# Declaring the menu class whioch inherits from Tkinter's Frame class            
class menu(tk.Frame):

    # Declaring menu's constructor method which is called when the class in instantiated
    def __init__(self, parent, controller):

        # Initialises Tkinter's Frame class
        tk.Frame.__init__(self, parent, bg='grey11') # Setting the background of the frame to 'grey11'
    
        # Storking controller as a varioable of the menu class
        self.controller = controller

        # Loading the image for the Get rec button
        get_rec_img = tk.PhotoImage(file= IMAGES_FOLDER+"get_rec_button.png")
        # Shrinks the image
        get_rec_img = get_rec_img.subsample(3)
        # Crerating the get_rec_button with get_rec_img as its image and binding it with the function to display the get rec screen
        get_rec_button = tk.Button(self,image=get_rec_img, borderwidth = 0,command=lambda: controller.show_frame(get_rec), background = "grey11")
        # Keeping a reference of get_rec_button's image
        get_rec_button.image=get_rec_img
        # Displaying the Button widget on the window
        get_rec_button.grid(row=0,sticky="nsew")      


        # Loading the image for the browse button
        browse_button_img = tk.PhotoImage(file= IMAGES_FOLDER+"browse_button.png")
        # Shrinks the image
        browse_button_img = browse_button_img.subsample(3)
        # Crerating the browse_button with browse_button_img as its image and binding it with the function to display the browse screen
        browse_button = tk.Button(self, image= browse_button_img, borderwidth = 0,command=lambda: controller.show_frame(browse), background = "grey11")
        # Keeping a reference of browse_button's image
        browse_button.image=browse_button_img
        # Displaying the Button widget on the window
        browse_button.grid(row=0,column=1, sticky="nsew")

        # Loading the image for the profile button
        profile_button_img = tk.PhotoImage(file= IMAGES_FOLDER+"profile_button.png")
        # Shrinks the image
        profile_button_img = profile_button_img.subsample(3)
        # Crerating the profile_button with profile_button_img as its image and binding it with the function to display the profile screen
        profile_button = tk.Button(self,image=profile_button_img, borderwidth = 0,command=lambda: controller.show_frame(profile), background = "grey11")
        # Keeping a reference of profile_button's image
        profile_button.image=profile_button_img
        # Displaying the Button widget on the window
        profile_button.grid(row=1,sticky="nsew")

        # Loading the image for the pictionary button
        pictionary_button_img = tk.PhotoImage(file= IMAGES_FOLDER+"pictionary_button.png")
        # Shrinks the image
        pictionary_button_img = pictionary_button_img.subsample(3)
        # Crerating the pictionary_button with pictionary_button_img as its image and binding it with the function to display the pictionary screen
        pictionary_button = tk.Button(self,image=pictionary_button_img, borderwidth = 0,command=lambda: controller.show_frame(pictionary), background = "grey11")
        # Keeping a reference of pictionary_button's image
        pictionary_button.image=pictionary_button_img
        # Displaying the Button widget on the window
        pictionary_button.grid(row=1,column=1, sticky="nsew")
        
        # Configuring the priority of the widgets
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        
class get_rec(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg = 'grey11')
        

        self.controller = controller

        self.getRec_label = tk.Label(self, text='Find recommendation for:', width=210, relief='flat', bg = 'grey11', fg='lime green', borderwidth=2,highlightbackground="lime green" )
        self.getRec_label.place(relx=0.00, rely=0.07, height=35, width=200)

        self.search_entry = ttk.Entry(self)
        self.search_entry.place(relx=0.28, rely=0.08, relheight=0.05, relwidth=0.23)

        self.search_butt = tk.Button(self, text='Search', command= self.populate, bg = 'grey11', fg='lime green', borderwidth=2,highlightbackground="lime green" )
        self.search_butt.place(relx=0.54, rely=0.08, height=30, width=120)

        

        frm = tk.Frame(self)
        frm.place(relx=0.03, rely=0.16, relheight=0.73, relwidth=0.7)

        scrollbar = tk.Scrollbar(frm, orient="vertical", highlightcolor="#d9d9d9", highlightbackground="#d9d9d9")
        scrollbar.pack(side='right', fill='y')


        self.listNodes = tk.Listbox(frm, width=100, yscrollcommand=scrollbar.set, font=("Helvetica", 12))
        self.listNodes.bind("<Double-Button-1>", self.OnDouble)
        self.listNodes.pack(expand=True, fill='y')

        scrollbar.config(command=self.listNodes.yview)

        self.getRec_note = tk.Label(self, text='Note - Search for anime then Double click on the anime you wish to select', bg = 'grey11', fg='lime green')
        self.getRec_note.place(relx=0.02, rely=0.9, relheight=0.06, relwidth=0.67)
    
    def OnDouble(self, event):
        
        self.popup = tk.Tk()
        self.popup.wm_title("Anime Recommendations!")
        widget = event.widget
        selection=widget.curselection()
        value = widget.get(selection[0])
        
        anime = get_similar_animes(value)
        t_text = "Recommendations for "+value

        title = tk.Label(self.popup, text = t_text,bg='grey11',fg='limegreen')
        title.grid(row=0, sticky = "ne")
        

        a = tk.Label(self.popup,text=anime[0],bg='grey11',fg='limegreen')
        a.grid(row=1, column=0)
        b = tk.Button(self.popup,text='Click for more info', command=lambda:self.openLink(anime[0]),bg='grey11',fg='limegreen')
        b.grid(row=1, column=1)

        a1 = tk.Label(self.popup,text=anime[1],bg='grey11',fg='limegreen')
        a1.grid(row=2, column=0)
        b = tk.Button(self.popup,text='Click for more info',command=lambda:self.openLink(anime[1]),bg='grey11',fg='limegreen')
        b.grid(row=2, column=1)

        a2 = tk.Label(self.popup,text=anime[2],bg='grey11',fg='limegreen')
        a2.grid(row=3, column=0)
        b = tk.Button(self.popup,text='Click for more info',command=lambda:self.openLink(anime[2]),bg='grey11',fg='limegreen')
        b.grid(row=3, column=1)
        
        a3 = tk.Label(self.popup,text=anime[3],bg='grey11',fg='limegreen')
        a3.grid(row=4, column=0)
        b = tk.Button(self.popup,text='Click for more info',command=lambda:self.openLink(anime[3]),bg='grey11',fg='limegreen')
        b.grid(row=4, column=1)

        a4 = tk.Label(self.popup,text=anime[4],bg='grey11',fg='limegreen')
        a4.grid(row=5, column=0)
        b = tk.Button(self.popup,text='Click for more info',command=lambda:self.openLink(anime[4]),bg='grey11',fg='limegreen')
        b.grid(row=5, column=1)
    
                  
        self.popup.configure(bg='grey11')
        self.popup.mainloop()
        
    def populate(self):
        self.listNodes.delete(0, 'end')
        partial=string.capwords(self.search_entry.get())
        possibleSearch= get_possible_searches(partial)
        for i in range(0, len(possibleSearch)):
            self.listNodes.insert(i, possibleSearch[i])

    def openLink(self, anime):
        try:
            a_id=get_ID(anime)
            url = "https://myanimelist.net/anime/"+a_id[0][0]
            webbrowser.open(url)
        except IndexError:
            print("Link broken")
                
        
# Declaring the browse class which inherits from Tkinter's Frame class (Creating the browse screen)
class browse(tk.Frame):
    # Declaring browse class' constructor method
    def __init__(self, parent, controller):

        # Initialising Tkinter's Frame class
        tk.Frame.__init__(self, parent, bg='grey11')
        
       
        
        # Creating and displaying a genres label for the checkbuttons 
        GenreLabel = tk.Label(self, text="Genres:", fg='limegreen', bg='grey11')
        GenreLabel.grid(row=1, sticky='w')
        
        # List of all the genres
        self.GENRES = ["Action","Adventure","Cars","Comedy","Dementia",
                   "Demons","Drama","Ecchi","Fantasy","Game","Harem",
                  "Hentai","Historical","Horror","Josei","Kids",
                  "Magic","Martial Arts","Mecha","Military","Music",
                  "Mystery","Parody","Police","Psychological",
                  "Romance","Samurai","School","Sci-Fi","Seinen",
                  "Shoujo","Shoujo Ai","Shounen","Shounen Ai",
                  "Slice of Life","Space","Sports","Super Power",
                  "Supernatural","Thriller","Vampire","Yaoi","Yuri"]

        # Creating and displaying each genre ans a checkbutton, most efficient way in Tkinter
        self.vars = []
        self.chk = []
        for i in range(0,5):
            self.var = tk.IntVar()
            self.chk.append(tk.Checkbutton(self, text=self.GENRES[i], variable=self.var, fg='limegreen', bg='grey11'))
            self.chk[-1].grid(row=2, column=(i+1),sticky="w")
            self.vars.append(self.var)
        for i in range(5,10):
            self.var = tk.IntVar()
            self.chk.append(tk.Checkbutton(self, text=self.GENRES[i], variable=self.var, fg='limegreen', bg='grey11'))
            self.chk[-1].grid(row=(3),column=((i+1)-5),sticky="w")
            self.vars.append(self.var)
        for i in range(10,15):
            self.var = tk.IntVar()
            self.chk.append(tk.Checkbutton(self, text=self.GENRES[i], variable=self.var, fg='limegreen', bg='grey11'))
            self.chk[-1].grid(row=(4),column=((i+1)-10),sticky="w")
            self.vars.append(self.var)
        for i in range(15,20):
            self.var = tk.IntVar()
            self.chk.append(tk.Checkbutton(self, text=self.GENRES[i], variable=self.var, fg='limegreen', bg='grey11'))
            self.chk[-1].grid(row=(5),column=((i+1)-15),sticky="w")
            self.vars.append(self.var)
        for i in range(20,25):
            self.var = tk.IntVar()
            self.chk.append(tk.Checkbutton(self, text=self.GENRES[i], variable=self.var, fg='limegreen', bg='grey11'))
            self.chk[-1].grid(row=(6),column=((i+1)-20),sticky="w")
            self.vars.append(self.var)
        for i in range(25,30):
            self.var = tk.IntVar()
            self.chk.append(tk.Checkbutton(self, text=self.GENRES[i], variable=self.var, fg='limegreen', bg='grey11'))
            self.chk[-1].grid(row=(7),column=((i+1)-25),sticky="w")
            self.vars.append(self.var)
        for i in range(30,35):
            self.var = tk.IntVar()
            self.chk.append(tk.Checkbutton(self, text=self.GENRES[i], variable=self.var, fg='limegreen', bg='grey11'))
            self.chk[-1].grid(row=(8),column=((i+1)-30),sticky="w")
            self.vars.append(self.var)
        for i in range(35,40):
            self.var = tk.IntVar()
            self.chk.append(tk.Checkbutton(self, text=self.GENRES[i], variable=self.var, fg='limegreen', bg='grey11'))
            self.chk[-1].grid(row=(9),column=((i+1)-35),sticky="w")
            self.vars.append(self.var)
        for i in range(40,43):
            self.var = tk.IntVar()
            self.chk.append(tk.Checkbutton(self, text=self.GENRES[i], variable=self.var, fg='limegreen', bg='grey11'))
            self.chk[-1].grid(row=(10),column=((i+1)-40),sticky="w")
            self.vars.append(self.var)


        # Creating and displaying the Search button which takes all the inputs from the user and querys the database with the given criteria
        Search= tk.Button(self, text="Search", command =self.query, fg='limegreen', bg='grey11')
        Search.grid(columnspan=10)
    

    # Function for the Search buttons, which querys the database with the given criteria inputted by the user
    def query(self):

        # Creates a pop up window
        self.popup = tk.Tk()
        self.popup.configure(bg='grey11')

        # Creates and display a title label for the pop up window
        self.title = tk.Label(self.popup, text=("Search Results:\nDouble click for more info"), width=210, relief='flat',bg='grey11',fg='limegreen')
        self.title.place(relx=0.04, rely=0.07, height=35, width=210)

        # Creates and displays a frame used to hold the listbox widget and scroll bar widget
        frm = tk.Frame(self.popup)
        frm.place(relx=0.03, rely=0.16, relheight=0.73, relwidth=0.7)

        # Creates and adds a scroll bar to the list box to allow the user to scroll up and down the search results
        scrollbar2 = tk.Scrollbar(frm, orient="vertical", highlightcolor="#d9d9d9", highlightbackground="#d9d9d9")
        scrollbar2.pack(side='right', fill='y')

        # Creating and displaying the Listbox widget
        self.listNodes2 = tk.Listbox(frm, width=100, yscrollcommand=scrollbar2.set, font=("Helvetica", 12))
        self.listNodes2.bind("<Double-Button-1>", self.OnDouble2)
        self.listNodes2.pack(expand=True, fill='y')
        scrollbar2.config(command=self.listNodes2.yview)

        # Button which returns the user to the browse screen and closes the search results pop up window
        button1 = tk.Button(self.popup, text="Return", command = self.return1,bg='grey11',fg='limegreen')
        button1.pack(side='bottom')

        # Stores the whatever values are checked from the check buttons into an array
        states=[]
        for x in self.vars:
            states.append(x.get())
        genreIndex = [i for i, s in enumerate(states) if s == 1]
        self.genreResults=[]
        for x in genreIndex:
            self.genreResults.append(self.GENRES[x])
        

        # Connects to the anime database  and runs an sql query with the given criteria
        with sqlite3.connect(DATA_FOLDER+"animeData.db") as  db: #anime database
            c = db.cursor()
            #self.genreResults is the list containing the genres i want to query
            user_input = self.genreResults  # for example: ['Action','Drama']
            convert_to_like_conditions = ' and '.join(list(map(lambda item : "genre like '%{0}%'".format(item), user_input)))
            c.execute("select * from t where %s" % convert_to_like_conditions ) 
            self.results = c.fetchall()
            db.commit()
            
        
        # Displays all the search results from the query in the listbox
        for i in range(0,len(self.results)):
            self.listNodes2.insert(i,self.results[i][1])

        # Pop up window dimensions configuration
        width_of_window = 700
        height_of_window = 538
        screen_width = self.popup.winfo_screenwidth()
        screen_height = self.popup.winfo_screenheight()
        x_coordinate = (screen_width//2) - (width_of_window//2)
        y_coordinate = (screen_height//2) - (height_of_window//2)
        self.popup.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x_coordinate, y_coordinate))
        self.popup.mainloop()

    # Function which is executed when a search result in the listbox is double clicked
    def OnDouble2(self, event):
        # Gets the value of the anime of the listbox node that was double clicked
        widget = event.widget
        selection=widget.curselection()
        value = widget.get(selection)
        i = index = [idx for idx, s in enumerate(self.results) if value in s][0]

        # Creates a myanimelist.net website for that anime and opens it up in the user's browser
        url = 'https://myanimelist.net/anime/'+self.results[i][0]+self.results[i][1]
        webbrowser.open(url)

    # Function which is executed when the return button is clicked
    def return1(self):
        self.popup.destroy()
        
            
        
# Declaring the class for the Profile screen, which inherits from Tkinter's Frame class   
class profile(tk.Frame):
    
    # Declaring the constructor method for the profile class, which runs when the class is instantiated
    def __init__(self, parent, controller):
        # Initialising Tkinter's Frame class
        tk.Frame.__init__(self, parent, bg='grey11')

        # Storing controller as a variable of the profile class
        self.controller = controller

        # Creating and displaying the label for the entry widget which will be used so that the user can enter which anime they wish to add to their favourites
        self.getRec_label = tk.Label(self, text='Select an anime\nyou wish to add\nto your favourites:', width=210, relief='flat', bg = 'grey11', fg='lime green', borderwidth=2,highlightbackground="lime green" )
        self.getRec_label.place(relx=0.00, rely=0.07, height=38, width=200)

        # Creating and displaying the Entry widget which will allow the user to input the name of an anime
        self.search_entry = ttk.Entry(self)
        self.search_entry.place(relx=0.28, rely=0.08, relheight=0.05, relwidth=0.23)

        # Creating and displaying a button, which when clicked will output the search results of the user's input
        self.search_butt = tk.Button(self, text='Search', command= self.populate, bg = 'grey11', fg='lime green', borderwidth=2,highlightbackground="lime green" )
        self.search_butt.place(relx=0.54, rely=0.08, height=30, width=120)

        # Creating and displaying a button, which when clicked displays the user's current favourite anime list
        self.view_butt = tk.Button(self, text='view favourites', command = self.view_favourites, bg = 'grey11', fg='lime green', borderwidth=2,highlightbackground="lime green")
        self.view_butt.pack(side='top')
        
        

        # Creating and displaying a frame to contain the list box and scrollbar widget
        frm = tk.Frame(self)
        frm.place(relx=0.03, rely=0.16, relheight=0.73, relwidth=0.7)

        # Creating and displaying a scroll bar on the right of the frame which is used to scroll up and down the list box
        scrollbar = tk.Scrollbar(frm, orient="vertical", highlightcolor="#d9d9d9", highlightbackground="#d9d9d9")
        scrollbar.pack(side='right', fill='y')

        # Creating and displaying a Listbox widget within the same frame as the scrollbar
        self.listNodes = tk.Listbox(frm, width=100, yscrollcommand=scrollbar.set, font=("Helvetica", 12))
        self.listNodes.bind("<Double-Button-1>", self.OnDouble)
        self.listNodes.pack(expand=True, fill='y')
        scrollbar.config(command=self.listNodes.yview)

        # Creating and displaying a label to give the user some instructions as to how to use the list box.
        self.getRec_note = tk.Label(self, text='Note - Search for anime then Double click on the anime you wish to select', bg = 'grey11', fg='lime green')
        self.getRec_note.place(relx=0.02, rely=0.9, relheight=0.06, relwidth=0.67)

    # Function which populates the List box with the search results from the user's input.
    def populate(self):
        self.listNodes.delete(0, 'end')
        partial=string.capwords(self.search_entry.get())
        possibleSearch= get_possible_searches(partial)
        for i in range(0, len(possibleSearch)):
            self.listNodes.insert(i, possibleSearch[i])

    # Function which adds the selected anime to the user favourites
    def OnDouble(self, event):
        # Gets the value of the node that was selected from the list box and stores it in the varibale, value
        widget = event.widget
        selection=widget.curselection()
        value = widget.get(selection)

        # Gets the value from does file exist function
        # if th efile exists then we open the file in append mode and append the selected anime to the users favourite list
        if self.does_file_exist(usr_name+'.txt'):
            with open(usr_name+'.txt', "a") as f:
                f.write(value+'\t')
        # Else if the file does not exist then we create it using the write mode and write the selected value to the file
        else:
            with open(usr_name+'.txt', "w") as f:
                f.write(value+'\t')

                
        # Once the selected anime has been added to the users favourites list we give them the option to view their cirrent favourites list
        user_choice = tk.messagebox.askquestion("ADDED TO FAVOURITES",value+" Has been added to your favourites list\n Would you like to view your current favourites?")

        # If they select yes  then we execyte the view_favourites function which displays the current favourites
        if user_choice == 'yes':
            self.view_favourites()
        # If they select no then we just close the message box and return to the profile screen
        else:
            pass
            
      
    
            
    # Function to check whether a file already exist using the path.exists function from the os library
    def does_file_exist(self,file_name):
        return os.path.exists(file_name)

    # Function that displays the users curerent favourite animes on a pop up window
    def view_favourites(self):

        # UPDATE - added steps that will check if the favourites list text file exists
        # If it doesnt then we prompt the user that their list is empty
        if self.does_file_exist(usr_name+'.txt') == False:
            # Giving them an option to add an anime to their favourites list  or not
            user_choice = tk.messagebox.askquestion("ALERT","Your favourites list is currently empty, Would you like to add an anime to it?")

            # terminates the function regardless of the user choice thus preventing the error yet still keeping the program functional
            if user_choice == 'yes':
                return
            else:
                return
            
        
        # retrieves the users current favourite list by reading it from the text file
        with open(usr_name+'.txt', "r") as f:
            for lines in f:
                    favourites_list = lines
        # Creates the pop up window
        pop_up = tk.Toplevel()
        pop_up.title('Your favourites list')

        

        favs = tk.StringVar()
        favs.set(favourites_list)
        # Creating and displaying the label which will display the favourites list on screen
        label = tk.Label(pop_up, text = favs.get())
        label.pack()

        # Creating and displaying a button which will close the screen and return to the profile screen when the user is done
        close = tk.Button(pop_up, text= "Close", command = pop_up.destroy)
        close.pack()

        # Pop up windows mainloop
        pop_up.mainloop()
    
        
            
# Opens file in read mode
f = open(PICTIONARY_FOLDER+'questions.txt', 'r') 

# Temporary Python array
data = [] 

# For each line in the text file it splits the line based on tabs
for row_num, line in enumerate(f):
    values = line.strip().split('\t')
    # first line is the header (image, answer)
    if row_num == 0:
         # Stores the haeader in an array
         header = values 
    else:
        data.append([v for v in values])

# Converts Python array to a numpy array
question_data = np.array(data)


# Close the file
f.close() 
## TESTING PURPOSES ##
    #print(question_data) 
    #print(header)

## RANDOMIZE THE QUESTIONS BEFORE EACH RUN ##
np.random.shuffle(question_data)
    #print(question_data)# TESTING

# Declares the Pictionary class which inherits from Tkinters frame class (Creates the Pictionary screen)
class pictionary(tk.Frame):
    # Constructor method for the Pictionary class
    def __init__(self, parent, controller):

        # Initalises Tkinter's Frame class
        tk.Frame.__init__(self, parent, bg='grey11')

        # Stores controller as a variable of the pictionary class
        self.controller =controller
        self.parent = parent

        # Setting count to 0 at the start (indicating we are at the first question)
        self.count =0
        
        # Number of questions set to 10 for testing purposes
        self.max_questions = 10 

        # Executes the display_question function (declared below) with the question image, answer and choices for the first question from the text file
        self.display_question(question_data[self.count][0],question_data[self.count][1],question_data[self.count][2])
        

    # Function which display the question onto the window. Takes a questions image, answer and choices as parameters.
    def display_question(self, image, answer, choices):
        
        # Loads the image in a way that Python can read it
        self.img = tk.PhotoImage(file=PICTIONARY_FOLDER+image+'.png')
        
        
        # print('answer:',answer) ## Testing purposes to check the correct answer

        # Seperates the choices for the question into single elements so they can be displayed on the window
        choices = choices.replace('"','')
        choices = [x.strip() for x in choices.split(',')]
        # Randomizes the choices
        random.shuffle(choices)

        # Creating and displaying the label that contains the image that is to be guessed
        self.anime_image = tk.Label(self, image=self.img,relief='flat')
        self.anime_image.image = self.img
        self.anime_image.pack()
        
        
        # Creating and displaying the label which displays the current level to the user i.e their score
        level = 'level',self.count+1
        self.level = tk.Label(self, text=level,borderwidth=0, relief='flat', bg='limegreen', fg='black')
        self.level.place(relx=0.4, rely=0.04, height=29, width=120)

        # Creating and displaying the Buttons which represent the 4 available choices to the user
        # Note the command for each button passes the value of the choice to the check answer function so that the users choice can be compared with the-
        # correct answer
        self.answer_a = tk.Button(self,text=choices[0],command = lambda:self.check(choices[0],answer),width=410, bg='limegreen', fg='black')
        self.answer_a.place(relx=0.17, rely=0.58, height=45, width=410)

        self.answer_c = tk.Button(self,text=choices[1],command = lambda:self.check(choices[1],answer),width=410, bg='limegreen', fg='black')
        self.answer_c.place(relx=0.17, rely=0.76, height=45, width=410)

        self.answer_b = tk.Button(self,text=choices[2],command = lambda:self.check(choices[2],answer),width=410, bg='limegreen', fg='black')
        self.answer_b.place(relx=0.17, rely=0.67, height=45, width=410)

        self.answer_d = tk.Button(self,text=choices[3],command = lambda:self.check(choices[3],answer),width=410, bg='limegreen', fg='black')
        self.answer_d.place(relx=0.17, rely=0.86, height=45, width=410)

    # Function that checks the user's answer. The function takes the user's answer and the correct answer as parameters
    def check(self,user_answer,correct_answer):
        
        # Checks if this is the last question, if it is then the user has won the game
        if self.count == self.max_questions:
            # Instantiating Tkinter's messagebox wwhich asks the use if they want to play again
            user_answer=tkinter.messagebox.askquestion("You won", "Play again?")
            # if the user wants to play again then we reset the game
            if user_answer == 'yes':
                np.random.shuffle(question_data)
                self.anime_image.forget()
                self.answer_a.forget()
                self.answer_b.forget()
                self.answer_c.forget()
                self.answer_d.forget()
                self.count =0
                self.display_question(question_data[self.count][0],question_data[self.count][1],question_data[self.count][2])
            # If they dont then we reset the game and return to the menu screen
            else:
                self.forget()
                self.controller.show_frame(menu)
            return

        # If the user's answer is correct then we display a correct prompt and display the next question
        if user_answer == correct_answer:
            # Instantiating Tkinter's messagebox with the given  window title and message respectively
            tkinter.messagebox.showinfo("Anime Pictionary","Correct answer")
            
            # Increment count, i.e. move onto next question
            self.count += 1

            # Removing the current image and choices on screen. I.E. Removing the current question
            self.anime_image.forget()
            self.answer_a.forget()
            self.answer_b.forget()
            self.answer_c.forget()
            self.answer_d.forget()
            
            # Ececutes the display_question function with the image,correct answer and choices for the next question
            self.display_question(question_data[self.count][0],question_data[self.count][1],question_data[self.count][2])

        # Else if the user gets the questions wrong then its Game over!
        else:
            # Instantiating Tkinter's messagebox asking the user if they want to try agian
            user_answer=tkinter.messagebox.askquestion("Game Over!", "Try again?")
            
            # If they want to try  again then we reset the game
            if user_answer == 'yes':
                np.random.shuffle(question_data)
                self.anime_image.forget()
                self.answer_a.forget()
                self.answer_b.forget()
                self.answer_c.forget()
                self.answer_d.forget()
                self.count =0
                self.display_question(question_data[self.count][0],question_data[self.count][1],question_data[self.count][2])
            # If they dont then we reset the game and return to the menu screen
            else:
                self.forget()
                self.controller.show_frame(menu)
                
            

app = interface()
width_of_window = 605
height_of_window = 538
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
x_coordinate = (screen_width//2) - (width_of_window//2)
y_coordinate = (screen_height//2) - (height_of_window//2)
app.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x_coordinate, y_coordinate))
app.resizable(False, False)
app.configure(background='grey11')
app.mainloop()


        
