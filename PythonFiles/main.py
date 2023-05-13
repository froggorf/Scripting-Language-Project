import tkinter as tk                        #tkinter 모듈입니다.
import tkinter.ttk                          #tkinter.ttk.Notebook 용 모듈입니다.
from cefpython3 import cefpython as cef     #지도 삽입용 모듈입니다.

WINDOW_WIDTH = 800                          #윈도우 가로/세로
WINDOW_HEIGHT = 1000

def main():
    root = tk.Tk()
    app = MainFrame(root)
    cef.Initialize()
    app.mainloop()
    cef.Shutdown()

class MainFrame(tk.Frame):
    def __init__(self, root):
        self.browser_frame = None                                       #브라우저(지도) 객체
        self.show_browser_frame=False                                   #브라우저 렌더링 여부 변수
        self.root = root                                                #==window(tk.Tk())

        #메인 윈도우
        root.geometry(str(WINDOW_WIDTH)+'x'+str(WINDOW_HEIGHT))
        root.title("기관지 지킴이")
        tk.Grid.rowconfigure(root, 0, weight=1)
        tk.Grid.columnconfigure(root, 0, weight=1)


        #메인 프레임
        tk.Frame.__init__(self, root)

        #이미지 로드
        self.LoadAllImage()


        #TODO: 후에 UI용 함수화 진행
        # 노트북 추가
        self.notebook = tk.ttk.Notebook(root)
        self.notebook.bind('<<NotebookTabChanged>>',self.my_notebook_msg)
        self.notebook.grid(row = 0 , column = 0,sticky = tk.NW)

        #탭0 추가
        self.tab0_frame = tk.Frame(root)
        self.notebook.add(self.tab0_frame,image=self.note_tab0_active_image)
        tk.Label(self.tab0_frame,text="설정 지역 날씨").pack()

        #탭1 추가
        self.tab1_frame = tk.Frame(root)
        self.notebook.add(self.tab1_frame, image=self.note_tab1_inactive_image)
        #tk.Label(self.tab1_frame, text="지도").pack()


        # BrowserFrame
        self.browser_frame = BrowserFrame(self)


    #노트북 탭이 바뀔 때 실행될 함수
    def my_notebook_msg(self,_):
        if self.show_browser_frame == True: #지도가 보이고 있을 때
            self.show_browser_frame=False   #지도가 안보이도록 설정
            self.browser_frame.grid_remove()
            self.grid_remove()

        #현재 선택된 탭 인덱스 받아오기
        select_notetab_index =self.notebook.index("current")

        #현재 선택된 탭은 Active로, 나머지는 Inactive로 이미지 수정
        self.SetAllImageToInactive(select_notetab_index)

        if select_notetab_index == 0:
            #0번탭에 해당하는 함수를 진행
            pass

        elif select_notetab_index == 1:
            #1번탭에 해당하는 함수를 진행
            #지도를 보이도록 추가
            self.browser_frame.grid(row=0, column=0,
                                sticky=(tk.N + tk.S + tk.E + tk.W))

            tk.Grid.rowconfigure(self, 0, weight=1)
            tk.Grid.columnconfigure(self, 0, weight=1)
            self.grid(row=3,column=0,ipadx = 500,ipady=300,sticky=tk.NW)

            tk.Grid.rowconfigure(self, 0, weight=1)
            tk.Grid.columnconfigure(self, 0, weight=1)
            self.show_browser_frame = True

    #노트북의 탭 이미지 활성화/비활성화
    def SetAllImageToInactive(self,index):
        #self.notebook.configure(image = self.note_tab1_inactive_image)

        self.notebook.tab(self.tab0_frame,image = self.note_tab0_inactive_image)
        self.notebook.tab(self.tab1_frame, image=self.note_tab1_inactive_image)

        #TODO: 나중에 배열로 리팩토링 진행해보기
        if index == 0:
            self.notebook.tab(self.tab0_frame, image=self.note_tab0_active_image)
        elif index == 1:
            self.notebook.tab(self.tab1_frame, image=self.note_tab1_active_image)

    #모든 이미지 로드
    def LoadAllImage(self):
        self.note_tab0_active_image = tk.PhotoImage(file='Resource\\Note_Tab0_Active.png')
        self.note_tab0_inactive_image = tk.PhotoImage(file='Resource\\Note_Tab0_Inactive.png')
        self.note_tab1_active_image = tk.PhotoImage(file='Resource\\Note_Tab1_Active.png')
        self.note_tab1_inactive_image = tk.PhotoImage(file='Resource\\Note_Tab1_Inactive.png')





class BrowserFrame(tk.Frame):           #지도 프레임
    def __init__(self, mainframe):
        self.browser = None
        tk.Frame.__init__(self, mainframe)
        self.mainframe = mainframe
        self.bind("<Configure>", self.on_configure)

    #브라우저 가져오기 및 tkinter에 내장하는 함수
    def embed_browser(self):
        window_info = cef.WindowInfo()                                  #상위윈도우 정보 받기
        rect = [50,50, self.winfo_width()-50, self.winfo_height()-50]   #상위윈도우 영역 기반 보일 영역 잡기
        window_info.SetAsChild(self.get_window_handle(), rect)          #상위 윈도우의 차일드 윈도우 속성으로 내장되도록 설정
        self.browser = cef.CreateBrowserSync(window_info,               #브라우저 객체 생성
                                             url="https://weather.naver.com/map/02390118")
        self.message_loop_work()                                        #메시지 루프 입장

    def get_window_handle(self):
        return self.winfo_id()

    def message_loop_work(self):
        cef.MessageLoopWork()                                           #메시지를 받고
        self.after(10, self.message_loop_work)                          #10ms이후 다시 메시지루프로 가도록, 이방식으로 진행해야 메인 윈도우가 실행 가능해지는 것으로 확인.

    #설정될 때 실행될 함수
    def on_configure(self, _):
        if not self.browser:
            self.embed_browser()


if __name__ == '__main__':
    main()

