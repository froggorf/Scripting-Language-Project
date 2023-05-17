import tkinter as tk  # tkinter 모듈입니다.
import tkinter.ttk  # tkinter.ttk.Notebook 용 모듈입니다.
from cefpython3 import cefpython as cef  # 지도 삽입용 모듈입니다.
import naverweather
from datetime import datetime
import tkinter.font

WINDOW_WIDTH = 800  # 윈도우 가로/세로
WINDOW_HEIGHT = 1000
BACKGROUNDCOLOR = '#AAAAAA'
temp_font = None

def main():
    root = tk.Tk()
    app = MainFrame(root)
    cef.Initialize()

    app.mainloop()
    cef.Shutdown()


class MainFrame(tk.Frame):
    def __init__(self, root):
        temp_font = tkinter.font.Font(family="맑은 고딕", size=20, slant="italic")

        style = tk.ttk.Style()
        #current_theme = style.theme_use()

        style.element_create('Plain.Notebook.tab', "from", 'default')
        # Redefine the TNotebook Tab layout to use the new element
        style.layout("TNotebook.Tab",[('Plain.Notebook.tab',{'children': [('Notebook.padding',{'side': 'top','children':[('Notebook.focus',{'side': 'top','children':[('Notebook.label',{'side': 'top', 'sticky': ''})],'sticky': 'nswe'})],'sticky': 'nswe'})],'sticky': 'nswe'})])
        style.configure("TNotebook", background=BACKGROUNDCOLOR, borderwidth=0)
        style.configure("TNotebook.Tab",
                        background = BACKGROUNDCOLOR,
                        foreground='black',lightcolor='black',borderwidth=1,font = temp_font,bordermode="inside",padding = [10,5])
        #style.layout("TNotebook.Tab",{'map':{"background":[("selected","black")]}})
        style.configure("TFrame", background=BACKGROUNDCOLOR, foreground=BACKGROUNDCOLOR, borderwidth=0)


        self.browser_frame = None  # 브라우저(지도) 객체
        self.show_browser_frame = False  # 브라우저 렌더링 여부 변수
        self.search_frame = None  # 브라우저(검색) 객체
        self.show_search_frame = False  # 브라우저(검색) 렌더링 여부 변수
        self.root = root  # ==window(tk.Tk())

        # 메인 윈도우
        root.geometry(str(WINDOW_WIDTH) + 'x' + str(WINDOW_HEIGHT))
        root.title("기관지 지킴이")
        tk.Grid.rowconfigure(root, 0, weight=1)
        tk.Grid.columnconfigure(root, 0, weight=1)
        root.bind('<Escape>', self.close_window)
        tk.Label(root, bg = BACKGROUNDCOLOR,width = WINDOW_WIDTH,height = WINDOW_HEIGHT).place(x=0, y=0)
        #root.attributes('-alpha',0.5)

        # 이미지 로드
        self.LoadAllImage()
        self.LoadWeatherIcon()

        # 메인 프레임
        super(MainFrame, self).__init__(root,highlightbackground="black",highlightthickness=10)
        #tk.Frame.__init__(self, root)



        # TODO: 후에 UI용 함수화 진행
        # 노트북 추가
        self.notebook = tk.ttk.Notebook(root,width = WINDOW_WIDTH-50,height = WINDOW_HEIGHT-100)
        self.notebook.bind('<<NotebookTabChanged>>', self.my_notebook_msg)
        self.notebook.place(x=25,y=20)


        # 탭0 추가
        self.tab0_frame = tk.Frame(root)
        self.notebook.add(self.tab0_frame, text = "지역 날씨")
        tk.Label(self.tab0_frame, text="설정 지역 날씨", font=temp_font).place(x=0, y=0)
        tk.Label(self.tab0_frame, text="현재 지역: ", font=temp_font).place(x=250, y=0)
        self.tab0_location_label = tk.Label(self.tab0_frame, text="현재 지역", font=temp_font)
        self.tab0_location_label.place(x=500,y=0)
        self.tab0_temperature_label = tk.Label(self.tab0_frame, text="온도", font=temp_font)
        self.tab0_temperature_label.place(x=0,y=50)
        self.tab0_weather_state_label = tk.Label(self.tab0_frame, text="상태", font=temp_font)
        self.tab0_weather_state_label.place(x=250,y=50)
        tk.Label(self.tab0_frame, text="갱신 시간", font=temp_font).place(x=0,y=100)
        self.tab0_time_label = tk.Label(self.tab0_frame, text="시간", font=temp_font)
        self.tab0_time_label.place(x=250,y=100)
        tk.Button(self.tab0_frame, text="갱신", font=temp_font, command=self.PrintTab0).place(x=550,y=100)
        self.graph_canvas = tk.Canvas(self.tab0_frame,width = 650, height = 300, bg='white',bd=2)
        self.graph_canvas.place(x=50,y=520)
        self.canvas_scrollX = tk.Scrollbar(self.tab0_frame)
        self.canvas_scrollX.config(orient = tk.HORIZONTAL,command=self.graph_canvas.xview)
        self.canvas_scrollX.place(x=50,y=820,width = 650)

        self.graph_canvas.configure(xscrollcommand=self.canvas_scrollX.set)
        self.graph_canvas.config(scrollregion=self.graph_canvas.bbox("all"))


        tk.Label(self.tab0_frame, text= "시간별 그래프 // 미세먼지 추가 예정",font=temp_font).place(x=50,y=470)

        # 탭1 추가
        self.tab1_frame = tk.Frame(root)
        self.notebook.add(self.tab1_frame, text = "지도")
        # tk.Label(self.tab1_frame, text="지도").pack()
        self.map_weather_url = "https://weather.naver.com/map/02390118"
        self.map_dust_url = "https://weather.naver.com/air/02390118"
        tk.Button(self.tab1_frame,text="지도 초기화(날씨)",command=lambda: self.ResetMapBrowser(self.map_weather_url),font=temp_font,background='#888888').place(x=50,y=10)
        tk.Button(self.tab1_frame, text="지도 초기화(미세먼지)", command=lambda: self.ResetMapBrowser(self.map_dust_url),font=temp_font, background='#888888').place(x=300, y=10)

        # 탭2 추가
        self.tab2_frame = tk.Frame(root)
        self.notebook.add(self.tab2_frame, text = "검색")
        tk.Label(self.tab2_frame, text="날씨를 검색할 지역 이름을 적어주세요 ex) 정왕").grid(row=0, column=0)

        self.search_entrybox = tk.Entry(self.tab2_frame, font=temp_font)
        self.search_entrybox.bind("<Return>", self.SearchInput)
        self.search_entrybox.bind("<Button-1>", self.SearchLButton)
        self.search_entrybox.grid(row=0, column=1)

        tk.Button(self.tab2_frame, text="날씨", command = lambda x= '날씨' : self.SearchInput(x), font=temp_font).grid(row=0, column=2)
        tk.Button(self.tab2_frame,text="미세먼지",command= lambda x='미세먼지':self.SearchInput(x),font=temp_font).grid(row=0,column=3)

        # 탭3 추가
        self.tab3_frame=tk.Frame(root)
        self.notebook.add(self.tab3_frame,text="주간 날씨 추가 예정")


        # 지도 Frame
        self.browser_frame = BrowserFrame(self, self.map_weather_url)
        self.browser_frame.grid(row=0, column=0,
                                sticky=(tk.N + tk.S + tk.E + tk.W))
        # 검색 Frame
        self.search_frame = BrowserFrame(self, "https://www.google.com")

        tk.Label(root, text="기관지 지킴이",font = temp_font,background=BACKGROUNDCOLOR).place(x=600,y=25)

    def PrintTab0(self):
        weathers = naverweather.GetWeatherInformation()
        self.weather_per_hour = weathers[3]
        #TODO: 미세먼지 관련 그래프로 추가 예정 self.dust_per_hour = weathers[4]
        self.tab0_location_label.configure(text=weathers[0])
        self.tab0_temperature_label.configure(text=weathers[1])
        self.tab0_weather_state_label.configure(text=weathers[2])
        self.tab0_time_label.configure(text=GetTimeText())
        #TODO: 나중엔 미세먼지랑 날씨 라디오 버튼이든 버튼으로든 받아서 그거로 나눠서 그려지게 할 예정
        self.DrawGraph()

    def DrawGraph(self):
        #0 ~ 150 을 - 온도맥스+5 ~ 온도min-5
        self.graph_canvas.delete("all")
        maxdegree = max(self.weather_per_hour[2]) + 5
        mindegree = min(self.weather_per_hour[2]) - 5
        diffdegree = abs(maxdegree-mindegree)
        gap = 100
        prev_x = 0
        prev_y = 0
        self.graph_canvas.create_text(20, 10,text= str(maxdegree)+'°',font = ('Arial',14))
        self.graph_canvas.create_text(20, 150, text=str(mindegree) + '°', font=('Arial', 14))
        for index, data in enumerate(self.weather_per_hour[2]):
            x = index * gap + gap/2
            percent = (data - mindegree) / (maxdegree-mindegree)
            y = 150 - percent*150
            print(y)
            if prev_x == 0 :
                prev_x = x
                prev_y = y
            self.graph_canvas.create_oval(x-3,y-3,x+3,y+3)
            self.graph_canvas.create_line(prev_x,prev_y,x,y)
            prev_x = x
            prev_y = y
            self.graph_canvas.create_text(x, 280,text= str(self.weather_per_hour[2][index])+'°',font = ('Arial',14))
            self.graph_canvas.create_text(x, 260, text=self.weather_per_hour[0][index],font=('Arial',14))
            self.graph_canvas.create_text(x, 240, text=self.weather_per_hour[1][index],font=('Arial',14))
            #그림 출력 TODO: 나중엔 바로바로 로드가 아니라 한번에 로드를 하면 좋겠다만 귀찮으니 걍 시간 더쓴다
            filename = text=self.weather_per_hour[1][index]

            if filename == '황사' or filename == '안개' or filename == '맑음' or filename == '구름조금' or filename == '구름많음' or filename == '가끔 비':
                if self.weather_per_hour[0][index][0] == '0' or self.weather_per_hour[0][index][0] == '1' or self.weather_per_hour[0][index][0]=='2':
                    time = int(self.weather_per_hour[0][index][:-1])
                    if (6<=time) and (time<=20):
                        filename += '(낮)'
                    else:
                        filename += '(밤)'
                else:
                    filename += '(밤)'
            self.graph_canvas.create_image(x, 200, image = self.weather_icon[filename])

        self.graph_canvas.configure(scrollregion= [0,0,49*gap-gap/2,300])

    # 노트북 탭이 바뀔 때 실행될 함수
    def my_notebook_msg(self, _):
        if self.show_browser_frame:  # 지도가 보이고 있을 때
            self.show_browser_frame = False  # 지도가 안보이도록 설정
            self.browser_frame.grid_remove()
            self.grid_remove()

        if self.show_search_frame:
            self.show_search_frame = False
            self.search_frame.grid_remove()
            self.grid_remove()
        # 현재 선택된 탭 인덱스 받아오기
        select_notetab_index = self.notebook.index("current")

        # 현재 선택된 탭은 Active로, 나머지는 Inactive로 이미지 수정
        #self.SetAllImageToInactive(select_notetab_index)

        if select_notetab_index == 0:
            # 0번탭에 해당하는 함수를 진행
            self.PrintTab0()

        elif select_notetab_index == 1:
            # 1번탭에 해당하는 함수를 진행
            # 지도를 보이도록 추가

            self.browser_frame.grid(row=0, column=0,
                                   sticky=(tk.N + tk.S + tk.E + tk.W))
            tk.Grid.rowconfigure(self, 0, weight=1)
            tk.Grid.columnconfigure(self, 0, weight=1)
            self.grid(row=3, column=0, padx=50, ipady =400,pady = 55,sticky=tk.N+tk.E+tk.W+tk.S)
            self.lift()
            self.show_browser_frame = True

        elif select_notetab_index == 2:
            pass

    # 노트북의 탭 이미지 활성화/비활성화
    def SetAllImageToInactive(self, index):

        self.notebook.tab(self.tab0_frame, background = BACKGROUNDCOLOR)
        self.notebook.tab(self.tab1_frame, background = BACKGROUNDCOLOR)
        self.notebook.tab(self.tab2_frame, background = BACKGROUNDCOLOR)

        # TODO: 나중에 배열로 리팩토링 진행해보기
        if index == 0:
            self.notebook.tab(self.tab0_frame, image=self.note_tab0_active_image)
        elif index == 1:
            self.notebook.tab(self.tab1_frame, image=self.note_tab1_active_image)
        elif index == 2:
            self.notebook.tab(self.tab2_frame, image=self.note_tab2_active_image)

    # 모든 이미지 로드
    def LoadAllImage(self):
        self.note_tab0_active_image = tk.PhotoImage(file='Resource\\Note_Tab0_Active.png')
        self.note_tab0_inactive_image = tk.PhotoImage(file='Resource\\Note_Tab0_Inactive.png')
        self.note_tab1_active_image = tk.PhotoImage(file='Resource\\Note_Tab1_Active.png')
        self.note_tab1_inactive_image = tk.PhotoImage(file='Resource\\Note_Tab1_Inactive.png')
        self.note_tab2_active_image = tk.PhotoImage(file='Resource\\Note_Tab2_Active.png')
        self.note_tab2_inactive_image = tk.PhotoImage(file='Resource\\Note_Tab2_Inactive.png')
        self.main_image = tk.PhotoImage(file='Resource\\MainImage.png')

    def ResetMapBrowser(self,url):
        self.browser_frame.LoadUrl(url)
    def SearchInput(self, button):

        # 브라우저가 켜져있다면
        if self.show_search_frame:
            # url만 바꾸기
            location = self.search_entrybox.get()
            self.search_entrybox.delete(0, len(location))
            if button =='미세먼지':
                self.search_frame.LoadUrl(GetNaverWeatherSearch(location,button))
            else:
                self.search_frame.LoadUrl(GetNaverWeatherSearch(location,None))

        else:
            self.search_frame.grid(row=0, column=0,
                                   sticky=(tk.N + tk.S + tk.E + tk.W))

            self.grid(row=3, column=0, ipadx=350,padx = 50, ipady=380,pady = 50, sticky=tk.NW)
            self.lift()
            tk.Grid.rowconfigure(self, 0, weight=1)
            tk.Grid.columnconfigure(self, 0, weight=1)
            self.show_search_frame = True
            location = self.search_entrybox.get()
            self.search_entrybox.delete(0, len(location))

            if self.search_frame.GetBrowser():
                if button == '미세먼지':
                    self.search_frame.LoadUrl(GetNaverWeatherSearch(location, button))
                else:
                    self.search_frame.LoadUrl(GetNaverWeatherSearch(location, 'None'))
            else:
                if button == '미세먼지':
                    self.search_frame.SetInitUrl(GetNaverWeatherSearch(location,button))
                else:
                    self.search_frame.SetInitUrl(GetNaverWeatherSearch(location,'None'))


    def SearchLButton(self, _):
        self.search_entrybox.focus_force()

    def close_window(self,_):
        self.root.destroy()

    def LoadWeatherIcon(self):
        self.weather_icon = dict()
        self.weather_icon['흐림'] = tk.PhotoImage(file= "Resource\\WeatherIcon\\흐림.png")
        self.weather_icon['황사(밤)'] = tk.PhotoImage(file="Resource\\WeatherIcon\\황사(밤).png")
        self.weather_icon['황사(낮)'] = tk.PhotoImage(file="Resource\\WeatherIcon\\황사(낮).png")
        self.weather_icon['진눈깨비'] = tk.PhotoImage(file="Resource\\WeatherIcon\\진눈깨비.png")
        self.weather_icon['우박'] = tk.PhotoImage(file="Resource\\WeatherIcon\\우박.png")
        self.weather_icon['약한비'] = tk.PhotoImage(file="Resource\\WeatherIcon\\약한비.png")
        self.weather_icon['약한눈'] = tk.PhotoImage(file="Resource\\WeatherIcon\\약한눈.png")
        self.weather_icon['안개(밤)'] = tk.PhotoImage(file="Resource\\WeatherIcon\\안개(밤).png")
        self.weather_icon['안개(낮)'] = tk.PhotoImage(file="Resource\\WeatherIcon\\안개(낮).png")
        self.weather_icon['소낙눈'] = tk.PhotoImage(file="Resource\\WeatherIcon\\소낙눈.png")
        self.weather_icon['소나기'] = tk.PhotoImage(file="Resource\\WeatherIcon\\소나기.png")
        self.weather_icon['비'] = tk.PhotoImage(file="Resource\\WeatherIcon\\비.png")
        self.weather_icon['번개'] = tk.PhotoImage(file="Resource\\WeatherIcon\\번개, 뇌우.png")
        self.weather_icon['뇌우'] = tk.PhotoImage(file="Resource\\WeatherIcon\\번개, 뇌우.png")
        self.weather_icon['맑음(밤)'] = tk.PhotoImage(file="Resource\\WeatherIcon\\맑음(밤).png")
        self.weather_icon['맑음(낮)'] = tk.PhotoImage(file="Resource\\WeatherIcon\\맑음(낮).png")
        self.weather_icon['눈'] = tk.PhotoImage(file="Resource\\WeatherIcon\\눈.png")
        self.weather_icon['구름조금(밤)'] = tk.PhotoImage(file="Resource\\WeatherIcon\\구름조금(밤).png")
        self.weather_icon['구름조금(낮)'] = tk.PhotoImage(file="Resource\\WeatherIcon\\구름조금(낮).png")
        self.weather_icon['구름많음(밤)'] = tk.PhotoImage(file="Resource\\WeatherIcon\\구름많음(밤).png")
        self.weather_icon['구름많음(낮)'] = tk.PhotoImage(file="Resource\\WeatherIcon\\구름많음(낮).png")
        self.weather_icon['강한비'] = tk.PhotoImage(file="Resource\\WeatherIcon\\강한비.png")
        self.weather_icon['강한눈'] = tk.PhotoImage(file="Resource\\WeatherIcon\\강한눈.png")
        self.weather_icon['가끔 비(밤)'] = tk.PhotoImage(file="Resource\\WeatherIcon\\가끔 비(밤).png")
        self.weather_icon['가끔 비(낮)'] = tk.PhotoImage(file="Resource\\WeatherIcon\\가끔 비(낮).png")


class BrowserFrame(tk.Frame):  # 지도 프레임
    def __init__(self, mainframe, url):
        self.browser = None
        tk.Frame.__init__(self, mainframe)
        self.mainframe = mainframe
        self.url = url
        self.bind("<Configure>", self.on_configure)
        # self.on_configure(None)

    # 브라우저 가져오기 및 tkinter에 내장하는 함수
    def embed_browser(self):
        window_info = cef.WindowInfo()  # 상위윈도우 정보 받기
        rect = [0, 0, self.winfo_width(), self.winfo_height() ]  # 상위윈도우 영역 기반 보일 영역 잡기
        window_info.SetAsChild(self.get_window_handle(), rect)  # 상위 윈도우의 차일드 윈도우 속성으로 내장되도록 설정
        self.browser = cef.CreateBrowserSync(window_info,  # 브라우저 객체 생성
                                             url=self.url)
        self.message_loop_work()  # 메시지 루프 입장

    def get_window_handle(self):
        return self.winfo_id()

    def message_loop_work(self):
        cef.MessageLoopWork()  # 메시지를 받고
        self.after(1, self.message_loop_work)  # 10ms이후 다시 메시지루프로 가도록, 이방식으로 진행해야 메인 윈도우가 실행 가능해지는 것으로 확인.

    # 설정될 때 실행될 함수
    def on_configure(self, _):
        if not self.browser:
            self.embed_browser()

    def GetBrowser(self):
        if self.browser:
            return self.browser

    def LoadUrl(self, url):
        if self.browser:
            self.browser.StopLoad()
            self.browser.LoadUrl(url)

    def SetInitUrl(self, url):
        self.url = url


def GetNaverWeatherSearch(location,button):
    print(button)
    if button == '미세먼지':
        return "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=" + location + "+미세먼지&oquery=" + location + "&tqi=ibu4pdp0J1ZssTMblOwssssssio-160161"
    return "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=" + location + "+날씨&oquery=" + location + "&tqi=ibu4pdp0J1ZssTMblOwssssssio-160161"


def GetTimeText():
    time = datetime.now()
    text = str(time.year) + "-"
    if time.month < 10: text += "0"
    text = text + str(time.month) + "-"
    if time.day < 10: text += "0"
    text = text + str(time.day) + "  "
    if time.hour < 10: text += "0"
    text = text + str(time.hour) + ":"
    if time.minute < 10: text += "0"
    text = text + str(time.minute) + ":"
    if time.second < 10: text += "0"
    text = text + str(time.second)

    return text


if __name__ == '__main__':
    main()