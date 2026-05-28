const int pinEMG = 34; 

void setup() {
  Serial.begin(115200);
  analogReadResolution(12); // Configura el ADC a 12 bits (0-4095)
}

void loop() {
  int valorRaw = analogRead(pinEMG);
  float voltaje = (valorRaw * 3.3) / 4095.0; // Convierte a Voltios
  
  // Envía los datos separados por una coma a Python
  Serial.print(valorRaw);
  Serial.print(",");
  Serial.println(voltaje, 4); 
  
  delay(10); // Muestreo controlado a ~100 Hz
}
