# ===============================================
# FILE: tobii_input_handler.py
# Handles Tobii eye tracker input
# ===============================================

import sys

class TobiiInputHandler:
    """Handles input from Tobii eye tracker."""
    
    def __init__(self):
        self.tobii_available = False
        self.eyetracker = None
        self.current_gaze_x = 0
        self.current_gaze_y = 0
        self.gaze_callback = None
        
        try:
            import tobii_research as tr
            self.tobii_research = tr
            self._initialize_tobii()
        except ImportError:
            print("WARNING: tobii_research module not found. Tobii mode will not be available.")
            print("Install with: pip install tobii-research")
            self.tobii_research = None
    
    def _initialize_tobii(self):
        """Initialize connection to Tobii eye tracker."""
        try:
            eyetrackers = self.tobii_research.find_all_eyetrackers()
            
            if len(eyetrackers) == 0:
                print("WARNING: No Tobii eye trackers found.")
                self.tobii_available = False
                return
            
            self.eyetracker = eyetrackers[0]
            print(f"Connected to Tobii eye tracker: {self.eyetracker.model}")
            print(f"Serial number: {self.eyetracker.serial_number}")
            self.tobii_available = True
            
        except Exception as e:
            print(f"ERROR: Failed to initialize Tobii eye tracker: {e}")
            self.tobii_available = False
    
    def _gaze_data_callback(self, gaze_data):
        """Internal callback for gaze data from Tobii."""
        try:
            # Get left and right eye data
            left_gaze = gaze_data['left_gaze_point_on_display_area']
            right_gaze = gaze_data['right_gaze_point_on_display_area']
            
            # Check validity
            left_valid = gaze_data['left_gaze_point_validity']
            right_valid = gaze_data['right_gaze_point_validity']
            
            # Average the two eyes if both are valid, otherwise use the valid one
            if left_valid and right_valid:
                avg_x = (left_gaze[0] + right_gaze[0]) / 2.0
                avg_y = (left_gaze[1] + right_gaze[1]) / 2.0
            elif left_valid:
                avg_x = left_gaze[0]
                avg_y = left_gaze[1]
            elif right_valid:
                avg_x = right_gaze[0]
                avg_y = right_gaze[1]
            else:
                return  # No valid data
            
            # Store normalized coordinates (0-1)
            self.current_gaze_x = avg_x
            self.current_gaze_y = avg_y
            
            # Call external callback if set
            if self.gaze_callback:
                self.gaze_callback(avg_x, avg_y)
                
        except Exception as e:
            print(f"Error processing gaze data: {e}")
    
    def start_tracking(self, callback=None):
        """Start receiving gaze data from Tobii."""
        if not self.tobii_available or not self.eyetracker:
            print("ERROR: Tobii eye tracker not available.")
            return False
        
        try:
            self.gaze_callback = callback
            self.eyetracker.subscribe_to(
                self.tobii_research.EYETRACKER_GAZE_DATA,
                self._gaze_data_callback
            )
            print("Started Tobii gaze tracking.")
            return True
        except Exception as e:
            print(f"ERROR: Failed to start tracking: {e}")
            return False
    
    def stop_tracking(self):
        """Stop receiving gaze data."""
        if self.eyetracker:
            try:
                self.eyetracker.unsubscribe_from(
                    self.tobii_research.EYETRACKER_GAZE_DATA
                )
                print("Stopped Tobii gaze tracking.")
            except Exception as e:
                print(f"ERROR: Failed to stop tracking: {e}")
    
    def get_current_gaze(self):
        """Get current gaze position (normalized 0-1)."""
        return (self.current_gaze_x, self.current_gaze_y)
    
    def is_available(self):
        """Check if Tobii is available and ready."""
        return self.tobii_available
    
    def calibrate(self):
        """
        Open Tobii calibration interface.
        Note: This requires Tobii Eye Tracker Manager to be installed.
        """
        print("Please use Tobii Eye Tracker Manager to calibrate your device.")
        print("Calibration should be done before using the eye tracker for best accuracy.")