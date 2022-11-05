// top
translate([0, 0, 690])
    color("White")
    cube([750, 2050 , 40]);

// legs
translate([10, 10, 0])
    color("White")
    cube([60, 80 , 690]);
    
translate([680, 10, 0])
    color("White")
    cube([60, 80 , 690]);
    
translate([10, 10, 200])
    color("White")
    cube([700, 80, 60]);
    
translate([10, 1950, 0])
    color("White")
    cube([60, 80, 690]);
    
translate([680, 1950, 0])
    color("White")
    cube([60, 80, 690]);
    
translate([10, 1950, 200])
    color("White")
    cube([700, 80, 60]);
    
// standalone

translate([100, 150, 0]){
    color("Black")
    cube([500, 250, 500]);
}
translate([100, 450, 0]){
    color("Black")
    cube([500, 250, 500]);
}
translate([100, 750, 0]){
    color("Black")
    cube([500, 250, 500]);
}
translate([100, 1050, 0]){
    color("Black")
    cube([500, 250, 500]);
}
translate([100, 1350, 0]){
    color("Black")
    cube([500, 250, 500]);
}
translate([100, 1650, 0]){
    color("Goldenrod")
    cube([600, 250, 650]);
}