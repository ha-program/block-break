import tkinter as tk
import sys

class Game(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.win_width=600
        self.win_height=480
        self.flag=True
        self.b_flag=False
        self.title(u"ブロック崩し")
        self.geometry("600x480")
        self.cv=tk.Canvas(self,width=self.win_width,height=self.win_height)
        self.cv.pack()

    def finish(self):
        if self.ball_y+self.r>self.win_height or self.score==18:
            self.cv.delete("paddle")
            self.cv.delete("ball")
            fin_text="GAME CREAR" if self.score==18 else "GAME OVER"
            self.cv.create_text(self.win_width/2,self.win_height/2,text=fin_text,font=("Times New Roman",40),tag="text")
            self.ball_dx=0
            self.ball_dy=0
            self.flag=False
            self.reset_button()

    def reset_button(self):
        self.button=tk.Button(self,text="Restart",command=self.reset)
        self.button.place(x=280,y=400)

    def setting(self):
        self.score=0
        self.ball_x=250
        self.ball_y=250
        self.r=10
        self.ball_dx=self.ball_dy=5

        self.paddle_x=self.win_width/2
        self.paddle_y=self.win_height-30
        self.paddle_wx=45
        self.paddle_wy=8
        self.paddle_dx=6

        self.block_w_x=100
        self.block_w_y=30
        self.block_list=[[1,1,1,1,1,1],
                        [1,1,1,1,1,1],
                        [1,1,1,1,1,1]]
        self.ball_draw()
        self.paddle_draw()
        self.block_draw()
        self.score_draw()

    def gameloop(self):
        if self.flag:
            self.ball_delete()
            self.ball_move()
            self.paddle_move()
            self.reflect()
            self.ball_draw()
            self.finish()
            self.after(40,self.gameloop)

    def reset(self):
        self.setting()

        self.button.destroy()
        self.flag=True
        self.cv.delete("paddle")
        self.cv.delete("text")
        self.paddle_draw()
        self.gameloop()

    def game_end(self):
        self.mainloop()

    def score_draw(self):
        self.cv.create_text(self.win_width-50,50,text="Score="+str(self.score),font=("Times New Roman",16),tag="score")
    def score_delete(self):
        self.cv.delete("score")
    
    def ball_draw(self):
        self.cv.create_oval(self.ball_x-self.r, self.ball_y-self.r, self.ball_x+self.r, self.ball_y+self.r, fill="red",tag="ball")

    def ball_move(self):
        self.ball_x+=self.ball_dx
        self.ball_y+=self.ball_dy
        ue=self.paddle_y-self.paddle_wy
        shita=self.paddle_y+self.paddle_wy
        migi=self.paddle_x+self.paddle_wx
        hidari=self.paddle_x-self.paddle_wx

        if self.ball_x-self.r<0 or self.ball_x+self.r>self.win_width \
            or((hidari<self.ball_x+self.r<migi or hidari<self.ball_x-self.r<migi) and ue<self.ball_y<shita):

            self.ball_dx*=-1
            
        if self.b_flag: #角から入ってギザギザした挙動になるのを防ぐ
            self.b_flag=False
            return
            
        if self.ball_y-self.r<0 or (ue<self.ball_y+self.r<shita and hidari<self.ball_x<migi):
            self.ball_dy*=-1
        
        if (migi-self.ball_x)**2+(ue-self.ball_y)**2<self.r**2 or self.ball_dx>0 and (hidari-self.ball_x)**2+(ue-self.ball_y)**2<self.r**2:
            self.ball_dy*=-1
            self.b_flag=True

    def ball_delete(self):
        self.cv.delete("ball")

    
    def paddle_draw(self):
        self.cv.create_rectangle(self.paddle_x-self.paddle_wx, self.paddle_y-self.paddle_wy, self.paddle_x+self.paddle_wx, self.paddle_y+self.paddle_wy, fill="blue", tag="paddle")

    def right(self,event):
        self.cv.delete("paddle")
        self.paddle_x+=self.paddle_dx
        self.paddle_draw()

    def left(self,event):
        self.cv.delete("paddle")
        self.paddle_x-=self.paddle_dx
        self.paddle_draw()

    def paddle_move(self):
        self.bind("<Right>",self.right)
        self.bind("<Left>",self.left)

    def block_draw(self):
        for i in range(6):
            for j in range(3):
                self.cv.create_rectangle(i*self.block_w_x, j*self.block_w_y, (i+1)*self.block_w_x,(j+1)*self.block_w_y,fill="orange",tag="b"+str(j)+str(i))
        
    def reflect(self):
        for i in range(6):
            for j in range(3):
                if (self.ball_y-self.r<(j+1)*self.block_w_y and i*self.block_w_x<self.ball_x<(i+1)*self.block_w_x and self.block_list[j][i]==1):
                    self.ball_dy*=-1
                    self.cv.delete("b"+str(j)+str(i))
                    self.block_list[j][i]=0
                    self.score+=1
                    self.score_delete()
                    self.score_draw()

if __name__=="__main__":
    game=Game()
    game.setting()
    game.gameloop()
    game.game_end()