from Tkinter import *
import os
import hashlib
import widgets # my own library - custom widgets
import json # to encode lists to strings
import ast # to return strings back to lists
import __future__ # used in calculator app to check if there is 0 division
#import datetime - will use later to get time to add to bottom task bar
#print datetime.datetime.now()

# main - the main class is the backbone of the application, it contains everything
# that is needed throughout the whole application (e.g. user directory, open applications,
# all the files, etc..)
class main():
    def __init__(self):
        # application's width and height
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 600

        self.BAR_HEIGHT = 50
        self.START_BUTTON = 40

        # current logged in user
        self.user = ""
        self.users_directory = os.path.dirname(os.path.realpath(__file__)) + "/Users"

        # notice that stores the string to be shown when you hover
        self.messageNotice = None

        self.files = []
        self.openApplications = []
        self.folderFrames = []

    # makes the menubar and startmenu
    def create(self):
        self.bar = menuBar(mainFrame)
        self.menu = startMenu(mainFrame)

    def toggleMenu(self):
        self.menu.toggle()

    # loads all the files from the user directory
    def loadFiles(self):
        unacceptable = ["hash", ".DS_Store"]
        self.files = []
        files = os.listdir(self.users_directory + "/" + self.user)
        files.sort(key=lambda x: os.path.getmtime(self.users_directory + "/" + self.user + "/" + x))
        if len(files) > 0:
            for index, mfile in enumerate(files):
                canAdd = True
                for word in unacceptable:
                    if word in mfile:
                        canAdd = False
                if canAdd:
                    self.files.append(mfile)

    # show the files in the desktop
    def showFiles(self):
        startX = 20
        startY = 20

        for folder in self.folderFrames:
            folder.keys()[0].destroy()
            self.folderFrames.remove(folder)

        self.folder_dim = 50
        for file in self.files:
            fileFrame = Frame(mainFrame, width=self.folder_dim, height=self.folder_dim, bg="orange")
            fileFrame.place(x=startX, y=startY)
            myText = (file[0:10] + ' ...') if len(file) > 10 else file
            fileLabel = Label(mainFrame, text=myText, bg="black", fg="white", wraplength=50)
            fileLabel.place(x=startX, y=startY + self.folder_dim + 5)

            self.folderFrames.append({fileFrame:file})

            fileFrame.bind("<Enter>", lambda event, coord=(startX + self.folder_dim/2, startY + self.folder_dim + 10), text=file: self.displayMessage(event, coord, text))
            fileFrame.bind("<Leave>", self.removeMessage)

            fileFrame.bind("<Double-Button-1>", lambda event, myfile=file: self.openFile(event, myfile))

            startY += self.folder_dim + 55

            if startY > 470:
                startY = 20
                startX += self.folder_dim + 40

    # shows the message when u hover over files
    def displayMessage(self, e, coord, text):
        if self.messageNotice == None:
            self.messageNotice = Label(mainFrame, text=text, wraplength=100, bg="yellow")
            self.messageNotice.place(x=coord[0], y=coord[1])

    def removeMessage(self, e):
        if self.messageNotice != None:
            self.messageNotice.destroy()
            self.messageNotice = None

    def openFile(self, e, myfile):
        ext = myfile.split(".")
        ext = ext[len(ext) - 1]
        for format in formats:
            if format == ext:
                openFile = open(self.users_directory + "/" + self.user + "/" + myfile)
                mywindow = eval(formats[format])(content=openFile.read(), title=myfile)

    def optionMenu(self, e):
        # when user right clicks on desktop
        print "open menu"

# this class is for the startup (i.e. the login screen and register screen
class startup():
    def __init__(self):
        self.wholeUsersFrame = None
        self.users_directory = os.path.dirname(os.path.realpath(__file__)) + "/Users"
        print self.users_directory
        self.wholeUsersFrame = self.usersScreen()

    def usersScreen(self, e=None):
        if self.wholeUsersFrame != None:
            self.wholeUsersFrame.destroy()
        self.usersFrame = Frame(mainFrame, width=WIDTH, height=HEIGHT, bg="black")
        self.usersFrame.place(x=0, y=0)
        self.users_label = Label(self.usersFrame, text="Users", font=('Helvetica', 32)).place(x=WIDTH / 2, y=50, anchor="center")
        currYPos = 0
        if not os.path.exists(self.users_directory):
            self.notice_label = Label(self.usersFrame, text="No Users Found...", font=('Helvetica', 24)).place(x=WIDTH / 2, y=150, anchor="center")
            currYPos = 120
        else:
            for subdir, dirs, files in os.walk(self.users_directory):
                if len(dirs) > 0:
                    for index, mydir in enumerate(dirs):
                        func = lambda event, user=mydir: self.loginUser(event, user)
                        btn_width, btn_height = 200, 75
                        x = (WIDTH / 2)
                        y = 125 + (index * (btn_height + 15))
                        userBtn = widgets.wButton(parent=self.usersFrame, width=btn_width, height=btn_height, x=x, y=y, bg="green", func=func, text=mydir)
                        currYPos = 150+(index * 85)

        btn_width, btn_height = 100, 50
        x = (WIDTH / 2)
        y = currYPos + 85
        regBtn = widgets.wButton(parent=self.usersFrame, width=btn_width, height=btn_height, x=x, y=y, bg="orange", func=self.registerScreen, text="Register")
        return self.usersFrame

    def registerScreen(self, e):
        start_y = 100
        self.wholeUsersFrame.destroy()
        self.registerFrame = Frame(mainFrame, width=WIDTH, height=HEIGHT, bg="black")
        self.registerFrame.place(x=0, y=0)
        self.registerLabel = Label(self.registerFrame, text="Register", font=('Helvetica', 32)).place(x=WIDTH / 2, y=50, anchor="center")

        self.usernameLabel = Label(self.registerFrame, text="Username", font=('Helvetica', 26)).place(x=WIDTH / 2, y=start_y + 70, anchor="center")
        self.usernameEntry = Entry(self.registerFrame, width=30, font=('Helvetica', 26))
        self.usernameEntry.place(x=WIDTH / 2, y=start_y + 120, anchor="center")
        self.usernameEntry.config({"bg":"black", "bd":0, "fg":"white", "highlightthickness":1, "highlightcolor":"white"})

        self.passwordLabel = Label(self.registerFrame, text="Password", font=('Helvetica', 26)).place(x=WIDTH / 2, y=start_y + 170, anchor="center")
        self.passwordEntry = Entry(self.registerFrame, width=30, font=('Helvetica', 26), show="*")
        self.passwordEntry.place(x=WIDTH / 2, y=start_y + 220, anchor="center")
        self.passwordEntry.config({"bg": "black", "bd": 0, "fg": "white", "highlightthickness": 1, "highlightcolor": "white"})

        btn_width, btn_height = 100, 50
        x = (WIDTH / 2)
        y = start_y + 280
        regBtn = widgets.wButton(parent=self.registerFrame, width=btn_width, height=btn_height, x=x, y=y, bg="orange",func=self.registerUser, text="Register")
        self.wholeUsersFrame = self.registerFrame

    def registerUser(self, e):
        if len(self.passwordEntry.get()) > 0:
            if not os.path.exists(self.users_directory):
                os.makedirs(self.users_directory)
            if not os.path.exists(self.users_directory + "/" + self.usernameEntry.get()):
                os.makedirs(self.users_directory + "/" + self.usernameEntry.get())
                mypass = open(self.users_directory + "/" + self.usernameEntry.get() + "/hash.os2", "w")
                hash = hashlib.md5(self.passwordEntry.get()).hexdigest()
                mypass.write(hash)
                mypass.close()
            else:
                print "user already exists"
            self.wholeUsersFrame = self.usersScreen()

    def loginUser(self, e, user):
        start_y = 100
        self.wholeUsersFrame.destroy()
        self.loginFrame = Frame(mainFrame, width=WIDTH, height=HEIGHT, bg="black")
        self.loginFrame.place(x=0, y=0)
        self.loginLabel = Label(self.loginFrame, text="Login", font=('Helvetica', 32)).place(x=WIDTH / 2, y=50, anchor="center")

        self.logPasswordLabel = Label(self.loginFrame, text="Password", font=('Helvetica', 26)).place(x=WIDTH / 2, y=start_y + 70, anchor="center")
        self.logPasswordEntry = Entry(self.loginFrame, width=30, font=('Helvetica', 26), show="*")
        self.logPasswordEntry.place(x=WIDTH / 2, y=start_y + 120, anchor="center")
        self.logPasswordEntry.config({"bg": "black", "bd": 0, "fg": "white", "highlightthickness": 1, "highlightcolor": "white"})

        btn_width, btn_height = 100, 50
        x = (WIDTH / 2)
        y = start_y + 170
        func = lambda event, user=user: self.checkLogin(event, user)
        logBtn = widgets.wButton(parent=self.loginFrame, width=btn_width, height=btn_height, x=x, y=y, bg="orange",func=func, text="Login")
        self.wholeUsersFrame = self.loginFrame

    def checkLogin(self, e, user):
        hash = hashlib.md5(self.logPasswordEntry.get()).hexdigest()
        fileOpen = open(self.users_directory + "/" + user + "/hash.os2")
        readAll = fileOpen.read()
        if readAll.strip() == hash:
            self.wholeUsersFrame.destroy()
            global mainObject
            mainObject = main()
            mainObject.user = user
            mainObject.create()
            mainObject.loadFiles()
            mainObject.showFiles()
            mainFrame.bind("<Button-2>", mainObject.optionMenu)
        else:
            print "nah fam what is u doing"

# the start menu with all the applications
class startMenu():
    def __init__(self, parent):
        self.main = mainObject
        self.parent = parent

        self.visible = False

        self.menu_width = 250
        self.menu_height = 300

        self.programs = {
            "Notepad":1,
            "Paint":2,
            "Calculator":3,
        }

    def shutdown(self, e):
        root.destroy()
        root.quit()

    def sideBar(self):
        self.sideFrame_width = 50
        self.sideFrame = Frame(self.start_menu, width=self.sideFrame_width, height=self.menu_height, bg="orange")
        self.sideFrame.place(x=self.menu_width-self.sideFrame_width, y=0)

        shutdown_dim = 30
        self.shutdown_btn = Frame(self.sideFrame, width=shutdown_dim, height=shutdown_dim, bg="purple")
        self.shutdown_btn.place(x=(self.sideFrame_width-shutdown_dim)/2, y=self.menu_height-shutdown_dim-10)
        self.shutdown_btn.bind("<Button-1>", self.shutdown)

    def mainBar(self):
        self.mainFrame_width = self.menu_width-self.sideFrame_width
        self.mainFrame = Frame(self.start_menu, width=self.mainFrame_width, height=self.menu_height, bg="blue")
        self.mainFrame.place(x=0, y=0)

        self.mainFrameTitle = Label(self.mainFrame, text="Programs", font=("Helvetica", 24))
        self.mainFrameTitle.place(x=0, y=0)

        self.programFrame_height = 50
        for i in range(len(self.programs.keys())):
            self.programFrame = Frame(self.mainFrame, width=self.mainFrame_width, height=self.programFrame_height, bg="yellow")
            self.programFrame.place(x=0, y=50 + (i*self.programFrame_height) + (i * 10))

            programPicture_dim = self.programFrame_height - 10
            programPicture = Frame(self.programFrame, width=programPicture_dim, height=programPicture_dim, bg="green")
            programPicture.place(x=5, y=(self.programFrame_height - programPicture_dim)/2)

            programTitle = Label(self.programFrame, text=self.programs.keys()[i])
            programTitle.place(x=programPicture_dim + 15, y=0)

            self.programFrame.bind("<Button-1>", lambda event, app=self.programs.keys()[i]: self.openProgram(event, app))

    def openProgram(self, e, App):
        print "Opening",App
        window = eval(App)()
        self.toggle()

    def toggle(self):
        if not self.visible:
            self.start_menu = Frame(self.parent, width=self.menu_width, height=self.menu_height, bg="green")
            self.start_menu.place(x=0, y=HEIGHT - self.menu_height - self.main.BAR_HEIGHT)
            self.sideBar()
            self.mainBar()
        else:
            self.start_menu.destroy()
        self.visible = not self.visible

# the menu bar that holds the start button (coming soon: applications stack)
class menuBar():
    def __init__(self, parent):
        self.main = mainObject
        self.parent = parent

        # start menu
        bar = Frame(self.parent, width=WIDTH, height=self.main.BAR_HEIGHT, bg="yellow")
        bar.place(x=0, y=HEIGHT - self.main.BAR_HEIGHT)

        # start button
        start_btn = Frame(bar, width=self.main.START_BUTTON, height=self.main.START_BUTTON, bg="purple")
        start_btn.place(x=5, y=(self.main.BAR_HEIGHT - self.main.START_BUTTON) / 2)
        start_btn.bind("<Button-1>", self.openStartMenu)

    # user clicked on the square start button
    def openStartMenu(self, e):
        self.main.toggleMenu()

# window class which is the general template for an application window
class Window():
    def __init__(self, width=500, height=400, App=None, fileName=None, options=None, appObject=None):
        self.width = width
        self.height = height
        self.app = App
        self.fileName = fileName
        self.appObject = appObject
        self.options = options

        self.open_dropdowns = []

        self.borderWidth = 2

        self.borderFrame = Frame(mainFrame, width=self.width + self.borderWidth, height=self.height + self.borderWidth, bg="black")
        self.borderFrame.place(x=(WIDTH - self.width + self.borderWidth)/2, y=(HEIGHT - self.height + self.borderWidth)/2)

        self.frame = Frame(self.borderFrame, width=self.width, height=self.height)
        self.frame.place(x=self.borderWidth/2, y=self.borderWidth/2)

        self.topBar_height = 30
        self.topBar = Frame(self.frame, width=self.width, height=self.topBar_height, bg="blue")
        self.topBar.place(x=0, y=0)

        self.topBar.bind("<ButtonPress-1>", self.startMove)
        self.topBar.bind("<ButtonRelease-1>", self.stopMove)
        self.topBar.bind("<B1-Motion>", self.onMotion)

        if fileName != None:
            self.title = Label(self.topBar, text=App + " - " + fileName, bg="blue", foreground="white")
        else:
            self.title = Label(self.topBar, text=App, bg="blue", foreground="white")
        self.title.place(x=5, y=(self.topBar_height - (self.topBar_height - 10))/2)

        self.close = Frame(self.topBar, width=self.topBar_height - 10, height=self.topBar_height - 10, bg="red")
        self.close.place(x=self.width - (self.topBar_height - 5), y=(self.topBar_height - (self.topBar_height - 10))/2)
        self.close.bind("<Button-1>", self.closeWindow)

        self.statusBar_height = 25
        self.statusBar = Frame(self.frame, width=self.width, height=self.statusBar_height, bg="grey")
        self.statusBar.place(x=0, y=self.topBar_height)

        self.contentFrame_height = self.height - self.topBar_height - self.statusBar_height
        self.contentFrame = Frame(self.frame, width=self.width, height=self.contentFrame_height)
        self.contentFrame.place(x=0, y=self.topBar_height+self.statusBar_height)

        if self.options != None:
            for i in range(len(self.options)):
                if type(self.options[i]) is dict:
                    # drop down menu
                    key = self.options[i].keys()[0]
                    menu_item = Label(self.statusBar, width=7, text=key, bg="grey")
                    menu_item.place(x=i*60, y=0)
                    dropdown_start_position = self.topBar_height + self.statusBar_height
                    menu_item.bind("<Button-1>", lambda event, coord=(i*60, dropdown_start_position), key=key, items=self.options[i][key]: self.toggleDropdown(event, coord, key, items))
                else:
                    # normal single button
                    Label(self.statusBar, width=7, text=self.options[i], bg="grey").place(x=i*60, y=0)

    # Dragging windows functionality adapted from StackOverflow (startMove, stopMove, onMotion):
    # https://stackoverflow.com/questions/4055267/python-tkinter-mouse-drag-a-window-without-borders-eg-overridedirect1
    # Modified the code a little to suite my needs (i.e. last line of onMotion)

    # START OF ADAPTED CODE

    def startMove(self, event):
        self.x, self.y = event.x, event.y

        self.borderFrame.tkraise()

        for applic in mainObject.openApplications:
            if applic.App == "Paint":
                applic.fileContent = json.dumps([applic.canvas.coords(lineItem) + [applic.canvas.itemcget(lineItem, 'fill')] + [applic.canvas.itemcget(lineItem, 'width')] for lineItem in applic.items])
                applic.canvas.delete(ALL)
                applic.items[:] = []
                applic.toolkit.destroy()
            elif applic.App == "Notepad":
                applic.content = applic.textEntry.get(1.0, END)
                applic.textEntry.delete(1.0, END)
            elif applic.App == "Calculator":
                applic.removeButtons()

    def stopMove(self, event):
        self.x, self.y = None, None

        for applic in mainObject.openApplications:
            if applic.App == "Paint":
                applic.insertContent(applic.fileContent)
                applic.createToolkit()
            elif applic.App == "Notepad":
                applic.textEntry.insert(INSERT, applic.content)
            elif applic.App == "Calculator":
                applic.addButtons()


    def onMotion(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.borderFrame.winfo_x() + deltax
        y = self.borderFrame.winfo_y() + deltay

        self.borderFrame.place(x=x, y=y)

    # END OF ADAPTED CODE

    def closeWindow(self, e):
        self.borderFrame.destroy()
        for applic in mainObject.openApplications:
            if applic == self.appObject:
                mainObject.openApplications.remove(applic)

        print mainObject.openApplications

    def toggleDropdown(self, e, coord, key, items):
        self.foundOpenDropdown = False
        for dropdown in self.open_dropdowns:
            if dropdown.keys()[0] == key:
                # menu already open, just close
                self.foundOpenDropdown = True
            dropdown[dropdown.keys()[0]].destroy()
            self.open_dropdowns.remove(dropdown)
        if not self.foundOpenDropdown:
            dropdown_dim = 100
            dropdown = Frame(self.frame, width=dropdown_dim, height=dropdown_dim, bg="grey")
            dropdown.place(x=coord[0], y=coord[1])
            self.open_dropdowns.append({key:dropdown})

            for index, item in enumerate(items):
                item_label = Label(dropdown, text=item, bg="grey")
                item_label.place(x=0, y=20*index)
                content = None
                if self.app == "Notepad":
                    content = self.appObject.textEntry.get("1.0", END)
                elif self.app == "Paint":
                    content = [self.appObject.canvas.coords(lineItem) + [self.appObject.canvas.itemcget(lineItem, 'fill')] + [self.appObject.canvas.itemcget(lineItem, 'width')] for lineItem in self.appObject.items]
                item_label.bind("<Button-1>", lambda event, dropdown=dropdown, window=self, filename=self.fileName, content=content: items[item](event, dropdown, window, filename, content))

# notepad application
class Notepad():
    def __init__(self, content=None, title=None):
        # SAMPLE USAGE OF TOP BAR
        '''self.statusBarOptions = [
            {"File":
                 {"Save": self.saveFile,
                  "Open": self.saveFile}
             },
            "About",
            "Test",
            {"Options":
                 {"Save": self.saveFile}
             },
        ]'''

        self.statusBarOptions = [
            {"File":
                 {"Save": self.saveFile,}
                 # "Open": self.saveFile}
             }
        ]

        self.App = "Notepad"
        self.title = "Untitled" if title == None else title
        self.window = Window(App=self.App, fileName=self.title, options=self.statusBarOptions, appObject=self)

        self.mainFrame_height = self.window.height-self.window.topBar_height-self.window.statusBar_height
        self.mainFrame = Frame(self.window.frame, width=self.window.width, height=self.mainFrame_height)
        self.mainFrame.place(x=0, y=self.window.topBar_height+self.window.statusBar_height)
        self.textEntry = Text(self.mainFrame, width=72, height=28, wrap="word", borderwidth=0, highlightcolor="white")
        self.textEntry.place(x=0, y=0)

        self.content = ""

        if content != None:
            self.textEntry.insert(INSERT, content)
            self.content = content

        mainObject.openApplications.append(self)

    def saveFile(self, e, dropdown, window, filename, content):

        for i in window.open_dropdowns:
            window.open_dropdowns.remove(i)
        dropdown.destroy()

        if not os.path.exists(mainObject.users_directory + "/" + mainObject.user + "/" + filename):
            saveFrame_width, saveFrame_height = 200, 140
            self.saveFrame = Frame(window.frame, width=200, height=140, bg="grey")
            self.saveFrame.place(x=window.width/2, y=window.height/2, anchor="center")

            self.saveLabel = Label(self.saveFrame, text="Save File", bg="grey", font=('Helvetica', 22)).place(x=10, y=10)

            self.fileNameLabel = Label(self.saveFrame, text="File Name:", bg="grey", font=('Helvetica', 14)).place(x=25, y=50)
            self.fileNameEntry = Entry(self.saveFrame, highlightthickness=1, highlightcolor="black")
            self.fileNameEntry.place(x=saveFrame_width/2, y= 80, anchor="center")

            btn_width, btn_height = 50, 25
            x = saveFrame_width/2
            y = 110
            saveBtn = widgets.wButton(parent=self.saveFrame, width=btn_width, height=btn_height, x=x, y=y, bg="orange",func=lambda event, window=window, content=content: self.saveFileToDir(event, window, self.fileNameEntry.get(), content, False), text="Save")
        else:
            self.saveFileToDir(None, window, filename, content, True)

    def saveFileToDir(self, e, window, filename, content, alreadyExists):
        if len(filename) > 0:
            if alreadyExists:
                new_file = open(mainObject.users_directory + "/" + mainObject.user + "/" + filename, "w")
            else:
                new_file = open(mainObject.users_directory + "/" + mainObject.user + "/" + filename + ".ntpd", "w")

            new_file.write(content)
            new_file.close()

            mainObject.loadFiles()
            mainObject.showFiles()

            self.window.borderFrame.tkraise()

            window.title.destroy()
            if alreadyExists:
                window.title = Label(window.topBar, text=window.app + " - " + filename, bg="blue", foreground="white")
            else:
                window.title = Label(window.topBar, text=window.app + " - " + filename + ".ntpd", bg="blue",foreground="white")
            window.title.place(x=5, y=(window.topBar_height - (window.topBar_height - 10)) / 2)

            # if file does not already exist, it means saveFrame was shown to input file name
            if not alreadyExists:
                self.saveFrame.destroy()


# calculator application
class Calculator():
    def __init__(self, content=None, title=None):
        self.statusBarOptions = [
            {"File":
                 {"Scientific": self.scientific}
             }
        ]

        self.App = "Calculator"
        self.title = None
        self.window = Window(App=self.App, fileName=self.title, options=self.statusBarOptions, appObject=self, width=230, height=370)

        self.mainFrame_height = self.window.height - self.window.topBar_height - self.window.statusBar_height
        self.mainFrame = Frame(self.window.contentFrame, width=self.window.width, height=self.mainFrame_height)
        self.mainFrame.place(x=0, y=0)

        self.display = Frame(self.mainFrame, width=self.window.width, height=78, bg="#323232")
        self.display.place(x=0, y=0)

        self.displayText = Label(self.display, width=18, height=3, text="", justify=RIGHT, anchor=E, font=('Helvetica', 20), fg="white", bg="#323232", padx=10, wraplength=self.window.width - 20)
        self.displayText.place(x=6, y=5)

        self.btn_dim = (58, 48)
        self.btns = ['AC', 'DEL', '%', '/', '7', '8', '9', '*', '4', '5', '6', '-', '1', '2', '3', '+', '0', '.', '=']

        self.inError = False
        self.allButtons = []

        self.addButtons()

        mainObject.openApplications.append(self)

    def btnClick(self, event, key):
        unacceptable = ["=", "AC", "DEL"]
        if self.inError:
            self.displayText.config(text="")
            self.inError = False

        if key not in unacceptable:
            self.displayText.config(text=self.displayText.cget('text') + key)
        else:
            if key == "=":
                if len(self.displayText.cget('text')) > 0:
                    try:
                        result = eval(compile(self.displayText.cget('text').strip(), '<string>', 'eval', __future__.division.compiler_flag))
                    except SyntaxError:
                        result = "Syntax Error"
                        self.inError = True
                    except ZeroDivisionError:
                        result = "Math Error"
                        self.inError = True

                    self.displayText.config(text=str(result))
            elif key == "AC":
                self.displayText.config(text="")
            elif key == "DEL":
                self.displayText.config(text=self.displayText.cget('text')[:len(self.displayText.cget('text')) - 1])

    def removeButtons(self):
        for btn in self.allButtons:
            btn.f.destroy()

    def addButtons(self):
        x = self.btn_dim[0] / 2
        y = 101
        count = 0
        for i, btn in enumerate(self.btns):
            w = self.btn_dim[0] if btn != '0' else self.btn_dim[0] * 2
            mins = self.btn_dim[0] / 2 if btn == '0' else 0
            bg = "orange" if x == 203 else "#bfbfbf"
            if count == 4:
                x = w / 2
                y += self.btn_dim[1]
                count = 0
            btn = widgets.wButton(parent=self.mainFrame, width=w, height=self.btn_dim[1], x=x, y=y, bg=bg, text=btn, func=lambda event, key=btn: self.btnClick(event, key))
            btn.f.config(bd=1, highlightthickness=1, highlightcolor="black", highlightbackground="black", relief=RAISED)
            count += 1
            x += w - mins

            self.allButtons.append(btn)

    def scientific(self, e, dropdown, window, filename, content):
        print "switch to scientific (coming soon)"

# paint application
class Paint():
    def __init__(self, content=None, title=None):
        self.statusBarOptions = [
            {"File":
                 {"Save": self.saveFile}
             }
        ]

        self.App = "Paint"
        self.title = "Untitled" if title == None else title
        self.window = Window(App=self.App, fileName=self.title, options=self.statusBarOptions, appObject=self)

        self.toolkit_height = 55

        self.selectedColor = "black"
        self.selectedWidth = 2

        self.canvas_height = self.window.height - self.window.topBar_height - self.window.statusBar_height - self.toolkit_height
        self.canvas = Canvas(self.window.contentFrame, width=self.window.width, height=self.canvas_height, bg="white", highlightthickness=0)
        self.canvas.place(x=0, y=0)

        self.createToolkit()

        self.old_x = None
        self.old_y = None

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

        self.items = []
        self.fileContent = content

        self.insertContent(self.fileContent)

        mainObject.openApplications.append(self)

    def createToolkit(self):
        self.toolkit = Frame(self.window.contentFrame, width=self.window.width, height=self.toolkit_height, bg="grey")
        self.toolkit.place(x=0, y=self.canvas_height)

        colors = ["black", "blue", "red", "yellow", "green", "purple", "orange", "gold", "tomato", "maroon", "navy",
                  "cyan", "lime green", "coral"]
        self.colorBtns = []
        y = 5
        x = 5
        for index, color in enumerate(colors):
            if index > 6 and y < 25:
                y += 25
                x = 5
            cFrame = Frame(self.toolkit, width=20, height=20, bg=color)
            cFrame.place(x=x, y=y)
            cFrame.bind("<Button-1>", lambda event, col=cFrame: self.selectColor(event, col))
            self.colorBtns.append(cFrame)
            x += 25

        self.selectColor(col="black")

        widths = [2, 5, 7]
        x += 5
        y = 5

        widths_height = 13

        for index, width in enumerate(widths):
            wFrame = Frame(self.toolkit, width=30, height=widths_height, bg="white")
            wFrame.place(x=x, y=y)
            visFrame = Frame(wFrame, width=20, height=width, bg="black")
            visFrame.place(x=15, y=widths_height / 2, anchor="center")

            func = lambda event, wid=width: self.changeWidth(event, wid)
            wFrame.bind('<Button-1>', func)
            visFrame.bind('<Button-1>', func)

            y += widths_height + 3

    def changeWidth(self, e, wid):
        self.selectedWidth = wid

    def paint(self, event):
        if self.old_x and self.old_y:
            newLine = self.canvas.create_line(self.old_x, self.old_y, event.x, event.y, width=self.selectedWidth, fill=self.selectedColor, capstyle=ROUND, smooth=TRUE, splinesteps=36)
            self.items.append(newLine)
        self.old_x = event.x
        self.old_y = event.y

    def insertContent(self, content):
        if content != None:
            l = ast.literal_eval(content)

            for newLine in l:
                mcoords = [i for i in newLine]
                nLine = self.canvas.create_line([mcoords[0], mcoords[1], mcoords[2], mcoords[3]], width=mcoords[5], fill=mcoords[4], capstyle=ROUND, smooth=TRUE, splinesteps=36)
                self.items.append(nLine)

    def reset(self, event):
        self.old_x, self.old_y = None, None

    def selectColor(self, e=None, col=None):
        if e != None and col != None:
            if type(col) is str:
                self.selectedColor = col
            else:
                self.selectedColor = col.cget('bg')
        for color in self.colorBtns:
            color.config(highlightthickness=0)
            if color.cget('bg') == self.selectedColor:
                color.config(highlightthickness=1)

    def saveFile(self, e, dropdown, window, filename, content):

        for i in window.open_dropdowns:
            window.open_dropdowns.remove(i)
        dropdown.destroy()

        if not os.path.exists(mainObject.users_directory + "/" + mainObject.user + "/" + filename):
            saveFrame_width, saveFrame_height = 200, 140
            self.saveFrame = Frame(window.frame, width=200, height=140, bg="grey")
            self.saveFrame.place(x=window.width/2, y=window.height/2, anchor="center")

            self.saveLabel = Label(self.saveFrame, text="Save File", bg="grey", font=('Helvetica', 22)).place(x=10, y=10)

            self.fileNameLabel = Label(self.saveFrame, text="File Name:", bg="grey", font=('Helvetica', 14)).place(x=25, y=50)
            self.fileNameEntry = Entry(self.saveFrame, highlightthickness=1, highlightcolor="black")
            self.fileNameEntry.place(x=saveFrame_width/2, y= 80, anchor="center")

            btn_width, btn_height = 50, 25
            x = saveFrame_width/2
            y = 110
            saveBtn = widgets.wButton(parent=self.saveFrame, width=btn_width, height=btn_height, x=x, y=y, bg="orange",func=lambda event, window=window, content=content: self.saveFileToDir(event, window, self.fileNameEntry.get(), content, False), text="Save")
        else:
            self.saveFileToDir(None, window, filename, content, True)

    def saveFileToDir(self, e, window, filename, content, alreadyExists):
        if len(filename) > 0:
            if alreadyExists:
                new_file = open(mainObject.users_directory + "/" + mainObject.user + "/" + filename, "w")
            else:
                new_file = open(mainObject.users_directory + "/" + mainObject.user + "/" + filename + ".pnt", "w")

            new_file.write(json.dumps(content))
            new_file.close()

            mainObject.loadFiles()
            mainObject.showFiles()

            self.window.borderFrame.tkraise()

            window.title.destroy()
            if alreadyExists:
                window.title = Label(window.topBar, text=window.app + " - " + filename, bg="blue", foreground="white")
            else:
                window.title = Label(window.topBar, text=window.app + " - " + filename + ".ntpd", bg="blue", foreground="white")
            window.title.place(x=5, y=(window.topBar_height - (window.topBar_height - 10)) / 2)

            # if file does not already exist, it means saveFrame was shown to input file name
            if not alreadyExists:
                self.saveFrame.destroy()

root = Tk()
WIDTH = 800
HEIGHT = 600
root.geometry('{}x{}'.format(WIDTH, HEIGHT))

# main frame
mainFrame = Frame(root, width=WIDTH, height=HEIGHT, bg="black")
mainFrame.pack()

mainObjectStart = startup()

mainObject = None
formats = {"ntpd":"Notepad", "pnt":"Paint"}

root.mainloop()