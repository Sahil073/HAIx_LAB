# Tobii Eye Tracker Setup Guide

## Prerequisites

1. **Tobii Eye Tracker Hardware**
   - Tobii Eye Tracker 5 (shown in your image)
   - USB connection to your PC
   - Make sure the device is properly connected and recognized by Windows

2. **Tobii Software**
   - Download and install **Tobii Eye Tracker Manager** from:
     https://gaming.tobii.com/getstarted/
   - This software is required for device drivers and calibration

## Installation Steps

### Step 1: Install Tobii Eye Tracker Manager

1. Download from: https://gaming.tobii.com/getstarted/
2. Run the installer
3. Follow the installation wizard
4. Restart your computer if prompted

### Step 2: Connect and Test Your Tobii Device

1. Connect the Tobii Eye Tracker to your PC via USB
2. Open Tobii Eye Tracker Manager
3. The device should appear in the manager
4. Run the **calibration** process in the manager (very important!)

### Step 3: Install Python Dependencies

Open a command prompt or terminal and run:

```bash
# Install Tobii Research SDK
pip install tobii-research

# Verify installation
python -c "import tobii_research as tr; print('Tobii SDK installed successfully')"
```

### Step 4: Test Tobii Connection

Create a test file `test_tobii.py`:

```python
import tobii_research as tr

# Find connected eye trackers
eyetrackers = tr.find_all_eyetrackers()

if len(eyetrackers) == 0:
    print("No eye trackers found!")
else:
    print(f"Found {len(eyetrackers)} eye tracker(s):")
    for et in eyetrackers:
        print(f"  - {et.model} (Serial: {et.serial_number})")
```

Run it:
```bash
python test_tobii.py
```

If you see your device listed, you're ready to go!

## Running the BCI Interface

```bash
python main.py
```

## Using the Interface

### Controls:

1. **Input Mode Dropdown** (top-left)
   - Select "Mouse (Manual)" for traditional mouse control
   - Select "Tobii Eye Tracker" to use eye tracking

2. **Hover Time Dropdown** (middle)
   - Choose how long you need to look at a box before it activates
   - Options: 1.0, 1.5, 2.0, 2.5, 3.0 seconds
   - Default: 2.0 seconds

3. **Status Indicator** (right)
   - Shows current mode and device status
   - Green: Active and working
   - Red: Device unavailable

### How It Works:

1. Look at (or move mouse to) one of the 8 numbered boxes
2. Keep your gaze steady on the box for the configured hover time
3. The dots in the center circle will move toward your gaze direction
4. The progress bar on the left of each box fills up as you focus
5. Press **SPACEBAR** to trigger a "neuro" selection (purple highlight)

## Troubleshooting

### "No Tobii eye trackers found"
- Check USB connection
- Ensure Tobii Eye Tracker Manager recognizes the device
- Try unplugging and reconnecting the device
- Restart Tobii Eye Tracker Manager

### "tobii_research module not found"
```bash
pip install --upgrade tobii-research
```

### Eye tracking seems inaccurate
- Run calibration in Tobii Eye Tracker Manager
- Ensure proper lighting (avoid backlighting)
- Sit at the recommended distance (50-95 cm from screen)
- Keep your head relatively still

### Device connects but tracking doesn't work
- Check that no other application is using the Tobii device
- Close Tobii Eye Tracker Manager (it may hold exclusive access)
- Restart the application

## Calibration Tips

For best accuracy:
1. Calibrate in the same lighting conditions you'll use the app
2. Sit at your normal distance from the screen
3. Follow the on-screen dots carefully during calibration
4. Recalibrate if you change seating position

## File Structure

Your project should have these files:
```
your_project/
├── config.py                 # Configuration settings
├── ui_components.py          # Visual components
├── tobii_input_handler.py    # Tobii integration
├── logic_controller.py       # Main controller
└── main.py                   # Application entry point
```

## Advanced Configuration

Edit `config.py` to customize:
- `HOVER_THRESHOLD_OPTIONS`: Available hover time values
- `RETURN_DELAY`: Time before dots return to center
- `DOT_COUNT`: Number of EEG visualization dots
- Colors and visual appearance

## Support

- Tobii Documentation: https://developer.tobii.com/
- Tobii Research SDK: https://github.com/tobiipro/prosdk-addons-python

## Notes

- The application will work in mouse mode even without a Tobii device
- Tobii mode automatically falls back to mouse if device is unavailable
- The spacebar trigger works in both modes for "neuro" selection