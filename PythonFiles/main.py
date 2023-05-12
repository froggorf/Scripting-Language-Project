import tkinter as tk
import openmap
from cefpython3 import cefpython as cef



root = tk.Tk()
def main():

    root.geometry('600x500')
    b = tk.Button(root, text='ㅇㅇ', command= lambda r = root:openmap.create(r))
    b.pack()
    root.mainloop()
    cef.Shutdown()



if __name__ == '__main__':
    main()