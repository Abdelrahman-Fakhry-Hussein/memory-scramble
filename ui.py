import tkinter as tk
from tkinter import messagebox

from game_logic import GameState
from timer import  Timer

from board import generate_board

from config import get_config


class GameUI:
    def __init__(self, root,board, rows,cols, timeout):
        self.root= root

        self.rows =     rows
        self.cols= cols

        self.timeout =  timeout
        self.game_ended= False
        self.root.title( "Memory Scramble" )
        self.root.configure( bg="#2c3e50" )

        # size window based on cells
        cell_size =70


        min_w,min_h= 400,350
        max_w, max_h =900, 700

        win_w   = max(min_w, min(  cols*cell_size +60, max_w)  )

        win_h =max(min_h,  min(rows * cell_size+130, max_h) )

        sw =self.root.winfo_screenwidth()

        sh= self.root.winfo_screenheight()

        x= (sw -win_w) //2

        y =(sh- win_h)// 2
        self.root.geometry( f"{win_w}x{win_h}+{x}+{y}" )

        self.game =GameState(board, rows,cols)

        self.timer= Timer(timeout)
        self.buttons =[]

        # top bar
        top= tk.Frame(root, bg="#2c3e50",height=50)
        top.pack(fill="x",side="top", pady=5)
        top.pack_propagate( False )

        tk.Label(top,text="🧠 Memory Scramble", font=("Arial",18,"bold"),
                bg="#2c3e50", fg="white").pack(side="left",padx=15)

        self.timer_label =tk.Label(top, text=f"⏱ {timeout}s",
                                   font=("Arial",16, "bold"),
                                   bg="#2c3e50",fg="#f1c40f")
        self.timer_label.pack( side="right",padx=15 )

        # grid frame
        self.grid_frame= tk.Frame(root, bg="#2c3e50")


        self.grid_frame.pack(   expand=True, fill="both",   padx=15,pady=10)

        for i in range( rows  ):
            self.grid_frame.grid_rowconfigure(i  , weight=1)

        for j in range( cols ):

            self.grid_frame.grid_columnconfigure(j  ,weight=1)

        # font size based on board
        if max(rows,cols) <=4:
            fsize=22

        elif max(rows, cols)<=6:
            fsize =17

        elif max(rows,cols) <=8:
            fsize= 14
        else:
            fsize =11

        for i in range( rows ):
            row_btns=[]
            for j in range(cols):
                btn= tk.Button(self.grid_frame, text="❓",
                               
                               font=("Segoe UI Emoji",fsize),

                               bg="#3498db",fg="white",

                               activebackground="#2980b9",

                               relief="raised",bd=3,
                               command=lambda r=i,c=j: self.on_click(r,c))
                btn.grid(row=i,column=j, padx=2,pady=2, sticky="nsew")
                row_btns.append( btn )


            self.buttons.append(row_btns)

        self.timer.start()

        self.update_timer()

    def on_click( self,r, c ):
        if self.game_ended or not self.timer.running:
            return

        flipped= self.game.flip_card(r,c)
        if not flipped:
            return

        emoji =self.game.board[r][c]


        self.buttons[r][c].config(text=emoji, bg="#1abc9c",
                                  
                                  state="disabled",disabledforeground="black")

        if len( self.game.flipped)==  2:
            self.game.locked    = True
            self.root.after(700, self.check_pair)

    def check_pair(self):
        if self.game_ended:
            return

        result =self.game.check_match()

        if result==True:
            pass
        else:
            for (r,c) in self.game.flipped:
                self.buttons[r][c].config( text="❓",bg="#3498db",
                                         state="normal", fg="white" )
            self.game.reset_flipped()

        self.game.locked =False

        if self.game.is_complete():
            self.game_ended =True


            self.timer.stop()
            self.end_screen( "🎉 You Win!","Congratulations! You matched all pairs!" )

    def update_timer( self ):
        if self.game_ended:
            return

        remaining= self.timer.get_remaining()
        self.timer_label.config(text=f"⏱ {remaining}s")

        if remaining<=10:
            self.timer_label.config( fg="#e74c3c" )

        if remaining <=0:
            self.game_ended= True
            self.end_screen("😢 Game Over", "Time's up! You didn't match all cards.")
            return

        self.root.after( 1000,self.update_timer )

    def end_screen(self, title,msg):
        for w in self.root.winfo_children():
            w.destroy()

        self.root.configure(bg= "#2c3e50")

        tk.Label(self.root, text=title,font=("Arial",28,"bold"),
                bg="#2c3e50",fg="white").pack( pady=40 )
        

        tk.Label(self.root,text=msg, font=("Arial",14),
                bg="#2c3e50", fg="#ecf0f1").pack(pady=10)

        btn_frame =tk.Frame(self.root, bg="#2c3e50")
        btn_frame.pack( pady=30 )

        tk.Button(btn_frame, text="🔄 Play Again",font=("Arial",13,"bold"),
                 bg="#27ae60", fg="white",padx=20,pady=8,


                 command=self.play_again).pack(side="left", padx=10)

        tk.Button(btn_frame,text="❌ Quit", font=("Arial",13,"bold"),
                 bg="#e74c3c",fg="white", padx=20,pady=8,
                 command=self.root.destroy).pack( side="left",padx=10 )

    def play_again( self ):
        self.root.destroy()
        start_game()


def start_game():
    cfg= get_config()
    if cfg is None:
        return

    rows,cols, timeout =cfg


    board= generate_board(rows, cols)

    root =tk.Tk()
    game= GameUI(root, board,rows,cols, timeout)
    
    root.mainloop()
