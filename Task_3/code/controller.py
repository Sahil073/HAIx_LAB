# ===============================================
# FILE: controller.py
# Main BCI Interface Logic Controller
# ===============================================

import time
import math
import random
from config import *
from ui_components import CenterCircle, StimulusCircle, Timer
from tobii_handler import TobiiHandler


class BCIController:
    """
    Main controller for BCI interface.
    Handles all phases: Testing, Calibration, Start.
    Manages animations and user interactions.
    """
    
    def __init__(self, canvas, status_callback=None):
        self.canvas = canvas
        self.status_callback = status_callback
        
        # Window dimensions
        self.width = WINDOW_WIDTH
        self.height = WINDOW_HEIGHT
        self.center_x = WINDOW_WIDTH // 2
        self.center_y = WINDOW_HEIGHT // 2
        
        # Calculate initial radius
        self.center_radius = self._calculate_center_radius()
        
        # Create UI components
        self.center_circle = CenterCircle(
            canvas, self.center_x, self.center_y, self.center_radius
        )
        self.stimulus_circles = []
        self._create_stimulus_circles()
        
        # Create timer
        self.timer = Timer(canvas)
        self.timer.reposition(self.height)
        
        # Tobii handler
        self.tobii = TobiiHandler()
        
        # Input tracking
        self.input_mode = INPUT_MODE_MOUSE
        self.mouse_x = self.center_x
        self.mouse_y = self.center_y
        self.gaze_x = self.center_x
        self.gaze_y = self.center_y
        
        # Phase management
        self.current_phase = PHASE_TESTING
        self.focus_time = DEFAULT_FOCUS_TIME
        self.gap_time = DEFAULT_GAP_TIME
        self.calibration_rounds = DEFAULT_CALIBRATION_ROUNDS
        
        # Calibration state
        self.calibration_active = False
        self.calibration_sequence = []
        self.current_calibration_index = 0
        self.calibration_start_time = None
        self.calibration_session_start = None
        self.calibration_completed_rounds = 0
        self.is_in_glow_phase = False
        self.is_in_gap_phase = False
        
        # Animation
        self.last_time = time.time()
        self.running = False
    
    def _calculate_center_radius(self):
        """Calculate center circle radius based on window size."""
        min_dimension = min(self.width, self.height - CONTROL_PANEL_HEIGHT)
        return int(min_dimension * CENTER_CIRCLE_RADIUS_RATIO)
    
    def _create_stimulus_circles(self):
        """Create 8 stimulus circles positioned around center."""
        min_dimension = min(self.width, self.height - CONTROL_PANEL_HEIGHT)
        distance = int(min_dimension * STIMULUS_DISTANCE_RATIO)
        
        for i, angle_deg in enumerate(STIMULUS_ANGLES, start=1):
            angle_rad = math.radians(angle_deg)
            
            x = self.center_x + distance * math.cos(angle_rad)
            y = self.center_y + distance * math.sin(angle_rad)
            
            circle = StimulusCircle(
                self.canvas, i, x, y, STIMULUS_CIRCLE_RADIUS
            )
            self.stimulus_circles.append(circle)
    
    # ==================== Input Management ====================
    
    def set_input_mode(self, mode):
        """Switch between mouse and Tobii input."""
        self.input_mode = mode
        
        if mode == INPUT_MODE_TOBII:
            if self.tobii.is_available():
                self.tobii.start_tracking(self._on_gaze_update)
                self._update_status("Tobii Active", "success")
                return True
            else:
                self._update_status("Tobii Unavailable - Using Mouse", "error")
                self.input_mode = INPUT_MODE_MOUSE
                return False
        else:
            self.tobii.stop_tracking()
            self._update_status("Mouse Active", "info")
            return True
    
    def _on_gaze_update(self, norm_x, norm_y):
        """Callback from Tobii handler with normalized gaze data."""
        self.gaze_x = int(norm_x * self.width)
        self.gaze_y = int(norm_y * self.height)
    
    def on_mouse_move(self, x, y):
        """Update mouse position."""
        self.mouse_x = x
        self.mouse_y = y
    
    def get_current_position(self):
        """Get current cursor/gaze position based on mode."""
        if self.input_mode == INPUT_MODE_TOBII:
            return self.gaze_x, self.gaze_y
        else:
            return self.mouse_x, self.mouse_y
    
    # ==================== Phase Management ====================
    
    def set_phase(self, phase):
        """Switch to a different phase."""
        # Stop any ongoing calibration
        self.stop_calibration()
        
        self.current_phase = phase
        
        if phase == PHASE_TESTING:
            self._update_status("Testing Phase - Move cursor/gaze to test", "info")
        elif phase == PHASE_CALIBRATION:
            self._update_status("Calibration Phase - Click 'Start' to begin", "info")
        elif phase == PHASE_START:
            self._update_status("Start Phase - System ready for use", "success")
    
    def set_focus_time(self, time_seconds):
        """Set focus time for calibration."""
        self.focus_time = time_seconds
    
    def set_gap_time(self, time_seconds):
        """Set gap time between calibration stimuli."""
        self.gap_time = time_seconds
    
    def set_calibration_rounds(self, rounds):
        """Set number of calibration rounds."""
        self.calibration_rounds = rounds
    
    # ==================== Calibration Control ====================
    
    def start_calibration(self):
        """Begin automatic calibration sequence."""
        if self.current_phase != PHASE_CALIBRATION:
            self._update_status("Switch to Calibration Phase first", "error")
            return False
        
        # Generate calibration sequence
        self._generate_calibration_sequence()
        
        self.calibration_active = True
        self.current_calibration_index = 0
        self.calibration_completed_rounds = 0
        self.calibration_start_time = time.time()
        self.calibration_session_start = time.time()
        self.is_in_glow_phase = True
        self.is_in_gap_phase = False
        
        # Show timer
        self.timer.show()
        
        # Start first stimulus
        self._activate_stimulus(self.calibration_sequence[0])
        
        self._update_status(
            f"Calibration: Round 1/{self.calibration_rounds}",
            "info"
        )
        
        return True
    
    def stop_calibration(self):
        """Stop calibration sequence."""
        if self.calibration_active:
            self.calibration_active = False
            self._deactivate_all_stimuli()
            self.center_circle.return_dots_home()
            self.timer.hide()
            self._update_status("Calibration Stopped", "warning")
    
    def _generate_calibration_sequence(self):
        """
        Generate randomized calibration sequence.
        Each round covers all 8 circles in random order.
        """
        self.calibration_sequence = []
        
        for round_num in range(self.calibration_rounds):
            # Create shuffled list of circle indices (0-7)
            circle_indices = list(range(8))
            random.shuffle(circle_indices)
            self.calibration_sequence.extend(circle_indices)
    
    def _activate_stimulus(self, index):
        """Activate (glow) a specific stimulus circle."""
        self._deactivate_all_stimuli()
        self.stimulus_circles[index].set_glow(True)
    
    def _deactivate_all_stimuli(self):
        """Deactivate all stimulus circles."""
        for circle in self.stimulus_circles:
            circle.set_glow(False)
    
    # ==================== Animation Loop ====================
    
    def start_animation(self):
        """Start animation loop."""
        self.running = True
        self.last_time = time.time()
    
    def stop_animation(self):
        """Stop animation loop."""
        self.running = False
    
    def update(self):
        """Main update loop called every frame."""
        if not self.running:
            return
        
        now = time.time()
        dt = now - self.last_time
        self.last_time = now
        
        # Update calibration if active
        if self.calibration_active:
            self._update_calibration(now)
            
            # Update timer
            if self.calibration_session_start:
                elapsed = now - self.calibration_session_start
                self.timer.update(elapsed)
        
        # In testing phase, move dots toward cursor/gaze
        elif self.current_phase == PHASE_TESTING:
            cursor_x, cursor_y = self.get_current_position()
            
            # Check if cursor is outside center circle
            dx = cursor_x - self.center_x
            dy = cursor_y - self.center_y
            dist_from_center = math.hypot(dx, dy)
            
            if dist_from_center > self.center_radius:
                # Move dots toward cursor direction
                self.center_circle.move_dots_toward(cursor_x, cursor_y, 1.0)
            else:
                # Inside circle, return home
                self.center_circle.return_dots_home()
        else:
            # Other phases - dots stay home
            self.center_circle.return_dots_home()
        
        # Update center circle dots
        self.center_circle.update(dt)
    
    def _update_calibration(self, now):
        """Update calibration state machine."""
        elapsed = now - self.calibration_start_time
        
        if self.is_in_glow_phase:
            # Check if dots should start moving
            move_trigger_time = self.focus_time * DOT_MOVE_TRIGGER_RATIO
            
            if elapsed >= move_trigger_time:
                # Move dots toward current stimulus
                current_stimulus_index = self.calibration_sequence[
                    self.current_calibration_index
                ]
                target_x, target_y = self.stimulus_circles[
                    current_stimulus_index
                ].get_position()
                
                # Calculate progress (0 to 1)
                remaining_time = self.focus_time - move_trigger_time
                time_in_move_phase = elapsed - move_trigger_time
                progress = min(1.0, time_in_move_phase / remaining_time)
                
                self.center_circle.move_dots_toward(
                    target_x, target_y, progress
                )
            
            # Check if glow phase complete
            if elapsed >= self.focus_time:
                # End glow phase, start gap phase
                self.is_in_glow_phase = False
                self.is_in_gap_phase = True
                self.calibration_start_time = now
                self._deactivate_all_stimuli()
                self.center_circle.return_dots_home()
                
        elif self.is_in_gap_phase:
            # Check if gap phase complete
            if elapsed >= self.gap_time:
                # Move to next stimulus
                self.current_calibration_index += 1
                
                # Check if all stimuli completed
                if self.current_calibration_index >= len(self.calibration_sequence):
                    # Calibration complete
                    self.calibration_active = False
                    self._deactivate_all_stimuli()
                    self.timer.hide()
                    self._update_status("✓ Calibration Complete!", "success")
                else:
                    # Check if round completed
                    completed_count = self.current_calibration_index
                    round_num = (completed_count // 8) + 1
                    
                    if completed_count % 8 == 0:
                        self.calibration_completed_rounds = round_num - 1
                        self._update_status(
                            f"Calibration: Round {round_num}/{self.calibration_rounds}",
                            "info"
                        )
                    
                    # Start next glow phase
                    self.is_in_glow_phase = True
                    self.is_in_gap_phase = False
                    self.calibration_start_time = now
                    self._activate_stimulus(
                        self.calibration_sequence[self.current_calibration_index]
                    )
    
    # ==================== Window Resize ====================
    
    def resize(self, width, height):
        """Handle window resize - maintain responsive layout."""
        self.width = width
        self.height = height
        self.center_x = width // 2
        self.center_y = height // 2
        
        # Update center circle
        self.center_radius = self._calculate_center_radius()
        self.center_circle.resize(
            self.center_x, self.center_y, self.center_radius
        )
        
        # Update stimulus circles
        min_dimension = min(width, height - CONTROL_PANEL_HEIGHT)
        distance = int(min_dimension * STIMULUS_DISTANCE_RATIO)
        
        for i, angle_deg in enumerate(STIMULUS_ANGLES):
            angle_rad = math.radians(angle_deg)
            x = self.center_x + distance * math.cos(angle_rad)
            y = self.center_y + distance * math.sin(angle_rad)
            self.stimulus_circles[i].reposition(x, y)
        
        # Update timer position
        self.timer.reposition(height)
    
    # ==================== Theme Management ====================
    
    def update_theme(self):
        """Update all components for theme change."""
        # Update canvas background
        self.canvas.config(bg=get_color('bg'))
        
        # Update center circle
        self.center_circle.update_theme()
        
        # Update stimulus circles
        for circle in self.stimulus_circles:
            circle.update_theme()
        
        # Update timer
        self.timer.update_theme()
    
    # ==================== Status Updates ====================
    
    def _update_status(self, message, level="info"):
        """Update status message via callback."""
        if self.status_callback:
            self.status_callback(message, level)
    
    # ==================== Cleanup ====================
    
    def cleanup(self):
        """Clean up resources."""
        self.stop_animation()
        self.tobii.stop_tracking()
        print("✓ Controller cleaned up")