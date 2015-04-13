// Carvin ArduGuitar Button
totalZ = 9.0;
spaceAtTop = 0.5;
boxZ= totalZ+ spaceAtTop;

baseXY = 4.0;
baseZ  = 0.5;

innerXY = 3.6;//3.4;

ridgeZ = 1.0;
z1 = 2.0;
epsilon = ridgeZ * 0.15;

$fn=500;

module cyl(){
    color("Magenta"){
        cylinder(h=17.0,d=9.0);
    }
}

module base(){
    translate([0,0,baseZ/2.0]){
        color("Navy"){
            cube([baseXY,baseXY,baseZ],center=true);
        }
    }
}
module box(){
    color("Lime"){
        translate([0,0,boxZ/2.0]){
            cube([innerXY,innerXY,boxZ],center=true);
        }
    }
}


module cylHX(){
    rotate([90,0,0]){
        cylinder(r=0.3, h=innerXY,center=true);
    }
}
module cylHY(){
    rotate([0,90,0]){
        cylinder(r=0.3, h=innerXY,center=true);
    }
}
module cyls(){
    color("Red"){
        translate([innerXY/2.0+epsilon,0,baseZ+z1+ridgeZ/2.0]){
            cylHX();
        }
        translate([-(innerXY/2.0+epsilon),0,baseZ+z1+   ridgeZ/2.0]){
            cylHX();
        }
        translate([0,innerXY/2.0+epsilon,baseZ+z1+ridgeZ/2.0]){
            cylHY();
        }
        translate([0,-(innerXY/2.0+epsilon),baseZ+z1+ridgeZ/2.0]){
                cylHY();
        }
    }
}
module guts(){
    base();
    box();
}
module outside(){
    cyl();
}
module all(){
    difference(){  
        outside();
        guts();
    }
    cyls();
}
all();
