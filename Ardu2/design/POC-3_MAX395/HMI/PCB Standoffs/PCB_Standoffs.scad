// PCB_Standoffs 
// For HMI PCB mounting to back plane

$fn = 100;
lowHeight = 5.0;
highHeight = 9.5;
m3Dia =  3.3;
extDia = 10.0;
rInt = m3Dia/2.0;
rExt = extDia/2.0;
epsilon=1;

module extCyl(height){
    cylinder(r=rExt,h=height, center=false);
}
module intCyl(height){
    translate([0,0,-epsilon/2.0])
        cylinder(r=rInt,h=height+epsilon, center=false);
}
module standoff(hi=false){
    h = hi ? highHeight : lowHeight;
    difference(){
        extCyl(h);
        intCyl(h);
    }
}
standoff(hi=true);
