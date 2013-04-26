
int pixDens = 2;

void setup()
{
  //size(1196/pixDens,768/pixDens);
  orientation(LANDSCAPE);
  noStroke();
  background(0);
  colorMode(HSB, 100, 1, 1);

}
void draw()
{
  fill(dist(pmouseX, pmouseY, mouseX, mouseY),1,1);
  ellipse(mouseX, mouseY, mouseX-pmouseX, mouseY-pmouseY);
}

