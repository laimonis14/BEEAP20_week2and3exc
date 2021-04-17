
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import tkinter.font as tkFont
import os #imported os  for showing file name
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


        
class App:
    def __init__(self, root):
        # setting title
        root.title("DATA Browser/test changing")
        # setting window size
        width = 700
        height = 500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height,
                                    (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        self.__Button1 = tk.Button(root)
        self.__Button1["bg"] = "#efefef"
        ft = tkFont.Font(family='Times', size=10)
        self.__Button1["font"] = ft
        self.__Button1["fg"] = "#000000"
        self.__Button1["justify"] = "center"
        self.__Button1["text"] = "Select CSV file"
        self.__Button1.place(x=30, y=50, width=100, height=25)
        self.__Button1["command"] = self.__Button1_command

        self.__List_Box = ttk.Combobox(root)
        self.__List_Box.place(x=500, y=50, width=150, height=25)
        self.__List_Box.bind("<<ComboboxSelected>>", self.__comboBoxCb)

        self.__File_Label = tk.Label(root)
        ft = tkFont.Font(family='Times', size=10)
        self.__File_Label["font"] = ft
        self.__File_Label["fg"] = "#333333"
        self.__File_Label["justify"] = "left"
        self.__File_Label["text"] = "No file selected"
        self.__File_Label.place(x=130, y=50, width=200, height=25)
        
        #List box label
        self.__List_Label = tk.Label(root)
        ft = tkFont.Font(family = "Times", size = 12)
        self.__List_Label["font"] = ft
        self.__List_Label["fg"] = "#333333"
        self.__List_Label["justify"] = "center"
        self.__List_Label["text"] = "Select the city:"
        self.__List_Label.place(x=380, y=50, width=100, height=25)
        

        
        self.__First_Canvas = tk.Canvas(root, width=305, height=150)
        self.__First_Canvas.place(x=30, y=130)

        self.__Second_Canvas = tk.Canvas(root, width=305, height=150)
        self.__Second_Canvas.place(x=365, y=130)
 
        self.__Third_Canvas = tk.Canvas(root, width=305, height=150)  
        self.__Third_Canvas.place(x=30, y=290)
        
        self.__Fourth_Canvas = tk.Canvas(root, width=305, height=150)
        self.__Fourth_Canvas.place(x=365, y=290)
        
                

    def __Button1_command(self):
        filePath = fd.askopenfilename(initialdir='.')
        
        #Displaying just file name
        self.__File_Label.config(text = os.path.basename(filePath))
        try:
            self.__df = pd.read_csv(filePath)
            self.__df = self.__df.dropna()
            self.__List_Box['values'] = sorted(list(self.__df['COMMUNITY AREA NAME'].unique()))
        except:
            # quick and dirty, desired behavior would be to show a notification pop up that says
            # "nope!"
                     
            tk.messagebox.showinfo("ERROR", "ERROR Wrong file")
            
            
          
          

    # desired behavior: select one area, show 4 plots drawn on 4 canvases of that area: 
    # top left: bar chart, average KWH by month
    # top right: bar chart, average THERM by month
    # bottom left and bottom right up to you
    def __comboBoxCb(self, event=None):
        self.__subdf = self.__df.loc[self.__df['COMMUNITY AREA NAME'] == self.__List_Box.get()]
                
        
        fig1 = plt.figure(dpi=50)                 
        ax1 = fig1.add_subplot(111)
        graph1 = FigureCanvasTkAgg(fig1, root)
        graph1.get_tk_widget().place(x=30, y=130, width=305, height=150)
        self.__KWH_jan_loc = self.__subdf.columns.get_loc('KWH JANUARY 2010')
        self.__subdf.iloc[:, range(self.__KWH_jan_loc, self.__KWH_jan_loc+12)].mean().plot.bar(ax=ax1)
        str_month_list = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        ax1.set_xticks(range(0,12))
        ax1.set_xticklabels(str_month_list)
        ax1.set_title('Average KWH by month')   
       
       
        fig2 = plt.figure(dpi=50)
        ax2 = fig2.add_subplot(111)      
        graph2 = FigureCanvasTkAgg(fig2, root)
        graph2.get_tk_widget().place(x=365, y=130, width=305, height=150)
        self.__THERM_jan_loc = self.__subdf.columns.get_loc('THERM JANUARY 2010')
        self.__subdf.iloc[:, range(self.__THERM_jan_loc, self.__THERM_jan_loc+12)].mean().plot.pie(ax=ax2)
        
        
        fig3 = plt.figure(dpi=50)
        ax3 = fig3.add_subplot(111)      
        graph3 = FigureCanvasTkAgg(fig3, root)
        graph3.get_tk_widget().place(x=30, y=290, width=305, height=150)
        self.__KWH_jan_loc = self.__subdf.columns.get_loc('KWH JANUARY 2010')
        self.__subdf.iloc[:, range(self.__KWH_jan_loc, self.__KWH_jan_loc+12)].max().plot.pie(ax=ax3)
        
        
        fig4 = plt.figure(dpi=50)
        ax4 = fig4.add_subplot(111)      
        graph4 = FigureCanvasTkAgg(fig2, root)
        graph4.get_tk_widget().place(x=365, y=290, width=305, height=150)
        self.__THERM_jan_loc = self.__subdf.columns.get_loc('THERM JANUARY 2010')
        self.__subdf.iloc[:, range(self.__THERM_jan_loc, self.__THERM_jan_loc+12)].max().plot.bar(ax=ax4)
       
        
        

      
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
