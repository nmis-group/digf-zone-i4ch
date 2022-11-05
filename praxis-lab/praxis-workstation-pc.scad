// top
translate([0, 0, 690])
    color("White")
    cube([750, 1500 , 40]);

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
    
translate([10, 1400, 0])
    color("White")
    cube([60, 80, 690]);
    
translate([680, 1400, 0])
    color("White")
    cube([60, 80, 690]);
    
translate([10, 1400, 200])
    color("White")
    cube([700, 80, 60]);
    
// pc + monitor

translate([300, 450, 750]){
    color("Black")
    cube([8, 600 , 400]);
    translate([-50, 225, 0]){
        color("Black")
        cube([15, 100, 200]);
    }
    translate([-50, 225, 0]){
        color("Black")
        cube([100, 150, 15]);
    }
    translate([-45, 225, 150]){
        color("Black")
        cube([45, 50, 50]);
    }
    translate([200, 125, 0]){
        color("Black")
        cube([100, 350, 20]);
    }
    translate([150, 600, 0]){
        color("Black")
        cube([100, 50, 20]);
    }
    translate([-200, -350, 0]){
        color("Black")
        cube([400, 180, 270]);
    }      
}

// chair
translate([950, 750, 400]){
    color("White")
    cylinder(h=30, r1=250, r2=250, center=true); 
}

translate([950, 750, 0]){
    color("White")
    cylinder(h=400, r1=80, r2=80, center=false); 
}

translate([1250, 750, 700]){
    color("White")
    rotate([0, 90, 0])
    cylinder(h=30, r1=250, r2=250, center=true); 
}