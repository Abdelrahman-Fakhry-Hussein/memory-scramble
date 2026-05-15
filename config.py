import tkinter as tk

from tkinter import  messagebox

def generate_emojis( count ):
    
    """generate unique emojis dynamically from unicode ranges"""
    import random
    import unicodedata

    ranges = [
        (0x1F400, 0x1F4FF),

        ( 0x1F300, 0x1F3FF ),

        (0x1F600,0x1F64F),
        (0x1F680 , 0x1F6FF),

        ( 0x1F900, 0x1F9FF),
        (0x1FA70, 0x1FAFF ),
    ]

    # words that we want to skip
    skip_words = ['HEART','CIRCLE','SQUARE', 'DIAMOND','TRIANGLE',
                  'MODIFIER','VARIATION','COMPONENT','SKIN' ,'TONE',
                  'REGIONAL','TAG', 'SELECTOR','KEYCAP','DIGIT',
                  'ARROW','BUTTON']

    pool =[]

    for start,end in ranges:
        for cp in range(start, end +1):
            ch = chr(cp)
            try:
                name = unicodedata.name(ch , '')
            except:
                continue
            if not name:
                continue

            upper_name =name.upper()
            skip= False
            for word in skip_words:
                if word in upper_name:
                    skip =True
                    break
            if skip:
                continue

            pool.append( ch )

    # shuffle and pick
    while True:
        random.shuffle( pool )
        selected = pool[:count]
        if len(selected)==len(set(selected)) and len(selected)==count:
            return selected
        unique =list(set(pool))
        if len(unique)>= count:
            random.shuffle(unique)
            return unique[:count]
        else:
            return unique



class ConfigWindow:
    def __init__( self ):
        self.root = tk.Tk()
        self.root.title( "Memory Scramble - Setup" )
        self.root.configure(bg= "#34495e")
        self.root.geometry("350x280")
        self.root.resizable(False,False)
        self.result =None

        # center window
        self.root.update_idletasks()

        sw= self.root.winfo_screenwidth()
        sh =self.root.winfo_screenheight()
        x =(sw - 350)   // 2
        y= (sh - 280) //2
        self.root.geometry(f"350x280+{x}+{y}")

        tk.Label(self.root, text="🧠 Memory Scramble",font=("Arial",18,"bold"),
                bg="#34495e",fg="white").pack(pady=15)

        frame= tk.Frame(self.root, bg="#34495e")
        frame.pack( pady=5 )

        # rows
        tk.Label(frame,text="Rows:", font=("Arial",12),bg="#34495e",fg="white").grid(row=0,column=0,padx=10,pady=8,sticky="e")
        
        self.rows_entry =tk.Entry(frame,width=10, font=("Arial",12))
        
        
        self.rows_entry.grid(row=0, column=1,padx=10,pady=8)
        
        self.rows_entry.insert(0,"4")

        # cols
        tk.Label(frame,text="Columns:",font=("Arial", 12),bg="#34495e",fg="white").grid(row=1,column=0,padx=10,pady=8,sticky="e")
        
        self.cols_entry= tk.Entry(frame, width=10,font=("Arial",12))
        
        self.cols_entry.grid( row=1,column=1, padx=10, pady=8)
        
        self.cols_entry.insert(0, "4")

        #timeout
        tk.Label(frame,text="Time (sec):",font=("Arial",12), bg="#34495e",fg="white").grid(row=2,column=0,padx=10,pady=8,sticky="e")
        
        self.time_entry= tk.Entry(frame,width=10,font=("Arial",12))
        
        self.time_entry.grid(row=2,column=1,padx=10, pady=8)
        
        
        self.time_entry.insert(0,"60")

        btn =tk.Button(self.root, text="▶ Start Game",font=("Arial",13,"bold"),
                       bg="#27ae60",fg="white", activebackground="#2ecc71",
                       command=self.on_start,padx=20,pady=5)
        btn.pack(pady=15)

    def on_start( self ):
        try:
            r= int(self.rows_entry.get())
            c =int(self.cols_entry.get())

            t= int( self.time_entry.get() )
        except ValueError:
            messagebox.showerror( "Error",   "Please enter valid numbers" )
            return

        total =r * c
        if total % 2 !=0:
            messagebox.showerror( "Error",  "Board size must be even (rows x cols)")
            return

        if t <=0:
            messagebox.showerror( "Error","Time must be positive" )
            return

        if r<=0 or c <=0:
            messagebox.showerror("Error"    , "Rows and columns must be positive")
            return

        self.result =(r, c, t)
        self.root.destroy()

    def run( self ):
        self.root.mainloop()
        return self.result


def get_config():

    w =ConfigWindow()


    return w.run()
