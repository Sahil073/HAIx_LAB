# ===============================================
# FILE: main.py
# BCI Interface Application - Main Entry Point
# ===============================================

import tkinter as tk
from tkinter import ttk
from config import *
from controller import BCIController


class BCIApplication:
    """
    Main application class.
    Creates UI, manages controller, and handles themes.
    """
    
    def __init__(self):
        # Create main windowi
        self.root = tk.Tk()
        self.root.title("BCI Interface - Eye Tracking & Calibration System")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT + CONTROL_PANEL_HEIGHT}")
        self.root.minsize(MIN_WIDTH, MIN_HEIGHT)
        self.root.configure(bg=get_color('bg'))
        
        # Configure grid weights for responsive layout
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Theme management
        self.current_theme_name = THEME_LIGHT
        
        # Create UI
        self._create_control_panel()
        self._create_canvas()
        
        # Create controller
        self.controller = BCIController(
            self.canvas,
            status_callback=self._update_status
        )
        
        # Bind events
        self._bind_events()
        
        # Start animation
        self.controller.start_animation()
        self._animate()
        
        # Set initial phase
        self.controller.set_phase(PHASE_TESTING)
        
        # Initial theme setup
        self._apply_theme(LIGHT_THEME)
    
    # ==================== UI Creation ====================
    
    def _create_control_panel(self):
        """Create top control panel with all controls in one row."""
        panel = tk.Frame(
            self.root,
            bg=get_color('control_bg'),
            height=CONTROL_PANEL_HEIGHT
        )
        panel.grid(row=0, column=0, sticky="ew")
        panel.grid_propagate(False)
        
        # Configure ttk style
        self._configure_ttk_style()
        
        # Main horizontal container
        container = tk.Frame(panel, bg=get_color('control_bg'))
        container.pack(side="top", fill="x", padx=CONTROL_PADDING, pady=10)
        
        # Theme buttons (Left side)
        theme_frame = tk.Frame(container, bg=get_color('control_bg'))
        theme_frame.pack(side="left", padx=(0, 20))
        
        self.light_btn = tk.Button(
            theme_frame,
            text="☀",
            command=lambda: self._switch_theme(THEME_LIGHT),
            bg="#FFFFFF",
            fg="#2D3142",
            font=("Segoe UI", 12),
            relief="flat",
            width=3,
            height=1,
            cursor="hand2",
            borderwidth=2
        )
        self.light_btn.pack(side="left", padx=2)
        
        self.dark_btn = tk.Button(
            theme_frame,
            text="🌙",
            command=lambda: self._switch_theme(THEME_DARK),
            bg="#2D3748",
            fg="#E2E8F0",
            font=("Segoe UI", 12),
            relief="flat",
            width=3,
            height=1,
            cursor="hand2",
            borderwidth=2
        )
        self.dark_btn.pack(side="left", padx=2)
        
        self.colorblind_btn = tk.Button(
            theme_frame,
            text="👁",
            command=lambda: self._switch_theme(THEME_COLORBLIND),
            bg="#E0E0E0",
            fg="#1A1A1A",
            font=("Segoe UI", 12),
            relief="flat",
            width=3,
            height=1,
            cursor="hand2",
            borderwidth=2
        )
        self.colorblind_btn.pack(side="left", padx=2)
        
        # Separator
        sep1 = tk.Frame(container, bg=get_color('text_secondary'), width=2)
        sep1.pack(side="left", fill="y", padx=10)
        
        # Input Mode
        self.input_mode_var = self._create_dropdown(
            container, "Input:", INPUT_MODE_MOUSE, INPUT_MODES,
            self._on_input_mode_change, width=12
        )
        
        # Phase
        self.phase_var = self._create_dropdown(
            container, "Phase:", PHASE_TESTING, PHASES,
            self._on_phase_change, width=12
        )
        
        # Focus Time
        focus_values = [f"{t}s" for t in FOCUS_TIME_OPTIONS]
        self.focus_time_var = self._create_dropdown(
            container, "Focus:", f"{DEFAULT_FOCUS_TIME}s", focus_values,
            self._on_focus_time_change, width=6
        )
        
        # Gap Time
        gap_values = [f"{t}s" for t in GAP_TIME_OPTIONS]
        self.gap_time_var = self._create_dropdown(
            container, "Gap:", f"{DEFAULT_GAP_TIME}s", gap_values,
            self._on_gap_time_change, width=6
        )
        
        # Calibration Rounds
        rounds_values = [str(r) for r in CALIBRATION_ROUNDS_OPTIONS]
        self.calibration_rounds_var = self._create_dropdown(
            container, "Rounds:", str(DEFAULT_CALIBRATION_ROUNDS),
            rounds_values, self._on_calibration_rounds_change, width=6
        )
        
        # Separator
        sep2 = tk.Frame(container, bg=get_color('text_secondary'), width=2)
        sep2.pack(side="left", fill="y", padx=10)
        
        # Start/Stop Calibration Button
        self.start_button = tk.Button(
            container,
            text="▶ Start",
            command=self._on_start_calibration,
            bg="#4CAF50",
            fg="white",
            font=BUTTON_FONT,
            relief="flat",
            padx=15,
            pady=5,
            cursor="hand2"
        )
        self.start_button.pack(side="left", padx=(0, 15))
        self.start_button.pack_forget()  # Hidden initially
        
        # Status Label (Right side, expands)
        self.status_label = tk.Label(
            container,
            text="Status: Ready",
            bg=get_color('control_bg'),
            fg=get_color('text_primary'),
            font=STATUS_FONT,
            anchor="w"
        )
        self.status_label.pack(side="left", fill="x", expand=True)
    
    def _configure_ttk_style(self):
        """Configure ttk combobox style."""
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            'TCombobox',
            fieldbackground=get_color('dropdown_bg'),
            background=get_color('dropdown_bg'),
            foreground=get_color('text_primary'),
            arrowcolor=get_color('text_primary'),
            borderwidth=1,
            relief="solid"
        )
        style.map('TCombobox',
            fieldbackground=[('readonly', get_color('dropdown_bg'))],
            selectbackground=[('readonly', get_color('dropdown_hover'))],
            selectforeground=[('readonly', get_color('text_primary'))]
        )
    
    def _create_dropdown(self, parent, label_text, default_value, values, callback, width=10):
        """Helper to create compact labeled dropdown."""
        # Label
        label = tk.Label(
            parent,
            text=label_text,
            bg=get_color('control_bg'),
            fg=get_color('text_primary'),
            font=LABEL_FONT
        )
        label.pack(side="left", padx=(5, 3))
        
        # Dropdown
        var = tk.StringVar(value=default_value)
        dropdown = ttk.Combobox(
            parent,
            textvariable=var,
            values=values,
            state="readonly",
            width=width,
            font=DROPDOWN_FONT
        )
        dropdown.pack(side="left", padx=(0, 10))
        dropdown.bind("<<ComboboxSelected>>", callback)
        
        return var
    
    def _create_canvas(self):
        """Create main canvas for visualization."""
        self.canvas = tk.Canvas(
            self.root,
            bg=get_color('bg'),
            highlightthickness=0
        )
        self.canvas.grid(row=1, column=0, sticky="nsew")
    
    # ==================== Event Handlers ====================
    
    def _bind_events(self):
        """Bind window and input events."""
        self.canvas.bind("<Motion>", self._on_mouse_move)
        self.canvas.bind("<Configure>", self._on_canvas_resize)
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _on_mouse_move(self, event):
        """Handle mouse movement."""
        self.controller.on_mouse_move(event.x, event.y)
    
    def _on_canvas_resize(self, event):
        """Handle canvas resize."""
        if event.widget == self.canvas:
            self.controller.resize(event.width, event.height)
    
    def _on_input_mode_change(self, event):
        """Handle input mode change."""
        mode = self.input_mode_var.get()
        self.controller.set_input_mode(mode)
    
    def _on_focus_time_change(self, event):
        """Handle focus time change."""
        time_str = self.focus_time_var.get().replace('s', '')
        try:
            time_val = float(time_str)
            self.controller.set_focus_time(time_val)
        except ValueError:
            pass
    
    def _on_gap_time_change(self, event):
        """Handle gap time change."""
        time_str = self.gap_time_var.get().replace('s', '')
        try:
            time_val = float(time_str)
            self.controller.set_gap_time(time_val)
        except ValueError:
            pass
    
    def _on_calibration_rounds_change(self, event):
        """Handle calibration rounds change."""
        rounds_str = self.calibration_rounds_var.get()
        try:
            rounds_val = int(rounds_str)
            self.controller.set_calibration_rounds(rounds_val)
        except ValueError:
            pass
    
    def _on_phase_change(self, event):
        """Handle phase change."""
        phase = self.phase_var.get()
        self.controller.set_phase(phase)
        
        # Show/hide start button based on phase
        if phase == PHASE_CALIBRATION:
            self.start_button.pack(side="left", padx=(0, 15), before=self.status_label)
        else:
            self.start_button.pack_forget()
    
    def _on_start_calibration(self):
        """Handle start/stop calibration button."""
        if self.controller.calibration_active:
            self.controller.stop_calibration()
            self.start_button.config(text="▶ Start", bg="#4CAF50")
        else:
            if self.controller.start_calibration():
                self.start_button.config(text="■ Stop", bg="#f44336")
    
    def _on_closing(self):
        """Handle window close."""
        self.controller.cleanup()
        self.root.destroy()
    
    # ==================== Theme Management ====================
    
    def _switch_theme(self, theme_name):
        """Switch to a different theme."""
        self.current_theme_name = theme_name
        
        if theme_name == THEME_LIGHT:
            theme = LIGHT_THEME
        elif theme_name == THEME_DARK:
            theme = DARK_THEME
        elif theme_name == THEME_COLORBLIND:
            theme = COLORBLIND_THEME
        else:
            theme = LIGHT_THEME
        
        self._apply_theme(theme)
        
        # Update button highlights
        self._update_theme_buttons()
    
    def _apply_theme(self, theme):
        """Apply theme colors to all components."""
        global CURRENT_THEME
        CURRENT_THEME = theme
        
        # Update root and canvas background
        self.root.config(bg=theme['bg'])
        self.canvas.config(bg=theme['bg'])
        
        # Update all frames recursively
        for widget in self.root.winfo_children():
            self._update_widget_theme(widget, theme)
        
        # Update ttk style
        self._configure_ttk_style()
        
        # Update controller components
        self.controller.update_theme()
    
    def _update_frame_colors(self, frame, theme):
        """Recursively update frame and child widget colors."""
        try:
            frame.config(bg=theme['control_bg'])
        except:
            pass
        
        for child in frame.winfo_children():
            if isinstance(child, tk.Frame):
                self._update_frame_colors(child, theme)
            elif isinstance(child, tk.Label):
                try:
                    child.config(
                        bg=theme['control_bg'],
                        fg=theme['text_primary']
                    )
                except:
                    pass
    
    def _update_widget_theme(self, widget, theme):
        """Recursively update all widgets with theme colors."""
        # Update the widget itself
        widget_type = widget.winfo_class()
        
        try:
            if widget_type in ('Frame', 'Labelframe'):
                widget.config(bg=theme['control_bg'])
            elif widget_type == 'Label':
                # Don't update theme buttons
                if widget not in [self.light_btn, self.dark_btn, self.colorblind_btn]:
                    widget.config(
                        bg=theme['control_bg'],
                        fg=theme['text_primary']
                    )
            elif widget_type == 'Button':
                # Only update start button, not theme buttons
                if widget == self.start_button:
                    # Start button keeps its own colors
                    pass
        except:
            pass
        
        # Recursively update children
        try:
            for child in widget.winfo_children():
                self._update_widget_theme(child, theme)
        except:
            pass
    
    def _update_theme_buttons(self):
        """Update theme button appearance to show active theme."""
        # Reset all borders
        self.light_btn.config(relief="flat", borderwidth=1)
        self.dark_btn.config(relief="flat", borderwidth=1)
        self.colorblind_btn.config(relief="flat", borderwidth=1)
        
        # Highlight active theme
        if self.current_theme_name == THEME_LIGHT:
            self.light_btn.config(relief="solid", borderwidth=3)
        elif self.current_theme_name == THEME_DARK:
            self.dark_btn.config(relief="solid", borderwidth=3)
        elif self.current_theme_name == THEME_COLORBLIND:
            self.colorblind_btn.config(relief="solid", borderwidth=3)
    
    # ==================== Status Updates ====================
    
    def _update_status(self, message, level="info"):
        """Update status label with color coding."""
        colors = {
            "info": "#2196F3",
            "success": "#4CAF50",
            "error": "#f44336",
            "warning": "#FF9800"
        }
        
        self.status_label.config(
            text=f"Status: {message}",
            fg=colors.get(level, get_color('text_primary'))
        )
    
    # ==================== Animation ====================
    
    def _animate(self):
        """Animation loop."""
        self.controller.update()
        self.root.after(FRAME_TIME, self._animate)
    
    # ==================== Run Application ====================
    
    def run(self):
        """Start application main loop."""
        self.root.mainloop()


# ==================== Entry Point ====================

def main():
    """Application entry point."""
    print("=" * 50)
    print("BCI Interface - Eye Tracking & Calibration System")
    print("=" * 50)
    print("Starting application...")
    
    app = BCIApplication()
    app.run()


if __name__ == "__main__":
    main()