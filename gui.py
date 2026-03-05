#!/usr/bin/env python3
import tkinter as tk
from utils.ioprocess import read_puzzle
from dfs import DFSBinairo
from heuristic import HeuristicBinairo

class BinairoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Binairo Visualizer")
        
        self.ctrl_frame = tk.Frame(root)
        self.ctrl_frame.pack(pady=10)
        
        self.btn_dfs = tk.Button(self.ctrl_frame, text="Solve DFS", command=lambda: self.run_solver("DFS"))
        self.btn_dfs.grid(row=0, column=0, padx=5)
        
        self.btn_heu = tk.Button(self.ctrl_frame, text="Solve Heuristic", command=lambda: self.run_solver("Heuristic"))
        self.btn_heu.grid(row=0, column=1, padx=5)
        
        self.btn_prev = tk.Button(self.ctrl_frame, text="< Prev", command=self.prev_step, state=tk.DISABLED)
        self.btn_prev.grid(row=0, column=2, padx=5)
        
        self.btn_next = tk.Button(self.ctrl_frame, text="Next >", command=self.next_step, state=tk.DISABLED)
        self.btn_next.grid(row=0, column=3, padx=5)
        
        self.btn_play = tk.Button(self.ctrl_frame, text="Auto Play", command=self.auto_play, state=tk.DISABLED)
        self.btn_play.grid(row=0, column=4, padx=5)
        
        self.lbl_info = tk.Label(root, text="Ready. Please select an algorithm.", font=("Arial", 12))
        self.lbl_info.pack(pady=5)
        
        self.canvas_size = 500
        self.canvas = tk.Canvas(root, width=self.canvas_size, height=self.canvas_size, bg="white")
        self.canvas.pack(pady=10)
        
        self.filepath = "data/14x14.txt" 
        self.initial_grid = read_puzzle(self.filepath)
        self.n = len(self.initial_grid)
        self.cell_size = self.canvas_size // self.n
        
        self.history = []
        self.current_step = 0
        self.is_playing = False
        
        self.draw_grid(self.initial_grid)

        self.root.bind("<Left>", self.prev_step)
        self.root.bind("<Right>", self.next_step)
        self.root.bind("<space>",self.auto_play)
    def run_solver(self, algo):
        self.lbl_info.config(text=f"Solving with {algo}... Please wait.")
        self.root.update()
        
        solver = DFSBinairo(self.initial_grid, enable_log=True) if algo == "DFS" else HeuristicBinairo(self.initial_grid, enable_log=True)
        is_solved = solver.solve()
        
        self.history = solver.history
        self.current_step = 0
        
        status = "Found Solution!" if is_solved else "No Solution!"
        self.lbl_info.config(text=f"{algo}: {status} (Total steps: {len(self.history)})")
        
        self.btn_next.config(state=tk.NORMAL)
        self.btn_play.config(state=tk.NORMAL)
        self.draw_grid(self.history[0])

    def draw_grid(self, grid_state):
        self.canvas.delete("all")
        for r in range(self.n):
            for c in range(self.n):
                x0, y0 = c * self.cell_size, r * self.cell_size
                x1, y1 = x0 + self.cell_size, y0 + self.cell_size
                
                self.canvas.create_rectangle(x0, y0, x1, y1, fill="white", outline="gray")
                
                val = grid_state[r][c]
                if val != -1:
                    pad = self.cell_size * 0.15 
                    
                    circle_color = "black" if val == 1 else "white"
                    
                    self.canvas.create_oval(
                        x0 + pad, y0 + pad, 
                        x1 - pad, y1 - pad, 
                        fill=circle_color, 
                        outline="black",
                        width=2
                    )
    def next_step(self, event=None):
        if self.current_step < len(self.history) - 1:
            self.current_step += 1
            self.draw_grid(self.history[self.current_step])
            self.lbl_info.config(text=f"Step: {self.current_step} / {len(self.history)-1}")
            self.btn_prev.config(state=tk.NORMAL)

    def prev_step(self, event=None):
        if self.current_step > 0:
            self.current_step -= 1
            self.draw_grid(self.history[self.current_step])
            self.lbl_info.config(text=f"Step: {self.current_step} / {len(self.history)-1}")

    def auto_play(self,event=None):
        if not self.is_playing:
            self.is_playing = True
            self.btn_play.config(text="Stop")
            self.play_loop()
        else:
            self.is_playing = False
            self.btn_play.config(text="Auto Play")

    def play_loop(self):
        if self.is_playing and self.current_step < len(self.history) - 1:
            self.next_step()
            self.root.after(300, self.play_loop) 
        else:
            self.is_playing = False
            self.btn_play.config(text="Auto Play")

if __name__ == "__main__":
    root = tk.Tk()
    app = BinairoGUI(root)
    root.mainloop()