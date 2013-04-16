// listBox tests

import controlP5.*;

ListBox l;
Textfield t;

String newName = "",
       newPresetDefaultName = "New";

int itemH = 60, //21,
    nbItems = 11;
int rectLb[] ={0,0,0,0};
              /*{3*rectP[0]+rectP[2], 
                3*itemH, 
                win[x]-rectP[x]-3*rectP[0]-rectP[2], 
                nbItems*itemH}; 
                */

boolean initListBox(ControlP5 cp5) {  
  rectLb[0] = 3*rectP[0]+rectP[2] ;
  rectLb[1] = 3*itemH; 
  rectLb[2] = win[x]-rectP[x]-3*rectP[0]-rectP[2]; 
  rectLb[3] = nbItems*itemH;
  //ControlP5.printPublicMethodsFor(ListBoxItem.class);
  t = cp5.addTextfield("newName")
     .setPosition(rectLb[x], rectLb[y] - itemH )
     .setSize(rectLb[dX], itemH )
     .setFont(createFont("Free Sans",12))
     .setFocus(false)
     .setColor(labelColor)
     .setLabel("")
     ;
  t.setVisible(false);
  
  l = cp5.addListBox("presets")
         .setPosition(rectLb[x], rectLb[y])
         .setSize(rectLb[dX], rectLb[dY])           
         .setItemHeight(itemH)
         .setBarHeight(itemH)
         .setColorForeground(itemForegroundColor)
         .setColorActive(itemActiveColor)
         .setColorLabel(labelColor)
         ;
  l.toUpperCase(false);
  l.captionLabel().toUpperCase(false);
  l.captionLabel().set("Presets");
  l.captionLabel().setColor(labelColor);
  l.captionLabel().style().marginTop = 3;
  l.valueLabel().style().marginTop = 3;
  l.captionLabel().setFont(createFont("Free Sans",12));
  l.valueLabel().setFont(createFont("Free Sans",12));
  l.valueLabel().toUpperCase(false);

  loadData(l);  
  l.captionLabel().set(l.getItem(0).getName());
  l.disableCollapse();
  println ("listBox initialized.");
  return true;
}

void loadData(ListBox l){
  for (int i = 0 ; i < presetsA.size(); i++) {
    String []line = (String[])presetsA.get(i);
    println("Loading listBox item: " + line[0]);
    ListBoxItem lbi = l.addItem(line[0], i);
    lbi.setColorBackground(itemBackgroundColor);
  }
}

void loadPreset(int n){
  l.setValue(0);
}


