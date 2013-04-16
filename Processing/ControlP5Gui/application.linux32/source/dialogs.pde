// dialogs tab

boolean bigG = false,
        isRename = false;

String small = "16x16",
       big   = "22x22",
       imageName[] = { "go-jump-3-",
                       "format-text-strikethrough-2-",
                       "list-add-3-", 
                       "list-remove-3-",
                       "document-save-3-",
                       "document-open-5-"},
       imageExt  = ".png";

String getImage(int i) {
  if (bigG){
  return imageName[i] + big + imageExt;
  }
  else{
  return imageName[i] + small + imageExt;
  }
}

boolean initButtons(ControlP5 cp5) {
  //String image = getImage();  
  int x1 = rectLb[x],
      y1 = rectV[y];
      
  Button b0 =  cp5.addButton("writeCurrentButton")
                 .setValue(0)
                 .setPosition(x1,y1)
                 .registerTooltip("Write Current Preset")
                 .setImage(loadImage(getImage(0)))
                 .updateSize()
                 ;
 
  x1 += b0.getWidth();
  Button b1 = cp5.addButton("renameCurrentButton")
                 .setValue(1)
                 .setPosition(x1,y1)
                 .registerTooltip("Rename Current Preset")
                 .setImage(loadImage(getImage(1)))
                 .updateSize()
                 ;
  x1 += b1.getWidth();                 ;
  Button b2 = cp5.addButton("writeNewButton")
                 .setValue(2)
                 .setPosition(x1,y1)
                 .registerTooltip("Create New Preset")
                 .setImage(loadImage(getImage(2)))
                 .updateSize()
                 ;
  x1 += b2.getWidth();                 ;
  Button b3 = cp5.addButton("deleteCurrentButton")
                 .setValue(3)
                 .setPosition(x1,y1)
                 .registerTooltip("Delete Current Preset")
                 .setImage(loadImage(getImage(3)))
                 .updateSize()
                 ;
  x1 += b3.getWidth();                 ;
  Button b4 = cp5.addButton("saveButton")
                 .setValue(4)
                 .setPosition(x1,y1)
                 .registerTooltip("Save Preset File")
                 .setImage(loadImage(getImage(4)))
                 .updateSize()
                 ;
  x1 += b4.getWidth();                 ;
  Button b5 = cp5.addButton("openButton")
                 .setValue(5)
                 .setPosition(x1,y1)
                 .registerTooltip("Open Preset File")
                 .setImage(loadImage(getImage(5)))
                 .updateSize()
                 ;
  cp5.getTooltip().getLabel().toUpperCase(false);
  println("Buttons initialized.");   
  return true;
}  

/*
void writeCurrentButton(int val){
  println("writeCurrentButton received " + val);
}
*/

void renameCurrentButton(int val){
  if (allInit){
    isRename = true;
    println("renameCurrentButton received " + val);
    l.setVisible(false);
    t.setText(l.captionLabel().getText());  
    t.setVisible(true);
    t.setFocus(true);
    t.keepFocus(true);
  }
}

void writeNewButton(int val){
  if (allInit){
    println("writeNewButton received " + val);
    l.setVisible(false);
    t.setText(newPresetDefaultName);  
    t.setVisible(true);
    t.setFocus(true);
    t.keepFocus(true);
  }
}

/*

void deleteCurrentButton(int val){
  println("deleteCurrentButton received " + val);
}

void saveButton(int val){
  println("saveButton received " + val);
}


void openButton(int val){
  println("openButton received " + val);
 
}

*/


