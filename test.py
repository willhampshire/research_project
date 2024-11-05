import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pandas as pd
import numpy as np

class ImageBrowserApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Browser")

        # Set default window size to one-third of the screen width
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width // 3}x{screen_height // 2}")

        # Folder navigation variables
        self.project_folder = None
        self.image_paths = []
        self.current_image_index = 0
        self.dimensions = {'img': [], 't': [], 'ax': [], 'ff': []}
        self.dimensions_df = pd.DataFrame(self.dimensions)  # init empty dataframe type safety

        # Notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.grid(row=0, column=0, sticky="nsew")

        # Create frames for each tab
        self.image_frame = ttk.Frame(self.notebook)
        self.dropdown_frame = ttk.Frame(self.notebook)

        # Add frames to notebook
        self.notebook.add(self.image_frame, text='Single Image')
        self.notebook.add(self.dropdown_frame, text='Multi Image')
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

        # Image frame setup
        self.setup_image_frame()

        # Dropdown frame setup
        self.setup_dropdown_frame()

        # Start with default project folder
        self.load_project_folder(initial=True)

    def setup_image_frame(self):
        """Setup the image frame with navigation buttons and image display."""
        # Frame for navigation buttons
        nav_frame = tk.Frame(self.image_frame)
        nav_frame.grid(row=0, column=0, pady=10, sticky="nsew")

        # -10 button
        self.minus_10_button = tk.Button(nav_frame, text="-10", command=lambda: self.change_image(-10))
        self.minus_10_button.grid(row=0, column=0, padx=5)

        # Previous button
        self.prev_button = tk.Button(nav_frame, text="Previous", command=self.show_prev_image)
        self.prev_button.grid(row=0, column=1, padx=5)

        # Next button
        self.next_button = tk.Button(nav_frame, text="Next", command=self.show_next_image)
        self.next_button.grid(row=0, column=2, padx=5)

        # +10 button
        self.plus_10_button = tk.Button(nav_frame, text="+10", command=lambda: self.change_image(10))
        self.plus_10_button.grid(row=0, column=3, padx=5)

        # Image display area
        self.image_label = tk.Label(self.image_frame)
        self.image_label.grid(row=1, column=0, pady=(10, 0))

        # Current image display label
        self.current_image_label = tk.Label(self.image_frame, text="")
        self.current_image_label.grid(row=2, column=0, pady=(5, 0))

    def setup_dropdown_frame(self):
        """Setup the dropdowns and control buttons in a top row of the Multi Image frame."""
        controls_frame = tk.Frame(self.dropdown_frame)
        controls_frame.grid(row=0, column=0, sticky="nsew")

        x_label = tk.Label(controls_frame, text="X:")
        x_label.grid(row=0, column=0, padx=5)
        self.compare_x_var = tk.StringVar()
        self.compare_x_combobox = ttk.Combobox(controls_frame, textvariable=self.compare_x_var, state="readonly")
        self.compare_x_combobox['values'] = ("Thickness", "Period", "Filling")
        self.compare_x_combobox.current(1)
        self.compare_x_combobox.grid(row=0, column=1, padx=5)

        y_label = tk.Label(controls_frame, text="Y:")
        y_label.grid(row=0, column=2, padx=5)
        self.compare_y_var = tk.StringVar()
        self.compare_y_combobox = ttk.Combobox(controls_frame, textvariable=self.compare_y_var, state="readonly")
        self.compare_y_combobox['values'] = ("Thickness", "Period", "Filling")
        self.compare_y_combobox.current(0)
        self.compare_y_combobox.grid(row=0, column=3, padx=5)

        # Increment and decrement buttons
        self.increment_button = tk.Button(controls_frame, text="+", command=self.increment_third_variable)
        self.increment_button.grid(row=0, column=4, padx=5)
        self.decrement_button = tk.Button(controls_frame, text="-", command=self.decrement_third_variable)
        self.decrement_button.grid(row=0, column=5, padx=5)

        # Main canvas and scrollbars for multi-image grid
        self.canvas = tk.Canvas(self.dropdown_frame)
        self.canvas.grid(row=1, column=0, sticky="nsew")

        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.grid(row=0, column=0, sticky="nsew")

        # Scrollbars
        self.v_scrollbar = ttk.Scrollbar(self.dropdown_frame, orient="vertical", command=self.canvas.yview)
        self.v_scrollbar.grid(row=1, column=1, sticky="ns")
        self.h_scrollbar = ttk.Scrollbar(self.dropdown_frame, orient="horizontal", command=self.canvas.xview)
        self.h_scrollbar.grid(row=2, column=0, sticky="ew")

        # Bind scrollbars to canvas
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Update scroll region based on content
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

    def refresh_grid(self, event=None):
        """Populate and refresh grid inside the scrollable frame based on dropdown selections."""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Dummy code to demonstrate images within scrollable_frame
        for row in range(10):  # Add multiple rows for demo
            for col in range(10):  # Add multiple columns for demo
                img_label = tk.Label(self.scrollable_frame, text=f"Image {row},{col}", width=15, height=8)
                img_label.grid(row=row, column=col, padx=5, pady=5)

    # Dummy functions for missing functionality in example
    def on_tab_change(self, event): pass
    def load_project_folder(self, initial=False): pass
    def change_image(self, step): pass
    def show_prev_image(self): pass
    def show_next_image(self): pass
    def increment_third_variable(self): pass
    def decrement_third_variable(self): pass

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageBrowserApp(root)
    root.mainloop()
