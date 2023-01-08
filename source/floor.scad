include<constants.scad>
include<qpp-openscad-library/qpp_constants.scad>
include<qpp-openscad-library/qpp_utils.scad>
include<qpp-openscad-library/qpp_basic_geometries.scad>

// customizable sloped segments
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
    _t_x_off = right ? bs_b_t : ss_l-bs_b_t;

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

        
        // degrees
        rotate([90,0,0])
            translate([_t_x_off,f_h-bs_b_t, -t_d+qpp_eps])
                linear_extrude(t_d)
                    text(text=str(ang, "°"), size=3, halign= right ? "left" : "right", valign="top");
    }
}

// customizable curvature segments
module __curves(temp)
{
    // hole dimensions
    _h_x = cs_l - 2*bs_b_t;
    _h_y = f_w-2*bs_b_t;
    _h_z = f_h - 2*bs_b_t;

    difference()
    {
        // main block
        cube([cs_l, f_w, f_h]);
        
        // carving hole
        translate([(cs_l-_h_x)/2, f_w-_h_y, (f_h-_h_z)/2])
        {
            // carving cube
            cube([_h_x-_h_z+qpp_eps, _h_y+qpp_eps, _h_z]);

            // carving arch
            translate([_h_x-_h_z,qpp_eps,0])
                rotate([-90,0,0])
                    qpp_cylinder_sector(h=_h_y,r=_h_z+qpp_eps,sector=[270,360]);

        }
        
        // temperature
        rotate([90,0,0])
            translate([cs_l/2,f_h/2, -t_d+qpp_eps])
                linear_extrude(t_d)
                    text(text=str(temp), size=6, halign="center", valign="center");
        
        // hole in the wall
        translate([cs_l-_h_x+qpp_eps,f_w/2,f_h/2])
            rotate([0,90,0])
                cylinder(d=ss_d, h=_h_x);

    }

    // right curvature
    translate([(cs_l-_h_x)/2,f_w-_h_y,f_h/2+_h_z/4])
        rotate([-90,0,0])
            qpp_cylinder_sector(h=_h_y,d=_h_z,sector=[0,90]);
    
}

// bridge segment
module __bridge()
{
    // bridge
    translate([0,0,f_h-bs_b_t])
        cube([bs_l, f_w, bs_b_t]); 
    
    // bigger cylinder
    _tf_c = [0, f_w/2, 0];
    translate(qpp_add_vec(_tf_c, [bs_c_off,0,0]))
        cylinder(d1=bs_c_D, d2=0, h=bs_c_h);

    // smaller cylinder
    translate(qpp_add_vec(_tf_c, [bs_l-bs_c_off,0,0]))
        cylinder(d1=bs_c_d, d2=0, h=bs_c_h);

    // block
    translate([bs_l/2-bs_b_l/2, 0, 0])
        cube([bs_b_l,bs_b_t,bs_b_h]);
}

// tower floor as a collection of segments
module tower_floor(temperature="230", slope_left=35, slope_right=45)
{
    // temperature string
    _temp_s = str(temperature);

    // left slope segment
    _tf_1 = [bp_cr, bp_cr, 0];
    translate(_tf_1)
        __slope(ang=slope_left, right=false);
    
    // curvaturse segment including temperature
    _tf_2 = qpp_add_vec(_tf_1,[ss_l,0,0]);
    translate(_tf_2)
        __curves(temp=_temp_s);
    
    // bridging segment
    _tf_3 = qpp_add_vec(_tf_2,[cs_l,0,0]);
    translate(_tf_3)
        __bridge();
    
    // right slope segment
    _tf_4 = qpp_add_vec(_tf_3,[bs_l,0,0]);
    translate(_tf_4)
        __slope(ang=slope_right, right=true);

}

