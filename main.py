import os
import json
from time import sleep
from tkinter import *
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Combobox
from datetime import *
import sqlite3 as sql

root = Tk()
root.title("Diary")
root.geometry("1000x800")
root.resizable(height=False, width=False)

Frame_Signup = Frame(root, height=800, width=1000)
Frame_Login = Frame(root, height=800, width=1000)
Frame_Main = Frame(root, height=800, width=1000)
Frame_Exists = Frame(height=50, width=400)




Frame_Signup.pack()
Frame_Login.pack()
Frame_Main.pack()
Frame_Exists.pack()


def Sign_Up():

    global First_User
    global First_Pass
    
    Log_Label = Label(Frame_Signup, text="Sign up", font="Times 20")
    First_User = Entry(Frame_Signup, font="Times 20")
    First_Pass = Entry(Frame_Signup, font="Times 20")
    Button_SignUp = Button(Frame_Signup, text="Save&Continue", font="Times 15", command=Save_and_login)
    Log_Label.grid(row=1, column=4)
    First_User.grid(row=2, column=4)
    First_Pass.grid(row=3, column=4)
    Button_SignUp.grid(row=4, column=4)


    
    
    return True

def Save_and_login():
    
    User_Data()
    Log_In()


    return True


def User_Data():
    

    First_User_Data = {"Username":First_User.get(),"Password":First_Pass.get()}
    
    with open(Path, 'w') as data:
        json.dump(First_User_Data, data)

    
    return True


def Log_In():

    global Logging_User
    global Logging_Pass
    global Log_Test


    Frame_Signup.destroy()

    Log_Label = Label(Frame_Login, text="Log In", font="Times 20")
    Logging_User = Entry(Frame_Login, font="Times 20")
    Logging_Pass = Entry(Frame_Login, font="Times 20")
    Button_Login = Button(Frame_Login, text="Continue", font="Times 15", command=User_Data_Pull)
    Log_Test = Label(Frame_Login, text="", font="Times 20")

    Log_Label.grid(row=1, column=4)
    Logging_User.grid(row=2, column=4)
    Logging_Pass.grid(row=3, column=4)
    Button_Login.grid(row=4, column=4)
    Log_Test.grid(row=5, column=4)
    

    return True



def User_Data_Pull():
    
    with open(Path, 'r') as data:
        User = json.load(data)

        if User["Username"] == Logging_User.get() and User["Password"] == Logging_Pass.get():
            Main_Window()

        else:
            Log_Test.configure(text="Failed to log in")
    


    return True


def Save_Diary():

    Db = sql.connect(Diary_Path)

    cursor = Db.cursor()

    cursor.execute("SELECT Name FROM Diaries")
   
    Db_Data = cursor.fetchall()


    global Data_Exists
    Data_Exists = False

    for data in Db_Data:
        if data[0] == Diary_Name.get():
            Data_Exists = True
            break
        else:
            Data_Exists=False
            



    if Data_Exists == True:
        
        R_or_K = messagebox.askyesno("Serveto Services", "Do you want to rewrite the page?")
        
        if R_or_K == True:
            
            cursor.execute("UPDATE Diaries SET Date='{0}' WHERE Name ='{1}'".format(Current_Date, Diary_Name.get()))
            cursor.execute("UPDATE Diaries SET Diary='{0}' WHERE Name ='{1}'".format(Diary_Text.get("1.0", "end-1c"), Diary_Name.get()))
            Db.commit()

        elif R_or_K == False:

                messagebox.showinfo("Serveto Services","No action has been taken")



    else:
        cursor.execute("INSERT INTO Diaries VALUES ('{0}', '{1}', '{2}')".format(str(Current_Date), str(Diary_Name.get()), str(Diary_Text.get("1.0",'end-1c'))))
        Diary_Page_Names.insert(0,Diary_Name.get())
        ComboBox_Diary_Names["values"] = Diary_Page_Names
    

        
    Db.commit()
    
    Db.close()
    

    return True

def Search_Page(): 
    global Selected_Page
    global Selected_Text

    Db_Search = sql.connect(Diary_Path)
    Cursor_Search = Db_Search.cursor()
    Cursor_Search.execute("SELECT Name, Diary FROM Diaries")
    Db_Search_List = Cursor_Search.fetchall()

    Selected_Page = ComboBox_Diary_Names.get()
    
    index = Unreversed_Names.index(Selected_Page)
    length = len(Unreversed_Names)

    Selected_Text = Db_Search_List[length - index - 1][1]
    
    

    Db_Search.close()
    return True

def Box_Inserter():
    Diary_Name.delete(0,END)
    Diary_Name.insert('insert', Selected_Page)
    
    Diary_Text.delete('1.0',END)
    Diary_Text.insert('insert', Selected_Text)
    
    
    return True


def Search_Insert():
    Search_Page()
    Box_Inserter()
    
    return True


def Clear_Boxes():

    Diary_Name.delete(0,END)
    Diary_Text.delete('1.0',END)
    
    return True

def Delete_Page():
    
    Db_Delete = sql.connect(Diary_Path)
    D_cursor = Db_Delete.cursor()
    D_cursor.execute("DELETE FROM Diaries WHERE Name='{}'".format(Diary_Name.get()))
    Db_Delete.commit()
    Db_Delete.close()
    
    Diary_Page_Names_List()
    ComboBox_Diary_Names.set("Pick a page")
    ComboBox_Diary_Names.config(values=Diary_Page_Names)
    
    
    Diary_Name.delete(0,END)
    Diary_Text.delete('1.0',END)
    

    return True

def Diary_Page_Names_List():
    
    global Unreversed_Names
    global Diary_Page_Names
    
    Diary_Page_Names = []
    
    Db_Pull = sql.connect(Diary_Path)
    cursor_Pull = Db_Pull.cursor()
    cursor_Pull.execute("SELECT Name FROM Diaries")
    Db_Data_Pull = cursor_Pull.fetchall()
    Db_Pull.close()

    for data in Db_Data_Pull:
        Diary_Page_Names.append(data[0])

    Unreversed_Names = Diary_Page_Names
    
    Diary_Page_Names.reverse()
    
    return True

def Main_Window():
    
    Frame_Login.destroy()
    
    global Diary_Name
    global Diary_Text
    global ComboBox_Diary_Names
    
    
    Db_Pull = sql.connect(Diary_Path)
    cursor_Pull = Db_Pull.cursor()

    cursor_Pull.execute("CREATE TABLE IF NOT EXISTS Diaries (Date TEXT, Name TEXT, Diary TEXT)")
    Db_Pull.close()
    
    Diary_Page_Names_List()


    
    Diary_Name = Entry(Frame_Main, font="Times 20", width=55, xscrollcommand=True)
    Diary_Text = ScrolledText(Frame_Main, font="Times 17", width=70, xscrollcommand=True)
    Button_Save_Diary = Button(Frame_Main, text="Save", font="Times 17", command=Save_Diary)
    ComboBox_Diary_Names= Combobox(Frame_Main, font="Times 17", values=Diary_Page_Names)
    ComboBox_Diary_Names.set("Pick a page")
    Button_Search = Button(Frame_Main, text="S", width=2, command=Search_Insert)
    Button_Clear = Button(Frame_Main, text="Clear", font="Times 17", command=Clear_Boxes)
    Button_Delete = Button(Frame_Main, text="Delete Page", font="Times 17", command=Delete_Page)

    Diary_Name.place(x=200, y=50)
    Diary_Text.place(x=200, y=100, height=650, anchor="nw")
    Button_Save_Diary.place(x=25, y=100, width=150)
    ComboBox_Diary_Names.place(x=25, y=50, width=150)
    Button_Search.place(x=175, y=50, height=32)
    Button_Clear.place(x=25, y=150, width=150)
    Button_Delete.place(x=25, y=200, width=150)

    return True



Current_User = os.getlogin()
Folder_Path = r"/Users/{0}/Desktop/ServetoServices".format(Current_User)
Path = r"/Users/{0}/Desktop/ServetoServices/loginfo.json".format(Current_User)
Diary_Path = r"/Users/{0}/Desktop/ServetoServices/diaries.db".format(Current_User)


global Current_Date    
Current_Date = datetime.today().strftime("%Y-%m-%d")



try:
    os.mkdir(Folder_Path)
except:
    try: 
            PassJson = open(Path, "x")
    except:

        Log_In()    
    
    else:

        Sign_Up()
else:
    PassJson = open(Path, "x")
    Sign_Up()






root.mainloop()







