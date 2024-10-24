# RCWA Electromagnetic Simulation

RCWA simulation script, adapted from a previous version by `ph1pbx`. 
Remake created by Will Hampshire. The script performs Reflective Coupled Wave Analysis (RCWA) 
for simulating the optical properties of layered materials, using [S4 (linked)](https://web.stanford.edu/group/fan/S4/).

## Script
Please run the `1D grating modes.py` script. The use of the classes is an intuitive upgrade that avoids errors. 
The original script is `One_set_of_parameters.py`. See code for usage of functions and explanation of variables.

## Classes
### `Pattern`
Defines the periodic structure of a patterned layer, including the period, filling factor, etc.

### `Material`
Represents a material in the waveguide, with support for dispersive and non-dispersive materials. 
It includes methods to assign patterns and create editable layers.
Assign `Pattern` object to the `.pattern` attribute to create the grating.
Layers are just Materials but with a thickness.

### `Waveguide`
Holds a stack of material layers, forming the waveguide stack.

