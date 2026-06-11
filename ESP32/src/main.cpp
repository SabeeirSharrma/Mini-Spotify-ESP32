#include <Arduino.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

String line1 = "";
String line2 = "";
String incoming = "";

int scroll1 = 0;
int scroll2 = 0;

unsigned long lastScroll = 0;
const unsigned long scrollDelay = 350; // ms

void drawLine(uint8_t row, const String& text, int offset) {
    lcd.setCursor(0, row);

    if (text.length() <= 16) {
        String padded = text;

        while (padded.length() < 16) {
            padded += " ";
        }

        lcd.print(padded);
        return;
    }

    String scrollText = text + "    ";

    for (int i = 0; i < 16; i++) {
        int index = (offset + i) % scrollText.length();
        lcd.print(scrollText[index]);
    }
}

void redraw() {
    drawLine(0, line1, scroll1);
    drawLine(1, line2, scroll2);
}

void setup() {
    Serial.begin(115200);

    Wire.begin(21, 22);

    lcd.init();
    lcd.backlight();

    lcd.clear();

    line1 = "Waiting for";
    line2 = "Spotify...";

    redraw();
}

void handleMessage(String message) {
    message.trim();

    if (message.startsWith("1:")) {
        line1 = message.substring(2);
        scroll1 = 0;
        redraw();
    }
    else if (message.startsWith("2:")) {
        line2 = message.substring(2);
        scroll2 = 0;
        redraw();
    }
}

void loop() {

    while (Serial.available()) {
        char c = Serial.read();

        if (c == '\r') {
            continue;
        }

        if (c == '\n') {
            handleMessage(incoming);
            incoming = "";
        }
        else {
            incoming += c;
        }
    }

    unsigned long now = millis();

    if (now - lastScroll >= scrollDelay) {

        bool needsRedraw = false;

        if (line1.length() > 16) {
            scroll1++;

            if (scroll1 >= line1.length() + 4) {
                scroll1 = 0;
            }

            needsRedraw = true;
        }

        if (line2.length() > 16) {
            scroll2++;

            if (scroll2 >= line2.length() + 4) {
                scroll2 = 0;
            }

            needsRedraw = true;
        }

        if (needsRedraw) {
            redraw();
        }

        lastScroll = now;
    }
}