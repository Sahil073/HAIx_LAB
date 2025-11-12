import time
from config import * 
from ui_components import *
class BCIInterface:
    """Main BCI interface controller with improved hover logic."""
    
    def __init__(self, root, canvas):
        self.root = root
        self.canvas = canvas
        
        self.width = WINDOW_WIDTH
        self.height = WINDOW_HEIGHT
        self.center_x = CENTER_X
        self.center_y = CENTER_Y
        self.circle_radius = CIRCLE_RADIUS
        
        # Create background circle with gradient effect
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
        
        # Create boxes
        self.boxes = [StimulusBox(canvas, i, *BOX_POSITIONS[i]) for i in BOX_POSITIONS]
        
        # Input tracking
        self.mouse_x, self.mouse_y = self.center_x, self.center_y
        self.neuro_active_box = None
        
        # Hover state management
        self.active_box = None
        self.hover_start_time = None
        self.hover_threshold = HOVER_THRESHOLD
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
    
    def on_mouse_move(self, event):
        """Handle mouse movement."""
        self.mouse_x, self.mouse_y = event.x, event.y
    
    def on_neuro_trigger(self, event):
        """Handle spacebar (neuro trigger)."""
        self.neuro_active_box = self.get_closest_box()
    
    def get_closest_box(self):
        """Get the closest box to cursor, or None if in neutral zone."""
        dx_c = self.mouse_x - self.center_x
        dy_c = self.mouse_y - self.center_y
        dist_center = math.hypot(dx_c, dy_c)
        
        # Neutral zone in center
        if dist_center < self.circle_radius * 0.7:
            return None
        
        min_dist = float("inf")
        target = None
        
        for box in self.boxes:
            dx = self.mouse_x - box.cx
            dy = self.mouse_y - box.cy
            d = math.hypot(dx, dy)
            if d < min_dist:
                min_dist = d
                target = box
        
        return target
    
    def animate(self):
        """Main animation loop with improved hover logic."""
        now = time.time()
        dt = now - self.last_time
        self.last_time = now
        
        closest_box = self.get_closest_box()
        
        # Hover state machine
        if closest_box != self.active_box:
            # Changed to different box or None
            self.active_box = closest_box
            self.hover_start_time = now if closest_box else None
            self.is_hovering_long_enough = False
            self.lost_focus_time = now if not closest_box else None
        else:
            # Same box as before
            if self.active_box is not None and self.hover_start_time is not None:
                hover_duration = now - self.hover_start_time
                if hover_duration >= self.hover_threshold:
                    self.is_hovering_long_enough = True
                    self.lost_focus_time = None
            elif self.active_box is None:
                # In neutral zone
                if self.lost_focus_time is None:
                    self.lost_focus_time = now
        
        # Determine if dots should move
        should_move_dots = False
        
        if self.is_hovering_long_enough and self.active_box is not None:
            should_move_dots = True
        elif self.lost_focus_time is not None:
            # Check if return delay has passed
            if (now - self.lost_focus_time) < self.return_delay:
                should_move_dots = True  # Keep current position briefly
            else:
                should_move_dots = False  # Return home
        
        # Update dot targets
        if should_move_dots and self.active_box is not None:
            self.dots.set_target(self.mouse_x, self.mouse_y, True)
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