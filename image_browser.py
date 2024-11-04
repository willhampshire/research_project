import tkinter as tk
from tkinter import filedialog
from tkinter import ttk  # Import the ttk module for Combobox
from pathlib import Path
from PIL import Image, ImageTk
import re
import pandas as pd

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
        self.dimensions: dict = {'img': [], 't': [], 'ax': [], 'ff': []}
        self.dimensions_df: pd.DataFrame = pd.DataFrame(self.dimensions) # init empty dataframe type safety

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

        # Setup Image Frame (all existing functionality goes here)
        self.setup_image_frame()

        # Setup Dropdown Frame
        self.setup_dropdown_frame()

        # Start by loading the default project folder
        self.load_project_folder(initial=True)

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

    # Setup Dropdown Frame
    def setup_dropdown_frame(self):
        """Setup the dropdowns in the comparison frame."""
        # Label for X
        x_label = tk.Label(self.dropdown_frame, text="X:")
        x_label.pack(side="left", padx=5)  # Add horizontal padding

        # Dropdown for Compare (GUI X)
        self.compare_x_var = tk.StringVar()
        self.compare_x_combobox = ttk.Combobox(self.dropdown_frame, textvariable=self.compare_x_var,
                                               state="readonly")  # Set state to readonly
        self.compare_x_combobox['values'] = ("Thickness", "Period", "Filling")
        self.compare_x_combobox.current(0)  # Set default selection
        self.compare_x_combobox.pack(side="left", padx=5)  # Add horizontal padding
        self.compare_x_combobox.bind("<<ComboboxSelected>>", self.compare_x_selected)

        # Label for Y
        y_label = tk.Label(self.dropdown_frame, text="Y:")
        y_label.pack(side="left", padx=5)  # Add horizontal padding

        # Dropdown for Compare (GUI Y)
        self.compare_y_var = tk.StringVar()
        self.compare_y_combobox = ttk.Combobox(self.dropdown_frame, textvariable=self.compare_y_var,
                                               state="readonly")  # Set state to readonly
        self.compare_y_combobox['values'] = ("Thickness", "Period", "Filling")
        (self.compare_y_combobox
         .current(0))  # Set default selection
        self.compare_y_combobox.pack(side="left", padx=5)  # Add horizontal padding
        self.compare_y_combobox.bind("<<ComboboxSelected>>", self.compare_y_selected)

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

    def compare_y_selected(self, event):
        """Handle selection from Compare (GUI Y) dropdown."""
        selected_value = self.compare_y_var.get()
        print(f"Compare (GUI Y) selected: {selected_value}")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageBrowserApp(root)
    root.mainloop()
