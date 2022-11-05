include <praxis-outer.scad>
//include <praxis-roof.scad>

translate([50, 9050, 5]){
    rotate([0, 0, 270]){
    include <praxis-workbench.scad>;
    }
}
translate([1300, 9050, 1200]){
    rotate([0, 0, 90]){
    include <praxis-wall-screens.scad>;
    }
}

translate([1550, 9050, 5]){
    rotate([0, 0, 270]){
    include <praxis-workbench.scad>;
    }
}
translate([2800, 9050, 1200]){
    rotate([0, 0, 90]){
    include <praxis-wall-screens.scad>;
    }
}

translate([3050, 9050, 5]){
    rotate([0, 0, 270]){
    include <praxis-workbench.scad>;
    }
}
translate([4300, 9050, 1200]){
    rotate([0, 0, 90]){
    include <praxis-wall-screens.scad>;
    }
}

translate([1550, 6100, 5]){
    rotate([0, 0, 90]){
    include <praxis-workbench.scad>;
    }
}
translate([3050, 6100, 5]){
    rotate([0, 0, 90]){
    include <praxis-workbench.scad>;
    }
}
translate([4550, 6100, 5]){
    rotate([0, 0, 90]){
    include <praxis-workbench.scad>;
    }
}





// desks
translate([1600, 3500, 5]){
    rotate([0, 0, 90]){
    include <praxis-workstation-pc.scad>;
    }
}
translate([3100, 3500, 5]){
    rotate([0, 0, 90]){
    include <praxis-workstation-pc.scad>;
    }
}
translate([4600, 3500, 5]){
    rotate([0, 0, 90]){
    include <praxis-workstation-pc.scad>;
    }
}

translate([100, 3500, 5]){
    rotate([0, 0, 270]){
    include <praxis-workstation-pc.scad>;
    }
}

translate([1600, 3500, 5]){
    rotate([0, 0, 270]){
    include <praxis-workstation-pc.scad>;
    }
}

translate([3100, 3500, 5]){
    rotate([0, 0, 270]){
    include <praxis-workstation-pc.scad>;
    }
}


translate([7600, 7000, 5]){
    rotate([0, 0, 180]){
    include <praxis-workstation-pc.scad>;
    }
}
translate([7600, 5500, 5]){
    rotate([0, 0, 180]){
    include <praxis-workstation-pc.scad>;
    }
}

//screens

translate([100, 600, 1400]){
    rotate([0, 0, 0]){
    include <praxis-wall-screen-large.scad>;
    }
}
translate([7600, 8500, 1400]){
    rotate([0, 0, 180]){
    include <praxis-wall-screen-large.scad>;
    }
}

translate([7400, 0, 1400]){
    rotate([0, 0, 90]){
    include <praxis-wall-screen-large.scad>;
    }
}

// server
translate([7500, 0, 5]){
    rotate([0, 0, 90]){
    include <praxis-servers-standalone.scad>;
    }
}
translate([7000, 8300, 5]){
    rotate([0, 0, 0]){
    include <praxis-servers.scad>;
    }
}
translate([7000, 7700, 5]){
    rotate([0, 0, 0]){
    include <praxis-servers.scad>;
    }
}
translate([7000, 7100, 5]){
    rotate([0, 0, 0]){
    include <praxis-servers.scad>;
    }
}