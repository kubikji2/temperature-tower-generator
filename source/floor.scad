include<constants.scad>
include<qpp-openscad-library/qpp_constants.scad>

$fn = 120;

module __slope(ang=45, right=false)
{
    // rotation angle
    _ang = right ? -ang : ang;
    // lenght of the cut
    _l = 2*ss_l;
    // cut x offset
    _c_x_off = right ? -ss_l : 0;
    // hole x offset
    _h_x_off = right ? ss_l - ss_off - ss_d/2 : ss_off + ss_d/2;

    difference()
    {
        // basic geometry
        cube([ss_l, f_w, f_h]);

        // slope
        translate([-_c_x_off,0,f_h])
            rotate([0,_ang,0])
                translate([_c_x_off,-qpp_eps,-f_h])
                    cube([_l, f_w+2*qpp_eps, f_h]);
        
        // hole
        translate([_h_x_off,f_w/2,0])
            cylinder(d=ss_d, h=f_h+qpp_eps);
    }
}

module floor(temperature="")
{
    _temp = str(temperature);


    __slope();

}

