#include <Wire.h>
#include <MPU6050.h>
#include "MAX30100_PulseOximeter.h"
#include <ESP8266WiFi.h>
#include <time.h>

// WiFi Credentials (optional if you want time sync)
const char* ssid = "Kunal's S23";
const char* password = "12345678";

// Sensor setup
MPU6050 mpu;
PulseOximeter pox;
#define REPORTING_PERIOD_MS 1000
uint32_t tsLastReport = 0;

// Time setup
const char* ntpServer = "pool.ntp.org";
const long gmtOffset_sec = 0;
const int daylightOffset_sec = 0;

void onBeatDetected() {
  Serial.println("Beat!");
}

void setup() {
  Serial.begin(115200);
  Wire.begin(D2, D1); // I2C SDA = D2, SCL = D1 on ESP8266

  // Connect to WiFi (optional)
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500); Serial.print(".");
  }
  Serial.println("\nWiFi connected");

  // Time Sync
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
  Serial.println("Syncing time...");
  while (time(nullptr) < 100000) delay(100);

  // Initialize MAX30100
  if (!pox.begin()) {
    Serial.println("MAX30100 initialization failed. Check wiring.");
    while (1);
  }
  Serial.println("MAX30100 ready.");
  pox.setOnBeatDetectedCallback(onBeatDetected);

  // Initialize MPU6050
  mpu.initialize();
  if (!mpu.testConnection()) {
    Serial.println("MPU6050 connection failed.");
    while (1);
  }
  Serial.println("MPU6050 ready.");
}

void loop() {
  pox.update();  // must be called frequently

  if (millis() - tsLastReport > REPORTING_PERIOD_MS) {
    tsLastReport = millis();

    // Get MPU6050 data
    int16_t ax_raw, ay_raw, az_raw, gx_raw, gy_raw, gz_raw;
    mpu.getMotion6(&ax_raw, &ay_raw, &az_raw, &gx_raw, &gy_raw, &gz_raw);

    float ax = ax_raw / 16384.0;
    float ay = ay_raw / 16384.0;
    float az = az_raw / 16384.0;

    float gx = gx_raw / 131.0;
    float gy = gy_raw / 131.0;
    float gz = gz_raw / 131.0;

    // Heart rate
    float heartRate = pox.getHeartRate();

    // Time
    time_t now = time(nullptr);
    struct tm* timeinfo = localtime(&now);
    char timeStr[30];
    strftime(timeStr, sizeof(timeStr), "%Y-%m-%d %H:%M:%S", timeinfo);

    // Print all data
    Serial.print("ax: "); Serial.print(ax, 3); Serial.print(" g, ");
    Serial.print("ay: "); Serial.print(ay, 3); Serial.print(" g, ");
    Serial.print("az: "); Serial.print(az, 3); Serial.print(" g, ");
    Serial.print("gx: "); Serial.print(gx, 3); Serial.print(" deg/s, ");
    Serial.print("gy: "); Serial.print(gy, 3); Serial.print(" deg/s, ");
    Serial.print("gz: "); Serial.print(gz, 3); Serial.print(" deg/s, ");

    if (heartRate > 30 && heartRate < 220) {
      Serial.print("Heart Rate: "); Serial.print(heartRate); Serial.print(" bpm, ");
    } else {
      Serial.print("Heart Rate: --- , ");
    }

    Serial.print("Time: "); Serial.println(timeStr);
  }
}