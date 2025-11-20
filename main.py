import tkinter as tk
from tkinter import ttk
from logic_controller import BCIInterface
from config import *

def main():
    root = tk.Tk()
    root.title("Hybrid BCI Interface - Enhanced with Tobii")
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT + CONTROL_PANEL_HEIGHT}")
    root.minsize(800, 650)
    
    # Dark background
    root.configure(bg=COLOR_BG)
    
    # Control panel
    control_frame = tk.Frame(root, bg=CONTROL_PANEL_BG, height=CONTROL_PANEL_HEIGHT)
    control_frame.pack(side="top", fill="x")
    control_frame.pack_propagate(False)
    
    # Style dropdowns
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TCombobox',
                    fieldbackground=DROPDOWN_BG,
                    background=DROPDOWN_BG,
                    foreground=DROPDOWN_FG,
                    arrowcolor=DROPDOWN_FG,
                    borderwidth=1)
    style.map('TCombobox',
              fieldbackground=[('readonly', DROPDOWN_BG)],
              selectbackground=[('readonly', DROPDOWN_BG)],
              selectforeground=[('readonly', DROPDOWN_FG)])
    
    # Input mode dropdown
    mode_label = tk.Label(control_frame, text="Input Mode:",
                          bg=CONTROL_PANEL_BG, fg=DROPDOWN_FG,
                          font=("Helvetica", 10))
    mode_label.pack(side="left", padx=(20,5), pady=10)
    
    mode_var = tk.StringVar(value=INPUT_MODE_MOUSE)
    mode_dropdown = ttk.Combobox(control_frame, textvariable=mode_var,
                                 values=INPUT_MODES, state="readonly",
                                 width=20, font=("Helvetica", 9))
    mode_dropdown.pack(side="left", padx=5, pady=10)
    
    # Hover threshold dropdown
    threshold_label = tk.Label(control_frame, text="Hover Time (sec):",
                               bg=CONTROL_PANEL_BG, fg=DROPDOWN_FG,
                               font=("Helvetica", 10))
    threshold_label.pack(side="left", padx=(30,5), pady=10)
    
    threshold_var = tk.StringVar(value=str(DEFAULT_HOVER_THRESHOLD))
    threshold_dropdown = ttk.Combobox(control_frame, textvariable=threshold_var,
                                      values=[str(t) for t in HOVER_THRESHOLD_OPTIONS],
                                      state="readonly", width=8,
                                      font=("Helvetica", 9))
    threshold_dropdown.pack(side="left", padx=5, pady=10)
    
    # Status label
    status_label = tk.Label(control_frame, text="Status: Ready",
                            bg=CONTROL_PANEL_BG, fg="#00FF88",
                            font=("Helvetica", 10))
    status_label.pack(side="left", padx=(30,20), pady=10)
    
    # Main canvas
    canvas = tk.Canvas(root, bg=COLOR_BG, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    
    # Create BCI interface
    interface = BCIInterface(root, canvas, status_label)
    
    # Mode change callback
    def on_mode_change(event):
        selected_mode = mode_var.get()
        interface.set_input_mode(selected_mode)
        
        if selected_mode == INPUT_MODE_TOBII:
            if interface.tobii_handler.is_available():
                status_label.config(text="Status: Tobii Active", fg="#00FF88")
            else:
                status_label.config(text="Status: Tobii Unavailable", fg="#FF6B6B")
                mode_var.set(INPUT_MODE_MOUSE)
                interface.set_input_mode(INPUT_MODE_MOUSE)
        else:
            status_label.config(text="Status: Mouse Active", fg="#00D9FF")
    
    # Threshold change callback
    def on_threshold_change(event):
        try:
            new_threshold = float(threshold_var.get())
            interface.set_hover_threshold(new_threshold)
            print(f"Hover threshold changed to {new_threshold} seconds")
        except ValueError:
            print("Invalid threshold value")
    
    mode_dropdown.bind("<<ComboboxSelected>>", on_mode_change)
    threshold_dropdown.bind("<<ComboboxSelected>>", on_threshold_change)
    
    # Handle canvas resize
    def on_configure(event):
        if event.widget == canvas:
            interface.update_layout(event.width, event.height)
    
    canvas.bind("<Configure>", on_configure)
    
    # Cleanup on close
    def on_closing():
        interface.cleanup()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Initialize mode
    on_mode_change(None)
    
    root.mainloop()


if __name__ == "__main__":
    main()
