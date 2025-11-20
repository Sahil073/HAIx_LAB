# ===============================================
# FILE: tobii_input_handler.py
# Updated: Fully robust gaze parser + session logging
# ===============================================

import os
import time
import json
from datetime import datetime

class TobiiInputHandler:
    """Handles input from Tobii eye tracker using Tobii Research SDK."""

    def __init__(self):
        # Shared state
        self.tobii_available = False
        self.current_gaze_x = 0.5
        self.current_gaze_y = 0.5
        self.gaze_callback = None

        # SDK handles
        self.tobii_research = None
        self.eyetracker = None

        # Tracking state
        self.running = False

        # Logging
        self.log_folder = "logs"
        self.session_log_path = None
        self._log_file = None

        # Try to initialize Tobii
        if self._load_tobii_research():
            self._initialize_tobii_research()

    # -------------------------------------------------
    # Tobii Research SDK setup
    # -------------------------------------------------
    def _load_tobii_research(self):
        """Try to load Tobii Research SDK."""
        try:
            import tobii_research as tr
            self.tobii_research = tr
            print("✅ Tobii Research SDK found.")
            return True
        except ImportError:
            print("⚠️ Tobii Research SDK not found.")
            print("➡️ Install with: pip install tobii-research")
            return False

    def _initialize_tobii_research(self):
        """Connect to eye tracker."""
        try:
            trackers = self.tobii_research.find_all_eyetrackers()
            if not trackers:
                print("⚠️ No Tobii devices found.")
                return False

            self.eyetracker = trackers[0]
            print(f"✅ Connected to Tobii: {self.eyetracker.model}")
            print(f"   Serial: {self.eyetracker.serial_number}")

            self.tobii_available = True
            return True

        except Exception as e:
            print(f"❌ ERROR initializing Tobii: {e}")
            return False

    # -------------------------------------------------
    # Logging System
    # -------------------------------------------------
    def _start_session_log(self):
        """Create logs/ folder and session file."""
        os.makedirs(self.log_folder, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.session_log_path = os.path.join(self.log_folder, f"session_{timestamp}.log")

        self._log_file = open(self.session_log_path, "w")

        self._log_file.write("=== Tobii Session Log ===\n")
        self._log_file.write(f"Started: {timestamp}\n")
        self._log_file.write("-----------------------------\n")
        self._log_file.flush()

        print(f"📁 Logging gaze data to: {self.session_log_path}")

    def _log_gaze(self, gaze_dict):
        """Write gaze samples to file."""
        if self._log_file:
            try:
                line = json.dumps(gaze_dict)
                self._log_file.write(line + "\n")
                self._log_file.flush()
            except Exception as e:
                print(f"⚠️ Logging error: {e}")

    # -------------------------------------------------
    # Gaze callback
    # -------------------------------------------------
    def _gaze_data_callback(self, gaze_data):
        """Internal callback from Tobii SDK."""
        try:
            # Handle both dictionary and object style
            if isinstance(gaze_data, dict):
                left = gaze_data.get("left_gaze_point_on_display_area")
                right = gaze_data.get("right_gaze_point_on_display_area")
            else:
                left = getattr(gaze_data, "left_gaze_point_on_display_area", None)
                right = getattr(gaze_data, "right_gaze_point_on_display_area", None)

            if left and right:
                gaze_x = (left[0] + right[0]) / 2
                gaze_y = (left[1] + right[1]) / 2

                # Update internal state
                self.current_gaze_x = gaze_x
                self.current_gaze_y = gaze_y

                # Log data
                entry = {
                    "timestamp": time.time(),
                    "left": left,
                    "right": right,
                    "avg_x": gaze_x,
                    "avg_y": gaze_y
                }
                self._log_gaze(entry)

                # Pass gaze to UI
                if self.gaze_callback:
                    self.gaze_callback(gaze_x, gaze_y)

        except Exception as e:
            print(f"⚠️ Gaze processing error: {e}")

    # -------------------------------------------------
    # Public API
    # -------------------------------------------------
    def start_tracking(self, callback=None):
        """Start gaze tracking & logging."""
        if not self.tobii_available:
            print("❌ Tobii unavailable.")
            return False

        self.gaze_callback = callback

        # Start logging session
        self._start_session_log()

        try:
            self.eyetracker.subscribe_to(
                self.tobii_research.EYETRACKER_GAZE_DATA,
                self._gaze_data_callback,
                as_dictionary=True  # safer / guaranteed working
            )
            self.running = True
            print("✅ Started Tobii gaze tracking.")
            return True

        except Exception as e:
            print(f"❌ ERROR starting tracking: {e}")
            return False

    def stop_tracking(self):
        """Stop gaze tracking & close log file."""
        if self.eyetracker and self.running:
            try:
                self.eyetracker.unsubscribe_from(
                    self.tobii_research.EYETRACKER_GAZE_DATA
                )
                print("🛑 Stopped Tobii gaze tracking.")
            except Exception as e:
                print(f"⚠️ Failed to stop tracking: {e}")

        self.running = False

        # Close log file
        if self._log_file:
            try:
                self._log_file.close()
                print(f"📁 Log saved: {self.session_log_path}")
            except:
                pass
            self._log_file = None

    def get_current_gaze(self):
        """Get latest normalized gaze values."""
        return self.current_gaze_x, self.current_gaze_y

    def is_available(self):
        """Check if Tobii is ready."""
        return self.tobii_available

    def calibrate(self):
        """User must calibrate via Tobii Manager."""
        print("🧭 Use Tobii Eye Tracker Manager to calibrate this device.")
