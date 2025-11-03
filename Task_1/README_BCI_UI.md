# Hybrid BCI Interactive UI

## Overview
This project implements an interactive user interface inspired by Hybrid Brain–Computer Interface (BCI) systems used for gaze and motor imagery experiments.  
It visualizes neural feedback through a dynamic dot field and visual cues that respond to user focus or simulated gaze direction.

Currently, the system uses **mouse cursor movement** to simulate gaze input, but it is designed for future integration with real-time **eye-tracking** or **EEG** data streams.

---

## Features

- **Central dynamic dot field**
  - Smooth collective motion toward gaze direction
  - Resting state when no box is focused
  - Colorful swarm dynamics with soft boundary correction
- **Stimulus boxes (1–8)** arranged around the central circle
  - Each has a distinct progress bar and outline
  - Progress bar fills as coherence (focus) increases
- **Feedback logic**
  - Gaze feedback (green outline)
  - Neuro-feedback (purple outline on spacebar press)
- **Industry-grade modular architecture**
  - Configurable, maintainable, and ready for sensor integration

---

## Folder Structure

```
bci_ui_v3/
│
├── config.py             # UI constants and tunable parameters
├── ui_components.py      # Classes for dots and boxes (render logic)
├── logic_controller.py   # Gaze tracking, coherence, and interaction logic
└── main.py               # Application entry point
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-org>/bci_ui_v3.git
cd bci_ui_v3
```

### 2. Install Python dependencies

This interface uses only the Python standard library (no external dependencies).

```bash
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

No external packages are required — only **Tkinter**, which is included in all standard Python installations.

---

## Configuration

All UI and system parameters are defined in `config.py`.  
You can adjust the following settings as needed:

```python
# Dot configuration
DOT_COUNT = 120
DOT_RADIUS = 3.5
DOT_COLORS = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00"]

# Box layout and sizes
BOX_WIDTH = 120
BOX_HEIGHT = 80

# Circle radius and window size
CIRCLE_RADIUS = 120
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
```

---

## Running the Interface

To start the simulation:

```bash
python main.py
```

---

## How It Works

### 1. Central Dot Field
The **CrowdDots** class creates a swarm of dots inside a circular area.

```python
self.dots = CrowdDots(canvas, CENTER_X, CENTER_Y, CIRCLE_RADIUS, DOT_COUNT)
```

Each dot:
- Has a random initial velocity and color.
- Moves smoothly toward the simulated gaze direction (mouse position).
- Remains inside the circular boundary via soft constraint forces.
- Returns to the center when the cursor is near the center (idle state).

Coherence of dot movement (alignment) determines the **progress bar fill**.

---

### 2. Stimulus Boxes
The **StimulusBox** class creates each numbered box with its associated progress bar.

```python
box = StimulusBox(canvas, label=1, dx=-250, dy=-220)
```

When a box is "active" (closest to gaze direction), its border turns **green**, and the progress bar fills based on coherence.  
If the **spacebar** is pressed (simulated neuro-feedback), the border turns **purple**.

---

### 3. Controller Logic
The **BCIInterface** class in `logic_controller.py` orchestrates updates and input handling.

```python
def animate(self):
    coherence = self.dots.update(self.mouse_x, self.mouse_y)
    active_box = self.get_closest_box()

    for box in self.boxes:
        neuro = (box == self.neuro_active_box)
        active = (box == active_box)
        box.update(coherence, active=active, neuro=neuro)
```

This loop runs every 30ms, ensuring smooth real-time visual feedback.

---

## Controls

| Action | Description |
|---------|--------------|
| Move Mouse | Simulates gaze direction |
| Keep Mouse Near Center | Dots rest at center, no box active |
| Press Spacebar | Activates neuro-feedback (purple outline) |
| ESC or Close Window | Exit program |

---

## Integration Notes

The architecture is modular and ready for external input sources.  
For example, to connect real **eye-tracker** or **EEG** data:

```python
# Example replacement for mouse tracking in BCIInterface
def update_gaze_position(self, gaze_x, gaze_y):
    self.mouse_x, self.mouse_y = gaze_x, gaze_y
```

You can feed real-time gaze or brain-derived focus coordinates to this function.

---

## License

This project is released under the MIT License.  
Feel free to modify and extend it for research or educational purposes.
