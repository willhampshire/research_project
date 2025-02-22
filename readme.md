# RCWA Electromagnetic Simulation

RCWA simulation script, adapted from a previous version. 
Remake created by Will Hampshire. The script performs Rigorous Coupled Wave Analysis (RCWA) 
for simulating the optical properties of layered materials, using [S4 (linked)](https://web.stanford.edu/group/fan/S4/).

## venv
Python 3.10(.11).

Install requirements with ```pip install -r requirements.txt```.

Compiled S4 from source. Would not recommend compiling from the original branch (was tricky, no good documentation). 
Instead, try one of the newer forks, phoebe-p/S4 and marcus-o/S4.

## Usage
### Generating simulations (regular)
Inside `WS2_GRrating_Eamonn/`, there are scripts called `vX.X 1D grating modes.py` - 
run script to generate simulations, and adjust parameter space via main loop entry point. Results will populate 
`/Results`. `image_browser.py` allows quick browsing of the simulations generated. `mode_detection` (.py or .ipynb) 
identifies the photonic mode vertex energies, and then `plotting_dependencies.ipynb` visualises the results using 
a 3D plot. The original simulation script is `One_set_of_parameters.py`. Using OOP avoids manual typos and errors. 
See code for usage of functions and explanation of variables.

### Generating simulations (asymmetry)
Instead of generating the full images, we can explore asymmetry through generating the kx=0 array, and plotting.
`v1.4a Asymmetry Dependance.py` (where 1.4a means it was adapted from v1.4) can be run across a large range of 
alpha much faster to plot the kx=0 profiles as Wavelength vs Alpha. Plotting is accomplished with `asymmetry_kx0_json.ipynb`, 
which reads the summary `.json` and saves the plot back to the directory.

### Other
`plotting_dependancies.ipynb` plots the dependency of the energy gap and central position against primarily period and 
thickness, colour coded by filling factor.

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



