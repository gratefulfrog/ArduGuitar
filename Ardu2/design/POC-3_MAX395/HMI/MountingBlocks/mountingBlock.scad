$fn=100;

// nut dimensions wrench, height, epsilon
/*  UNUSED
wNut = 5.5;
hNut = 2.5;
eNut = 0.2;
*/

// guitar max thickness at butt
hGuitar = 44;

// block height,width,depth
hBlock = 55;
wBlock = 25;
dBlock = 33;


// slot height above base and below top of column, all the rest is computed
sHeight=10;

// dBolt depthwise offset from face away from guitar
dOffset = dBlock/3.;

//hBolt hole offset from base
hOffset = hBlock-hGuitar/2.0; // high hole centered
hlOffset =  28.25;  // low hole average of 28 and 28.5

// bolt diamenters and epsilon
dBolt = 3;
hBolt = 4;
eBolt = 0.2;

// oval cover plate, ratio of ovality 2/1
hPlate = 3;
wPlate = wBlock;
ePlate=1;
ratioPlate = 0.5;

// single hole cylindrical spacer
dCy = 20.0;
hCy = hBlock;

// drilling jig
// 
hPanel = 3.0;
jigEpsilon = 0.2;
wJigCol = 5;
wJigHole = 5 + jigEpsilon;
hJig =  hPlate;
hJigCol = 2*hJig+ hPanel;
wJig = wBlock;
dJig = 50;
dColBack = 23;

module jigCol(wid,h){
    cube([wid,wid,hJigCol], center=true);
}
module jigCols(doCol){
    colY = -dJig+dColBack;
    color("SteelBlue")
    if(doCol){
        translate([-wJig/6,colY,hJigCol/2.])
            jigCol(wJigCol,hJigCol);
    }
    else{
        #translate([wJig/6,colY,0])
            jigCol(wJigHole,hJigCol);
    }
}
module jigPlate(){
    db = dBlock;
    do = dOffset;
    bDia = dBolt;
    bEps = eBolt;
    difference(){  
        union(){
            block(hJig,wJig,dBlock);
            translate([0,(dBlock-dJig)/2.,0])
              block(hJig,wJig,dJig);
        }
        // holes for vertical bolts
        #translate([wBlock/4.0,db/2.0-do,-10])
            column(bEps+bDia/2.0,hBlock+20);
        #translate([-wBlock/4.0,db/2.0-do,-10])
            column(bEps+bDia/2.0,hBlock+20);
    }
}

module jigAll(){
    difference(){
        color("SteelBlue")
        union(){
            jigPlate();
            jigCols(true);
        }
        jigCols(false);
    }
}
                
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
        
module all(cHeight,bDia,bEps,low, blocks,plates){
    // make a column of h=cHeight, 
    // with a bolt diamter of bDia, applying bEps
    
    hh =  (low ? hlOffset : hOffset);
    db = dBlock;
    do = dOffset;
    difference(){  
        union(){
            if (blocks)
                block(hBlock,wBlock,db);
            if (plates>0){
                translate([0,db/2.0-do,-5])
                    plate();
            }
            if (plates>1){
                translate([0,db/2.0-do,hBlock+5])
                    plate();
            }
        }
        
        // holes for vertical bolts
        #translate([wBlock/4.0,db/2.0-do,-10])
            column(bEps+bDia/2.0,hBlock+20);
        #translate([-wBlock/4.0,db/2.0-do,-10])
            column(bEps+bDia/2.0,hBlock+20);
        // hole for horizontal bolt
        if (blocks){
            #translate([0,0,hh])
                rotate([90,0,0])
                    translate([0,0,-db/2.-1])
                        column(eBolt+hBolt/2.0,db+2,center=true);
        }
    }
}


module triPlate(hh=3.0,rr=2){
    // make a block centered at 0,0,0
    //color("SteelBlue")
    x = 33/2.0-rr;
    y = 34.0-rr;
    bDia = dBolt;
    bEps = eBolt;
    difference(){
        hull(){
            translate([-x,-y,0])
                cylinder(r=rr,h=hh);
            translate([x,-y,0])
                cylinder(r=rr,h=hh);
            translate([0,0,0])
                cylinder(r=10,h=hh);
        }
        // hole for vertical bolt
        #translate([0,0,-10])
            column(bEps+bDia/2.0,hh+20);
    }
}
module triAll(){
    difference(){
        color("SteelBlue")
        union(){
            triPlate();
            jigCols(true);
        }
        jigCols(false);
    }
}
module cyAll(cHeight,bDia,bEps, cols, plates){
    // make a cylindrical column of h=cHeight, 
    // with a bolt diamter of bDia, applying bEps   
    difference(){        
        union(){
            if (cols){
                cyBlock(cHeight,dCy);
            }
            if (plates>0){
                translate([0,0,-5])
                    cyPlate();
            }
            if (plates>1){
                translate([0,0,cHeight+5])
                    cyPlate();
            }
        }
        // hole for vertical bolt
        #translate([0,0,-10])
            column(bEps+bDia/2.0,cHeight+20);
    }
}

module showThemAll(){
    translate([-wBlock-5,0,0]){   
        all(hBlock,dBolt,eBolt,true,1,2);
        translate([wBlock+5,0,0]){
            all(hBlock,dBolt,eBolt,false,1,2);
            translate([wBlock+5,0,0]){
                cyAll(hCy,dBolt,eBolt,1,2);
            }
        }
    }
}

//showThemAll();
//
module blockAll(low,blocks,plates){
   all(hBlock,dBolt,eBolt,low, blocks, plates);
}


//cyAll(hJig,dBolt,eBolt,1,0);
//blockAll(true,1,0);
//showThemAll();    
//echo("low hole vertical offset", hlOffset);
//echo("high hole vertical offset", hBlock - hOffset);

//jigCols();
//jigPlate();
//jigAll();
triAll();