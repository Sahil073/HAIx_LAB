# ===============================================
# FILE: tobii_handler.py
# Tobii Eye Tracker Integration
# ===============================================

import time
import os
import json
from datetime import datetime


class TobiiHandler:
    """
    Handles Tobii eye tracker connection and gaze data.
    Provides fallback to mouse if Tobii is unavailable.
    """
    
    def __init__(self):
        self.tobii_available = False
        self.tobii_research = None
        self.eyetracker = None
        self.running = False
        
        # Current gaze position (normalized 0-1)
        self.gaze_x = 0.5
        self.gaze_y = 0.5
        
        # Callback for gaze updates
        self.gaze_callback = None
        
        # Logging
        self.log_folder = "logs"
        self.session_log_path = None
        self.log_file = None
        
        # Try to load Tobii SDK
        self._load_tobii_sdk()
    
    def _load_tobii_sdk(self):
        """Attempt to load Tobii Research SDK."""
        try:
            import tobii_research as tr
            self.tobii_research = tr
            print("✓ Tobii Research SDK loaded successfully")
            self._connect_eyetracker()
        except ImportError:
            print("⚠ Tobii Research SDK not found")
            print("  Install with: pip install tobii-research")
            self.tobii_available = False
    
    def _connect_eyetracker(self):
        """Connect to first available Tobii eye tracker."""
        try:
            eyetrackers = self.tobii_research.find_all_eyetrackers()
            
            if not eyetrackers:
                print("⚠ No Tobii eye tracker devices found")
                self.tobii_available = False
                return False
            
            self.eyetracker = eyetrackers[0]
            print(f"✓ Connected to Tobii: {self.eyetracker.model}")
            print(f"  Serial: {self.eyetracker.serial_number}")
            
            self.tobii_available = True
            return True
            
        except Exception as e:
            print(f"✗ Error connecting to Tobii: {e}")
            self.tobii_available = False
            return False
    
    def is_available(self):
        """Check if Tobii is available."""
        return self.tobii_available
    
    def start_tracking(self, callback=None):
        """
        Start gaze tracking.
        callback: function(norm_x, norm_y) called on each gaze update.
        """
        if not self.tobii_available:
            print("✗ Cannot start tracking: Tobii unavailable")
            return False
        
        self.gaze_callback = callback
        
        # Start logging
        self._start_logging()
        
        try:
            self.eyetracker.subscribe_to(
                self.tobii_research.EYETRACKER_GAZE_DATA,
                self._on_gaze_data,
                as_dictionary=True
            )
            self.running = True
            print("✓ Gaze tracking started")
            return True
            
        except Exception as e:
            print(f"✗ Error starting gaze tracking: {e}")
            return False
    
    def stop_tracking(self):
        """Stop gaze tracking."""
        if self.eyetracker and self.running:
            try:
                self.eyetracker.unsubscribe_from(
                    self.tobii_research.EYETRACKER_GAZE_DATA
                )
                print("✓ Gaze tracking stopped")
            except Exception as e:
                print(f"⚠ Error stopping tracking: {e}")
        
        self.running = False
        self._stop_logging()
    
    def _on_gaze_data(self, gaze_data):
        """Internal callback for gaze data from Tobii SDK."""
        try:
            # Extract left and right gaze points
            left = gaze_data.get("left_gaze_point_on_display_area")
            right = gaze_data.get("right_gaze_point_on_display_area")
            
            if left and right:
                # Average both eyes
                gaze_x = (left[0] + right[0]) / 2.0
                gaze_y = (left[1] + right[1]) / 2.0
                
                # Update internal state
                self.gaze_x = gaze_x
                self.gaze_y = gaze_y
                
                # Log data
                self._log_gaze_data({
                    "timestamp": time.time(),
                    "left": left,
                    "right": right,
                    "avg_x": gaze_x,
                    "avg_y": gaze_y
                })
                
                # Call user callback
                if self.gaze_callback:
                    self.gaze_callback(gaze_x, gaze_y)
                    
        except Exception as e:
            print(f"⚠ Error processing gaze data: {e}")
    
    def get_current_gaze(self):
        """Get latest gaze position (normalized 0-1)."""
        return self.gaze_x, self.gaze_y
    
    # ==================== Logging ====================
    
    def _start_logging(self):
        """Create log file for this session."""
        os.makedirs(self.log_folder, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_log_path = os.path.join(
            self.log_folder,
            f"gaze_session_{timestamp}.log"
        )
        
        try:
            self.log_file = open(self.session_log_path, "w")
            self.log_file.write("=== Tobii Gaze Session Log ===\n")
            self.log_file.write(f"Started: {timestamp}\n")
            self.log_file.write("=" * 40 + "\n")
            self.log_file.flush()
            print(f"📝 Logging to: {self.session_log_path}")
        except Exception as e:
            print(f"⚠ Could not create log file: {e}")
    
    def _log_gaze_data(self, data):
        """Write gaze data to log file."""
        if self.log_file:
            try:
                line = json.dumps(data)
                self.log_file.write(line + "\n")
                self.log_file.flush()
            except Exception as e:
                print(f"⚠ Logging error: {e}")
    
    def _stop_logging(self):
        """Close log file."""
        if self.log_file:
            try:
                self.log_file.close()
                print(f"📝 Log saved: {self.session_log_path}")
            except:
                pass
            self.log_file = None