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
        self.home_positions = []  # Store initial positions for realignment

        # EEG electrode positions (normalized, will be scaled by radius)
        # Based on 10-20 system layout from the image
        electrode_positions = [
            # Top row
            (-0.17, -0.75), (0.17, -0.75),  # Fp1, Fp2
            # Second row  
            (-0.55, -0.45), (-0.28, -0.45), (0, -0.45), (0.28, -0.45), (0.55, -0.45),  # F7, F3, Fz, F4, F8
            # Middle row
            (-0.70, 0), (-0.35, 0), (0, 0), (0.35, 0), (0.70, 0),  # T3, C3, Cz, C4, T4
            # Fourth row
            (-0.55, 0.45), (-0.28, 0.45), (0, 0.45), (0.28, 0.45), (0.55, 0.45),  # T5, P3, Pz, P4, T6
            # Bottom row
            (-0.20, 0.70), (0.20, 0.70)  # O1, O2
        ]

        for norm_x, norm_y in electrode_positions:
            x = cx + norm_x * radius * 0.75
            y = cy + norm_y * radius * 0.75
            color = random.choice(DOT_COLORS)
            dot = canvas.create_oval(
                x - DOT_RADIUS, y - DOT_RADIUS, x + DOT_RADIUS, y + DOT_RADIUS,
                fill=color, outline=""
            )
            self.dots.append(dot)
            self.positions.append([x, y])
            self.home_positions.append([x, y])  # Save home position
            self.velocities.append([0, 0])

    def update(self, target_x, target_y):
        """Update dots and compute coherence (0–1)."""
        # Compute direction toward target or relax to center
        dx = target_x - self.cx
        dy = target_y - self.cy
        dist = math.hypot(dx, dy)

        # If cursor is close to center (no box focus) → return to home positions
        returning_home = dist < 120  # within resting zone radius
        
        if not returning_home:
            dx /= dist
            dy /= dist
            direction = (dx, dy)
        else:
            direction = None

        avg_dir_x, avg_dir_y = 0, 0
        total_speed = 0

        for i, dot in enumerate(self.dots):
            vx, vy = self.velocities[i]
            px, py = self.positions[i]
            home_x, home_y = self.home_positions[i]

            if returning_home:
                # Pull dots back to their home positions
                dx_home = home_x - px
                dy_home = home_y - py
                home_dist = math.hypot(dx_home, dy_home)
                
                if home_dist > 1:  # If not at home yet
                    vx += (dx_home / home_dist) * 0.3
                    vy += (dy_home / home_dist) * 0.3
                else:
                    # At home, reduce velocity
                    vx *= 0.8
                    vy *= 0.8
            else:
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

            # Soft boundary correction (only when not returning home)
            if not returning_home:
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
            fill="", outline="white", width=1
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