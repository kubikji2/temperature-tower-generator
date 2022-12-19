use<floor.scad>
include <constants.scad>
include <qpp-openscad-library/qpp_all.scad>

$fn = 60;

// TEMPERATURE PARAMETERS
// '-> these arguments are overriden by program arguments
// minimal temperature
min_temp = 200;
// maximal temperature
max_temp = 230;
// temperature step
step_temp = 5;

// slope parameters
slope_left = 35;
slope_right = 45;

// computing number of layers
n_layers = ceil((max_temp-min_temp)/step_temp);

// baseplate
qpp_cylindrocube([bp_l, bp_w, bp_t, bp_cr]);

// generating tower floors
for(i=[0:n_layers])
{
    _temp = min_temp + i*step_temp;
    _z = bp_t + i*f_h;
    translate([0,0,_z])
        tower_floor(temperature=_temp, slope_left=slope_left, slope_right=slope_right); 
}
