/* This is the code to be dumped to the ESP32.
Connect the MPU6050 to the ESP32 via standard I2C Pins, and connect a button to Pin 15 as a pullup button.
*/

#include<Wire.h>
#include<MPU6050.h>

MPU6050 mpu;

#define BUTTON 15 // Connect the other button pin to ground
#define SAMPLERATE 10 //100Hz

void setup()
{
  Serial.begin(115200);
  Wire.begin();
  mpu.initialize();
  pinMode(BUTTON, INPUT_PULLUP);
}

void loop()
{
  if (digitalRead(BUTTON) == HIGH)
  {
    Serial.println("IDLE");
    delay(100);
  }
  else
  {
    int16_t ax, ay, az, gx, gy, gz;
    mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

    Serial.print(ax / 16384.0, 4); Serial.print(","); # 16384 raw units ~ 1g
    Serial.print(ay / 16384.0, 4); Serial.print(",");
    Serial.print(az / 16384.0, 4); Serial.print(",");
    Serial.print(gx / 131.0, 4); Serial.print(","); # 131 raw units ~ 1'/s
    Serial.print(gy / 131.0, 4); Serial.print(",");
    Serial.print(gz / 131.0, 4);

    delay(SAMPLERATE);
  }
}
