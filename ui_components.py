# ===============================================
# FILE: ui_components.py
# Save this as 'ui_components.py' (replace your existing file)
# ===============================================

import math
import random
import tkinter as tk
from config import *  # Import all config variables


class CrowdDots:
    """EEG 10-20 electrode position dots with smooth motion."""
    
    def __init__(self, canvas, cx, cy, radius, count):
        self.canvas = canvas
        self.cx = cx
        self.cy = cy
        self.radius = radius
        
        # EEG 10-20 electrode positions (normalized coordinates)
        self.electrode_positions = [
            # Front row
            (-0.22, -0.82),  # Fp1
            (0.22, -0.82),   # Fp2
            # Second row
            (-0.65, -0.50),  # F7
            (-0.35, -0.50),  # F3
            (0.0, -0.50),    # Fz
            (0.35, -0.50),   # F4
            (0.65, -0.50),   # F8
            # Central row
            (-0.85, 0.0),    # T3
            (-0.42, 0.0),    # C3
            (0.0, 0.0),      # Cz
            (0.42, 0.0),     # C4
            (0.85, 0.0),     # T4
            # Fourth row
            (-0.65, 0.50),   # T5
            (-0.35, 0.50),   # P3
            (0.0, 0.50),     # Pz
            (0.35, 0.50),    # P4
            (0.65, 0.50),    # T6
            # Back row
            (-0.22, 0.78),   # O1
            (0.22, 0.78),    # O2
        ]
        
        self.count = min(count, len(self.electrode_positions))
        self.dots = []
        self.positions = []
        self.home_positions = []
        self.velocities = []
        self.target_positions = []
        
        # Create dots with glow effect
        for i in range(self.count):
            norm_x, norm_y = self.electrode_positions[i]
            x = cx + norm_x * radius * 0.85
            y = cy + norm_y * radius * 0.85
            
            color = DOT_COLORS[i % len(DOT_COLORS)]
            
            # Outer glow
            glow = canvas.create_oval(
                x - DOT_RADIUS * 2, y - DOT_RADIUS * 2,
                x + DOT_RADIUS * 2, y + DOT_RADIUS * 2,
                fill="", outline=color, width=1, state="hidden"
            )
            
            # Main dot
            dot = canvas.create_oval(
                x - DOT_RADIUS, y - DOT_RADIUS,
                x + DOT_RADIUS, y + DOT_RADIUS,
                fill=color, outline=COLOR_DOT_GLOW, width=1
            )
            
            self.dots.append((dot, glow))
            self.positions.append([x, y])
            self.home_positions.append([x, y])
            self.target_positions.append([x, y])
            self.velocities.append([0.0, 0.0])
    
    def recenter(self, cx, cy, radius):
        """Update center and radius, recompute home positions."""
        self.cx = cx
        self.cy = cy
        self.radius = radius
        
        for i in range(self.count):
            norm_x, norm_y = self.electrode_positions[i]
            hx = cx + norm_x * radius * 0.85
            hy = cy + norm_y * radius * 0.85
            self.home_positions[i] = [hx, hy]
            
            # Snap if too far away
            px, py = self.positions[i]
            if math.hypot(px - hx, py - hy) > radius * 2:
                self.positions[i] = [hx, hy]
                self.target_positions[i] = [hx, hy]
                self.velocities[i] = [0.0, 0.0]
                dot, glow = self.dots[i]
                self._update_dot_visual(i)
    
    def set_target(self, target_x, target_y, is_moving):
        """Set target position for dots - all dots move together as unified brain activity."""
        if is_moving:
            # Calculate direction from center
            dx = target_x - self.cx
            dy = target_y - self.cy
            dist = math.hypot(dx, dy)
            
            if dist > 10:
                # Normalize direction
                dx /= dist
                dy /= dist
                
                # ALL dots move together in the same direction
                # This simulates unified brain activity
                for i in range(self.count):
                    hx, hy = self.home_positions[i]
                    
                    # Each dot moves from its home position toward the target direction
                    # The push distance is consistent for all dots
                    push_dist = self.radius * 0.5  # How far dots travel from home
                    
                    # All dots shift in the same direction, maintaining their relative positions
                    tx = hx + dx * push_dist
                    ty = hy + dy * push_dist
                    
                    self.target_positions[i] = [tx, ty]
            else:
                # Return home
                for i in range(self.count):
                    self.target_positions[i] = list(self.home_positions[i])
        else:
            # Return home
            for i in range(self.count):
                self.target_positions[i] = list(self.home_positions[i])
    
    def update(self, dt=0.016):
        """Update dot positions with smooth spring physics."""
        avg_vx = 0.0
        avg_vy = 0.0
        total_speed = 0.0
        
        # Tuned physics parameters for smooth motion
        spring_strength = 8.0  # How strongly dots are pulled to target
        damping = 0.85  # Velocity damping (higher = more damping)
        max_speed = 300.0  # Maximum speed in pixels per second
        
        for i in range(self.count):
            px, py = self.positions[i]
            tx, ty = self.target_positions[i]
            vx, vy = self.velocities[i]
            
            # Spring force toward target
            dx = tx - px
            dy = ty - py
            dist = math.hypot(dx, dy)
            
            if dist > 0.5:
                # Spring acceleration
                ax = dx * spring_strength * dt
                ay = dy * spring_strength * dt
                
                vx += ax
                vy += ay
            else:
                # Very close to target, reduce velocity
                vx *= 0.5
                vy *= 0.5
            
            # Apply damping
            vx *= damping
            vy *= damping
            
            # Limit maximum speed
            speed = math.hypot(vx, vy)
            if speed > max_speed * dt:
                scale = (max_speed * dt) / speed
                vx *= scale
                vy *= scale
            
            # Update position
            px += vx
            py += vy
            
            # Keep within circle boundary (soft constraint)
            dx_c = px - self.cx
            dy_c = py - self.cy
            dist_c = math.hypot(dx_c, dy_c)
            
            if dist_c > self.radius * 0.95:
                # Push back gently
                scale = (self.radius * 0.95) / dist_c
                px = self.cx + dx_c * scale
                py = self.cy + dy_c * scale
                # Reduce velocity toward center
                vx *= 0.7
                vy *= 0.7
            
            self.positions[i] = [px, py]
            self.velocities[i] = [vx, vy]
            
            self._update_dot_visual(i)
            
            avg_vx += vx
            avg_vy += vy
            total_speed += speed
        
        # Calculate coherence
        coherence = (math.hypot(avg_vx, avg_vy) / (total_speed + 1e-6)) if total_speed > 0 else 0.0
        return max(0.0, min(1.0, coherence))
    
    def _update_dot_visual(self, i):
        """Update visual position of a dot."""
        px, py = self.positions[i]
        dot, glow = self.dots[i]
        
        self.canvas.coords(dot,
                          px - DOT_RADIUS, py - DOT_RADIUS,
                          px + DOT_RADIUS, py + DOT_RADIUS)
        self.canvas.coords(glow,
                          px - DOT_RADIUS * 2, py - DOT_RADIUS * 2,
                          px + DOT_RADIUS * 2, py + DOT_RADIUS * 2)


class StimulusBox:
    """Enhanced stimulus box with smooth animations."""
    
    def __init__(self, canvas, label, dx, dy):
        self.canvas = canvas
        self.label = label
        self.cx = CENTER_X + dx
        self.cy = CENTER_Y + dy
        self.width = BOX_WIDTH
        self.height = BOX_HEIGHT
        self.progress = 0.0
        self.glow_alpha = 0.0
        
        # Inner glow rectangle
        self.glow = canvas.create_rectangle(
            self.cx - self.width//2 - 4, self.cy - self.height//2 - 4,
            self.cx + self.width//2 + 4, self.cy + self.height//2 + 4,
            outline="", fill="", width=0, state="hidden"
        )
        
        # Main rectangle with rounded appearance
        self.rect = canvas.create_rectangle(
            self.cx - self.width//2, self.cy - self.height//2,
            self.cx + self.width//2, self.cy + self.height//2,
            outline=COLOR_BOX_INACTIVE, width=3, fill=""
        )
        
        # Label
        self.text = canvas.create_text(
            self.cx, self.cy,
            text=str(label),
            fill="#FFFFFF",
            font=("Helvetica", 20, "bold")
        )
        
        # Progress bar (left side, vertical)
        bar_width = 8
        bar_padding = 18
        
        self.bar_bg = canvas.create_rectangle(
            self.cx - self.width//2 - bar_padding - bar_width,
            self.cy - self.height//2,
            self.cx - self.width//2 - bar_padding,
            self.cy + self.height//2,
            fill=COLOR_PROGRESS_BG, outline="#3A4A5A", width=1
        )
        
        self.bar_fill = canvas.create_rectangle(
            self.cx - self.width//2 - bar_padding - bar_width,
            self.cy + self.height//2,
            self.cx - self.width//2 - bar_padding,
            self.cy + self.height//2,
            fill=COLOR_PROGRESS_FILL, outline=""
        )
    
    def update_position(self, cx, cy):
        """Update box position."""
        self.cx, self.cy = cx, cy
        bar_width = 8
        bar_padding = 18
        
        self.canvas.coords(self.glow,
                          self.cx - self.width//2 - 4, self.cy - self.height//2 - 4,
                          self.cx + self.width//2 + 4, self.cy + self.height//2 + 4)
        
        self.canvas.coords(self.rect,
                          self.cx - self.width//2, self.cy - self.height//2,
                          self.cx + self.width//2, self.cy + self.height//2)
        
        self.canvas.coords(self.text, self.cx, self.cy)
        
        self.canvas.coords(self.bar_bg,
                          self.cx - self.width//2 - bar_padding - bar_width,
                          self.cy - self.height//2,
                          self.cx - self.width//2 - bar_padding,
                          self.cy + self.height//2)
        
        self._update_progress_bar()
    
    def update(self, coherence, active=False, neuro=False, dt=0.016, hover_threshold=2.0):
        """Update box state with smooth transitions."""
        # Determine outline color with smooth transition
        if neuro:
            target_color = COLOR_BOX_NEURO
        elif active:
            target_color = COLOR_BOX_GAZE
        else:
            target_color = COLOR_BOX_INACTIVE
        
        self.canvas.itemconfig(self.rect, outline=target_color)
        
        # Update glow effect
        if active or neuro:
            self.glow_alpha = min(1.0, self.glow_alpha + dt * 3)
            self.canvas.itemconfig(self.glow, state="normal", outline=target_color, width=2)
        else:
            self.glow_alpha = max(0.0, self.glow_alpha - dt * 5)
            if self.glow_alpha <= 0:
                self.canvas.itemconfig(self.glow, state="hidden")
        
        # Progress bar animation
        if active:
            increment = (100.0 / max(0.001, hover_threshold)) * dt
            self.progress = min(100.0, self.progress + increment)
        else:
            decay = PROGRESS_DECAY * dt
            self.progress = max(0.0, self.progress - decay)
        
        self._update_progress_bar()
    
    def _update_progress_bar(self):
        """Update progress bar visual."""
        bar_width = 8
        bar_padding = 18
        bar_height = self.height * (self.progress / 100.0)
        
        self.canvas.coords(self.bar_fill,
                          self.cx - self.width//2 - bar_padding - bar_width,
                          self.cy + self.height//2 - bar_height,
                          self.cx - self.width//2 - bar_padding,
                          self.cy + self.height//2)