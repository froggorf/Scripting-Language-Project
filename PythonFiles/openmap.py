from cefpython3 import cefpython as cef


def message_loop_work(root):
    cef.MessageLoopWork()
    #root.after(5,message_loop_work)
    root.after(5, lambda r = root:message_loop_work(r))

def create(root):
    window_info = cef.WindowInfo()
    rect = [500,500,550,550]
    window_info.SetAsChild(root.winfo_id(),rect)
    cef.Initialize()
    cef.CreateBrowserSync(window_info,url="https://weather.naver.com/map/02390118", window_title="test")
    message_loop_work(root)
