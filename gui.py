from tkinter import *

root = Tk()
root.title("Diary")
root.geometry("1000x800")

Diary_Name = Entry(root, font="Times 20")
Diary_Name.place(x=200, y=50, width=750)

Diary_Text = Entry(root, width=55, font="Times 18", justify=LEFT)
Diary_Text.place(x=200, y=150, height=600, width=750)



root.mainloop()

