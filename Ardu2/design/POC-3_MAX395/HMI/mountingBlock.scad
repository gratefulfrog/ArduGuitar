$fn=100;

// nut dimensions wrench, height, epsilon
/*  UNUSED
wNut = 5.5;
hNut = 2.5;
eNut = 0.2;
*/

// column height, all the rest is computed
hCol = 44;

// block height,width,depth
hBlock = 45;
wBlock = 25;
dBlock = 33;

// slot height above base and below top of column, all the rest is computed
sHeight=10;

// dBolt depthwise offset from face away from guitar
dOffset = dBlock/3.;

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

// single hol cylindrical spacer
dCy = 20.0;
hCy = hBlock;

module cyPlate(){
    color("green")
    //scale([1,1,1])
        cylinder(d=dCy-ePlate,h=hPlate,center=true);
}

module cyBlock(hh,dd){
   color("SteelBlue")
       translate([0,0,hh/2.0])
           cylinder(d=dd, h=hh, center=true);
} 

module plate(){
    color("green")
    scale([1,ratioPlate,1])
        cylinder(d=wPlate-ePlate,h=hPlate,center=true);
}
/* UNUSED
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
*/
module column(rCol,hCol){
    // make the column, based at 0,0,0
    cylinder(r=rCol,h=hCol);
} 
    
module block(hh,w,d,rr=2,rounded=true){
    // make a block centered at 0,0,0
    color("SteelBlue")
    if (!rounded){
        translate([0,0,hh/2.0]){
            cube([w,d,hh], center=true);
        }
    }
    else{
        x = w/2.-rr;
        y = d/2.-rr;
        hull(){
            translate([-x,-y,0])
                cylinder(r=rr,h=hh);
            translate([-x,y,0])
                cylinder(r=rr,h=hh);
            translate([x,-y,0])
                cylinder(r=rr,h=hh);
            translate([x,y,0])
                cylinder(r=rr,h=hh);
        }
    }
}
        
module all(cHeight,bDia,bEps,low, smallBlock){
    // make a column of h=cHeight, 
    // with a bolt diamter of bDia, applying bEps
    
    hh = low ? hOffset/2.0 : hOffset;
    db = smallBlock ? dBlock/2. : dBlock;
    do = smallBlock ? 0 : dOffset;
    difference(){  
        union(){
            translate([0,smallBlock? db/2. :0,0])
                block(hBlock,wBlock,db);
            translate([0,db/2.0-do,-5])
                plate();
            translate([0,db/2.0-do,hBlock+5])
                plate();
        }
        
        // holes for vertical bolts
        #translate([wBlock/4.0,db/2.0-do,-10])
            column(bEps+bDia/2.0,cHeight+20);
        #translate([-wBlock/4.0,db/2.0-do,-10])
            column(bEps+bDia/2.0,cHeight+20);
        // hole for horizontal bolt
        if (!smallBlock){
            #translate([0,0,hh])
                rotate([90,0,0])
                translate([0,0,-db/2.-1])
                column(eBolt+hBolt/2.0,db+2,center=true);
            }
    }
}

module cyAll(cHeight,bDia,bEps){
    // make a cylindrical column of h=cHeight, 
    // with a bolt diamter of bDia, applying bEps   
    difference(){        
        union(){
            cyBlock(hCy,dCy);
            translate([0,0,-5])
                cyPlate();
            translate([0,0,hCy+5])
                cyPlate();
        }
        // hole for vertical bolt
        #translate([0,0,-10])
            column(bEps+bDia/2.0,cHeight+20);
    }
}

translate([-wBlock-5,0,0]){   
    all(hCol,dBolt,eBolt,true,false);
    translate([wBlock+5,0,0]){
        all(hCol,dBolt,eBolt,false,false);
        translate([wBlock+5,0,0]){
            cyAll(hCy,dBolt,eBolt);
        }
    }
}

