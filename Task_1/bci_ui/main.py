import tkinter as tk
from config import *
from logic_controller import BCIInterface

def main():
    root = tk.Tk()
    root.title("Hybrid BCI Interface - Version 3 (Crowd Motion)")

    canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT,
                       bg=COLOR_BG, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    BCIInterface(root, canvas)
    root.mainloop()

if __name__ == "__main__":
    main()
