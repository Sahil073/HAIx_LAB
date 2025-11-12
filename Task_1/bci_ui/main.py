from logic_controller import *
from ui_components import *
def main():
    root = tk.Tk()
    root.title("Hybrid BCI Interface - Enhanced")
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    root.minsize(800, 600)
    
    # Set dark background
    root.configure(bg=COLOR_BG)
    
    canvas = tk.Canvas(root, bg=COLOR_BG, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    
    interface = BCIInterface(root, canvas)
    
    def on_configure(event):
        interface.update_layout(event.width, event.height)
    
    root.bind("<Configure>", on_configure)
    
    root.mainloop()

if __name__ == "__main__":
    main()