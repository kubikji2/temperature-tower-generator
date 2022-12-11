include<constants.scad>
include<qpp-openscad-library/qpp_constants.scad>
include<qpp-openscad-library/qpp_utils.scad>

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

module __curves()
{
    // TODO
    cube([cs_l, f_w, f_h]);
}

module __bridge()
{
    
}

module floor(temperature="")
{
    _temp = str(temperature);


    _tf_1 = [bp_cr, bp_cr, 0];
    translate(_tf_1)
        __slope(ang=35, right=false);
    
    _tf_2 = qpp_add_vec(_tf_1,[ss_l,0,0]);
    translate(_tf_2)
        __curves();
    
    _tf_3 = qpp_add_vec(_tf_2,[cs_l,0,0]);
    translate(_tf_3)
        __bridge();
    
    _tf_4 = qpp_add_vec(_tf_3,[bs_l,0,0]);
    translate(_tf_4)
        __slope(ang=45, right=true);

}

