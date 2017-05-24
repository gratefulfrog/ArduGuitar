$fn=100;

// nut dimensions wrench, height, epsilon
wNut = 5.5;
hNut = 2.5;
eNut = 0.2;

// column height, all the rest is computed
hCol = 44;

// block height,width,depth
hBlock = 44;
wBlock = 25;
dBlock = 50;

// slot height above base and below top of column, all the rest is computed
sHeight=10;

// dBolt depthwise offset from face away from guitar
dOffset = 15;

//hBolt hole offset from base
hOffset = hBlock/2.0; // centered

// bolt diamenters and epsilon
dBolt = 3;
hBolt = 4;
eBolt = 0.2;

// oval cover plate, ratio of ovality 2/1
hPlate = 3;
wPlate = wBlock;
ePlate=1;
ratioPlate = 0.5;

module plate(){
    color("green")
    scale([1,ratioPlate,1])
        cylinder(d=wPlate-ePlate,h=hPlate,center=true);
}

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
module block(h,w,d){
    // make a block centered at 0,0,0
    color("SteelBlue")
    translate([0,0,h/2.0]){
        cube([w,d,h], center=true);
    }
}
module all(wrench,nHeight,sHeight,cHeight,bDia,nEps,bEps, low){
    // make a column of h=cHeight, r compute from nut wrench size,
    // with a slot+nut cutaway at sHeight above base, applying nEps
    // with a slot+nut cutaway at sHeight below the top of the column, applying nEps 
    // with a bolt diamter of bDia, applying bEps
    
    wNut=wrench+nEps;
    rNut= wNut/(2.0*cos(30));
    hNut= nHeight/2.0;
    rCyl = 2*rNut;
    hh = low ? hOffset/2.0 : hOffset;
    difference(){
        //column(rCyl,cHeight);
        union(){
            block(hBlock,wBlock,dBlock);
            translate([0,dBlock/2.0-dOffset,-5])
                plate();
            translate([0,dBlock/2.0-dOffset,hBlock+5])
                plate();
        }
        // slots for nuts, through and through??
        // no longer needed! Just use long vertical bolts!
        /*
        #translate([0,dBlock/2.0-dOffset,sHeight]){
            rotate([0,0,90]){
                nut(wrench,hNut);
                slot(wNut,5*wNut,nHeight+nEps);
            }
        }
        #translate([0,dBlock/2.0-dOffset,cHeight-sHeight]){
            rotate([180,0,90]){
                nut(wrench,hNut);
                slot(wNut,5*wNut,nHeight+nEps);
            }
        }
        */
        // holes for vertical bolts
        #translate([wBlock/4.0,dBlock/2.0-dOffset,-10])
            column(bEps+bDia/2.0,cHeight+20);
        #translate([-wBlock/4.0,dBlock/2.0-dOffset,-10])
            column(bEps+bDia/2.0,cHeight+20);
        // hole for horizontal bolt
        #translate([0,0,hh])
            rotate([90,0,0])
            translate([0,0,-dBlock/2.-1])
            column(eBolt+hBolt/2.0,dBlock+2,center=true);
    }
}


all(wNut,hNut,sHeight,hCol,dBolt,eNut,eBolt,true);

translate([wBlock+5,0,0])
    all(wNut,hNut,sHeight,hCol,dBolt,eNut,eBolt,false);

//block(hBlock,wBlock,dBlock);
//rotate([90,0,0])
  //  translate([0,0,-dBlock/2.-1])
    //column(eBolt+hBolt/2.0,dBlock+2,center=true);
  //plate();