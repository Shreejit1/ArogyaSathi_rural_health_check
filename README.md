# ArogyaSathi_rural_health_check
ArogyaSaathi is a Flask-based web application with a pure HTML/CSS/JavaScript frontend, implementing a rule-based risk scoring engine for health assessment. It processes user symptoms and risk factors via REST APIs, supports offline fallback logic in JavaScript, and modularly handles general, menstrual, PCOD, and mental health analysis.
Here’s a **clean, professional README.md** you can directly paste into your repo:

---

# 🌿 ArogyaSaathi

### *Screen • Inform • Protect*

ArogyaSaathi is a lightweight, offline-capable health risk screening tool designed to enable early disease detection and awareness, especially in rural and underserved communities.

---

## 🎯 Problem

Many rural populations lack timely access to healthcare. As a result, diseases like malaria, dengue, typhoid, and anemia often go undetected until they become severe.

---

## 🚀 Solution

ArogyaSaathi provides a simple interface where users can:

* Select symptoms and risk factors
* Get instant risk analysis
* Receive clear, actionable health guidance

---

## 🧠 Features

* 🩺 General health risk assessment (6 major diseases)
* 🌸 Menstrual health tracking & cycle prediction
* 🔬 PCOD risk analysis
* 🧠 Mental health screening
* 📊 Color-coded risk reports (High / Medium / Low)
* 🌐 Works offline (frontend fallback logic)
* 📱 Mobile-friendly, simple UI

---

## 🦠 Diseases Covered

* Malaria
* Typhoid
* Tuberculosis
* Dengue
* Anemia
* Diarrheal Diseases

---

## 🛠️ Tech Stack

* **Backend:** Python (Flask)
* **Frontend:** HTML, CSS, JavaScript
* **Architecture:** REST API + Offline JS fallback

---

## ▶️ How to Run

```bash
# Install dependencies
pip install flask

# Run the app
python app.py
```

Open in browser:

```
http://localhost:5000
```

---

## 📡 API Example

### POST `/api/check-risk`

```json
{
  "age": 30,
  "gender": "female",
  "symptoms": ["fever", "chills"],
  "risk_factors": ["standing_water"]
}
```

---

## ⚠️ Disclaimer

This tool is for **awareness and early screening only**.
It does NOT replace professional medical advice.
Always consult a doctor or visit a PHC for proper diagnosis.

---

## 🌍 Impact

* Designed for **low-resource environments**
* Works on **basic smartphones**
* No app install required
* Scalable with more diseases & languages

---

## 📌 Future Improvements

* Multilingual support (Hindi, regional languages)
* Voice input for low-literacy users
* SMS-based access
* Integration with ASHA workers

---

If you want, I can also:

* Add **badges (stars, license, tech icons)**
* Or make it look like a **top GitHub trending repo README** 🔥
