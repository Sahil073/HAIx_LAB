# 🧠 BCI Interface - Eye Tracking & Calibration System

A professional Brain-Computer Interface (BCI) application built with Python and Tkinter, featuring eye tracking integration, automated calibration, and accessibility options.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.7+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

---

## 📋 Table of Contents

- [Features](#-features)
- [System Requirements](#-system-requirements)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [User Guide](#-user-guide)
- [File Structure](#-file-structure)
- [Configuration](#-configuration)
- [Troubleshooting](#-troubleshooting)
- [Development](#-development)
- [Credits](#-credits)

---

## ✨ Features

### 🎯 Core Functionality
- **Dual Input Modes**: Mouse cursor or Tobii eye tracker
- **Three Operational Phases**: Testing, Calibration, and Start
- **Automated Calibration**: Configurable rounds with randomized stimulus sequence
- **Real-time Visualization**: 50 animated dots representing neural activity
- **Session Logging**: Automatic gaze data logging to files

### 🎨 Accessibility
- **Theme Modes**:
  - ☀ **Light Mode**: Default high-contrast theme
  - 🌙 **Dark Mode**: Reduced eye strain for low-light environments
  - 👁 **Colorblind Mode**: Deuteranopia-friendly color palette

### 📊 User Interface
- **Responsive Design**: Automatically adjusts to screen size
- **Horizontal Control Panel**: All controls in single row for efficiency
- **Non-intrusive Timer**: Bottom-left corner display during calibration
- **8 Stimulus Circles**: Numbered 1-8, positioned around center
- **Progress Tracking**: Visual feedback for calibration progress

---

## 💻 System Requirements

### Minimum Requirements
- **OS**: Windows 10/11, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: 3.7 or higher
- **RAM**: 4GB
- **Display**: 1024x768 minimum resolution

### Recommended Requirements
- **Python**: 3.9+
- **RAM**: 8GB
- **Display**: 1920x1080 or higher
- **Tobii Eye Tracker**: Optional, for eye tracking mode

---

## 📦 Installation

### Step 1: Clone or Download

```bash
git clone https://github.com/yourusername/bci-interface.git
cd bci-interface
```

### Step 2: Install Python Dependencies

**Basic Installation (Mouse mode only):**
```bash
pip install tkinter
```

**Full Installation (with Tobii support):**
```bash
pip install tobii-research
```

### Step 3: Verify Installation

```bash
python main.py
```

If the application window opens, installation was successful!

---

## 🚀 Quick Start

### Running the Application

```bash
python main.py
```

### Basic Usage Flow

1. **Select Input Mode**: Choose "Mouse Cursor" or "Tobii Eye Tracker"
2. **Test the System**: Use "Testing Phase" to verify input is working
3. **Configure Calibration**: Set focus time, gap time, and number of rounds
4. **Run Calibration**: Switch to "Calibration Phase" and click "▶ Start"
5. **Start Working**: Move to "Start Phase" when ready

---

## 📖 User Guide

### Control Panel Overview

The top control panel contains all interface controls in a single horizontal row:

| Control | Options | Description |
|---------|---------|-------------|
| **Theme Buttons** | ☀ 🌙 👁 | Switch between Light, Dark, and Colorblind modes |
| **Input** | Mouse / Tobii | Select input device |
| **Phase** | Testing / Calibration / Start | Current operational phase |
| **Focus** | 1.0s - 5.0s | Duration each stimulus glows |
| **Gap** | 0.5s - 3.0s | Delay between stimuli |
| **Rounds** | 5 - 50 | Number of calibration rounds |
| **Start Button** | ▶ / ■ | Start/Stop calibration (Calibration phase only) |
| **Status** | Text | Current system status |

---

### Phase Descriptions

#### 🔍 Testing Phase
**Purpose**: Verify that input tracking is working correctly

**What to do**:
- Move your mouse or look around the screen
- Observe that the system tracks your position
- If using Tobii, verify "Tobii Active" appears in status

**Expected behavior**:
- Dots remain centered in the circle
- No stimulus circles glow
- Status shows "Testing Phase - Move cursor/gaze to test"

---

#### 🎯 Calibration Phase
**Purpose**: Train the system to recognize your gaze patterns

**Configuration**:
1. **Focus Time**: How long each stimulus glows (e.g., 3.0s)
2. **Gap Time**: Delay between stimuli (e.g., 2.0s)
3. **Rounds**: Total calibration rounds (e.g., 5 rounds = 40 stimuli)

**What happens**:
1. A random stimulus circle glows with golden border
2. Focus your attention on the glowing circle
3. At 83% of focus time (2.5s of 3s), dots begin moving toward stimulus
4. After focus time ends, there's a gap delay
5. Next random stimulus activates
6. Process repeats until all rounds complete

**Visual Feedback**:
- Timer shows elapsed time in bottom-left corner
- Status shows current round (e.g., "Round 3/5")
- Dots animate toward active stimulus
- All 8 circles covered before moving to next round

**Tips**:
- ✅ Keep your head still during calibration
- ✅ Focus on the center of each glowing circle
- ✅ Blink naturally, don't strain
- ✅ Start with 5 rounds for quick calibration
- ✅ Use 20+ rounds for precision applications

---

#### ▶️ Start Phase
**Purpose**: System is ready for actual use

**Status**: "Start Phase - System ready for use"

---

### Theme Selection

Click the theme buttons in the top-left corner to switch modes:

#### ☀ Light Mode (Default)
- **Background**: Light gray (#E8EAF0)
- **Dots**: Coral red (#E07A7A)
- **Stimulus Glow**: Golden yellow (#FFD700)
- **Best for**: Well-lit environments, daytime use

#### 🌙 Dark Mode
- **Background**: Dark blue-black (#0A0E27)
- **Dots**: Bright red (#FF6B6B)
- **Stimulus Glow**: Orange (#FFA500)
- **Best for**: Low-light environments, reduced eye strain

#### 👁 Colorblind Mode
- **Background**: Light gray (#F0F0F0)
- **Dots**: Blue (#0066CC) instead of red
- **Stimulus Glow**: Orange (#FF8800) instead of yellow
- **Best for**: Users with deuteranopia (red-green colorblindness)

---

### Timer Display

**Location**: Bottom-left corner (non-intrusive)

**Format**: `MM:SS.D` (Minutes:Seconds.Deciseconds)

**Visibility**:
- ✅ Visible during calibration
- ❌ Hidden during testing and start phases

**Example**: `02:35.4` = 2 minutes, 35.4 seconds elapsed

---

## 📁 File Structure

```
bci-interface/
├── main.py                 # Application entry point
├── config.py              # Configuration and theme settings
├── controller.py          # Main logic controller
├── ui_components.py       # Visual components (dots, circles, timer)
├── tobii_handler.py       # Tobii eye tracker integration
├── logs/                  # Auto-generated gaze session logs
│   └── gaze_session_YYYYMMDD_HHMMSS.log
└── README.md             # This file
```

### File Descriptions

#### `main.py` (418 lines)
Application entry point and main window management.

**Key Classes**:
- `BCIApplication`: Main application controller
  - Creates UI components
  - Manages themes
  - Handles user interactions

**Key Methods**:
- `_create_control_panel()`: Build top control interface
- `_switch_theme()`: Change color theme
- `_on_start_calibration()`: Start/stop calibration

---

#### `config.py` (143 lines)
All configuration constants and theme definitions.

**Key Sections**:
- Window dimensions and constraints
- Theme color palettes (Light, Dark, Colorblind)
- Animation parameters
- UI layout constants
- Calibration defaults

**Customization**:
Edit this file to change:
- Colors, sizes, fonts
- Default values
- Physics parameters
- Available options

---

#### `controller.py` (369 lines)
Core application logic and state management.

**Key Classes**:
- `BCIController`: Main system controller
  - Manages all three phases
  - Handles calibration state machine
  - Coordinates animations
  - Processes input from mouse/Tobii

**Key Methods**:
- `start_calibration()`: Begin calibration sequence
- `_update_calibration()`: State machine for glow/gap phases
- `resize()`: Handle window resizing
- `update_theme()`: Apply theme changes

---

#### `ui_components.py` (421 lines)
Visual components with smooth animations.

**Key Classes**:
- `Dot`: Individual animated dot with spring physics
- `CenterCircle`: Container with 50 dots
- `StimulusCircle`: Outer numbered circles
- `Timer`: Non-intrusive elapsed time display

**Animation Features**:
- Spring physics for natural movement
- Damping and velocity limiting
- Boundary constraints
- Theme-aware colors

---

#### `tobii_handler.py` (201 lines)
Tobii eye tracker SDK integration.

**Key Classes**:
- `TobiiHandler`: Eye tracker interface
  - Device detection and connection
  - Gaze data streaming
  - Session logging
  - Error handling

**Features**:
- Automatic device discovery
- Normalized gaze coordinates (0-1)
- JSON-formatted log files
- Graceful fallback to mouse

---

## ⚙️ Configuration

### Modifying Default Values

Edit `config.py` to customize:

```python
# Change default focus time
DEFAULT_FOCUS_TIME = 3.0  # seconds

# Change default gap time
DEFAULT_GAP_TIME = 2.0  # seconds

# Change default rounds
DEFAULT_CALIBRATION_ROUNDS = 5

# Change dot count
DOT_COUNT = 50  # Increase for denser appearance

# Change dot physics
DOT_SPRING_STRENGTH = 8.0  # Higher = faster movement
DOT_DAMPING = 0.85  # Higher = more damping
```

### Creating Custom Themes

Add to `config.py`:

```python
CUSTOM_THEME = {
    'bg': '#YOUR_BG_COLOR',
    'circle_center': '#YOUR_CIRCLE_COLOR',
    'dot': '#YOUR_DOT_COLOR',
    # ... add all required keys
}
```

Then modify `main.py` to add theme button.

---

## 🔧 Troubleshooting

### Issue: Application won't start

**Solutions**:
1. Verify Python version: `python --version` (needs 3.7+)
2. Check tkinter: `python -c "import tkinter"`
3. Try: `pip install --upgrade tk`

---

### Issue: "Tobii Unavailable" message

**Solutions**:
1. Install SDK: `pip install tobii-research`
2. Connect Tobii device before starting application
3. Check Tobii Eye Tracker Manager is running
4. Verify device drivers are installed
5. Fallback: Use "Mouse Cursor" mode

---

### Issue: Dots not moving smoothly

**Solutions**:
1. Close other applications to free resources
2. Reduce DOT_COUNT in config.py (try 30 instead of 50)
3. Update graphics drivers
4. Check system isn't in power saving mode

---

### Issue: Calibration completes too fast/slow

**Solutions**:
- Adjust focus time: Control Panel → Focus dropdown
- Adjust gap time: Control Panel → Gap dropdown
- Modify defaults in config.py

---

### Issue: Can't see timer during calibration

**Solutions**:
1. Timer is in bottom-left corner
2. Check it's not hidden by taskbar
3. Resize window to see full canvas area
4. Timer only appears during calibration phase

---

### Issue: Theme colors don't look right

**Solutions**:
1. Try different theme modes (☀ 🌙 👁)
2. Check display color profile settings
3. Adjust monitor brightness/contrast
4. Edit theme colors in config.py

---

## 👨‍💻 Development

### Code Structure Philosophy

This codebase follows industry best practices:

1. **Modular Design**: Each file has single responsibility
2. **Separation of Concerns**: UI, logic, and config separated
3. **Documentation**: Comprehensive inline comments
4. **Error Handling**: Graceful fallbacks for all edge cases
5. **Extensibility**: Easy to add features or modify behavior

### Adding New Features

**Example: Add new input device**

1. Create handler in new file (e.g., `leap_handler.py`)
2. Follow `TobiiHandler` interface pattern
3. Add to `INPUT_MODES` in `config.py`
4. Integrate in `controller.py` `set_input_mode()`

**Example: Add new phase**

1. Add phase name to `PHASES` in `config.py`
2. Implement phase logic in `controller.py` `set_phase()`
3. Update `main.py` dropdown handler

### Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Follow existing code style and documentation
4. Test thoroughly with different themes and modes
5. Submit pull request with clear description

---

## 📊 Technical Specifications

### Animation System
- **Frame Rate**: 60 FPS (16ms per frame)
- **Physics**: Spring-damper system for smooth motion
- **Dot Movement**: Unified direction, maintains formation
- **Boundary**: Soft constraint within center circle

### Calibration Algorithm
- **Sequence**: Randomized within rounds
- **Coverage**: All 8 stimuli per round, no repeats
- **Timing**: Precise state machine with millisecond accuracy
- **Trigger**: Dots move at 83% of focus time

### Input Handling
- **Mouse**: Native OS cursor tracking
- **Tobii**: Normalized gaze coordinates (0-1 range)
- **Sampling**: Real-time processing at tracker refresh rate
- **Logging**: JSON format with timestamps

---

## 📝 Version History

### v1.0.0 (Current)
- ✅ Initial release
- ✅ Mouse and Tobii input modes
- ✅ Three-phase system
- ✅ Automated calibration
- ✅ Three theme modes
- ✅ Responsive design
- ✅ Session logging
- ✅ Non-intrusive timer

---

## 📄 License

This project is licensed under the MIT License.

```
MIT License

Copyright (c) 2025 BCI Interface Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Credits

### Technologies
- **Python**: Core programming language
- **Tkinter**: GUI framework
- **Tobii Research SDK**: Eye tracking integration

### Design Inspiration
- EEG 10-20 electrode positioning system
- Modern accessibility guidelines
- Neuroscience visualization principles

### Special Thanks
- Tobii AB for eye tracking technology
- Python community for excellent documentation
- Accessibility advocates for inclusive design principles

---

## 📧 Support

### Getting Help

1. **Check Documentation**: This README covers most use cases
2. **Search Issues**: Check existing GitHub issues
3. **Report Bugs**: Create detailed issue with:
   - Python version
   - Operating system
   - Steps to reproduce
   - Error messages
   - Screenshots if applicable

### Contact

- **Email**: support@bciinterface.example.com
- **GitHub**: github.com/yourusername/bci-interface
- **Issues**: github.com/yourusername/bci-interface/issues

---

## 🔮 Roadmap

### Planned Features

**v1.1.0**
- [ ] CSV export of calibration results
- [ ] Custom stimulus patterns
- [ ] Sound feedback options
- [ ] Keyboard shortcuts

**v1.2.0**
- [ ] Multi-user profiles
- [ ] Calibration quality metrics
- [ ] Advanced statistics dashboard
- [ ] Real-time performance graphs

**v2.0.0**
- [ ] Machine learning integration
- [ ] Custom neural network training
- [ ] API for external applications
- [ ] Cloud synchronization

---

## 📚 Additional Resources

### Eye Tracking
- [Tobii Developer Documentation](https://developer.tobii.com/)
- [Eye Tracking Basics](https://imotions.com/blog/learning/research-fundamentals/eye-tracking/)

### Brain-Computer Interfaces
- [BCI Fundamentals](https://www.nature.com/subjects/brain-computer-interfaces)
- [Neuroergonomics Research](https://www.frontiersin.org/journals/neuroergonomics)

### Python GUI Development
- [Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)
- [Python GUI Programming](https://realpython.com/python-gui-tkinter/)

---

**Made with ❤️ for neuroscience and accessibility**

*Last Updated: 2025*