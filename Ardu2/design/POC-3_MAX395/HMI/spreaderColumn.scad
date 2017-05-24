$fn=500;

// nut dimensions wrench, heihht, epsilon
wNut = 5.5;
hNut = 2.5;
eNut=0.2;

// column height, all the rest is computed
hCol =44;

// slot height above base and below top of column, all the rest is computed
sHeight=10;

// bolt diamenter and epsilon
dBolt=3;
eBolt=0.2;

module nut(wrench,thickness){
    // make a nut, centered at 0,0,0
    r = wrench/(2.0*cos(30));
    translate([0,0,-thickness/2.0])
        rotate([0,0,30])
        linear_extrude(height=thickness)
            circle(r,$fn=6);   
}
module slot(w,l,h){
    // make a slot centered at 0,0,0
    translate([0,0,h/2.0])
        cube([w,l,h],center=true);
}

module column(rCol,hCol){
    // make the column, based at 0,0,0
    cylinder(r=rCol,h=hCol);
}

module all(wrench,nHeight,sHeight,cHeight,bDia,nEps,bEps){
    // make a column of h=cHeight, r compute from nut wrench size,
    // with a slot+nut cutaway at sHeight above base, applying nEps
    // with a slot+nut cutaway at sHeight below the top of the column, applying nEps 
    // with a bolt diamter of bDia, applying bEps
    
    wNut=wrench+nEps;
    rNut= wNut/(2.0*cos(30));
    hNut= nHeight/2.0;
    rCyl = 2*rNut;
    difference(){
        column(rCyl,cHeight);
        #translate([0,0,sHeight]){
            nut(wrench,hNut);
            slot(wNut,4*wNut,nHeight+nEps);
        }
        #translate([0,0,cHeight-sHeight]){
            rotate([180,0,0]){
                nut(wrench,hNut);
                slot(wNut,4*wNut,nHeight+nEps);
            }
        }
        #translate([0,0,-1])
            column(bEps+bDia/2.0,cHeight+2);
    }
}


all(wNut,hNut,sHeight,hCol,dBolt,eNut,eBolt);

  