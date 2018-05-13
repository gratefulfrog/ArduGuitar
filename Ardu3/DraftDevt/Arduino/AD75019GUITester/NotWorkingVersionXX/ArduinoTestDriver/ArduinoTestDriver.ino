/*  Gratefulfrog
 *  2018 05 12
*/

#define BAUD_RATE (115200)

#include "app.h"

App *app;

void setup() {
  app = new App(BAUD_RATE);
}
void loop() {
  app->loop();
}
