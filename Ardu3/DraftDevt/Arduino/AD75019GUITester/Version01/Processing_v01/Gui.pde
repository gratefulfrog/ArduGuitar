class Gui{
  
  final String xLabelVec[] ={"A+","A-",
                             "B+","B-",
                             "C+","C-",
                             "D+","D-",
                             "E+","E-",
                             "F+","F-",
                             "xx","xx",
                             "xx","xx"},
               yLabelVec[] ={"B+","B-",
                             "C+","C-",
                             "D+","D-",
                             "E+","E-",
                             "F+","F-",
                             "O+","O-",
                             "xx","xx",
                             "xx","xx"};
                             
  
  final int nbHorizontal = 16,
            nbVertical   = 16;
  
  final float hSpace  = 10,
              vSpace  = 10;
  
  final float matrixPercentWindow = 0.6,
              matrixWidth = width*matrixPercentWindow,
              matrixHeight = height*matrixPercentWindow,
              matrixX = width*(1-matrixPercentWindow)/2.,
              matrixY = height*(1-matrixPercentWindow)/2.,
              alertDeltaX = ((matrixWidth-hSpace)+(width-(matrixX+matrixWidth)))/2.,
              alertDeltaY = -vSpace;
  
  final float autoExecXCenter = (2*matrixX+matrixWidth/2.)/2.,
              connectToggleXCenter = autoExecXCenter + matrixWidth/2.,
              toggleYCenter = (height + matrixY+matrixHeight)/2.,
              toggleWidth   = 0.66 *  matrixWidth/2.,
              toggleHeight  = 0.66 *(height - (matrixY+matrixHeight));
  
  final int clickEpsilon =  5;
  
  final float connectionRectWidth  = (matrixWidth - hSpace*(nbHorizontal+1))/nbHorizontal,
              connectionRectHeight = (matrixHeight -vSpace*(nbVertical+1))/nbVertical;
        
  final float toggleCornerArray[][] = {// {x0,y0,x1,y1}
                                        // autoexe button
                                       {autoExecXCenter - toggleWidth/2.  - clickEpsilon,
                                        toggleYCenter   - toggleHeight/2. - clickEpsilon,
                                        autoExecXCenter + toggleWidth/2.  + clickEpsilon,
                                        toggleYCenter   + toggleHeight/2. + clickEpsilon},
                                       {// All connections button
                                        connectToggleXCenter - toggleWidth/2.  - clickEpsilon,
                                        toggleYCenter        - toggleHeight/2. - clickEpsilon,
                                        connectToggleXCenter + toggleWidth/2.  + clickEpsilon,
                                        toggleYCenter        + toggleHeight/2. + clickEpsilon},
                                       {// X area
                                        matrixX -4*hSpace - connectionRectWidth - clickEpsilon,
                                        matrixY                                 - clickEpsilon,
                                        matrixX -2*hSpace                       + clickEpsilon,
                                        matrixY + matrixHeight                  + clickEpsilon},
                                       {// connection array
                                        matrixX                                 - clickEpsilon,
                                        matrixY                                 - clickEpsilon,
                                        matrixX + matrixWidth                   + clickEpsilon,
                                        matrixY + matrixHeight                  + clickEpsilon}};
                                       
                                        
  
  final int labelSizeVec[] = {30,30};
  final int smallLabelSize = 14;
  final float toggleXYArray[][] = {{autoExecXCenter,toggleYCenter},
                                   {connectToggleXCenter, toggleYCenter}};
  final String toggleLabelVec[] = {"Auto\nExec",
                                   "Connections\nL: Off  R:On"},
               xLabel        = "X Pins",
               yLabel        = "Y Pins",
               computedLable = "Theoretical\nOutputs";
                                   
  
  final float alertW = 2*connectionRectWidth,
              alertH = 2*connectionRectHeight;
  
  final color red   = #FF0000,
              green = #00FF00,
              blue  = #0000FF,
              yellow = #FFFF00,
              black  = #000000;
              
  boolean xPinValues[],
          yPinValues[],
          yCalculatedValues[];
        
  Gui(){
    xPinValues         = new boolean[16];
    yPinValues         = new boolean[16];
    yCalculatedValues  = new boolean[16];
    for (int i=0;i<16;i++){
      yCalculatedValues[i] = xPinValues[i] = yPinValues[i]=false;
    }
  }
  
  boolean isTrue(char c){
    return c== '1';
  }
  void displayFrame(){
    pushStyle();
    stroke(blue);
    fill(blue);
    rect(matrixX,matrixY,matrixWidth,matrixHeight);
    popStyle();
  }
  
  void matrixDisplay(String reversedBits){
    pushStyle();
    for (int i=0;i<16;i++){
      for (int j=0;j<16;j++){
        fill(isTrue(reversedBits.charAt((i*16)+j)) ? green : red);
        rect(i*(connectionRectWidth+hSpace),
             j*(connectionRectHeight+vSpace),
             connectionRectWidth,
             connectionRectHeight);
      }
    }
    popStyle();
  }
  
  void xDisplay(String vecBits){
    pushStyle();
    pushMatrix();
    translate(-(5*hSpace) - connectionRectWidth,-vSpace);
    rect(0,
         0,
         2*hSpace + connectionRectWidth,
         vSpace + 16*(connectionRectHeight+vSpace));
    for (int i=0;i<16;i++){
      // first the boxes
      //xPinValues[i] = isTrue(vecBits.charAt(i));
      //fill(xPinValues[i] ? green : red);
      fill(green);
      rect(hSpace,
           vSpace + i*(connectionRectHeight+vSpace),
           connectionRectWidth,
           connectionRectHeight);
      // now the labels
      pushStyle();
      pushMatrix();
      translate((2*hSpace+connectionRectWidth)/2.,
                i*(connectionRectHeight+vSpace) + (3*vSpace+connectionRectHeight)/2.);
      rectMode(CENTER);
      textAlign(CENTER);
      fill(0);
      textSize(smallLabelSize);
      //text(String.valueOf(i),0,0);
      text(xLabelVec[i],0,0);
      popMatrix();
      popStyle();
    }
    popMatrix();
    popStyle();
  }
  void yDisplay(String vecBits){
    pushStyle();
    pushMatrix();
    translate(-hSpace, -(5*vSpace) - connectionRectHeight);
    rect(0,
         0,
         hSpace + 16*(connectionRectWidth+hSpace),
         2*vSpace + connectionRectHeight);
    for (int i=0;i<16;i++){
      //yPinValues[i]= isTrue(vecBits.charAt(16+i));
      //fill(yPinValues[i] ? green : red);
      fill(green);
      rect(hSpace + i*(connectionRectWidth+hSpace),
           vSpace,
           connectionRectWidth,
           connectionRectHeight);
      // now the labels
      pushStyle();
      pushMatrix();
      translate(i*(connectionRectWidth+hSpace) +(2*hSpace+connectionRectWidth)/2.,
               (3*vSpace+connectionRectHeight)/2.);
      rectMode(CENTER);
      textAlign(CENTER);
      fill(0);
      textSize(14);
      //text(String.valueOf(i),0,0);
      text(yLabelVec[i],0,0);
      popMatrix();
      popStyle();
    }
    popMatrix();
    popStyle();
  }
  
  
  void alert(boolean good){
    pushStyle();
    pushMatrix();
    stroke(blue);
    translate(-(5*hSpace) - connectionRectWidth,
              -(10*vSpace) - connectionRectHeight);
    fill(good ? green : red);
    rect(0,0,alertW,alertH);
    popMatrix();
    popStyle();   
  }
  
  void displayToggle(int index, boolean active){
    pushStyle();
    pushMatrix();
    stroke(blue);
    if (index==0){
      fill(active ? green : red); 
    }
    else{
      fill(yellow);
    }
    rectMode(CENTER);
    textAlign(CENTER,CENTER);
    textSize(labelSizeVec[index]);
    translate(toggleXYArray[index][0],
              toggleXYArray[index][1]);
    rect(0,0,toggleWidth, toggleHeight);
    fill(black);
    text(toggleLabelVec[index],0,0);
    popMatrix();
    popStyle();
  }
  
  void displayLabels(){
    pushStyle();
    pushMatrix();
    // X inputs
    translate((toggleCornerArray[2][0] + toggleCornerArray[2][2])/2.,
              toggleCornerArray[2][3] + connectionRectHeight);
    fill(yellow);
    textSize(smallLabelSize);
    textAlign(CENTER,CENTER);
    rectMode(CENTER);
    text(xLabel,0,0);
    // Y outputs
    popMatrix();
    pushMatrix();
    translate(matrixX + matrixWidth + 1.5*connectionRectWidth,
              matrixY -1.5*(vSpace + connectionRectHeight));
    text(yLabel,0,0);
    // Computed values
    //translate(0,-3*vSpace -connectionRectHeight);
    //text(computedLable,0,0);
    popMatrix();
    popStyle();
  }
  
  void displayFixedElts(boolean autoExecOn){
    for (int i=0; i< toggleLabelVec.length; i++){
      displayToggle(i,autoExecOn);
    }
    displayLabels();
  }
  
  void display(String vecBits, boolean autoExecOn){
    displayFrame();
    pushStyle();
    stroke(blue);
    fill(blue);
    pushMatrix();
    translate(matrixX+hSpace,matrixY+vSpace);
    xDisplay(vecBits);
    yDisplay(vecBits);
    String reversedBits = new StringBuffer(vecBits.substring(32)).reverse().toString(); 
    matrixDisplay(reversedBits);
    //calculatedYDisplay(reversedBits);
    popMatrix();
    popStyle();
    displayFixedElts(autoExecOn);
  }
  
  int findBoxId(float md,float base, float end, float space, float box){
    float low  = base + space/2.,
          high = low + box + space,
          lastHigh = base;
    int   index = 0;
    
    while(high<=end){
      if ((md>= lastHigh) && (md < high)){
        return index;
      }
      else{
        index++;
        lastHigh=high;
        high+= box + space;
      }
    }
    return -99; // not found
  }
  
  int isAnXbutton(int mX,int mY){
    final int i = 2;
    int res = -99;
    if((mX > toggleCornerArray[i][0]) &&
       (mY > toggleCornerArray[i][1]) &&
       (mX < toggleCornerArray[i][2]) &&
       (mY < toggleCornerArray[i][3])){
         return findBoxId(mY,
                          toggleCornerArray[i][1],
                          toggleCornerArray[i][3],
                          vSpace, 
                          connectionRectHeight);
       }
       return -99;
  }
 
  int isAMatrixButton(int mX,int mY){
    final int i = 3;
    int res = -99;
    if((mX > toggleCornerArray[i][0]) &&
       (mY > toggleCornerArray[i][1]) &&
       (mX < toggleCornerArray[i][2]) &&
       (mY < toggleCornerArray[i][3])){
         int xPin =   findBoxId(mY,
                                toggleCornerArray[i][1],
                                toggleCornerArray[i][3],
                                vSpace, 
                                connectionRectHeight),
             yPin =   findBoxId(mX,
                                toggleCornerArray[i][0],
                                toggleCornerArray[i][2],
                                hSpace, 
                                connectionRectWidth);
       res = 255+nbVertical - (16*yPin + xPin) ;  
       // because the array is reversed and starts afer the 16 Xinput values! 
     }
     return res;
  }
    
  int getMouseAction(int mX,int mY){
    for (int i=0;i<toggleLabelVec.length;i++){
      if ((mX > toggleCornerArray[i][0]) &&
          (mY > toggleCornerArray[i][1]) &&
          (mX < toggleCornerArray[i][2]) &&
          (mY < toggleCornerArray[i][3])){
        return i-2;
      }
    }
    // we are still looking
    int res = isAnXbutton(mX,mY);
    return (res>=0) ? res : isAMatrixButton(mX,mY);
  }
}
  
