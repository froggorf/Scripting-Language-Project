import tkinter as tk
import tkinter.ttk
from cefpython3 import cefpython as cef

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 1000

def main():
    root = tk.Tk()
    app = MainFrame(root)
    cef.Initialize()
    app.mainloop()
    cef.Shutdown()

class MainFrame(tk.Frame):
    def __init__(self, root):
        self.browser_frame = None
        self.show_browser_frame=False
        self.navigation_bar = None
        self.root = root

        # Root
        root.geometry(str(WINDOW_WIDTH)+'x'+str(WINDOW_HEIGHT))
        #root.geometry('900x600')
        tk.Grid.rowconfigure(root, 0, weight=1)
        tk.Grid.columnconfigure(root, 0, weight=1)

        # MainFrame
        tk.Frame.__init__(self, root)
        self.master.title("기관지 지킴이")

        #노트북 추가
        self.notebook = tk.ttk.Notebook(root)
        self.notebook.bind('<<NotebookTabChanged>>',self.my_notebook_msg)
        self.notebook.grid(row = 0 , column = 0,sticky = tk.NW)

        #탭1 추가
        self.tab1_frame = tk.Frame(root)
        self.note_tab1_image = tk.PhotoImage(file = 'Resource\\Note_Tab1.png')
        self.notebook.add(self.tab1_frame,image=self.note_tab1_image)
        tk.Label(self.tab1_frame,text="설정 지역 날씨").pack()

        #탭2 추가
        #self.tab2_frame=tk.Frame(self)
        self.tab2_frame = tk.Frame(root)
        self.note_tab2_image = tk.PhotoImage(file='Resource\\Note_Tab1.png')
        self.notebook.add(self.tab2_frame, image=self.note_tab2_image)
        #tk.Label(self.tab2_frame, text="지도").pack()


        # BrowserFrame
        #self.browser_frame = None
        self.browser_frame = BrowserFrame(self)
        #self.browser_frame.grid(row=0, column=0,
        #                        sticky=(tk.N + tk.S + tk.E + tk.W))
        #tk.Grid.rowconfigure(self, 0, weight=1)
        #tk.Grid.columnconfigure(self, 0, weight=1)

        # Pack MainFrame
        #self.pack(fill=tk.BOTH, expand=tk.YES)




    def my_notebook_msg(self,_):
        if(self.show_browser_frame==True):
            self.show_browser_frame=False
            self.browser_frame.grid_remove()
            self.grid_remove()


        select_notetab_index =self.notebook.index("current")


        if(select_notetab_index==0):
            #0번탭에 해당하는 함수를 진행
            pass
        elif(select_notetab_index==1):
            #1번탭에 해당하는 함수를 진행
            self.browser_frame.grid(row=0, column=0,
                                sticky=(tk.N + tk.S + tk.E + tk.W))

            tk.Grid.rowconfigure(self, 0, weight=1)
            tk.Grid.columnconfigure(self, 0, weight=1)
            self.grid(row=3,column=0,ipadx = 500,ipady=300,sticky=tk.NW)

            tk.Grid.rowconfigure(self, 0, weight=1)
            tk.Grid.columnconfigure(self, 0, weight=1)
            self.show_browser_frame = True




class BrowserFrame(tk.Frame):
    def __init__(self, mainframe):
        self.browser = None
        tk.Frame.__init__(self, mainframe)
        self.mainframe = mainframe
        self.bind("<Configure>", self.on_configure)

    def embed_browser(self):
        window_info = cef.WindowInfo()
        rect = [50,50, self.winfo_width()-50, self.winfo_height()-50]
        print(rect)
        window_info.SetAsChild(self.get_window_handle(), rect)
        self.browser = cef.CreateBrowserSync(window_info,
                                             url="https://weather.naver.com/map/02390118")
        self.message_loop_work()

    def get_window_handle(self):
        return self.winfo_id()

    def message_loop_work(self):
        cef.MessageLoopWork()
        self.after(10, self.message_loop_work)

    def on_configure(self, _):
        if not self.browser:
            self.embed_browser()



if __name__ == '__main__':
    main()


#지도 넣는 버튼
#b = tk.Button(root, text='ㅇㅇ', command=lambda r=root: openmap.create(r))
#b.pack()