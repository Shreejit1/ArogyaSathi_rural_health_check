#ArogyaSathi
____________
______________________________
# 🌿 Rural Health Risk Checker


---

## 🎯 Problem Statement
Rural communities in India and similar regions often lack access to doctors. People develop serious illnesses (Malaria, Typhoid, TB, Dengue, Anemia) because they don't recognize early warning signs or delay seeking help. 

**This tool provides instant, simple health risk screening** — no internet required after deployment, no medical jargon, no smartphone expertise needed.

---

## 🚀 What It Does (MVP Features)
1. **Symptom Input** — 22 checkboxes covering the most common rural disease symptoms
2. **Risk Factor Selection** — Environmental & lifestyle factors (water source, mosquito nets, sanitation)
3. **AI-style Risk Scoring** — Weighted algorithm checks against 6 major rural diseases
4. **Risk Report** — Color-coded risk levels (High/Medium/Low) with % score
5. **Actionable Precautions** — Disease-specific, plain-language next steps
6. **Offline-capable** — Works in browser without backend if needed

---

## 🦠 Diseases Covered
| Disease | Key Symptoms Checked |
|---|---|
| Malaria | Fever, chills, sweating, headache |
| Typhoid | Fever, stomach pain, diarrhea |
| Tuberculosis | Weeks-long cough, weight loss, night sweats |
| Anemia | Pale skin, fatigue, dizziness |
| Dengue | Fever, rash, joint pain, eye pain |
| Diarrheal Disease | Diarrhea, vomiting, dehydration |

---

## 🛠️ Tech Stack
- **Backend**: Python + Flask (REST API)
- **Frontend**: Pure HTML/CSS/JS (no framework needed)
- **Deployment**: Single `python app.py` command

---

## ▶️ How to Run

```bash
# 1. Install dependencies
pip install flask

# 2. Run the server
python app.py

# 3. Open browser
# → http://localhost:5000
```

The frontend (`index.html`) can also be opened **directly in a browser** — it includes a built-in JavaScript fallback that mirrors the Python scoring logic, so it works 100% offline too.

---

## 📡 API Endpoints

### POST `/api/check-risk`
```json
{
  "age": 35,
  "gender": "female",
  "symptoms": ["fever", "chills", "headache"],
  "risk_factors": ["standing_water", "no_mosquito_net"]
}
```
**Response:**
```json
{
  "risks": [
    {
      "disease": "Malaria",
      "risk_score": 72,
      "risk_level": "High",
      "matched_symptoms": ["fever", "chills", "headache"],
      "matched_factors": ["standing_water", "no_mosquito_net"],
      "precautions": ["Sleep under a mosquito net every night", "..."]
    }
  ],
  "total_analyzed": 6
}
```

### GET `/api/diseases`
Returns all diseases, symptoms, and risk factors supported.

---

## ⚠️ Disclaimer
This tool is for **awareness and early screening only**. It does NOT replace professional medical diagnosis. Always visit a Primary Health Centre (PHC) or doctor for proper evaluation.

---

## 🏆 Hackathon Impact
- **Target Users**: Rural populations in India, Africa, Southeast Asia
- **Access**: Works on low-end smartphones via browser, no app install
- **Scalability**: Can add more diseases, languages (Hindi/regional), voice input
- **Next Steps**: SMS-based interface, ASHA worker integration, multilingual support
