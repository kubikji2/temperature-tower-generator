use<floor.scad>
include <constants.scad>
include <interface.scad>
include <qpp-openscad-library/qpp_all.scad>

$fn = 60;

// minimal temperature
min_temp = 200;
// maximal temperature
max_temp = 230;
// temperature step
step_temp = 5;

// number of layers
n_layers = ceil((max_temp-min_temp)/step_temp);

// baseplate
qpp_cylindrocube([bp_l, bp_w, bp_t, bp_cr]);

for(i=[0:n_layers])
{
    _temp = min_temp + i*step_temp;
    _z = bp_t + i*f_h;
    translate([0,0,_z])
        tower_floor(temperature=_temp); 
}
