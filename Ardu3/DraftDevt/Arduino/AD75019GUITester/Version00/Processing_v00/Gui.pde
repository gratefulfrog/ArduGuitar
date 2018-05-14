class Gui{
  float matrixPercentWindow = 0.6,
        matrixWidth = width*matrixPercentWindow,
        matrixHeight = height*matrixPercentWindow,
        matrixX = width*(1-matrixPercentWindow)/2.,
        matrixY = height*(1-matrixPercentWindow)/2.;
  
  int nbHorizontal = 16,
      nbVertical   = 16;
  
  float hSpace  = 10,
        vSpace  = 10;
  
  float connectionRectWidth  = (matrixWidth - hSpace*(nbHorizontal+1))/nbHorizontal,
        connectionRectHeight = (matrixHeight -vSpace*(nbVertical+1))/nbVertical;
  
  final color red   = #FF0000,
              green = #00FF00,
              blue  = #0000FF;
              
  color guiStroke = #FF0000,
        guiFill   = #0000FF;
        
  Gui(){}
  
  void matrixDisplay(String vecBits){
    display();
    pushStyle();
    stroke(blue);
    fill(blue);
    pushMatrix();
    translate(matrixX+hSpace,matrixY+vSpace);
    xDisplay(vecBits);
    yDisplay(vecBits);
    for (int i=0;i<16;i++){
      for (int j=0;j<16;j++){
        //print(vecBits.charAt(32 + (i*16)+j));
        fill(vecBits.charAt(32+(j*16)+i) == '0' ? red : green);
        rect(i*(connectionRectWidth+hSpace),
             j*(connectionRectHeight+vSpace),
             connectionRectWidth,
             connectionRectHeight);
      }
    }
    popMatrix();
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
      fill(vecBits.charAt(i) == '0' ? red : green);
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
      fill(vecBits.charAt(16+i) == '0' ? red : green);
      rect(hSpace + i*(connectionRectWidth+hSpace),
           vSpace,
           connectionRectWidth,
           connectionRectHeight);
    }
    popMatrix();
    popStyle();
  }
  
  void display(){
    pushStyle();
    stroke(blue);
    fill(blue);
    rect(matrixX,matrixY,matrixWidth,matrixHeight);
    popStyle();
  }
}
