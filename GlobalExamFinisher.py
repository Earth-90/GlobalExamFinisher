import pyautogui
import time
import threading
import math
import tkinter as tk
from tkinter import ttk


def click_and_find_color(click_coords, corner1, corner2, target_color, nb_activite, nb_levels, questions_per_level, total_questions, cooldown_between_questions=0, log_func=print, stop_event=None, color_tolerance=5):
    x1, y1 = corner1
    x2, y2 = corner2
    region_x = min(x1, x2)
    region_y = min(y1, y2)
    region_w = abs(x2 - x1)
    region_h = abs(y2 - y1)

    for loop_index in range(nb_activite):
        if stop_event and stop_event.is_set():
            log_func("Stopped by user.")
            return
        remaining_questions = total_questions
        for level_index in range(nb_levels):
            if remaining_questions <= 0:
                return

            questions_this_level = min(questions_per_level, remaining_questions)
            level_click_coords = click_coords[:questions_this_level]
            remaining_questions -= questions_this_level

            question = 0
            for x, y in level_click_coords:
                if stop_event and stop_event.is_set():
                    log_func("Stopped by user.")
                    return
                question += 1
                log_func("=" * 66)
                log_func(f"Activity {loop_index + 1}/{nb_activite}, Level {level_index + 1}/{nb_levels}, Question {question}/{questions_this_level}")
                pyautogui.click(x=x, y=y - 5)
                pyautogui.click(x=x, y=y)
                pyautogui.click(x=x, y=y + 5)

                capture = pyautogui.screenshot(region=(region_x, region_y, region_w, region_h))

                largeur, hauteur = capture.size
                couleur_trouvee = False
                absolu_x = None
                absolu_y = None

                for offset_x in range(largeur):
                    for offset_y in range(hauteur):
                        pixel_courant = capture.getpixel((offset_x, offset_y))
                        pixel_rgb = pixel_courant[:3]

                        if all(abs(pixel_rgb[i] - target_color[i]) <= color_tolerance for i in range(3)):
                            absolu_x = region_x + offset_x
                            absolu_y = region_y + offset_y
                            couleur_trouvee = True
                            log_func(f"Solution founded and clicked at coordinates: ({absolu_x}, {absolu_y})")
                            break

                    if couleur_trouvee:
                        break

                if not couleur_trouvee:
                    log_func("The target color was not found in the specified area.")
                    log_func("Stopping the script.")
                    capture.show()
                    return
                else:
                    if len(click_coords) >= 2:
                        interval = abs(click_coords[1][1] - click_coords[0][1])
                    else:
                        interval = 140
                    step_px = 10
                    offset = step_px
                    while offset <= interval-15:
                        pyautogui.click(x=x, y=y + offset)
                        offset += step_px
                    for i in range(0, 60, 10):
                        pyautogui.click(x=absolu_x + 5 - i, y=absolu_y + 5)

                # cooldown between questions (responsive to stop_event)
                try:
                    cooldown = float(cooldown_between_questions)
                except Exception:
                    cooldown = 0.0

                if cooldown > 0:
                    slept = 0.0
                    step = 0.1
                    while slept < cooldown:
                        if stop_event and stop_event.is_set():
                            log_func("Stopped by user.")
                            return
                        to_sleep = min(step, cooldown - slept)
                        time.sleep(to_sleep)
                        slept += to_sleep


            time.sleep(1)
            pyautogui.click(x=960, y=1065)
            time.sleep(2)
            
        if loop_index < nb_activite - 1:
            time.sleep(2)
            log_func("=" * 66)
            log_func("End of the activity, preparing the next one...")

            second_region_x, second_region_y = 1000, 180
            second_region_w, second_region_h = 300, 60
            second_target_color = (254, 108, 53)
            color_tolerance = 5
            
            capture = pyautogui.screenshot(region=(second_region_x, second_region_y, second_region_w, second_region_h))
            color_found = False
            
            for offset_x in range(second_region_w):
                for offset_y in range(second_region_h):
                    pixel = capture.getpixel((offset_x, offset_y))
                    pixel_rgb = pixel[:3]
                    
                    if all(abs(pixel_rgb[i] - second_target_color[i]) <= color_tolerance for i in range(3)):
                        click_x = second_region_x + offset_x
                        click_y = second_region_y + offset_y
                        
                        pyautogui.click(x=click_x+5, y=click_y)
                        
                        log_func(f"Next activity button found and clicked at ({click_x}, {click_y})")
                        
                        color_found = True
                        break
                if color_found:
                    break

            if not color_found:
                log_func(f"Next activity button not found in the specified area.")
                capture.show()
                return
            time.sleep(3)


class GuiLogger:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, msg):
        if not msg:
            return
        if not msg.endswith("\n"):
            msg += "\n"

        def inner():
            self.text_widget.insert(tk.END, msg)
            self.text_widget.see(tk.END)

        self.text_widget.after(0, inner)

    def flush(self):
        pass


def start_gui():
    time.sleep(1.5)
    root = tk.Tk()
    root.title("GlobalExam Finisher")
    root.geometry("700x700")
    root.minsize(600, 600)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)

    mainframe = ttk.Frame(root, padding=10)
    mainframe.grid(row=0, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.columnconfigure(1, weight=1)
    mainframe.rowconfigure(0, weight=0)
    mainframe.rowconfigure(1, weight=1)

    left_frame = ttk.LabelFrame(mainframe, text="Settings", padding=10)
    left_frame.grid(row=0, column=0, sticky=(tk.N, tk.W, tk.E, tk.S), padx=(0, 8))
    left_frame.columnconfigure(1, weight=1)

    right_frame = ttk.LabelFrame(mainframe, text="Points to Capture", padding=10)
    right_frame.grid(row=0, column=1, sticky=(tk.N, tk.W, tk.E, tk.S))
    right_frame.columnconfigure(1, weight=1)

    # Inputs
    ttk.Label(left_frame, text="Number of activities:").grid(row=0, column=0, sticky=tk.W, pady=2)
    nb_activite_var = tk.StringVar(value='1')
    ttk.Entry(left_frame, textvariable=nb_activite_var, width=12).grid(row=0, column=1, sticky=tk.W, pady=2)

    ttk.Label(left_frame, text="Total questions:").grid(row=1, column=0, sticky=tk.W, pady=2)
    total_questions_var = tk.StringVar(value='5')
    ttk.Entry(left_frame, textvariable=total_questions_var, width=12).grid(row=1, column=1, sticky=tk.W, pady=2)

    ttk.Label(left_frame, text="Questions per level:").grid(row=2, column=0, sticky=tk.W, pady=2)
    questions_per_level_var = tk.StringVar(value='5')
    ttk.Entry(left_frame, textvariable=questions_per_level_var, width=12).grid(row=2, column=1, sticky=tk.W, pady=2)

    ttk.Label(left_frame, text="Cooldown between questions :").grid(row=3, column=0, sticky=tk.W, pady=2)
    cooldown_var = tk.StringVar(value='0')
    ttk.Entry(left_frame, textvariable=cooldown_var, width=12).grid(row=3, column=1, sticky=tk.W, pady=2)

    ttk.Label(left_frame, text="Color tolerance:").grid(row=4, column=0, sticky=tk.W, pady=2)
    tolerance_var = tk.IntVar(value=5)
    tolerance_slider = ttk.Scale(left_frame, from_=0, to=15, orient=tk.HORIZONTAL, variable=tolerance_var)
    tolerance_slider.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=2)
    tolerance_value = ttk.Label(left_frame, textvariable=tolerance_var, width=3)
    tolerance_value.grid(row=4, column=2, sticky=tk.W, padx=(8, 0), pady=2)

    # Region corner entries
    ttk.Label(left_frame, text="Corner 1 (x,y):").grid(row=5, column=0, sticky=tk.W, pady=(10, 2))
    coin1_var = tk.StringVar(value='900,200')
    ttk.Entry(left_frame, textvariable=coin1_var, width=20).grid(row=5, column=1, sticky=tk.W, pady=(10, 2))

    ttk.Label(left_frame, text="Corner 2 (x,y):").grid(row=6, column=0, sticky=tk.W, pady=2)
    coin2_var = tk.StringVar(value='1000,900')
    ttk.Entry(left_frame, textvariable=coin2_var, width=20).grid(row=6, column=1, sticky=tk.W, pady=2)

    ttk.Label(left_frame, text="Target color:").grid(row=7, column=0, sticky=tk.W, pady=(10, 2))
    target_color_var = tk.StringVar(value='(230, 255, 224)')
    ttk.Label(left_frame, textvariable=target_color_var).grid(row=7, column=1, sticky=tk.W, pady=(10, 2))
    target_preview = tk.Canvas(left_frame, width=42, height=24, highlightthickness=1, highlightbackground="#777")
    target_preview.grid(row=7, column=2, padx=(10, 0), pady=(10, 2), sticky=tk.W)

    def update_target_color_display(rgb):
        target_color_var.set(f"{rgb}")
        hex_color = "#%02x%02x%02x" % rgb
        target_preview.delete("all")
        target_preview.create_rectangle(0, 0, 42, 24, fill=hex_color, outline=hex_color)

    update_target_color_display((230, 255, 224))

    def pick_target_color():
        gui_logger.write("Pipette active: hover the target color, then wait 3 seconds.")
        for remaining in (3, 2, 1):
            gui_logger.write(f"Sampling in {remaining}...")
            root.update()
            time.sleep(1)

        x, y = pyautogui.position()
        pixel = pyautogui.screenshot().getpixel((x, y))[:3]
        update_target_color_display(pixel)
        gui_logger.write(f"Captured target color at ({x}, {y}): {pixel}")

    ttk.Button(left_frame, text="Pick by hover", command=lambda: threading.Thread(target=pick_target_color, daemon=True).start()).grid(row=7, column=2, padx=(10, 0), pady=(10, 2))

    ttk.Label(right_frame, text="Selected color preview:").grid(row=2, column=0, sticky=tk.W, pady=(10, 2))
    right_color_preview = tk.Canvas(right_frame, width=120, height=36, highlightthickness=1, highlightbackground="#777")
    right_color_preview.grid(row=2, column=1, sticky=tk.W, pady=(10, 2))
    right_color_text = ttk.Label(right_frame, textvariable=target_color_var)
    right_color_text.grid(row=2, column=2, sticky=tk.W, padx=(10, 0), pady=(10, 2))

    def sync_right_preview(*_):
        value = target_color_var.get().strip().strip("()")
        try:
            parts = [int(part.strip()) for part in value.split(",")]
            if len(parts) == 3:
                hex_color = "#%02x%02x%02x" % tuple(parts)
                right_color_preview.delete("all")
                right_color_preview.create_rectangle(0, 0, 120, 36, fill=hex_color, outline=hex_color)
        except Exception:
            pass

    target_color_var.trace_add("write", sync_right_preview)
    sync_right_preview()

    ttk.Label(right_frame, text="First point (X,Y):").grid(row=0, column=0, sticky=tk.W, pady=2)
    first_coord_var = tk.StringVar(value='')
    ttk.Label(right_frame, textvariable=first_coord_var).grid(row=0, column=1, sticky=tk.W, pady=2)

    ttk.Button(right_frame, text="Pick First Click", command=lambda: threading.Thread(target=pick_coord, args=(first_coord_var,), daemon=True).start()).grid(row=0, column=2, padx=(10, 0), pady=2)

    ttk.Label(right_frame, text="Second point (Y only):").grid(row=1, column=0, sticky=tk.W, pady=2)
    second_y_var = tk.StringVar(value='')
    ttk.Label(right_frame, textvariable=second_y_var).grid(row=1, column=1, sticky=tk.W, pady=2)

    ttk.Button(right_frame, text="Pick Second Y", command=lambda: threading.Thread(target=pick_coord, args=(second_y_var, 'y'), daemon=True).start()).grid(row=1, column=2, padx=(10, 0), pady=2)

    stop_event = threading.Event()
    worker_thread = {'thread': None}

    # Log window
    log_frame = ttk.LabelFrame(mainframe, text="Logs", padding=10)
    log_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.N, tk.S, tk.E, tk.W), pady=(10, 0))
    log_frame.columnconfigure(0, weight=1)
    log_frame.rowconfigure(0, weight=1)

    log_box = tk.Text(log_frame, width=100, height=18, wrap='word')
    log_box.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
    log_scroll = ttk.Scrollbar(log_frame, orient='vertical', command=log_box.yview)
    log_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
    log_box.configure(yscrollcommand=log_scroll.set)

    gui_logger = GuiLogger(log_box)

    def pick_coord(var, mode='xy'):
        for i in range(3, 0, -1):
            gui_logger.write(f"Capture in {i}...")
            root.update()
            time.sleep(1)
        x, y = pyautogui.position()
        if mode == 'y':
            var.set(f"{y}")
            gui_logger.write(f"Captured Y: {y}")
        else:
            var.set(f"{x},{y}")
            gui_logger.write(f"Captured: {x},{y}")

    def get_tuple_from_str(s):
        try:
            parts = [int(p.strip()) for p in s.split(',')]
            return (parts[0], parts[1])
        except Exception:
            return None

    def start_automation():
        if worker_thread['thread'] and worker_thread['thread'].is_alive():
            gui_logger.write("Already running")
            return
        try:
            nb_activite = int(nb_activite_var.get())
            total_questions = int(total_questions_var.get())
            questions_per_level = int(questions_per_level_var.get())
            try:
                cooldown = float(cooldown_var.get())
                if cooldown < 0:
                    gui_logger.write("Cooldown cannot be negative. Using 0.")
                    cooldown = 0.0
            except Exception:
                cooldown = 0.0
        except Exception as e:
            gui_logger.write(f"Invalid numeric input: {e}")
            return

        if total_questions <= 0 or questions_per_level <= 0:
            gui_logger.write("Total questions and questions per level must be greater than zero.")
            return

        nb_levels = math.ceil(total_questions / questions_per_level)
        gui_logger.write(f"=" * 66)
        gui_logger.write(f"Calculated levels: {nb_levels}")
        gui_logger.write(f"Cooldown between questions: {cooldown} seconds (default 0)")

        first = get_tuple_from_str(first_coord_var.get())
        try:
            second_y = int(second_y_var.get().strip())
        except Exception:
            second_y = None

        if not first or second_y is None:
            gui_logger.write("Please pick the first point and the second Y value.")
            return

        try:
            color_text = target_color_var.get().strip().strip('()')
            target_parts = [int(part.strip()) for part in color_text.split(',')]
            if len(target_parts) != 3:
                raise ValueError("Target color must have 3 components")
            COULEUR_CIBLE = tuple(target_parts)
        except Exception as e:
            gui_logger.write(f"Invalid target color: {e}")
            return

        tolerance = int(tolerance_var.get())

        FIRST_CLICK = first
        CLICK_STEP_Y = second_y - first[1]
        click_count = min(questions_per_level, total_questions)
        CLICS = [(FIRST_CLICK[0], FIRST_CLICK[1] + (index * CLICK_STEP_Y)) for index in range(click_count)]

        coin1 = get_tuple_from_str(coin1_var.get()) or (900, 200)
        coin2 = get_tuple_from_str(coin2_var.get()) or (1000, 900)

        stop_event.clear()

        def run():
            try:
                click_and_find_color(CLICS, coin1, coin2, COULEUR_CIBLE, nb_activite, nb_levels, questions_per_level, total_questions, cooldown_between_questions=cooldown, log_func=gui_logger.write, stop_event=stop_event, color_tolerance=tolerance)
                gui_logger.write(f"=" * 66)
                gui_logger.write(f"All activities finished.")
            except Exception as e:
                gui_logger.write(f"Error: {e}")

        t = threading.Thread(target=run, daemon=True)
        worker_thread['thread'] = t
        t.start()

    def stop_automation():
        stop_event.set()
        gui_logger.write("Stop requested.")

    controls_frame = ttk.Frame(mainframe)
    controls_frame.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(10, 0))
    ttk.Button(controls_frame, text="Start", command=start_automation).grid(row=0, column=0, padx=(0, 8))
    ttk.Button(controls_frame, text="Stop", command=stop_automation).grid(row=0, column=1)

    root.mainloop()

# --- Variable configuration ---

# Define the analysis area using two opposite corners (corner1: top-left, corner2: bottom-right).
COIN1 = (900, 200)
COIN2 = (1000, 900)

# Target color in RGB format (Red, Green, Blue). Example: pure red.
COULEUR_CIBLE = (240, 253, 229)

# --- Exécution ---

if __name__ == "__main__":
    start_gui()