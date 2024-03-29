use<floor.scad>
include <constants.scad>

include <solidpp/cubepp.scad>
include <solidpp/modifiers/modifiers.scad>

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
module baseplate(material="???", printer="???")
{
    difference()
    {
        // baseplate
        size = [bp_l, bp_w, bp_t];
        mod_list = [round_edges(r=bp_cr)];
        cubepp(size, mod_list=mod_list);

        _tw = bp_w-2*bp_cr;
        _tl = bp_l-2*bp_cr;
        mirror([0,1,0])
        translate([bp_cr,-bp_w/2,-eps])
        linear_extrude(0.2)
        {
            // material label
            text(text=material, size=0.5*_tw, halign="left", valign="bottom");
            // printer label
            translate([_tl,0,0])
                text(text=printer, size=0.5*_tw, halign="right", valign="top");
        }
    }
}

// printing material
material = "PLA";
// printer name
printer = "generic printer";

// MAIN
baseplate(material=material,printer=printer);

// generating tower floors
for(i=[0:n_layers])
{
    _temp = min_temp + i*step_temp;
    _z = bp_t + i*f_h;
    translate([0,0,_z])
        tower_floor(temperature=_temp, slope_left=slope_left, slope_right=slope_right); 
}
