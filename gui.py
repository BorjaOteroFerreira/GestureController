import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import cv2
from PIL import Image, ImageTk
import mediapipe as mp
import gestures.HandsTogether as Ht
import gestures.OpenHand as Oh
import gestures.OpenMouth as Om
import gestures.HeadTilt as Het
import gestures.GestureController as Gc

class GestureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gesture Controller")
        
        # Dark theme colors
        self.bg_color = "#2e2e2e"
        self.fg_color = "#f5f5f5"
        self.widget_bg = "#3c3c3c"
        self.highlight_color = "#505050"
        self.border_color = "#FFFF00"

        self.root.configure(bg=self.bg_color)
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background=self.bg_color, borderwidth=0)
        self.style.configure("TLabel", background=self.bg_color, foreground=self.fg_color, borderwidth=0)
        self.style.configure("TButton", background=self.widget_bg, foreground=self.fg_color, borderwidth=1, relief="flat")
        self.style.map("TButton", background=[("active", self.highlight_color)])
        self.style.configure("TCombobox", fieldbackground=self.widget_bg, background=self.widget_bg, foreground=self.fg_color, borderwidth=1, relief="flat")
        self.style.map("TCombobox", fieldbackground=[("readonly", self.widget_bg)], selectbackground=[("readonly", self.widget_bg)], selectforeground=[("readonly", self.fg_color)])
        self.style.configure("TEntry", fieldbackground=self.widget_bg, foreground=self.fg_color, borderwidth=1, relief="flat")
        self.style.configure("TScrollbar", background=self.bg_color, troughcolor=self.widget_bg)
        self.controller = Gc.GestureController()

        self.gestures = {
            "OpenMouth": {"class": Om.OpenMouth, "params": ["Button"]},
            "HandsTogether": {"class": Ht.HandsTogether, "params": ["Button"]},
            "OpenHand": {"class": Oh.OpenHand, "params": ["Left hand", "Right hand"]},
            "HeadTilt": {"class": Het.HeadTilt, "params": ["Left side", "Right side"]},
        }
        self.selected_gestures = []
        self.camera_running = False
        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding="20 20 20 20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.gesture_listbox = tk.Listbox(frame, height=15, bg=self.widget_bg, fg=self.fg_color, selectbackground=self.highlight_color, selectforeground=self.fg_color, bd=0, relief="flat")
        self.gesture_listbox.grid(row=0, column=0, rowspan=7, padx=10, pady=10, sticky=(tk.N, tk.S, tk.E, tk.W))
        
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.gesture_listbox.yview)
        self.gesture_listbox.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, rowspan=7, sticky=(tk.N, tk.S))

        gesture_frame = ttk.Frame(frame, borderwidth=1, relief="flat")
        gesture_frame.grid(row=0, column=2, padx=10, pady=10, sticky=(tk.W, tk.E))

        self.gesture_selector = ttk.Combobox(gesture_frame, values=list(self.gestures.keys()), state="readonly", style="TCombobox")
        self.gesture_selector.grid(row=0, column=0, padx=10, pady=10, sticky=(tk.W, tk.E))
        self.gesture_selector.bind("<<ComboboxSelected>>", self.on_gesture_selected)

        self.param_frame = ttk.Frame(gesture_frame, borderwidth=1, relief="flat")
        self.param_frame.grid(row=1, column=0, padx=10, pady=10, sticky=(tk.W, tk.E))

        self.add_button = ttk.Button(gesture_frame, text="Add Gesture", command=self.add_gesture, style="TButton")
        self.add_button.grid(row=2, column=0, padx=10, pady=5, sticky=(tk.W, tk.E))

        self.remove_button = ttk.Button(gesture_frame, text="Remove Gesture", command=self.remove_gesture, style="TButton")
        self.remove_button.grid(row=3, column=0, padx=10, pady=5, sticky=(tk.W, tk.E))

        control_frame = ttk.Frame(frame, borderwidth=1, relief="flat")
        control_frame.grid(row=1, column=2, rowspan=5, padx=10, pady=10, sticky=(tk.N, tk.S, tk.E, tk.W))

        self.start_button = ttk.Button(control_frame, text="Start", command=self.start_controller, style="TButton")
        self.start_button.grid(row=0, column=0, padx=10, pady=5, sticky=(tk.W, tk.E))

        self.stop_button = ttk.Button(control_frame, text="Stop", command=self.stop_controller, style="TButton")
        self.stop_button.grid(row=1, column=0, padx=10, pady=5, sticky=(tk.W, tk.E))

        self.save_button = ttk.Button(control_frame, text="Save Config", command=self.save_config, style="TButton")
        self.save_button.grid(row=2, column=0, padx=10, pady=5, sticky=(tk.W, tk.E))

        self.load_button = ttk.Button(control_frame, text="Load Config", command=self.load_config, style="TButton")
        self.load_button.grid(row=3, column=0, padx=10, pady=5, sticky=(tk.W, tk.E))

        self.clear_button = ttk.Button(control_frame, text="Clear All", command=self.clear_all, style="TButton")
        self.clear_button.grid(row=4, column=0, padx=10, pady=5, sticky=(tk.W, tk.E))

        # Cámara y visualización
        self.camera_label = ttk.Label(control_frame)
        self.camera_label.grid(row=5, column=0, padx=10, pady=5, sticky=(tk.W, tk.E))

        self.camera_selector = ttk.Combobox(control_frame, values=["Camera 0", "Camera 1"], style="TCombobox")
        self.camera_selector.grid(row=6, column=0, padx=10, pady=5, sticky=(tk.W, tk.E))
        self.camera_selector.current(0)

    def on_gesture_selected(self, event):
        for widget in self.param_frame.winfo_children():
            widget.destroy()
        
        gesture_name = self.gesture_selector.get()
        params = self.gestures[gesture_name]["params"]
        self.param_vars = []

        for param in params:
            label = ttk.Label(self.param_frame, text=param, style="TLabel")
            label.grid(row=params.index(param), column=0, padx=5, pady=5)
            entry = ttk.Entry(self.param_frame, style="TEntry")
            entry.grid(row=params.index(param), column=1, padx=5, pady=5)
            self.param_vars.append(entry)

    def add_gesture(self):
        gesture_name = self.gesture_selector.get()
        params = [entry.get() for entry in self.param_vars]
        gesture_class = self.gestures[gesture_name]["class"]
        if len(params) == 1:
            gesture = gesture_class(params[0])
            self.gesture_listbox.insert(tk.END, f"{gesture_name} ({params[0]})")
        else:
            gesture = gesture_class(*params)
            self.gesture_listbox.insert(tk.END, f"{gesture_name} ({', '.join(params)})")
        self.selected_gestures.append(gesture)
        self.controller.add_gesture(gesture)

    def remove_gesture(self):
        selected_index = self.gesture_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            self.gesture_listbox.delete(index)
            del self.selected_gestures[index]
            self.controller.gestures.pop(index)

    def clear_all(self):
        self.gesture_listbox.delete(0, tk.END)
        self.selected_gestures = []
        self.controller = Gc.GestureController()  # Reinicia el controlador

    def save_config(self):
        config = []
        for gesture in self.selected_gestures:
            index = self.selected_gestures.index(gesture)
            params = self.gesture_listbox.get(index).split("(")[1][:-1].split(", ")
            config.append({"gesture": gesture.__class__.__name__, "params": params})

        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'w') as f:
                json.dump(config, f)
            messagebox.showinfo("Save Config", "Configuration saved successfully")

    def load_config(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r') as f:
                config = json.load(f)

            self.gesture_listbox.delete(0, tk.END)
            self.selected_gestures = []
            self.controller = Gc.GestureController()  # Reinicia el controlador

            for item in config:
                gesture_name = item["gesture"]
                params = item["params"]
                gesture_class = self.gestures[gesture_name]["class"]

                if len(params) == 1:
                    gesture = gesture_class(params[0])
                    self.gesture_listbox.insert(tk.END, f"{gesture_name} ({params[0]})")
                else:
                    gesture = gesture_class(*params)
                    self.gesture_listbox.insert(tk.END, f"{gesture_name} ({', '.join(params)})")

                self.selected_gestures.append(gesture)
                self.controller.add_gesture(gesture)

            messagebox.showinfo("Load Config", "Configuration loaded successfully")

    def start_controller(self):
        selected_camera = self.camera_selector.get()
        if selected_camera:
            camera_index = int(selected_camera.split()[1])
            self.start_camera_preview(camera_index)
        self.controller.start()
        self.update_camera_preview()

    def start_camera_preview(self, camera_index):
        self.cap = cv2.VideoCapture(camera_index)
        self.camera_running = True

    def update_camera_preview(self):
        if self.camera_running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = self.controller.process_frame(frame)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                img = ImageTk.PhotoImage(image=img)
                self.camera_label.config(image=img)
                self.camera_label.image = img
            if self.camera_running:
                self.root.after(10, self.update_camera_preview)

    def stop_controller(self):
        self.camera_running = False
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
            self.cap = None
        self.controller.stop()
        self.camera_label.config(image='')
        self.camera_label.image = None

if __name__ == "__main__":
    root = tk.Tk()
    app = GestureApp(root)
    root.mainloop()