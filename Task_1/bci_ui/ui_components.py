import math, random
from config import *

class CrowdDots:
    """Smoothly moving, colorful dots that drift toward gaze direction."""
    def __init__(self, canvas, cx, cy, radius, count):
        self.canvas = canvas
        self.cx, self.cy, self.radius = cx, cy, radius
        self.dots = []
        self.velocities = []
        self.positions = []

        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            r = random.uniform(0, radius * 0.8)
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            color = random.choice(DOT_COLORS)
            dot = canvas.create_oval(
                x - DOT_RADIUS, y - DOT_RADIUS, x + DOT_RADIUS, y + DOT_RADIUS,
                fill=color, outline=""
            )
            self.dots.append(dot)
            self.positions.append([x, y])
            self.velocities.append([random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5)])

    def update(self, target_x, target_y):
        """Update dots and compute coherence (0–1)."""
# Compute direction toward target or relax to center
        dx = target_x - self.cx
        dy = target_y - self.cy
        dist = math.hypot(dx, dy)

        # If cursor is close to center (no box focus) → gentle pull to center
        if dist < 120:  # within resting zone radius
            direction = (
                (self.cx - target_x) / (self.radius * 2),
                (self.cy - target_y) / (self.radius * 2)
            )
        else:
            dx /= dist
            dy /= dist
            direction = (dx, dy)


        avg_dir_x, avg_dir_y = 0, 0
        total_speed = 0

        for i, dot in enumerate(self.dots):
            vx, vy = self.velocities[i]
            px, py = self.positions[i]

            # Random jitter
            vx += random.uniform(-0.08, 0.08)
            vy += random.uniform(-0.08, 0.08)

            # Directional drift (faster than before)
            vx += direction[0] * 0.24
            vy += direction[1] * 0.24

            # Damping for smoothness
            vx *= 0.94
            vy *= 0.94

            # Update position
            px += vx
            py += vy

            # Soft boundary correction
            dx_c, dy_c = px - self.cx, py - self.cy
            dist_c = math.hypot(dx_c, dy_c)
            if dist_c > self.radius * 0.9:
                pull_strength = (dist_c - self.radius * 0.9) / (self.radius * 0.1)
                vx -= (dx_c / dist_c) * pull_strength * 0.5
                vy -= (dy_c / dist_c) * pull_strength * 0.5

            # Save state
            self.positions[i] = [px, py]
            self.velocities[i] = [vx, vy]

            self.canvas.coords(dot,
                px - DOT_RADIUS, py - DOT_RADIUS,
                px + DOT_RADIUS, py + DOT_RADIUS
            )

            avg_dir_x += vx
            avg_dir_y += vy
            total_speed += math.hypot(vx, vy)

        # Calculate coherence (0–1)
        if total_speed > 0:
            coherence = math.hypot(avg_dir_x, avg_dir_y) / (total_speed + 1e-6)
        else:
            coherence = 0.0

        return max(0.0, min(1.0, coherence))


class StimulusBox:
    """Stimulus box with label and progress bar."""
    def __init__(self, canvas, label, dx, dy):
        self.canvas = canvas
        self.label = label
        self.cx = CENTER_X + dx
        self.cy = CENTER_Y + dy
        self.width = BOX_WIDTH
        self.height = BOX_HEIGHT
        self.progress = 0
        self.state = "inactive"

        # Rectangle
        self.rect = canvas.create_rectangle(
            self.cx - self.width//2, self.cy - self.height//2,
            self.cx + self.width//2, self.cy + self.height//2,
            outline=COLOR_BOX_INACTIVE, width=2
        )
        # Label
        self.text = canvas.create_text(self.cx, self.cy, text=str(label),
                                       fill="white", font=("Arial", 18, "bold"))
        # Progress bar
        self.bar_bg = canvas.create_rectangle(
            self.cx - self.width//2 - 15, self.cy - self.height//2,
            self.cx - self.width//2 - 5, self.cy + self.height//2,
            fill=COLOR_PROGRESS_BG, outline=""
        )
        self.bar_fill = canvas.create_rectangle(
            self.cx - self.width//2 - 15, self.cy + self.height//2,
            self.cx - self.width//2 - 5, self.cy + self.height//2,
            fill=COLOR_PROGRESS_FILL, outline=""
        )

    def update(self, coherence, active=False, neuro=False):
        """Progress tied to dot coherence."""
        if neuro:
            outline_color = COLOR_BOX_NEURO
        elif active:
            outline_color = COLOR_BOX_GAZE
            self.progress = min(100, self.progress + PROGRESS_SPEED * coherence * 2)
        else:
            outline_color = COLOR_BOX_INACTIVE
            self.progress = max(0, self.progress - PROGRESS_DECAY)

        self.canvas.itemconfig(self.rect, outline=outline_color)

        # Progress bar height
        bar_height = self.height * (self.progress / 100)
        self.canvas.coords(
            self.bar_fill,
            self.cx - self.width//2 - 15,
            self.cy + self.height//2 - bar_height,
            self.cx - self.width//2 - 5,
            self.cy + self.height//2
        )
