# 15-112-Project

My final project will be a “fake OS” (inspired by an upperclassmen). It isn’t really an OS in the sense that it can’t organize the use of memory or control storage, hence emphasis on the word “fake”. 

### Description
A fake OS where you can create an account and log in. There will be essential programs like a calculator, paint and notepad and a game or two. You can also save files from these programs (e.g. save a file of what you wrote on notepad, it’ll show up on your fake OS’s desktop and save it to your actual computer in a directory for later access when you log back in).

### Libraries/APIs Used
- Tkinter - used to create the UI.
- hashlib - to create a hash value for passwords.
- PIL - to add images with .png format to tkinter.
- threading - to create threads that update the time
- Other built-in libraries to provide certain functionalities.

### User Interface
It will be created with Tkinter, there will be a screen where the user can choose their name from the registered users and login or create an account. In the main screen after logging in, there will be a task bar at the bottom with a start button that opens a start menu where you could access the different applications as well as sign out or shutdown. Applications will run in the form of windows where you can close them completely.

### Initial Features (first checkpoint)
- A user registration and login system where each person can have their own account on the program.
- Initial programs which include: notepad, paint, calculator.
- The ability to save files under the logged in user and access them later when you log back in (i.e. save your drawings on paint, save text on notepad).

### Final Features (complete features)
All the features listed above as well as:
- Add a game to the project
- Better and cleaner UI with images in place of empty buttons (e.g. shutdown button) which in turn, improves the UX.

### Special Features
- Saving files to the user’s computer and parsing it later to be able to retrieve the data (e.g. on paint).
- Nice UI. (hopefully)

---
##### Omar Sinan
