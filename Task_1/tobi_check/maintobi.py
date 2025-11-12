import tobii_research as tr

found_eyetrackers = tr.find_all_eyetrackers()
my_eyetracker = found_eyetrackers[0]

def gaze_data_callback(gaze_data):
    print("Left eye: ", gaze_data['left_gaze_point_on_display_area'])
    print("Right eye:", gaze_data['right_gaze_point_on_display_area'])

my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)
