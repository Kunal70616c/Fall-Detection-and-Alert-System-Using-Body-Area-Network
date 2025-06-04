# Fall Detection and Alert System Using Body Area Network

[![Project Status](https://img.shields.io/badge/Status-67%25%20Complete-orange)]()
[![Hardware](https://img.shields.io/badge/Hardware-ESP8266-blue)]()
[![ML Model](https://img.shields.io/badge/ML-Python-green)]()
[![Mobile](https://img.shields.io/badge/Mobile-Flutter-cyan)]()
[![Cloud](https://img.shields.io/badge/Cloud-Render-purple)]()

## 🚀 Project Overview

An intelligent IoT-based healthcare monitoring system that combines wearable sensors, machine learning, and mobile technology to detect falls in real-time and provide immediate emergency alerts. This comprehensive solution is designed to enhance safety for elderly individuals and people at risk of falls.

## 📋 Table of Contents

- [Features](#features)
- [System Architecture](#system-architecture)
- [Components](#components)
- [Project Status](#project-status)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [Future Enhancements](#future-enhancements)
- [License](#license)

## ✨ Features

- **Real-time Health Monitoring**: Continuous tracking of heart rate, body temperature, and motion
- **AI-Powered Fall Detection**: Machine learning model trained on 370,000+ data points
- **GPS Location Tracking**: Precise location identification for emergency response
- **Automated Alert System**: Instant email notifications to emergency contacts
- **Nearby Hospital Locator**: Location-based identification of nearby healthcare facilities
- **Health Data Translation**: AI-powered interpretation of health metrics (upcoming)
- **Mobile Dashboard**: Flutter-based mobile application for real-time monitoring (upcoming)
- **Cloud Integration**: Scalable cloud infrastructure for data processing

## 🏗️ System Architecture

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐
│   Wrist Band    │────│  ThingSpeak  │────│  Cloud Backend  │
│   (Sensors)     │    │   Platform   │    │   (ML + Alerts) │
└─────────────────┘    └──────────────┘    └─────────────────┘
         │                                            │
         │              ┌──────────────┐              │
         └──────────────│ Flutter App  │──────────────┘
                        │   (Mobile)   │
                        └──────────────┘
```

## 🔧 Components

### 1. **Hardware Wrist Band** ✅ *Completed*

**Sensors Integrated:**
- **MAX30100**: Heart rate and SpO2 sensor
- **DS18B20**: Digital temperature sensor
- **MPU6050**: 6-axis accelerometer and gyroscope
- **Neo 6M GPS**: Location tracking module
- **NodeMCU (ESP8266)**: Main microcontroller

**Data Pipeline:**
- Real-time sensor data collection
- WiFi connectivity for data transmission
- Integration with ThingSpeak IoT platform

### 2. **ML Fall Detection Model** ✅ *Completed*

**Model Specifications:**
- **Dataset Size**: 370,000+ data points
- **Classes**: Fall vs Non-Fall detection
- **Output Files**: `model.pkl` and `scaler.pkl`
- **Accuracy**: High precision binary classification
- **Integration**: Real-time processing of ThingSpeak data

### 3. **Location-Based Alert System** ✅ *Completed*

**Features:**
- GPS coordinate processing
- Nearby hospital and healthcare center identification
- SMTP email alert system via Gmail
- Emergency contact notification
- Location-aware response system

### 4. **Bio-GPT Health Translation** ❌ *Pending*

**Planned Features:**
- Hugging Face Bio-GPT API integration
- Health data interpretation and translation
- BMI calculation and health insights
- User-friendly health metric explanations
- Personalized health recommendations

### 5. **Cloud Infrastructure** ✅ *Completed*

**Deployment Details:**
- **Platform**: Render cloud deployment
- **Services**: ML model hosting, alert system backend
- **API Endpoints**: Real-time data processing
- **Data Source**: Live ThingSpeak integration
- **Scalability**: Auto-scaling cloud architecture

### 6. **Flutter Mobile Application** ❌ *Pending*

**Planned Features:**
- User registration and profile management
- Real-time health dashboard
- Live sensor data visualization
- Fall detection status monitoring
- Heart rate charts and trends
- Bio-GPT health translations display
- Emergency contact management

## 📊 Project Status

| Component | Status | Progress |
|-----------|--------|----------|
| Hardware Wrist Band | ✅ Complete | 100% |
| ML Fall Detection | ✅ Complete | 100% |
| Alert System | ✅ Complete | 100% |
| Cloud Infrastructure | ✅ Complete | 100% |
| Bio-GPT Integration | ❌ Pending | 0% |
| Flutter Mobile App | ❌ Pending | 0% |

**Overall Progress: 67% Complete (4/6 modules)**

## 🛠️ Technologies Used

### Hardware
- ESP8266 (NodeMCU)
- MAX30100 Heart Rate Sensor
- DS18B20 Temperature Sensor
- MPU6050 Accelerometer/Gyroscope
- Neo 6M GPS Module

### Software & Platforms
- **Programming Languages**: Python, C++ (Arduino), Dart (Flutter)
- **IoT Platform**: ThingSpeak
- **Machine Learning**: Python (Scikit-learn/TensorFlow)
- **Cloud Platform**: Render
- **Mobile Framework**: Flutter
- **AI Integration**: Hugging Face Bio-GPT API
- **Communication**: SMTP Gmail API
- **Data Format**: JSON, CSV

## 🚀 Installation

### Prerequisites
- Python 3.8+
- Arduino IDE
- Flutter SDK (for mobile app)
- ThingSpeak account
- Gmail account for SMTP
- Render account for cloud deployment

### Hardware Setup
1. Connect all sensors to NodeMCU according to the wiring diagram
2. Flash the Arduino code to NodeMCU
3. Configure WiFi credentials and ThingSpeak API keys
4. Assemble components into wristband housing

### Software Setup
```bash
# Clone the repository
git clone https://github.com/Kunal70616c/Fall-Detection-and-Alert-System-Using-Body-Area-Network.git
cd Fall-Detection-and-Alert-System-Using-Body-Area-Network

# Install Python dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your API keys and credentials
```

### Cloud Deployment
1. Deploy ML model and alert system to Render
2. Configure ThingSpeak channel integration
3. Set up SMTP email credentials
4. Test API endpoints

## 📱 Usage

### For End Users
1. **Setup**: Wear the wristband and ensure proper sensor contact
2. **Monitoring**: Real-time health data is automatically collected
3. **Fall Detection**: System automatically detects falls and sends alerts
4. **Mobile App**: Use Flutter app to monitor health metrics (when available)

### For Developers
```python
# Example: Using the ML model
from fall_detection import FallDetectionModel

model = FallDetectionModel()
prediction = model.predict(sensor_data)
print(f"Fall Detected: {prediction}")
```

## 📡 API Documentation

### Endpoints

#### Health Data Endpoint
```
GET /api/health-data
Returns: Current sensor readings and health metrics
```

#### Fall Detection Endpoint
```
POST /api/fall-detection
Body: Sensor data array (accelerometer, heart rate, temperature)
```

**Response Format:**
```json
// When fall is detected
{
    "status": "success",
    "fall_detected": true,
    "location": {
        "latitude": 22.5726,
        "longitude": 88.3639
    }
}

// When no fall is detected
{
    "status": "success",
    "fall_detected": false
}
```

#### Alert System Endpoint
```
POST /api/send-alert
Body: Location and user data
Returns: Alert status and nearby hospitals
```

## 🤝 Contributing

We welcome contributions to improve this fall detection system!

### How to Contribute
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Areas Needing Contribution
- [ ] Bio-GPT integration module
- [ ] Flutter mobile application development
- [ ] UI/UX improvements
- [ ] Additional sensor integration
- [ ] Testing and validation
- [ ] Documentation improvements

## 🔮 Future Enhancements

### Immediate (Next Phase)
- [ ] Complete Bio-GPT health data translation
- [ ] Develop and deploy Flutter mobile application
- [ ] Implement user authentication system
- [ ] Add data visualization charts

### Long-term Vision
- [ ] Multi-user family monitoring dashboard
- [ ] Integration with hospital emergency systems
- [ ] Advanced predictive health analytics
- [ ] Wearable device miniaturization
- [ ] Voice assistant integration
- [ ] Telemedicine platform integration

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Kunal Pal** - [Kunal70616c](https://github.com/Kunal70616c)
**Indranil Kundu** - [Orton1269](https://github.com/Orton1269)

## 🙏 Acknowledgments

- ThingSpeak for IoT platform services
- Hugging Face for Bio-GPT API
- Open source sensor libraries and communities
- Contributors and testers

## 📞 Support

For support, email kunal.cs.dev@outlook.com or create an issue in this repository.

---

⭐ **Star this repository if you found it helpful!**

**Made with ❤️ for safer living**
