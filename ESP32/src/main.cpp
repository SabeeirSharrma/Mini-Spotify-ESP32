#include <Arduino.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

String line1 = "";
String line2 = "";
String incoming = "";

void redraw() {
    lcd.clear();

    lcd.setCursor(0, 0);
    lcd.print(line1.substring(0, 16));

    lcd.setCursor(0, 1);
    lcd.print(line2.substring(0, 16));
}

void setup() {
    Serial.begin(115200);

    Wire.begin(21, 22);

    lcd.init();
    lcd.backlight();

    lcd.setCursor(0, 0);
    lcd.print("Waiting for");

    lcd.setCursor(0, 1);
    lcd.print("Spotify...");
}

void loop() {
    while (Serial.available()) {

        char c = Serial.read();

        if (c == '\r')
            continue;

        if (c == '\n') {

            if (incoming.startsWith("1:")) {
                line1 = incoming.substring(2);
                line1.trim();
                redraw();
            }
            else if (incoming.startsWith("2:")) {
                line2 = incoming.substring(2);
                line2.trim();
                redraw();
            }

            incoming = "";
        }
        else {
            incoming += c;
        }
    }
}