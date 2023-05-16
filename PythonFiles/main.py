import tkinter as tk                        #tkinter 모듈입니다.
import tkinter.ttk                          #tkinter.ttk.Notebook 용 모듈입니다.
from cefpython3 import cefpython as cef     #지도 삽입용 모듈입니다.
import naverweather
from datetime import datetime
import tkinter.font

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
        self.search_frame = None                                        #브라우저(검색) 객체
        self.show_search_frame=False                                    #브라우저(검색) 렌더링 여부 변수
        self.root = root                                                #==window(tk.Tk())

        #메인 윈도우
        root.geometry(str(WINDOW_WIDTH)+'x'+str(WINDOW_HEIGHT))
        root.title("기관지 지킴이")
        tk.Grid.rowconfigure(root, 0, weight=1)
        tk.Grid.columnconfigure(root, 0, weight=1)

        #이미지 로드
        self.LoadAllImage()

        #메인 프레임
        tk.Frame.__init__(self, root)
        

        self.temp_font = tkinter.font.Font(family = "맑은 고딕", size=  20,slant="italic")

        #TODO: 후에 UI용 함수화 진행
        # 노트북 추가
        self.notebook = tk.ttk.Notebook(root)
        self.notebook.bind('<<NotebookTabChanged>>',self.my_notebook_msg)
        self.notebook.grid(row = 0 , column = 0,sticky = tk.N + tk.W + tk.E + tk.S)

        #탭0 추가
        self.tab0_frame = tk.Frame(root)
        self.notebook.add(self.tab0_frame,image=self.note_tab0_active_image)
        tk.Label(self.tab0_frame,text="설정 지역 날씨",font=self.temp_font).grid(row=0, column=0)
        tk.Label(self.tab0_frame,text="현재 지역: ",font=self.temp_font).grid(row=1,column=0)
        self.tab0_location_label = tk.Label(self.tab0_frame,text="현재 지역",font=self.temp_font)
        self.tab0_location_label.grid(row=1,column=1)
        self.tab0_temperature_label = tk.Label(self.tab0_frame,text="온도",font=self.temp_font)
        self.tab0_temperature_label.grid(row=2,column=0)
        self.tab0_weather_state_label= tk.Label(self.tab0_frame,text="상태",font=self.temp_font)
        self.tab0_weather_state_label.grid(row=2,column=1)
        tk.Label(self.tab0_frame, text = "갱신 시간",font=self.temp_font).grid(row=3,column=0)
        self.tab0_time_label = tk.Label(self.tab0_frame,text="시간",font=self.temp_font)
        self.tab0_time_label.grid(row=3,column=1)
        tk.Button(self.tab0_frame,text = "갱신",font = self.temp_font,command = self.PrintTab0).grid(row=3,column=2)

        #탭1 추가
        self.tab1_frame = tk.Frame(root)
        self.notebook.add(self.tab1_frame, image=self.note_tab1_inactive_image)
        #tk.Label(self.tab1_frame, text="지도").pack()

        #탭2 추가
        self.tab2_frame=tk.Frame(root)
        self.notebook.add(self.tab2_frame,image = self.note_tab2_inactive_image)
        tk.Label(self.tab2_frame,text="날씨를 검색할 지역 이름을 적어주세요 ex) 정왕 엔터도됨").grid(row=0,column=0)

        self.search_entrybox = tk.Entry(self.tab2_frame,font=  self.temp_font)
        self.search_entrybox.bind("<Return>",self.SearchInput)
        self.search_entrybox.bind("<Button-1>", self.SearchLButton)
        self.search_entrybox.grid(row=0,column=1)

        tk.Button(self.tab2_frame,text="검색",command= lambda x = None : self.SearchInput(x),font = self.temp_font).grid(row=0,column=2)


        #지도 Frame
        self.browser_frame = BrowserFrame(self,"https://weather.naver.com/map/02390118")

        #검색 Frame
        self.search_frame = BrowserFrame(self,"https://www.google.com")

    def PrintTab0(self):
        weathers = naverweather.GetWeatherInformation()
        self.tab0_location_label.configure(text = weathers[0])
        self.tab0_temperature_label.configure(text = weathers[1])
        self.tab0_weather_state_label.configure(text=weathers[2])
        self.tab0_time_label.configure(text=GetTimeText())
        pass

    #노트북 탭이 바뀔 때 실행될 함수
    def my_notebook_msg(self,_):
        if self.show_browser_frame: #지도가 보이고 있을 때
            self.show_browser_frame=False   #지도가 안보이도록 설정
            self.browser_frame.grid_remove()
            self.grid_remove()

        if self.show_search_frame:
            self.show_search_frame=False
            self.search_frame.grid_remove()
            self.grid_remove()
        #현재 선택된 탭 인덱스 받아오기
        select_notetab_index =self.notebook.index("current")

        #현재 선택된 탭은 Active로, 나머지는 Inactive로 이미지 수정
        self.SetAllImageToInactive(select_notetab_index)

        if select_notetab_index == 0:
            #0번탭에 해당하는 함수를 진행
            self.PrintTab0()

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

        elif select_notetab_index == 2:
            pass


    #노트북의 탭 이미지 활성화/비활성화
    def SetAllImageToInactive(self,index):
        #self.notebook.configure(image = self.note_tab1_inactive_image)
        self.notebook.tab(self.tab0_frame, image = self.note_tab0_inactive_image)
        self.notebook.tab(self.tab1_frame, image = self.note_tab1_inactive_image)
        self.notebook.tab(self.tab2_frame, image = self.note_tab2_inactive_image)

        #TODO: 나중에 배열로 리팩토링 진행해보기
        if index == 0:
            self.notebook.tab(self.tab0_frame, image=self.note_tab0_active_image)
        elif index == 1:
            self.notebook.tab(self.tab1_frame, image=self.note_tab1_active_image)
        elif index == 2:
            self.notebook.tab(self.tab2_frame, image=self.note_tab2_active_image)

    #모든 이미지 로드
    def LoadAllImage(self):
        self.note_tab0_active_image = tk.PhotoImage(file='Resource\\Note_Tab0_Active.png')
        self.note_tab0_inactive_image = tk.PhotoImage(file='Resource\\Note_Tab0_Inactive.png')
        self.note_tab1_active_image = tk.PhotoImage(file='Resource\\Note_Tab1_Active.png')
        self.note_tab1_inactive_image = tk.PhotoImage(file='Resource\\Note_Tab1_Inactive.png')
        self.note_tab2_active_image = tk.PhotoImage(file='Resource\\Note_Tab2_Active.png')
        self.note_tab2_inactive_image = tk.PhotoImage(file='Resource\\Note_Tab2_Inactive.png')
        self.main_image = tk.PhotoImage(file = 'Resource\\MainImage.png')

    def SearchInput(self,_):
        # 브라우저가 켜져있다면
        if self.show_search_frame:
            #url만 바꾸기
            location = self.search_entrybox.get()
            self.search_entrybox.delete(0,len(location))
            self.search_frame.LoadUrl(GetNaverWeatherSearch(location))

        else:
            self.search_frame.grid(row=0, column=0,
                                   sticky=(tk.N + tk.S + tk.E + tk.W))
            tk.Grid.rowconfigure(self, 0, weight=1)
            tk.Grid.columnconfigure(self, 0, weight=1)
            self.grid(row=3, column=0, ipadx=500, ipady=300, sticky=tk.NW)

            tk.Grid.rowconfigure(self, 0, weight=1)
            tk.Grid.columnconfigure(self, 0, weight=1)
            self.show_search_frame = True
            location = self.search_entrybox.get()
            self.search_entrybox.delete(0,len(location))

            if self.search_frame.GetBrowser():
                self.search_frame.LoadUrl(GetNaverWeatherSearch(location))
            else:
                self.search_frame.SetInitUrl(GetNaverWeatherSearch((location)))

    def SearchLButton(self,_):
        self.search_entrybox.focus_force()



class BrowserFrame(tk.Frame):           #지도 프레임
    def __init__(self, mainframe,url):
        self.browser = None
        tk.Frame.__init__(self, mainframe)
        self.mainframe = mainframe
        self.url = url
        self.bind("<Configure>", self.on_configure)
        #self.on_configure(None)

    #브라우저 가져오기 및 tkinter에 내장하는 함수
    def embed_browser(self):
        window_info = cef.WindowInfo()                                  #상위윈도우 정보 받기
        rect = [50,50, self.winfo_width()-50, self.winfo_height()-50]   #상위윈도우 영역 기반 보일 영역 잡기
        window_info.SetAsChild(self.get_window_handle(), rect)          #상위 윈도우의 차일드 윈도우 속성으로 내장되도록 설정
        self.browser = cef.CreateBrowserSync(window_info,               #브라우저 객체 생성
                                             url=self.url)
        self.message_loop_work()                                        #메시지 루프 입장

    def get_window_handle(self):
        return self.winfo_id()

    def message_loop_work(self):
        cef.MessageLoopWork()                                           #메시지를 받고
        self.after(1, self.message_loop_work)                          #10ms이후 다시 메시지루프로 가도록, 이방식으로 진행해야 메인 윈도우가 실행 가능해지는 것으로 확인.

    #설정될 때 실행될 함수
    def on_configure(self, _):
        if not self.browser:
            self.embed_browser()

    def GetBrowser(self):
        if self.browser:
            return self.browser

    def LoadUrl(self,url):
        if self.browser:
            self.browser.StopLoad()
            self.browser.LoadUrl(url)

    def SetInitUrl(self,url):
        self.url = url

def GetNaverWeatherSearch(location):
    return "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=" + location + "+날씨&oquery=" + location + "&tqi=ibu4pdp0J1ZssTMblOwssssssio-160161"

def GetTimeText():
    time = datetime.now()
    text = str(time.year)+"-"
    if time.month<10: text += "0"
    text = text + str(time.month)+"-"
    if time.day < 10:text+="0"
    text = text+str(time.day)+"  "
    if time.hour<10:text+="0"
    text = text + str(time.hour) +":"
    if time.minute<10: text+="0"
    text = text + str(time.minute) + ":"
    if time.second < 10: text += "0"
    text = text + str(time.second)

    return text


if __name__ == '__main__':
    main()

