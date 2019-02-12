import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk#Agg
from matplotlib.figure import Figure
from matplotlib.widgets import Cursor
import matplotlib.animation as animation
from matplotlib import style
import matplotlib.dates as mdate
import matplotlib.pyplot as plt
import dateutil

import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter import *
import urllib
import json
import numpy as np
import pandas as pd
import datetime
import csv
import pylab as pl

import time
import re
from time import gmtime, strftime
from time import localtime, strftime

import sqlite3

check_count=0

conn = sqlite3.connect('ABB_LGR.db')
cs= conn.cursor()

read_time=strftime("%d %m %Y %H:%M:%S ", localtime())

LARGE_FONT = ("Verdana", 12)
style.use("dark_background")



#f = Figure(figsize=(5,5), dpi=100)
f=plt.figure()
a=plt.subplot2grid((3, 3), (0, 0), colspan=3,rowspan=2)
a1=plt.subplot2grid((4, 3), (3, 0), colspan=3)
#a=f.add_subplot(2,1,1)
#a1=f.add_subplot(3,1,3)
# a2=f.add_subplot(233)
# a3=f.add_subplot(234)
# a4=f.add_subplot(235)

g=plt.figure()
b=plt.subplot2grid((3, 3), (0, 0), colspan=3,rowspan=2)
b1=plt.subplot2grid((4, 3), (3, 0), colspan=3)
# b2=g.add_subplot(233)
# b3=g.add_subplot(234)
# b4=g.add_subplot(235)

yyyy_f_=""
mm_f_=""
dd_f_=""
HH_f_=""
MM_f_=""
SS_f_=""
yyyy_t_=""
mm_t_=""
dd_t_=""
HH_t_=""
MM_t_=""
SS_t_=""

def animate(i):
    #refresh_time()
    timeint=7200
    SQ_comm1="SELECT * FROM ABB_LGR WHERE unix >= (strftime('%s','now')"
    SQ_comm2="-%s)" % timeint
    SQ_comm=SQ_comm1+SQ_comm2
    df = pd.read_sql_query(SQ_comm,conn)
    df['datestamp'] = pd.to_datetime(df['datestamp'])#, unit='s')
    #last_col=df.iloc[-1,1:5]
    HF_q=df.iloc[-1,4]
    t.delete(1.0,END)
    t.insert('insert',HF_q)
    #print(last_col)
    #print("HF/n")
    #print(HF_q)
    a.clear()
    a1.clear()
    # a2.clear()
    # a3.clear()
    # a4.clear()
    xfmt = mdate.DateFormatter('%m/%d-%H:%M')
    #x1fmt = mdate.DateFormatter('%H')
    a.xaxis.set_major_formatter(xfmt)
    a1.xaxis.set_major_formatter(xfmt)
    # a2.xaxis.set_major_formatter(xfmt)
    # a3.xaxis.set_major_formatter(xfmt)
    # a4.xaxis.set_major_formatter(xfmt)
    #ax.set_xticklabels( rotation=45 )
    a.plot(df['datestamp'],df['HF'])
    #cursor = Cursor(a, useblit=True, color='red', linewidth=2)
    #a.set_xticklabels(xlabels, rotation=45)
    a.set_title('HF ppm')
    a1.plot(df["datestamp"],df["H2O"])
    #a1.set_xticklabels(xlabels, rotation=45)
    a1.set_title('H2O ppm')
    # a2.plot(df["datestamp"],df["value3"])
    # # a2.set_xticklabels(xlabels, rotation=45)
    # a2.set_title('Compressor2 temp')
    # a3.plot(df["datestamp"],df["value4"])
    # # a3.set_xticklabels(xlabels, rotation=45)
    # a3.set_title('Pump1 temp')
    # a4.plot(df["datestamp"],df["value5"])
    # # a4.set_xticklabels(xlabels, rotation=45)
    # a4.set_title('Romm Humi')
    
    

def LoadData():
    global yyyy_f_
    global mm_f_
    global dd_f_
    global HH_f_
    global MM_f_
    global SS_f_
    global yyyy_t_
    global mm_t_
    global dd_t_
    global HH_t_
    global MM_t_
    global SS_t_                                                                
    from_str=yyyy_f_+"-"+mm_f_+"-"+dd_f_#+" "+HH_f_+":"+MM_f_+":"+SS_f_
    to_str=yyyy_t_+"-"+mm_t_+"-"+dd_t_#+" "+HH_t_+":"+MM_t_+":"+SS_t_
    load_comm='SELECT * FROM ABB_LGR WHERE datestamp BETWEEN "%s" AND "%s"' %(from_str , to_str)
    print(load_comm)
    df = pd.read_sql_query(load_comm,conn)
    df['datestamp'] = pd.to_datetime(df['datestamp'])
    print(df)

    #print (name)
    #Using try in case user types in unknown file or closes without choosing a file.
    try:
        b.clear()
        b1.clear()
        # b2.clear()
        # b3.clear()
        # b4.clear()
        xfmt = mdate.DateFormatter('%m/%d-%H:%M')
        b.xaxis.set_major_formatter(xfmt)
        b1.xaxis.set_major_formatter(xfmt)
        # b2.xaxis.set_major_formatter(xfmt)
        # b3.xaxis.set_major_formatter(xfmt)
        # b4.xaxis.set_major_formatter(xfmt)
        b.plot(df["datestamp"],df['HF'])
        b.set_title('HF ppm')
        #b.canvas.flush_events()
        b1.plot(df["datestamp"],df["H2O"])
        b1.set_title('H20 ppm')
        # b2.plot(df["datestamp"],df["value3"])
        # b2.set_title('Compressor2 temp')
        # b3.plot(df["datestamp"],df["value4"])
        # b3.set_title('Pump1 temp')
        # b4.plot(df["datestamp"],df["value5"])
        # b4.set_title('Romm Humi')
    except:
        print("No file exists")
    return 
def SaveCSV():
    global yyyy_f_
    global mm_f_
    global dd_f_
    global HH_f_
    global MM_f_
    global SS_f_
    global yyyy_t_
    global mm_t_
    global dd_t_
    global HH_t_
    global MM_t_
    global SS_t_                                                                
    from_str=yyyy_f_+"-"+mm_f_+"-"+dd_f_+" "+HH_f_+":"+MM_f_+":"+SS_f_
    to_str=yyyy_t_+"-"+mm_t_+"-"+dd_t_+" "+HH_t_+":"+MM_t_+":"+SS_t_
    load_comm='SELECT * FROM ABB_LGR WHERE datestamp BETWEEN "%s" AND "%s"' %(from_str , to_str)
    #print(load_comm)
    df = pd.read_sql_query(load_comm,conn)
    #if len(load_comm)<97 :
    #    return
    sf = asksaveasfilename(initialdir = "/",title = "Save file",
                                      filetypes = (("csv files","*.csv"),("all files","*.*")))
    if sf is None:
        return
    df.to_csv(sf)
    

class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.attributes(self, '-fullscreen',True)
        tk.Tk.iconbitmap(self,default="Troll Face.ico")
        tk.Tk.wm_title(self,"ABB_LGR data visualization program")
        #tk.Tk.configure(self,background='black')
        
        container=tk.Frame(self)
        container.pack(side="top",fill="both",expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0,weight=1)

        self.frames={}
        
        for F in (StartPage, PageOne, GraphPage): 

            frame=F(container,self)

            self.frames[F]=frame

            frame.grid(row=0,column=0,sticky="nsew")

        self.show_frame(StartPage)


    def show_frame(self, cont):
        frame=self.frames[cont]
        frame.tkraise()
    
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent,background='black')
        
        label =tk.Label(self, text="Weltall TECH. CO. ABB-LGR Data Viewer",font=('Arial', 32),background='black',foreground="white")
        label.pack(pady=120,padx=10)

        # logo_img = PhotoImage(file = "logo.gif")
        # logo=tk.Label(self,image=logo_img)
        # logo.pack()

        button1=tk.Button(self,text="Start",font=('Arial', 32),
        command=lambda: controller.show_frame(GraphPage))
        button1.pack(pady=30,padx=10)
        
        #button2=ttk.Button(self,text="Quit",
        #command=quit)
        #button2.pack()

        #button3=ttk.Button(self,text="Visit to Page Three",
        #command=lambda: controller.show_frame(PageThree))
        #button3.pack()

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent,background='black')
        frm = tk.Frame(self,background='black')
        #image1=PhotoImage(file="logo.png")
        frm.pack()
        #frm.img=image1
        #frm.create_image(0, 0, anchor=NW, image=image1)
        frm_1 = tk.Frame(frm,background='black')
        frm_2 = tk.Frame(frm,background='black')
        frm_3 = tk.Frame(frm,background='black')
        frm_1.pack(anchor='n')
        frm_2.pack(anchor='n')
        frm_3.pack(anchor='n')

        label =tk.Label(frm_1, text="History Chart",font=('Arial', 24),background='black',foreground="white")
        label.pack(pady=10,padx=10,anchor='n')


        button1=tk.Button(frm_1,text="Back to Live Chart Page",font=('Arial', 16), fg = "red", bg = "#313938",
        command=lambda: controller.show_frame(GraphPage))
        #button1.config(bg='black',foreground="yellow")
        button1.pack(pady=10,padx=10,anchor='nw')
        

        def go1(*args):   
            global yyyy_f_
            yyyy_f_=comboxlist.get()
            print(yyyy_f_) 

        def go2(*args):   
            global mm_f_
            mm_f_=comboxlist2.get()
            print(mm_f_) 
        
        def go3(*args):   
            global dd_f_
            dd_f_=comboxlist3.get()
            print(dd_f_) 
        
        # def go4(*args):   
        #     global HH_f_
        #     HH_f_=comboxlist4.get()
        #     print(HH_f_) 

        # def go5(*args):   
        #     global MM_f_
        #     MM_f_=comboxlist5.get()
        #     print(MM_f_) 

        # def go6(*args):   
        #     global SS_f_
        #     SS_f_=comboxlist6.get()
        #     print(SS_f_)

        def go7(*args):   
            global yyyy_t_
            yyyy_t_=comboxlist7.get()
            print(yyyy_t_) 

        def go8(*args):   
            global mm_t_
            mm_t_=comboxlist8.get()
            print(mm_t_) 
        
        def go9(*args):   
            global dd_t_
            dd_t_=comboxlist9.get()
            print(dd_t_) 
        
        # def go10(*args):   
        #     global HH_t_
        #     HH_t_=comboxlist10.get()
        #     print(HH_t_) 

        # def go11(*args):   
        #     global MM_t_
        #     MM_t_=comboxlist11.get()
        #     print(MM_t_) 

        # def go12(*args):   
        #     global SS_t_
        #     SS_t_=comboxlist12.get()
        #     print(SS_t_)  


        label =tk.Label(frm_2, text="From",font=('Arial', 12),background='black',foreground="white")
        label.pack(padx=10,side='left')

        comvalue=tk.StringVar()
        comboxlist=ttk.Combobox(frm_2,width=4,textvariable=comvalue) 
        comboxlist["values"]=("2018","2019","2020","2021","2022","2023","2024","2025")
        comboxlist.current(0)  
        comboxlist.bind("<<ComboboxSelected>>",go1)  
        comboxlist.pack(side='left')

        label =tk.Label(frm_2, text="-",font=('Arial', 12),background='black',foreground="white")
        label.pack(side='left')

        comvalue2=tk.StringVar()
        comboxlist2=ttk.Combobox(frm_2,width=4,textvariable=comvalue2) 
        comboxlist2["values"]=("01","02","03","04","05","06","07","08","09","10","11","12")
        comboxlist2.current(0)  
        comboxlist2.bind("<<ComboboxSelected>>",go2)  
        comboxlist2.pack(side='left')

        label =tk.Label(frm_2, text="-",font=('Arial', 12),background='black',foreground="white")
        label.pack(side='left')

        comvalue3=tk.StringVar()
        comboxlist3=ttk.Combobox(frm_2,width=4,textvariable=comvalue3) 
        comboxlist3["values"]=("01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31")
        comboxlist3.current(0)  
        comboxlist3.bind("<<ComboboxSelected>>",go3)  
        comboxlist3.pack(side='left')

        label =tk.Label(frm_2, text=" ",font=('Arial', 12),background='black',foreground="white")
        label.pack(side='left')

        # comvalue4=tk.StringVar()
        # comboxlist4=ttk.Combobox(frm_2,width=4,textvariable=comvalue4) 
        # comboxlist4["values"]=("00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23")
        # comboxlist4.current(0)  
        # comboxlist4.bind("<<ComboboxSelected>>",go4)  
        # comboxlist4.pack(side='left')

        # label =tk.Label(frm_2, text=":",font=LARGE_FONT)
        # label.pack(side='left')

        # comvalue5=tk.StringVar()
        # comboxlist5=ttk.Combobox(frm_2,width=4,textvariable=comvalue5) 
        # comboxlist5["values"]=("00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30"
        #                     ,"31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59")
        # comboxlist5.current(0)  
        # comboxlist5.bind("<<ComboboxSelected>>",go5)  
        # comboxlist5.pack(side='left')

        # label =tk.Label(frm_2, text=":",font=LARGE_FONT)
        # label.pack(side='left')

        # comvalue6=tk.StringVar()
        # comboxlist6=ttk.Combobox(frm_2,width=4,textvariable=comvalue6) 
        # comboxlist6["values"]=("00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30"
        #                     ,"31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59")
        # comboxlist6.current(0)  
        # comboxlist6.bind("<<ComboboxSelected>>",go6) 
        # comboxlist6.pack(side='left')

        label =tk.Label(frm_2, text="To",font=('Arial', 12),background='black',foreground="white")
        label.pack(padx=10,side='left')

        comvalue7=tk.StringVar()
        comboxlist7=ttk.Combobox(frm_2,width=4,textvariable=comvalue7) 
        comboxlist7["values"]=("2018","2019","2020","2021","2022","2023","2024","2025")
        comboxlist7.current(0)  
        comboxlist7.bind("<<ComboboxSelected>>",go7)  
        comboxlist7.pack(side='left')

        label =tk.Label(frm_2, text="-",font=('Arial', 12),background='black',foreground="white")
        label.pack(side='left')

        comvalue8=tk.StringVar()
        comboxlist8=ttk.Combobox(frm_2,width=4,textvariable=comvalue8) 
        comboxlist8["values"]=("01","02","03","04","05","06","07","08","09","10","11","12")
        comboxlist8.current(0)  
        comboxlist8.bind("<<ComboboxSelected>>",go8)  
        comboxlist8.pack(side='left')

        label =tk.Label(frm_2, text="-",font=('Arial', 12),background='black',foreground="white")
        label.pack(side='left')

        comvalue9=tk.StringVar()
        comboxlist9=ttk.Combobox(frm_2,width=4,textvariable=comvalue9) 
        comboxlist9["values"]=("01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31")
        comboxlist9.current(0) 
        comboxlist9.bind("<<ComboboxSelected>>",go9)  
        comboxlist9.pack(side='left')

        # label =tk.Label(frm_2, text=" ",font=LARGE_FONT)
        # label.pack(side='left')

        # comvalue10=tk.StringVar()
        # comboxlist10=ttk.Combobox(frm_2,width=4,textvariable=comvalue10) 
        # comboxlist10["values"]=("00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23")
        # comboxlist10.current(0)  
        # comboxlist10.bind("<<ComboboxSelected>>",go10)  
        # comboxlist10.pack(side='left')

        # label =tk.Label(frm_2, text=":",font=LARGE_FONT)
        # label.pack(side='left')

        # comvalue11=tk.StringVar()
        # comboxlist11=ttk.Combobox(frm_2,width=4,textvariable=comvalue11) 
        # comboxlist11["values"]=("00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30"
        #                     ,"31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59")
        # comboxlist11.current(0)  
        # comboxlist11.bind("<<ComboboxSelected>>",go11)  
        # comboxlist11.pack(side='left')

        # label =tk.Label(frm_2, text=":",font=LARGE_FONT)
        # label.pack(side='left')

        # comvalue12=tk.StringVar()
        # comboxlist12=ttk.Combobox(frm_2,width=4,textvariable=comvalue12) 
        # comboxlist12["values"]=("00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30"
        #                     ,"31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59")
        # comboxlist12.current(0)  
        # comboxlist12.bind("<<ComboboxSelected>>",go12)  
        # comboxlist12.pack(side='left')

        button2=tk.Button(frm_2,text="Save Data as CSV file",font=('Arial', 12),fg = "red", bg = "#313938",
                           command=lambda: SaveCSV())
        button2.pack(padx=10,side='right')

        button3=tk.Button(frm_2,text="Load Data",font=('Arial', 12),fg = "red", bg = "#313938",
                           command=lambda: LoadData())
        button3.pack(padx=10,side='right')

        

        canvas= FigureCanvasTkAgg(g,self)
        
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        #canvas.get_tk_widget().grid( padx=10, pady=10)
        toolbar = NavigationToolbar2Tk(canvas, self)
        #toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        #canvas._tkcanvas.grid( padx=10, pady=10)
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
        
#root=SeaofBTCapp()
#time_string=StringVar()
   
# def refresh_time():
#     get_time=time.strftime('%H:%M:%S')
#     t.delete(1.0,END)
#     t.insert('insert',get_time)
#     print(get_time)

# def animate_pause():
#     #global pause
#     if (var.get() == 1) :   #如果选中第一个选项，未选中第二个选项
#         #pause=True
#         ani.event_source.stop()
#         print("test")
#     elif(var.get() == 0):
#         print("off")
#         ani.event_source.stop()
        #print(var1)
    # else:
    #     print(var1)
    #     ani.event_source.start()

class GraphPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent,background='black')
        frm = tk.Frame(self,background='black')
        frm.pack()
        frm_1 = tk.Frame(frm,background='black')
        frm_1.pack(anchor='n')
        #logo_img = PhotoImage(file = "logo.png")
        label =tk.Label(frm_1, text="ABB LGR Live Chart Page",font=('Arial', 24),background='black',foreground="white")
        label.pack(pady=10,padx=10)
        #label.Tk(background='black')
        # img = PhotoImage(file='logo.gif')
        # panel = Label(frm_1, image = img)
        # panel.pack(side = "left", fill = "both", expand = "yes")
        button1=tk.Button(frm_1,text="Quit",fg = "white", bg = "red",font=('Arial', 16),width=8, height=1, 
        command=quit)
        button1.pack(padx=30,side='right')
        
        #global time_string
        show_time=tk.Label(frm_1, text = "HF",font=('Arial', 24),fg = "white", bg = "black")#, compound = tk.CENTER)
        #show_time.after(10,refresh_time())
        show_time.pack(side='left')
        global t
        # get_time=time.strftime('%H:%M:%S')
        t = tk.Text(frm_1,height=1,width=8,font=('Arial', 24))#,fg = "white", bg = "black")
        # t.insert('insert',get_time)
        # # #t.after(1000,refresh_time())
        t.pack(side='left')
        # # #refresh_time()

        def animate_pause():
            global check_count
            # if (var.get() == 1) :   #如果选中第一个选项，未选中第二个选项
            #     #ani.event_source.stop()
            #     print("1")
            if (var.get() == 0) :
                check_count=check_count+1
                print(check_count)
                print("0")
                if(check_count%2==0):
                    ani.event_source.start()
                    print("start live chart")
                else:
                    ani.event_source.stop()
                    print("pause")

        button2=tk.Button(frm_1,text="History chart",fg = "red", bg = "#313938",font=('Arial', 16),width=15, height=1, 
        command=lambda: controller.show_frame(PageOne)
        )
        button2.pack(padx=30,side='left')

        var = tk.IntVar()
        c1 = tk.Checkbutton(frm_1, text='Pause', variable=var, onvalue=1, offvalue=0,fg = "green", bg = "black",font=('Arial', 16),
        command=lambda:animate_pause())
        c1.pack(side='left')


        canvas= FigureCanvasTkAgg(f,self)
        canvas.draw()
        toolbar = NavigationToolbar2Tk(canvas, self)
        #toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    

#cs.close()
#conn.close()
app= SeaofBTCapp()
ani=animation.FuncAnimation(f, animate,  interval=1000)#, blit=True)init_func=init,
app.mainloop()


