import tkinter as tk
from tkinter import filedialog, ttk
from pathlib import Path
from PIL import Image, ImageTk
import re
import pandas as pd
import numpy as np

# fix - things become misaligned when using navigation
# replace incrament/decrament with dropdown, or something

class ImageBrowserApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Browser")
        self.firstrun = 0

        # Set default window size to one-third of the screen width
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width // 3}x{screen_height // 2}")

        # Folder navigation variables
        self.project_folder = None
        self.image_paths = []
        self.current_image_index = 0
        self.dimensions: dict = {'img': [], 't': [], 'ax': [], 'ff': []}
        self.dimensions_df: pd.DataFrame = pd.DataFrame(self.dimensions)  # init empty dataframe type safety

        # Set default project directory (cwd / WS2_Grating_Eamonn / Results)
        self.default_project_dir = Path.cwd() / "WS2_Grating_Eamonn" / "Results"

        # Create a notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both')

        # Create frames for each tab
        self.image_frame = ttk.Frame(self.notebook)
        self.dropdown_frame = ttk.Frame(self.notebook)

        # Add frames to notebook
        self.notebook.add(self.image_frame, text='Single Image')
        self.notebook.add(self.dropdown_frame, text='Multi Image')
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

        # Bind Page Up and Page Down keys to scroll vertically
        self.root.bind("<Next>", lambda e: self.canvas.yview_scroll(1, "pages"))
        self.root.bind("<Prior>", lambda e: self.canvas.yview_scroll(-1, "pages"))

        # Setup Image Frame (all existing functionality goes here)
        self.setup_image_frame()

        # Setup Dropdown Frame
        self.setup_dropdown_frame()

        # Start by loading the default project folder
        self.load_project_folder(initial=True)

        self.dimensions = {'img': [], 't': [], 'ax': [], 'ff': []}
        self.dimensions_df = pd.DataFrame(self.dimensions)
        self.third_var_loc: int = 0

        self.scroll_container = tk.Frame(self.dropdown_frame)
        self.scroll_container.pack(expand=True, fill="both")

        # Canvas for displaying the images
        self.canvas = tk.Canvas(self.scroll_container)
        self.scrollable_frame = ttk.Frame(self.canvas)

        # Vertical and horizontal scrollbars attached to the canvas
        self.v_scrollbar = ttk.Scrollbar(self.scroll_container, orient="vertical", command=self.canvas.yview)
        self.h_scrollbar = ttk.Scrollbar(self.scroll_container, orient="horizontal", command=self.canvas.xview)

        # Grid layout to position canvas and scrollbars
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.v_scrollbar.grid(row=0, column=1, sticky="ns")
        self.h_scrollbar.grid(row=1, column=0, sticky="ew")

        # Configure the scroll region of the canvas
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)

        # Allow canvas and scrollbars to resize with the window
        self.scroll_container.grid_rowconfigure(0, weight=1)
        self.scroll_container.grid_columnconfigure(0, weight=1)

        # Bind canvas to frame for scrolling
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Callbacks for dropdown selections
        self.compare_x_combobox.bind("<<ComboboxSelected>>", self.refresh_grid)
        self.compare_y_combobox.bind("<<ComboboxSelected>>", self.refresh_grid)

    def show_popup(self, message):
        self.popup = tk.Toplevel(self.root)
        self.popup.title("Notification")
        self.popup.geometry("300x100")
        self.popup.resizable(False, False)

        # Create a frame to center the content
        frame = ttk.Frame(self.popup, padding="20 20 20 20")
        frame.pack(fill=tk.BOTH, expand=True)

        # Use a Label with word wrap
        label = ttk.Label(
            frame,
            text=message,
            font=("Helvetica", 12),
            wraplength=260,  # Adjust this value to control wrapping
            justify=tk.CENTER  # Center-align the text
        )
        label.pack(expand=True, fill=tk.BOTH)


    def on_tab_change(self, event):
        """Handle tab change events."""
        selected_tab = self.notebook.index(self.notebook.select())

        # Check if the Multi Image tab (index 1) is selected
        if selected_tab == 1:  # Assuming Multi Image tab is at index 1
            print("Multi Image tab selected.")
            self.show_popup("Please wait, lots of images can take a while to load")
            self.root.after(100, self.refresh_grid)

    def refresh_grid(self, event=None, third_var_call=0):
        """Refresh the grid layout based on dropdown selection."""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Ensure dimensions have been parsed
        if not self.determine_dimensions():
            return

        # Get selected values for X, Y, and third variables
        x_sel = self.compare_x_var.get()
        y_sel = self.compare_y_var.get()

        # Map dropdown selections to dataframe columns
        self.selection_mapping = {
            "Thickness": 't',
            "Period": 'ax',
            "Filling": 'ff'
        }

        self.x_dim, self.y_dim = [self.selection_mapping[sel] for sel in [x_sel, y_sel]]

        # Ensure valid selections before proceeding
        if self.x_dim is None or self.y_dim is None:
            print("Invalid selection.")
            return

        # Group images by the selected X, Y, and third variable values
        unique_x = sorted(self.dimensions_df[self.x_dim].unique())
        unique_y = sorted(self.dimensions_df[self.y_dim].unique())

        third_var = self.get_third_var([self.x_dim, self.y_dim])
        unique_third = sorted(self.dimensions_df[third_var].unique())
        print(f"THIRD VARIABLE = {third_var}")

        self.third_var_combobox['values'] = [str(val) for val in unique_third]
        if third_var_call == 0:
            self.third_var_combobox.set(str(unique_third[0]))
            self.firstrun += 1

        # Get the selected value for the third variable
        selected_third_value = float(self.third_var_var.get())

        for row_idx, x_value in enumerate(unique_x):
            for col_idx, y_value in enumerate(unique_y):
                # Filter images matching current X, Y, and third variable values
                image_paths = self.dimensions_df[
                    (self.dimensions_df[third_var] == selected_third_value) &
                    (self.dimensions_df[self.x_dim] == x_value) &
                    (self.dimensions_df[self.y_dim] == y_value)
                    ]['img'].tolist()

                for image_path in image_paths:  # Load all images that match the criteria
                    try:
                        image = Image.open(image_path)
                        image.thumbnail((250, 250))  # Resize image for display
                        img_tk = ImageTk.PhotoImage(image)

                        # Create and place the label with the image in the grid
                        img_label = tk.Label(self.scrollable_frame, image=img_tk)
                        img_label.image = img_tk  # Keep a reference to prevent garbage collection
                        img_label.grid(row=row_idx, column=col_idx, padx=5, pady=5)
                    except Exception as e:
                        print(f"Could not open image. Error: {e}")
                        print(f"Image paths: {image_paths}")

        # Adjust canvas scroll region based on new grid
        self.scrollable_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def setup_image_frame(self):
        """Setup the image frame with navigation buttons and image display."""
        # Frame for navigation buttons
        nav_frame = tk.Frame(self.image_frame)
        nav_frame.pack(pady=10)  # Add some vertical padding to the frame

        # Configure grid layout for nav_frame
        nav_frame.grid_rowconfigure(0, weight=1)
        nav_frame.grid_columnconfigure(0, weight=1)

        # -10 button
        self.minus_10_button = tk.Button(nav_frame, text="-10", command=lambda: self.change_image(-10))
        self.minus_10_button.grid(row=0, column=0, padx=5)  # Add horizontal padding

        # Previous button
        self.prev_button = tk.Button(nav_frame, text="Previous", command=self.show_prev_image)
        self.prev_button.grid(row=0, column=1, padx=5)  # Add horizontal padding

        # Next button
        self.next_button = tk.Button(nav_frame, text="Next", command=self.show_next_image)
        self.next_button.grid(row=0, column=2, padx=5)  # Add horizontal padding

        # +10 button
        self.plus_10_button = tk.Button(nav_frame, text="+10", command=lambda: self.change_image(10))
        self.plus_10_button.grid(row=0, column=3, padx=5)  # Add horizontal padding

        # Image display area
        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack()

        # Current image display label
        self.current_image_label = tk.Label(self.image_frame, text="")
        self.current_image_label.pack()

        # Load project button
        load_button = tk.Button(self.image_frame, text="Select Project Folder", command=self.load_project_folder)
        load_button.pack()

    def setup_dropdown_frame(self):
        """Setup the dropdowns and control buttons in a top row of the Multi Image frame."""

        # Create a new frame at the top of dropdown_frame for controls
        controls_frame = tk.Frame(self.dropdown_frame)
        controls_frame.pack(side="top", fill="x", pady=5)

        # Label and dropdown for X dimension selection
        x_label = tk.Label(controls_frame, text="X:")
        x_label.pack(side="left", padx=5)
        self.compare_x_var = tk.StringVar()
        self.compare_x_combobox = ttk.Combobox(controls_frame, textvariable=self.compare_x_var, state="readonly")
        self.compare_x_combobox['values'] = ("Thickness", "Period", "Filling")
        self.compare_x_combobox.current(0)
        self.compare_x_combobox.pack(side="left", padx=5)
        self.compare_x_combobox.bind("<<ComboboxSelected>>", self.refresh_grid)

        # Label and dropdown for Y dimension selection
        y_label = tk.Label(controls_frame, text="Y:")
        y_label.pack(side="left", padx=5)
        self.compare_y_var = tk.StringVar()
        self.compare_y_combobox = ttk.Combobox(controls_frame, textvariable=self.compare_y_var, state="readonly")
        self.compare_y_combobox['values'] = ("Thickness", "Period", "Filling")
        self.compare_y_combobox.current(1)
        self.compare_y_combobox.pack(side="left", padx=5)
        self.compare_y_combobox.bind("<<ComboboxSelected>>", self.refresh_grid)

        # Dropdown for third variable selection
        third_label = tk.Label(controls_frame, text="Third Variable:")
        third_label.pack(side="left", padx=5)
        self.third_var_var = tk.StringVar()
        self.third_var_combobox = ttk.Combobox(controls_frame, textvariable=self.third_var_var, state="readonly")
        self.third_var_combobox.pack(side="left", padx=5)
        # self.third_var_combobox.bind("<<ComboboxSelected>>", self.refresh_grid)
        self.third_var_combobox.bind("<<ComboboxSelected>>", lambda event: self.refresh_grid(event, third_var_call=1))

    def get_third_var(self, vars:list):
        all_vars = self.selection_mapping.values()
        all_vars_list = list(all_vars)
        for var in all_vars_list:
            print(var, vars, all_vars_list)
            if str(var) not in vars:
                print("FOUND")
                return var
        return 0

    def increment_third_variable(self):
        """Increment the third variable based on the current selections."""
        vars = [self.x_dim, self.y_dim]
        third_var = self.get_third_var(vars)
        self.set_third_variable(1, third_var)

    def decrement_third_variable(self):
        """Decrement the third variable based on the current selections."""
        vars = [self.x_dim, self.y_dim]
        third_var = self.get_third_var(vars)
        self.set_third_variable(-1, third_var)

    def set_third_variable(self, direction:int, var:str):
        if (self.third_var_loc + direction) >= 0:
            self.third_var_loc += direction
        else:
            print(f"NOT ALLOWED: self.third_var_loc + direction = {self.third_var_loc + direction}")

        self.refresh_grid()

        print(f"Changed {var} by {direction}. New val {self.third_var_loc}.")


    def load_project_folder(self, initial=False):
        """Load the project folder, with an initial directory prompt."""
        if initial:
            # Use the default directory on the first load
            initial_dir = self.default_project_dir
        else:
            # If user selects folder, start from the last chosen directory
            initial_dir = self.project_folder if self.project_folder else self.default_project_dir

        # Prompt the user to select the Results folder
        selected_folder = filedialog.askdirectory(title="Select Project Folder", initialdir=initial_dir)

        if selected_folder:
            self.project_folder = Path(selected_folder)
            self.load_images()

            if self.image_paths:
                self.show_image(0)

    def load_images(self):
        """Load all PNG images from the specified folder structure under the selected project."""
        self.image_paths = []

        print(f"Selected project folder: {self.project_folder}")

        # Ensure project_folder is not None and exists
        if self.project_folder and self.project_folder.exists():
            # Loop through each experiment folder in the selected project folder
            for experiment_folder in self.project_folder.iterdir():
                if experiment_folder.is_dir():
                    # Define the 'images' directory within each experiment folder
                    images_folder = experiment_folder / "images"

                    # Check if the 'images' folder exists
                    if images_folder.exists() and images_folder.is_dir():
                        # Search for PNG files within the 'images' folder
                        for image_file in images_folder.glob("*.png"):
                            self.image_paths.append(image_file)

            if not self.image_paths:
                print("No images found in the specified folder structure.")
            else:
                print(f"Total images found: {len(self.image_paths)}")

        else:
            print("Project folder is either not set or does not exist.")

        self.image_paths.sort()  # Optional: Sort to keep the images ordered
        self.current_image_index = 0  # Reset index when loading new images

        self.determine_dimensions()

    def determine_dimensions(self):
        """Extract dimensions from image filenames."""
        for _, image in enumerate(self.image_paths):
            img_name = image.name

            # Define the regex pattern
            pattern = r'.*? - t=(\d*(\.\d+)?)nm\s*Λ=(\d*(\.\d+)?)nm\s*FF=(\d*(\.\d+)?)\.png$'

            # Search for matches in the filename
            match = re.search(pattern, img_name)

            # Check if a match was found
            if match:
                # Extract the groups and convert them to floats
                thickness = float(match.group(1))  # t
                period = float(match.group(3))  # Λ
                filling_fraction = float(match.group(5))  # FF

                self.dimensions['img'].append(image)
                self.dimensions['t'].append(thickness)
                self.dimensions['ax'].append(period)
                self.dimensions['ff'].append(filling_fraction)
            else:
                print("No match found.")

        df = pd.DataFrame(self.dimensions)
        df.info()
        print(df.head())

        self.dimensions_df = df
        return True

    def show_image(self, index):
        """Display image at the given index while preserving its aspect ratio."""
        if self.image_paths:
            image_path = self.image_paths[index]
            image = Image.open(image_path)

            # Define maximum display dimensions (e.g., width=500, height=500)
            max_width, max_height = 500, 500
            original_width, original_height = image.size

            # Calculate the scaling factor to fit within max dimensions while maintaining aspect ratio
            scaling_factor = min(max_width / original_width, max_height / original_height)
            new_width = int(original_width * scaling_factor)
            new_height = int(original_height * scaling_factor)

            # Resize the image with the calculated dimensions
            resized_image = image.resize((new_width, new_height), Image.LANCZOS)

            # Convert to a format suitable for Tkinter display
            self.photo_image = ImageTk.PhotoImage(resized_image)
            self.image_label.config(image=self.photo_image)

            # Update the current image label
            self.current_image_label.config(text=f"Image {index + 1} of {len(self.image_paths)}")

    def show_prev_image(self):
        """Show previous image in the list."""
        if self.image_paths:
            self.current_image_index = (self.current_image_index - 1) % len(self.image_paths)
            self.show_image(self.current_image_index)

    def show_next_image(self):
        """Show next image in the list."""
        if self.image_paths:
            self.current_image_index = (self.current_image_index + 1) % len(self.image_paths)
            self.show_image(self.current_image_index)

    def change_image(self, step):
        """Change the image by a given step (positive or negative)."""
        if self.image_paths:
            self.current_image_index = (self.current_image_index + step) % len(self.image_paths)
            self.show_image(self.current_image_index)

    def compare_x_selected(self, event):
        """Handle selection from Compare (GUI X) dropdown."""
        selected_value = self.compare_x_var.get()
        print(f"Compare (GUI X) selected: {selected_value}")
        return selected_value

    def compare_y_selected(self, event):
        """Handle selection from Compare (GUI Y) dropdown."""
        selected_value = self.compare_y_var.get()
        print(f"Compare (GUI Y) selected: {selected_value}")
        return selected_value

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageBrowserApp(root)
    root.mainloop()
