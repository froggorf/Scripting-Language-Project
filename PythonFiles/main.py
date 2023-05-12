import tkinter as tk
import tkinter.ttk

import cefpython3.examples.tkinter_

import openmap
from cefpython3 import cefpython as cef
from tkinter import messagebox


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 1000

class MainGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry(str(WINDOW_WIDTH) + 'x' + str(WINDOW_HEIGHT))
        self.window.title("")

        self.mapView = None

        settings={}
        cef.Initialize(settings = settings)
        self.CreateInitUI()


        self.window.mainloop()
        cef.Shutdown()
    def CreateInitUI(self):
        self.notebook = tk.ttk.Notebook(self.window)
        self.notebook.bind('<<NotebookTabChanged>>',self.my_msg)
        self.notebook.pack(padx=10,pady=10)

        #1번탭 관련
        self.tab1_frame = tk.Frame(self.window)
        self.note_tab1_image = tk.PhotoImage(file=  'Resource\\Note_Tab1.png')

        self.notebook.add(self.tab1_frame, image=self.note_tab1_image)
        tk.Label(self.tab1_frame, text="설정 지역 날씨").pack()

        self.tab2_frame = tk.Frame(self.window)
        self.note_tab2_image = tk.PhotoImage(file = 'Resource\\Note_Tab1.png')
        self.notebook.add(self.tab2_frame,image=self.note_tab2_image)
        self.tab2_frame.pack_forget()

    def message_loop_work(self):
        cef.MessageLoopWork()
        # root.after(5,message_loop_work)
        self.window.after(10, self.message_loop_work)

    def createMap(self):
        self.window_info = cef.WindowInfo()
        self.rect = [100,500,WINDOW_WIDTH-50,WINDOW_HEIGHT-100]
        self.window_info.SetAsChild(self.window.winfo_id(), self.rect)

        self.mapView = cef.CreateBrowserSync(self.window_info, url="https://weather.naver.com/map/02390118", window_title="test")
        self.message_loop_work()

    def my_msg(self,event):
        if(self.mapView):
            print('엥1')
            cef.QuitMessageLoop()
            #cef.Initialize()

            #self.mapView = None
            print('엥')

        index = self.notebook.index("current")
        if index == 1:
            self.createMap()
        print(index)



if __name__ == '__main__':
    MainGUI()




#지도 넣는 버튼
#b = tk.Button(root, text='ㅇㅇ', command=lambda r=root: openmap.create(r))
#b.pack()