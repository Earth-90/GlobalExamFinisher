# GlobalExamFinisher

A small GUI automation tool that helps locate and click answer buttons in a fixed-screen activity using color detection and repeated click patterns.

![](image.png)

## Features
- Simple Tkinter GUI to pick click points and run/stop automation
- Configurable activity count, question totals, questions per level, and screenshot region
- Color-based solution detection inside a user-defined region

Additional UI improvements:
- The interface is now organized into three categories: **Settings**, **Points**, and **Colors** for clearer workflow.
- Two pipettes: one for the answer/solution color and one for the "next activity" button color — use the "Pick by hover" buttons and hover the mouse over the desired color; the picker samples the pixel after a 3-second countdown.
- Each pipette shows a small color preview next to the RGB text so you can visually confirm the selection.
- The "Next" click coordinate is now configurable via a "Pick Point" button (replaces the previous hard-coded coordinate).
- A color tolerance slider (0–15) lets you control how permissive the color-matching is.

## Requirements
- Python 3.8+
- Python packages:
  - `pyautogui`
  - `Pillow`

Install requirements with:

```bash
pip install pyautogui Pillow
```

Note: `tkinter` is typically included with standard Python installers on Windows. If missing, install the appropriate Python distribution for your OS.

## Files
- `GlobalExamFinisher.py` — main script with the GUI and automation logic.

## Quick Start
1. Run the script:

```bash
python GlobalExamFinisher.py
```

2. Use the GUI:
- Set `Number of activities`, `Total questions`, and `Questions per level`.
- Adjust the analysis corners if needed (Corner 1 / Corner 2 define the screenshot region where the script searches for the target color).
- In the **Colors** panel:
  - Use `Pick by hover` to capture the answer/solution color (hover the cursor over the color and wait 3 seconds).
  - Use `Pick next color` to capture the color used to detect the "next activity" button.
  - Verify each color with its small preview and RGB text displayed beside it.
- In the **Points** panel:
  - Use `Pick Point` to capture the coordinate the script will click to continue to the next level (replaces the previous fixed coordinate).
- Press `Start` to begin automation and `Stop` to request a graceful stop.

## Configuration (GUI fields)
- Number of activities — how many times to run the full sequence.
- Total questions — total number of questions to solve across activities.
- Questions per level — how many questions are in each level (script calculates levels automatically).
- Corner 1 / Corner 2 — two opposite corners (x,y) that define the screenshot search area.
- First point (X,Y) — the first click coordinate used as a reference for clicking answers.
- Second point (Y only) — capture the second point's Y to compute vertical spacing between answers.

## How it works (brief)
1. For each configured click coordinate, the script clicks a few times near the point to trigger UI updates.
2. It screenshots the configured region and searches for the exact RGB target color.
3. If found, the script clicks around the detected pixel to confirm/select the answer.
4. Between activities it searches a small region for the "next activity" button by approximate color matching and clicks it.

## Safety & Warnings
- This script performs real mouse clicks and screenshots — do not run while you are actively using your machine or with important unsaved work.
- Be careful when running on different screen resolutions or multi-monitor setups; coordinate values are absolute screen coordinates.
- Test with small numbers and observe behavior before running long or unattended loops.
- The script uses exact-color matching for the primary detection and a small-tolerance check for the end-of-activity button; lighting/UI changes may require adjusting the color or region.

## Troubleshooting
- If the script does not find the target color, re-check the screenshot region corners and verify the target RGB in the code or GUI defaults.
- If clicks land in wrong places, re-capture coordinates with `Pick First Click` and `Pick Second Y`.
- If the GUI is unresponsive, try running the script from a console to see error messages.

## License
Use at your own risk. This repository contains a small personal automation tool — no warranty provided.