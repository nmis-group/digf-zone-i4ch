//main dim


ix = 7700;
iy = 9100;
iz = 3000;
wall_t = 100;
wx = 2700;
wy = 2700;
wz = 2500;

wood_c = "wheat";
floor_c = "Silver";
glass = [];

// floor
//color(floor_c)
//cube([ix, iy, 100]);
translate([0, 0, -100])
    color(floor_c)
    cube([ix, iy, 105]);

// entrance
translate([0, -2000, -100])
    color(floor_c)
    cube([ix, 2000, 105]);

// power & network banks
pd = 50;
pz = 150;
pz_o = 1000;
color_r = "White";

// wall a
difference(){
translate([-wall_t, -wall_t, -1])
    color(wood_c)
    cube([ix+2*wall_t, wall_t, iz]);
translate([200, -wy/2, 0])
    color("Black")
    cube([3500, wy, wz]);
};
xv = 3900;    
translate([ix-xv, 0, pz_o])
    color(color_r)
    cube([xv, pd, pz]);

// wall b
offset_b = 5000;
difference(){
translate([-wall_t, iy, -1])
    color(wood_c)
    cube([ix+2*wall_t, wall_t, iz]);
translate([offset_b-150, iy-wy/2, 0])
    color("Black")
    cube([wx, wy, wz]);
}
translate([0, iy-wall_t, pz_o])
    color(color_r)
    cube([4800, pd, pz]);

// wall c
offset_c = 6500;
difference(){
translate([-wall_t, 0, -1])
    color(wood_c)
    cube([wall_t, iy, iz]);
translate([-wx/2, offset_c-220, 0])
    color("Black")
    cube([wx, wy, wz]);
translate([-wx/2, offset_c-3100, 0])
    color("Black")
    cube([wx, wy, wz]);
}
translate([0, 0, pz_o])
    color(color_r)
    cube([pd, 3400, pz]);

// wall d
offset_d = 100;
difference(){
translate([ix, 0, -1])
    color(wood_c)
    cube([wall_t, iy, iz]);
translate([ix-wx/2, offset_d, 0])
    color("Black")
    cube([wx, wy, wz]);
translate([ix-wx/2, offset_d+3100, 0])
    color("Black")
    cube([wx, wy, wz]);
}
yv = 3200;
translate([ix-wall_t, iy-yv, pz_o])
    color(color_r)
    cube([pd, yv, pz]);

// windows
//glass_t = 0.5;
//
//translate([offset_b-150, iy+50, 0])
//    color([0.9, 0.9, 0.9, glass_t])
//    cube([wx, 10, wz]);
//
//
//translate([-50, offset_c-200, 0])
//    color([0.9, 0.9, 0.9, glass_t])
//    cube([10, wy, wz]);
//translate([-50, offset_c-3100, 0])
//    color([0.9, 0.9, 0.9, glass_t])
//    cube([10, wy, wz]);
//
//translate([ix+50, offset_d, 0])
//    color([0.9, 0.9, 0.9, glass_t])
//    cube([10, wy, wz]);
//translate([ix+50, offset_d+3100, 0])
//    color([0.9, 0.9, 0.9, glass_t])
//    cube([10, wy, wz]);



// support column
translate([ix-150, 2700, 5])
    color("black")
    cube([150, 500, iz-5]);
    
translate([ix-90, 0, 2500])
    color("black")
    cube([100, 3000, 200]);








    
