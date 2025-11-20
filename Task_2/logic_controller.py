# ================= bci_interface.py ==================
import time
import math
from config import *
from ui_components import *
from tobii_input_handler import TobiiInputHandler

class BCIInterface:
    """Main BCI interface controller with Tobii eye tracking support."""
    
    def __init__(self, root, canvas, status_label=None):
        self.root = root
        self.canvas = canvas
        self.status_label = status_label
        
        # Window and circle
        self.width = WINDOW_WIDTH
        self.height = WINDOW_HEIGHT
        self.center_x = CENTER_X
        self.center_y = CENTER_Y
        self.circle_radius = CIRCLE_RADIUS
        
        # Create background circle with glow
        self.circle_bg = self.canvas.create_oval(
            self.center_x - self.circle_radius, self.center_y - self.circle_radius,
            self.center_x + self.circle_radius, self.center_y + self.circle_radius,
            fill="", outline=COLOR_CIRCLE_GLOW, width=1
        )
        self.circle_outline = self.canvas.create_oval(
            self.center_x - self.circle_radius, self.center_y - self.circle_radius,
            self.center_x + self.circle_radius, self.center_y + self.circle_radius,
            outline=COLOR_CIRCLE_OUTLINE, width=3
        )
        
        # Create dots
        self.dots = CrowdDots(canvas, self.center_x, self.center_y, self.circle_radius, DOT_COUNT)
        
        # Create stimulus boxes
        self.boxes = [StimulusBox(canvas, i, *BOX_POSITIONS[i]) for i in BOX_POSITIONS]
        
        # Tobii handler
        self.tobii_handler = TobiiInputHandler()
        self.current_input_mode = INPUT_MODE_MOUSE
        
        # Input tracking
        self.mouse_x, self.mouse_y = self.center_x, self.center_y
        self.gaze_x, self.gaze_y = self.center_x, self.center_y
        self.neuro_active_box = None
        
        # Hover state
        self.active_box = None
        self.hover_start_time = None
        self.hover_threshold = DEFAULT_HOVER_THRESHOLD
        self.is_hovering_long_enough = False
        self.lost_focus_time = None
        self.return_delay = RETURN_DELAY
        
        # Timing
        self.last_time = time.time()
        
        # Bindings
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.root.bind_all("<space>", self.on_neuro_trigger)
        
        # Start animation
        self.animate()
    
    # ---------------- Input Modes ----------------
    def set_input_mode(self, mode):
        """Switch between mouse and Tobii input modes."""
        if mode == INPUT_MODE_TOBII:
            if self.tobii_handler.is_available():
                self.current_input_mode = INPUT_MODE_TOBII
                self.tobii_handler.start_tracking(self.on_gaze_update)
                print("Switched to Tobii eye tracking mode")
            else:
                print("ERROR: Tobii eye tracker not available. Staying in mouse mode.")
                self.current_input_mode = INPUT_MODE_MOUSE
        else:
            self.current_input_mode = INPUT_MODE_MOUSE
            self.tobii_handler.stop_tracking()
            print("Switched to mouse mode")
    
    def set_hover_threshold(self, threshold):
        """Update hover threshold time."""
        self.hover_threshold = threshold
    
    def on_gaze_update(self, norm_x, norm_y):
        """Callback for Tobii gaze data (normalized 0-1 coordinates)."""
        self.gaze_x = int(norm_x * self.width)
        self.gaze_y = int(norm_y * self.height)
    
    def get_current_position(self):
        """Get current cursor position based on input mode."""
        if self.current_input_mode == INPUT_MODE_TOBII:
            return self.gaze_x, self.gaze_y
        else:
            return self.mouse_x, self.mouse_y
    
    # ---------------- Layout Updates ----------------
    def update_layout(self, new_width, new_height):
        """Handle window resize."""
        if new_width <= 0 or new_height <= 0:
            return
        
        self.width = new_width
        self.height = new_height
        self.center_x = new_width // 2
        self.center_y = new_height // 2
        
        scale = min(new_width / BASE_WIDTH, new_height / BASE_HEIGHT)
        self.circle_radius = max(60, int(CIRCLE_RADIUS * scale))
        
        # Update circles
        self.canvas.coords(self.circle_bg,
                          self.center_x - self.circle_radius,
                          self.center_y - self.circle_radius,
                          self.center_x + self.circle_radius,
                          self.center_y + self.circle_radius)
        self.canvas.coords(self.circle_outline,
                          self.center_x - self.circle_radius,
                          self.center_y - self.circle_radius,
                          self.center_x + self.circle_radius,
                          self.center_y + self.circle_radius)
        
        # Update dots
        self.dots.recenter(self.center_x, self.center_y, self.circle_radius)
        
        # Update boxes
        scale_x = new_width / BASE_WIDTH
        scale_y = new_height / BASE_HEIGHT
        for i, box in enumerate(self.boxes, start=1):
            dx, dy = BOX_POSITIONS[i]
            box.update_position(
                self.center_x + int(dx * scale_x),
                self.center_y + int(dy * scale_y)
            )
    
    # ---------------- Event Handlers ----------------
    def on_mouse_move(self, event):
        self.mouse_x, self.mouse_y = event.x, event.y
    
    def on_neuro_trigger(self, event):
        self.neuro_active_box = self.get_closest_box()
    
    # ---------------- Box Detection ----------------
    def get_closest_box(self):
        """Return closest box to cursor, or None if in neutral zone."""
        cursor_x, cursor_y = self.get_current_position()
        dx_c = cursor_x - self.center_x
        dy_c = cursor_y - self.center_y
        dist_center = math.hypot(dx_c, dy_c)
        
        if dist_center < self.circle_radius * 0.7:
            return None
        
        min_dist = float("inf")
        target = None
        for box in self.boxes:
            dx = cursor_x - box.cx
            dy = cursor_y - box.cy
            d = math.hypot(dx, dy)
            if d < min_dist:
                min_dist = d
                target = box
        return target
    
    # ---------------- Animation Loop ----------------
    def animate(self):
        now = time.time()
        dt = now - self.last_time
        self.last_time = now
        
        cursor_x, cursor_y = self.get_current_position()
        closest_box = self.get_closest_box()
        
        # Hover state management
        if closest_box != self.active_box:
            self.active_box = closest_box
            self.hover_start_time = now if closest_box else None
            self.is_hovering_long_enough = False
            self.lost_focus_time = now if not closest_box else None
        else:
            if self.active_box and self.hover_start_time:
                if now - self.hover_start_time >= self.hover_threshold:
                    self.is_hovering_long_enough = True
                    self.lost_focus_time = None
            elif self.active_box is None:
                if self.lost_focus_time is None:
                    self.lost_focus_time = now
        
        # Determine if dots should move
        should_move_dots = False
        if self.is_hovering_long_enough and self.active_box:
            should_move_dots = True
        elif self.lost_focus_time:
            should_move_dots = (now - self.lost_focus_time) < self.return_delay
        
        # Update dot targets
        if should_move_dots and self.active_box:
            self.dots.set_target(cursor_x, cursor_y, True)
        else:
            self.dots.set_target(self.center_x, self.center_y, False)
        
        # Update dots
        coherence = self.dots.update(dt)
        
        # Update boxes
        for box in self.boxes:
            is_active = (box == closest_box)
            is_neuro = (box == self.neuro_active_box)
            box.update(coherence, active=is_active, neuro=is_neuro,
                       dt=dt, hover_threshold=self.hover_threshold)
        
        # Schedule next frame
        self.root.after(UPDATE_INTERVAL, self.animate)
    
    # ---------------- Cleanup ----------------
    def cleanup(self):
        self.tobii_handler.stop_tracking()
        print("Cleaned up BCI interface")
