# RCWA Electromagnetic Simulation

RCWA simulation script, adapted from a previous version by `ph1pbx`. 
Remake created by Will Hampshire. The script performs Reflective Coupled Wave Analysis (RCWA) 
for simulating the optical properties of layered materials, using [S4 (linked)](https://web.stanford.edu/group/fan/S4/).

## venv
Python 3.10(.11).

Install requirements with ```pip install -r requirements.txt```.

Compiled S4 from source. Would not recommend compiling from the original branch (was tricky, no good documentation). 
Instead, try one of the newer forks, phoebe-p/S4 and marcus-o/S4.

## Scripts
Run `vx.x 1D grating modes.py` in `WS2_Grating_Eamonn/Results` script to generate simulations (adjust parameter space via main loop entry point). 
Image_browser allows efficient exploration of the results visually.

The original script is `One_set_of_parameters.py`. Using OOP avoids manual typos and errors. 
See code for usage of functions and explanation of variables.


`image_browser.py` allows quick browsing of the simulations generated. `mode_detection` identifies the photonic mode
vertex energies, and then `plotting_dependencies.ipynb` visualises the results using a 3D plot.

## Classes (simulation script)
### `Pattern`
Defines the periodic structure of a patterned layer, including the period, filling factor, etc.

### `Material`
Represents a material in the waveguide, with support for dispersive and non-dispersive materials. 
It includes methods to assign patterns and create editable layers.
Assign `Pattern` object to the `.pattern` attribute to create the grating.
`Layers` objects are just `Materials` assigned a thickness.

### `Waveguide`
Holds a stack of material layers, forming the waveguide stack. Has export method fully compatible with the same
functions as the original script.

