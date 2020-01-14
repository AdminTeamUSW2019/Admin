from tkinter import *

root = Tk()

one = Label(root, text="One", bg="red", fg="white")
one.pack()
two = Label(root, text="Two", bg="green", fg="black")
two.pack(fill = X)
three = Label(root, text = "Three", bg = "blue", fg = "white")
three.pack(side = LEFT, fill = Y)
four = Label(root, text = "Four", bg = "Orange", fg = "white")
four.pack(fill = BOTH, expand = True)

# topFrame = Frame(root)
# topFrame.pack()
# bottomFrame = Frame(root)
# bottomFrame.pack(side = BOTTOM)
#
# button1 = Button(topFrame, text = "Button1", fg = "red")
# button2 = Button(topFrame, text = "Button2", fg = "blue")
# button3 = Button(topFrame, text = "Button3", fg = "green")
# button4 = Button(bottomFrame, text = "Button4", fg = "purple")
#
# button1.pack(side = LEFT)
# button2.pack(side = LEFT)
# button3.pack(side = LEFT)
# button4.pack(side = BOTTOM)

root.mainloop()

