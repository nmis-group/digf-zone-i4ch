include <praxis-outer.scad>
//include <praxis-roof.scad>

translate([100, 7500, 5]){
    include <praxis-workbench.scad>;
}
translate([100, 6000, 5]){
    include <praxis-workbench.scad>;
}


translate([2000, 7500, 5]){
    include <praxis-workbench.scad>;
}
translate([2000, 6000, 5]){
    include <praxis-workbench.scad>;
}

translate([4000, 7500, 5]){
    include <praxis-workbench.scad>;
}
translate([4000, 6000, 5]){
    include <praxis-workbench.scad>;
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
translate([1100, 9050, 1600]){
    rotate([0, 0, 90]){
    include <praxis-wall-screens.scad>;
    }
}
translate([2950, 9050, 1600]){
    rotate([0, 0, 90]){
    include <praxis-wall-screens.scad>;
    }
}
translate([4800, 9050, 1600]){
    rotate([0, 0, 90]){
    include <praxis-wall-screens.scad>;
    }
}
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