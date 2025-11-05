import math
from config import *
from ui_components import CrowdDots, StimulusBox

class BCIInterface:
    def __init__(self, root, canvas):
        self.root = root
        self.canvas = canvas

        # Circle outline
        self.canvas.create_oval(
            CENTER_X - CIRCLE_RADIUS, CENTER_Y - CIRCLE_RADIUS,
            CENTER_X + CIRCLE_RADIUS, CENTER_Y + CIRCLE_RADIUS,
            outline=COLOR_CIRCLE_OUTLINE, width=2
        )

        # Dots (now return coherence)
        self.dots = CrowdDots(canvas, CENTER_X, CENTER_Y, CIRCLE_RADIUS, DOT_COUNT)

        # Stimulus boxes
        self.boxes = [StimulusBox(canvas, i, *BOX_POSITIONS[i]) for i in BOX_POSITIONS]

        # Inputs
        self.mouse_x, self.mouse_y = CENTER_X, CENTER_Y
        self.neuro_active_box = None

        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.root.bind_all("<space>", self.on_neuro_trigger)

        self.animate()

    def on_mouse_move(self, event):
        self.mouse_x, self.mouse_y = event.x, event.y

    def on_neuro_trigger(self, event):
        self.neuro_active_box = self.get_closest_box()

    def get_closest_box(self):
        """Return the closest box, but none if cursor is near center."""
        dx_c = self.mouse_x - CENTER_X
        dy_c = self.mouse_y - CENTER_Y
        dist_center = math.hypot(dx_c, dy_c)

        # Neutral zone: no active box if cursor is near center
        if dist_center < CIRCLE_RADIUS * 0.8:
            return None

        # Otherwise pick closest box
        min_dist, target = float("inf"), None
        for box in self.boxes:
            dx, dy = self.mouse_x - box.cx, self.mouse_y - box.cy
            dist = math.hypot(dx, dy)
            if dist < min_dist:
                min_dist, target = dist, box
        return target

    def animate(self):
        # Update dots and get coherence (0–1)
        coherence = self.dots.update(self.mouse_x, self.mouse_y)

        active_box = self.get_closest_box()
        
        # If no active box, reset coherence to calm down progress bars
        if active_box is None:
            coherence = 0
            
        for box in self.boxes:
            neuro = (box == self.neuro_active_box)
            active = (box == active_box)
            box.update(coherence, active=active, neuro=neuro)

        self.root.after(UPDATE_INTERVAL, self.animate)