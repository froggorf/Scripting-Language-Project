import tkinter as tk
from cefpython3 import cefpython as cef

root = tk.Tk()

def message_loop_work():
    cef.MessageLoopWork()
    root.after(5,message_loop_work)

def create():
    window_info = cef.WindowInfo()
    rect = [50,50,550,430]
    window_info.SetAsChild(root.winfo_id(),rect)
    cef.Initialize()
    cef.CreateBrowserSync(window_info,url="https://weather.naver.com/map/02390118", window_title="test")
    message_loop_work()

def main():



    root.geometry('600x500')
    b = tk.Button(root, text='ㅇㅇ', command=create)
    b.pack()
    root.mainloop()
    cef.Shutdown()




if __name__ == '__main__':
    main()