class Gui{
  final int nbHorizontal = 16,
            nbVertical   = 16;
  
  final float hSpace  = 10,
              vSpace  = 10;
  
  float matrixPercentWindow = 0.6,
        matrixWidth = width*matrixPercentWindow,
        matrixHeight = height*matrixPercentWindow,
        matrixX = width*(1-matrixPercentWindow)/2.,
        matrixY = height*(1-matrixPercentWindow)/2.,
        alertDeltaX = ((matrixWidth-hSpace)+(width-(matrixX+matrixWidth)))/2.,
        alertDeltaY = -vSpace;
  
  
  
  float connectionRectWidth  = (matrixWidth - hSpace*(nbHorizontal+1))/nbHorizontal,
        connectionRectHeight = (matrixHeight -vSpace*(nbVertical+1))/nbVertical;
        
  float alertW = 2*connectionRectWidth,
        alertH = 2*connectionRectHeight;
  
  final color red   = #FF0000,
              green = #00FF00,
              blue  = #0000FF;
              
  color guiStroke = #FF0000,
        guiFill   = #0000FF;
        
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
        fill(isTrue(reversedBits.charAt((j*16)+i)) ? green : red);
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
      xPinValues[i] = isTrue(vecBits.charAt(i));
      fill(xPinValues[i] ? green : red);
      rect(hSpace,
           vSpace + i*(connectionRectHeight+vSpace),
           connectionRectWidth,
           connectionRectHeight);
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
      yPinValues[i]= isTrue(vecBits.charAt(16+i));
      fill(yPinValues[i] ? green : red);
      rect(hSpace + i*(connectionRectWidth+hSpace),
           vSpace,
           connectionRectWidth,
           connectionRectHeight);
    }
    popMatrix();
    popStyle();
  }
  
  boolean shouldBeOn(int xi, int yj, String reversedBits){
    return xPinValues[xi] && isTrue(reversedBits.charAt(16*xi+yj));
  }           
  
  boolean yShouldBeOn(int yi,String reversedBits){
    for (int xi=0;xi<16;xi++){
      if (shouldBeOn(xi, yi, reversedBits)){
        return true;
      }
    }
    return false;
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
  
  
  void calculatedYDisplay(String reversedBits){
    for (int yi=0;yi<16;yi++){
      yCalculatedValues[yi]=yShouldBeOn(yi,reversedBits);
    }
    pushStyle();
    pushMatrix();
    translate(-hSpace, -(10*vSpace) - connectionRectHeight);
    rect(0,
         0,
         hSpace + 16*(connectionRectWidth+hSpace),
         2*vSpace + connectionRectHeight);
    boolean error = false;
    for (int i=0;i<16;i++){
      fill(yCalculatedValues[i] ? green : red);
      rect(hSpace + i*(connectionRectWidth+hSpace),
           vSpace,
           connectionRectWidth,
           connectionRectHeight);
      boolean currentError = (yCalculatedValues[i] != yPinValues[i]);
      error |= currentError;
      if(currentError){
        pushStyle();
        noStroke();
        fill(red);
        rect(i*(connectionRectWidth+hSpace),
             0,
             connectionRectWidth+2*hSpace,
             connectionRectHeight+2*vSpace);
        popStyle();
        rect(hSpace + i*(connectionRectWidth+hSpace),
           vSpace,
           connectionRectWidth,
           connectionRectHeight);
      }
    }
    popMatrix();
    popStyle();
    alert(!error);
  }
  
  void display(String vecBits){
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
    calculatedYDisplay(reversedBits);
    popMatrix();
    popStyle();
  }
  
}
  
