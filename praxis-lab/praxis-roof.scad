// roof

rx = 2500;
ry = 3000;
rz = 20;
color_r = "White";
rxo = 1000;
ryo = 1000;
rzo = 2800;
rxo_s = rxo+3300;
ryo_s = ryo+4300;

translate([rxo, ryo, rzo])
    color(color_r)
    cube([rx, ry, rz]);

translate([rxo, ryo_s, rzo])
    color(color_r)
    cube([rx, ry, rz]);
    
translate([rxo_s, ryo, rzo])
    color(color_r)
    cube([rx, ry, rz]);
    
translate([rxo_s, ryo_s, rzo])
    color(color_r)
    cube([rx, ry, rz]);