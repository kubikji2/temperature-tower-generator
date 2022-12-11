// Dimensions

// SLOPE segment parameters
ss_l = 15;
// '-> slope length
ss_d = 3;
// '-> slope hole diameter
ss_off = 2;
// '-> slope hole offset 

// BRIDGE segment parameters
bs_l = 30;
// '-> bridge length
bs_t = 1;
// '-> bridge thickness
bs_c_off = 5;
// '-> cone center offset
bs_c_d = 3;
// '-> smaller cone diameter
bs_c_D = 5;
// '-> bigger cone diameter
bs_c_h = 5;
// '-> cones height
bs_b_t = 1.5;
// '-> block thickness
bs_b_l = 6;
// '-> block length
bs_b_h = bs_c_h;
// '-> block height

// CURVE segment parameters
// '-> TODO
cs_l = 15;
// '-> curvature segment legth


// FLOOR parameters
f_h = 10;
// '-> floor height
f_w = 10;
// '-> floor widths
f_l = ss_l + bs_l + cs_l + ss_l; 

// BASE PLATE parameters
bp_cr = 5;
// '-> baseplate corner radius
bp_l = 2*bp_cr + f_l;
// '-> baseplate length
bp_w = 2*bp_cr + f_w;
// '-> baseplate width
bp_t = 1;
// '-> baseplate thickness

// TEXT perameters
t_d = 0.5;
// '-> text depth