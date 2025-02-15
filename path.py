import tkinter as tk
import tkinter.messagebox as tmsg
import numpy as np
import random
from collections import deque

class BFS:
    def __init__(self,a,b):
        self.x,self.y,self.n=a,b,a*b
        self.matrix=np.zeros((self.n,self.n))

    def adjacency(self,prohibited):
        for i in range(self.n):
            if i not in prohibited:
                for j in[i+self.x,i-self.x,i+1,i-1]:
                    if 0<=j< self.n and j not in prohibited:
                        self.matrix[i][j]=1

    def calculate_distance(self,m,n):
        visited=set()
        parent=np.zeros(self.n,dtype=int)
        queue=deque([m])
        visited.add(m)

        while queue:
            a=queue.popleft()
            for i in range(self.n):
                if self.matrix[a][i]==1 and i not in visited:
                    parent[i]=a
                    visited.add(i)
                    queue.append(i)
                    if i==n:
                        queue.clear()
                        break

        if n not in visited:
            return

        traversed,p=[],parent[n]
        while p!=m:
            traversed.append(p)
            p=parent[p]
        self.traversed=traversed

class Body:
    def __init__(self,root):
        self.root=root
        self.width,self.height=1050,700
        self.dx,self.dy=48,20
        self.cx,self.cy=50,50
        self.cell_size=20
        self.start_pt,self.end_pt=0,self.dx*self.dy-1
        self.prohibited,self.rs,self.hs=[],[],[]

        self.canvas=tk.Canvas(root,width=self.width,height=self.height,bg="white")
        self.canvas.pack()
        self.create_ui()
        self.grid()
        self.listen_mouse_clicks()
        root.resizable(False,False)

    def main(self):
        b=BFS(self.dx,self.dy)
        b.adjacency(self.prohibited)
        try:
            b.calculate_distance(self.start_pt,self.end_pt)
            for item in self.rs:
                self.canvas.delete(item)
            self.rs.clear()
            for i in b.traversed:
                self.draw_point(i,"black")
        except Exception as e:
            tmsg.showinfo("Not Found",f"No path found between the start and end points: {e}")

    def draw_point(self,n,color):
        x=self.cx+self.cell_size*(n%self.dx)
        y=self.cy+self.cell_size*(n//self.dx)
        item=self.canvas.create_rectangle(x,y,x+self.cell_size,y+self.cell_size,fill=color)
        self.rs.append(item)

    def draw_start(self):
        self.start,self.end,self.hurdles=True,False,False

    def draw_end(self):
        self.start,self.end,self.hurdles=False,True,False

    def draw_hurdles(self):
        self.start,self.end,self.hurdles=False,False,True

    def create_ui(self):
        instructions = [
            "a) Press 's' to place the start point (green).",
            "b) Press 'e' to place the end point (blue).",
            "c) Press 'h' to place hurdles (red).",
            "d) Press 'r' to place random hurdles.",
            "e) Press 'space' to find the shortest path (black).",
            "f) Press 'o' to clear the grid."
        ]
        y=500
        for text in instructions:
            self.canvas.create_text(20,y,anchor="nw",text=text,font=("Arial",12),fill="black")
            y+=25

    def draw_squares(self,event):
        x,y=event.x,event.y
        grid_x=(x-self.cx)//self.cell_size
        grid_y=(y-self.cy)//self.cell_size
        loc=grid_y*self.dx+grid_x
        if 0<=grid_x<self.dx and 0<=grid_y<self.dy:
            xcor=self.cx+grid_x*self.cell_size
            ycor=self.cy+grid_y*self.cell_size
            if self.hurdles:
                self.prohibited.append(loc)
                item=self.canvas.create_rectangle(xcor,ycor,xcor+self.cell_size,ycor+self.cell_size,fill="red")
                self.hs.append(item)
            elif self.start:
                self.start_pt=loc
                self.st=self.create_rectangle(xcor,ycor,"green")
            elif self.end:
                self.end_pt=loc
                self.et=self.create_rectangle(xcor,ycor,"blue")

    def create_rectangle(self,xcor,ycor,color):
        return self.canvas.create_rectangle(xcor,ycor,xcor+self.cell_size,ycor+self.cell_size,fill=color)

    def erase_all(self):
        self.canvas.delete("all")
        self.prohibited.clear()
        self.rs.clear()
        self.hs.clear()
        self.grid()

    def random_hurdles(self):
        for _ in range(100):
            loc=random.randint(0,self.dx*self.dy-1)
            if loc not in self.prohibited and loc!=self.start_pt and loc!=self.end_pt:
                self.prohibited.append(loc)
                self.draw_point(loc,"red")

    def listen_mouse_clicks(self):
        self.canvas.bind("<Button-1>",self.draw_squares)
        self.root.bind("<space>",lambda event:self.main())
        self.root.bind("s",lambda event:self.draw_start())
        self.root.bind("e",lambda event:self.draw_end())
        self.root.bind("h",lambda event:self.draw_hurdles())
        self.root.bind("o",lambda event:self.erase_all())
        self.root.bind("r",lambda event:self.random_hurdles())

    def grid(self):
        for i in range(self.dy+1):
            self.canvas.create_line(self.cx,self.cy+self.cell_size*i,self.cx+self.dx*self.cell_size,self.cy+self.cell_size*i,fill="black")
        for i in range(self.dx+1):
            self.canvas.create_line(self.cx+self.cell_size*i,self.cy,self.cx+self.cell_size*i,self.cy+self.dy*self.cell_size,fill="black")

if __name__=="__main__":
    root=tk.Tk()
    root.title("BFS Pathfinding Visualizer")
    app=Body(root)
    root.mainloop()
