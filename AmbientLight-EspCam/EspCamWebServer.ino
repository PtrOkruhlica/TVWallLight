#include <WebServer.h>
#include <Wifi.h>
#include <esp32cam.h>
#include <esp_camera.h>

define LED 4
const char* wifi = "XXXXXXXX";
const char* pass = "XXXXXXXX";

WebServer server(80);

static auto pic1 = esp32cam::Resolution::find(1024, 768);

void createJpg() {
  auto frame = esp32cam::capture();
  if(frame == nullptr){
    Serial.println("No data...");
    server.send(503, "", "");
    return;
  }
  Serial.println("Photo OK");
  server.setContentLength(frame->size());
  server.send(200, "image/jpeg");
  WiFiClient wifiClient = server.client();
  frame->writeTo(wifiClient);
}

void handlePicture() {
  if(!esp32cam::Camera.changeResolution(pic1)) {
    Serial.println("Wrong resolution...");
  }
  createJpg();
}

void setup() {
  
  pinMode(LED, OUTPUT);
  Serial.begin(115200);
  Serial.println();
  {
    using namespace esp32cam;
    Config cfg;
    cfg.setPins(pins::AiThinker);
    cfg.setResolution(pic1);
    cfg.setBufferCount(2);
    cfg.setJpeg(80);
    bool ok = Camera.begin(cfg);
    Serial.println(ok ? "Cam set successfully" : "Cam set unsuccessfully");
  }

  sensor_t * s = esp_camera_sensor_get();
  if( s->id.PID == OV2640_PID) {
    s->set_brightness(s,0);
    s->set_contrast(s,2);
    s->set_saturation(s,2);
    s->set_raw_gma(s,0);
  } else {
    Serial.println("Wrong choosed type of camera OVxxxx_PID");
  }

  WiFi.persistent(false);
  WiFi.mode(WIFI_STA);
  WiFi.begin(wifi, pass);
  while(WiFi.status() != WL_CONNECTED) {delay(800);}
  Serial.print("IP Address: http://");
  Serial.println(WiFi.localIP());
  server.on("/picture.jpg", handlePicture);
  server.begin();
}

void loop() {
  digitalWrite(LED, HIGH);
  server.handleClient();
}
