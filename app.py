"""
Rural Health Risk Checker — Enhanced Flask Backend
Includes: General Risk, Menstrual Health, PCOD Analysis, Mental Health
Run: pip install flask && python app.py
"""

from flask import Flask, request, jsonify, send_from_directory
from datetime import datetime, timedelta
import statistics

app = Flask(__name__, static_folder=".")

# ══════════════════════════════════════════════════════════════════
#  GENERAL DISEASE RISK ENGINE
# ══════════════════════════════════════════════════════════════════
DISEASE_RULES = {
    "Malaria":           {"conditions": ["fever","chills","headache","sweating","fatigue"],             "risk_factors": ["standing_water","no_mosquito_net","forest_area"], "weight": 1.4},
    "Typhoid":           {"conditions": ["fever","stomach_pain","diarrhea","weakness","loss_of_appetite"], "risk_factors": ["unclean_water","open_defecation","hand_washing_no"], "weight": 1.3},
    "Tuberculosis":      {"conditions": ["cough_weeks","weight_loss","night_sweats","chest_pain","blood_in_cough"], "risk_factors": ["crowded_living","smoker","tb_contact"], "weight": 1.5},
    "Anemia":            {"conditions": ["fatigue","pale_skin","dizziness","shortness_of_breath","weakness"], "risk_factors": ["poor_diet","pregnant"], "weight": 1.1},
    "Dengue":            {"conditions": ["fever","headache","eye_pain","joint_pain","rash"],             "risk_factors": ["standing_water","no_mosquito_net","urban_fringe"], "weight": 1.3},
    "Diarrheal Disease": {"conditions": ["diarrhea","stomach_pain","vomiting","dehydration"],           "risk_factors": ["unclean_water","hand_washing_no","open_defecation"], "weight": 1.2},
}

PRECAUTIONS = {
    "Malaria":           ["Sleep under a mosquito net every night","Drain standing water near your home","Wear long-sleeved clothing at dusk and dawn","Visit nearest health center for a rapid malaria test","Take prescribed anti-malarial medication if confirmed"],
    "Typhoid":           ["Drink only boiled or treated water","Wash hands before eating and after toilet","Avoid raw foods from unknown sources","Use a proper toilet or latrine","Get vaccinated if recommended by a doctor"],
    "Tuberculosis":      ["Visit a health center immediately for a sputum test","Cover mouth when coughing or sneezing","Ensure good ventilation in your home","Complete the full TB treatment course if diagnosed","Notify close contacts to get tested"],
    "Anemia":            ["Eat iron-rich foods: leafy greens, lentils, liver","Take iron and folate supplements if prescribed","Get a blood test at the nearest clinic","Pregnant women should take prenatal supplements","Treat any underlying infections like hookworm"],
    "Dengue":            ["Remove stagnant water from containers, pots, tires","Use mosquito repellent and nets","Stay hydrated and rest","Go to hospital immediately if bleeding or severe pain","Do not take aspirin — use paracetamol only"],
    "Diarrheal Disease": ["Drink ORS (Oral Rehydration Solution) to stay hydrated","Wash hands with soap after using toilet","Drink only safe, boiled water","Eat freshly cooked food","Seek medical help if diarrhea persists beyond 2 days"],
}

@app.route("/api/check-risk", methods=["POST"])
def check_risk():
    data = request.get_json()
    symptoms = set(data.get("symptoms", []))
    risk_factors = set(data.get("risk_factors", []))
    age = int(data.get("age", 30))
    age_mult = 1.2 if age < 5 or age > 60 else 1.0
    results = []
    for disease, rules in DISEASE_RULES.items():
        sm = symptoms & set(rules["conditions"])
        fm = risk_factors & set(rules["risk_factors"])
        ss = len(sm) / len(rules["conditions"])
        fs = len(fm) / max(len(rules["risk_factors"]), 1)
        pct = min(round((ss * 0.7 + fs * 0.3) * rules["weight"] * age_mult * 100), 99)
        if pct > 10:
            level = "High" if pct >= 60 else "Medium" if pct >= 30 else "Low"
            results.append({"disease": disease, "risk_score": pct, "risk_level": level,
                            "matched_symptoms": list(sm), "matched_factors": list(fm),
                            "precautions": PRECAUTIONS.get(disease, [])})
    results.sort(key=lambda x: x["risk_score"], reverse=True)
    return jsonify({"risks": results[:4], "total_analyzed": len(DISEASE_RULES)})


# ══════════════════════════════════════════════════════════════════
#  MENSTRUAL CYCLE TRACKER & ANALYSIS (FIXED IRREGULAR CYCLES)
# ══════════════════════════════════════════════════════════════════
@app.route("/api/menstrual-analysis", methods=["POST"])
def menstrual_analysis():
    data = request.get_json()
    period_dates_raw = data.get("period_dates", [])
    symptoms = set(data.get("symptoms", []))

    period_dates = []
    for d in period_dates_raw:
        try:
            period_dates.append(datetime.strptime(d.strip(), "%Y-%m-%d"))
        except:
            pass
    period_dates.sort()

    result = {}

    if len(period_dates) >= 2:
        cycle_lengths = [(period_dates[i+1] - period_dates[i]).days for i in range(len(period_dates)-1)]
        avg_cycle = round(statistics.mean(cycle_lengths), 1)
        variance = round(statistics.stdev(cycle_lengths), 1) if len(cycle_lengths) > 1 else 0
        last = period_dates[-1]

        # --- FIXED: Adjust next period prediction for irregular cycles ---
        if variance <= 3:  # Regular
            next_p = last + timedelta(days=round(avg_cycle))
        elif variance <= 7:  # Slightly irregular
            next_p = last + timedelta(days=round(avg_cycle + 1))  # small buffer
        else:  # Irregular
            next_p = last + timedelta(days=round(avg_cycle + 2))  # larger buffer

        # Ovulation window (approx mid-cycle)
        ovulation = last + timedelta(days=round(avg_cycle / 2))
        regularity = "Regular" if variance <= 3 else "Slightly Irregular" if variance <= 7 else "Irregular"

        result["cycle_analysis"] = {
            "average_cycle_days": avg_cycle,
            "variance": variance,
            "regularity": regularity,
            "last_period": last.strftime("%d %b %Y"),
            "next_period_predicted": next_p.strftime("%d %b %Y"),
            "days_until_next": max((next_p - datetime.now()).days, 0),
            "ovulation_window": {
                "start": (ovulation - timedelta(days=2)).strftime("%d %b %Y"),
                "peak": ovulation.strftime("%d %b %Y"),
                "end": (ovulation + timedelta(days=2)).strftime("%d %b %Y"),
            }
        }
    else:
        result["cycle_analysis"] = None

    concern_map = {
        "very_heavy_bleeding": "Heavy bleeding (soaking 1+ pad/hour) may indicate fibroids or hormonal imbalance.",
        "severe_cramps":       "Severe cramps that stop daily activity may indicate endometriosis.",
        "periods_stopped":     "Missing periods (not pregnant) may indicate hormonal issues or stress.",
        "bleeding_between":    "Bleeding between periods needs medical evaluation.",
        "period_over_7days":   "Periods lasting more than 7 days should be checked by a doctor.",
        "clots_in_blood":      "Passing large clots may indicate uterine fibroids.",
        "pelvic_pain":         "Chronic pelvic pain between periods needs evaluation.",
    }
    result["concern_flags"] = [{"symptom": k.replace("_"," ").title(), "message": v}
                                for k, v in concern_map.items() if k in symptoms]
    result["education_facts"] = [
        {"title": "Menstruation is NORMAL & HEALTHY", "body": "Every girl and woman has periods. It is a sign your body is healthy. There is no shame — it is as natural as breathing."},
        {"title": "Average Cycle is 28 Days", "body": "A cycle can be 21–35 days. Bleeding lasts 3–7 days. Both are normal. Stress, illness, or poor nutrition can change it."},
        {"title": "Use Safe Period Products", "body": "Cloth pads, sanitary napkins, and menstrual cups are all safe. Change pads every 4–6 hours to prevent infection."},
        {"title": "Rest & Nutrition During Periods", "body": "Eat iron-rich foods (jaggery, spinach, lentils). Warm water and light exercise help reduce pain."},
        {"title": "When to See a Doctor", "body": "See a doctor if periods stop 3+ months (not pregnant), bleeding is extremely heavy, or you have severe ongoing pain."},
    ]
    return jsonify(result)


# ══════════════════════════════════════════════════════════════════
#  PCOD RISK ANALYSIS
# ══════════════════════════════════════════════════════════════════
PCOD_WEIGHTS = {
    "irregular_periods": 3.0, "no_periods_3months": 3.5, "excess_facial_hair": 2.5,
    "hair_thinning": 2.0, "acne_jawline": 1.8, "weight_gain_belly": 2.2,
    "dark_skin_patches": 2.0, "skin_tags": 1.5, "difficulty_conceiving": 2.8,
    "mood_swings": 1.5, "fatigue_pcod": 1.5, "sugar_cravings": 1.5,
    "pelvic_pain_pcod": 2.0, "heavy_or_light_bleeding": 2.0,
}

@app.route("/api/pcod-analysis", methods=["POST"])
def pcod_analysis():
    data = request.get_json()
    symptoms = set(data.get("symptoms", []))
    age = int(data.get("age", 25))
    bmi = float(data.get("bmi", 0)) if data.get("bmi") else None
    family_history = bool(data.get("family_history_pcod", False))

    score = sum(PCOD_WEIGHTS.get(s, 0) for s in symptoms)
    matched = [s for s in symptoms if s in PCOD_WEIGHTS]
    if family_history: score += 2.5
    if bmi and bmi > 25: score += 1.5
    if age < 30: score *= 1.1

    pct = min(round((score / (sum(PCOD_WEIGHTS.values()) + 4)) * 100), 97)
    level = "High" if pct >= 55 else "Medium" if pct >= 30 else "Low"

    recs = {
        "High": "High PCOD likelihood. Please visit a gynaecologist soon. Ultrasound and hormone blood tests (LH, FSH, AMH) will confirm the diagnosis.",
        "Medium": "Some PCOD signs detected. Consult a doctor for evaluation. Early treatment greatly improves quality of life.",
        "Low": "Low PCOD risk. Continue monitoring your cycles. If new symptoms develop, consult a doctor.",
    }

    return jsonify({
        "risk_score": pct, "risk_level": level,
        "matched_symptoms": matched, "recommendation": recs[level],
        "what_is_pcod": {
            "definition": "PCOD is a hormonal condition where ovaries produce immature eggs that become cysts. It affects 1 in 5 women in India.",
            "causes": ["Hormonal imbalance", "Insulin resistance", "Genetics/family history", "Unhealthy diet and lifestyle", "Stress"],
            "treatments": ["Lifestyle changes: exercise and healthy diet", "Weight management", "Hormonal medications (by doctor)", "Metformin for insulin resistance", "Regular monitoring every 6 months"],
            "myths": [
                "MYTH: PCOD means you can never have children. FACT: With treatment, most women with PCOD can conceive.",
                "MYTH: PCOD only affects overweight women. FACT: Thin women can also have PCOD.",
                "MYTH: PCOD goes away after marriage. FACT: PCOD needs proper medical management.",
            ]
        }
    })


# ══════════════════════════════════════════════════════════════════
#  MENTAL HEALTH SCREENING
# ══════════════════════════════════════════════════════════════════
MH_WEIGHTS = {
    "sadness_2weeks": {"w": 2.5, "cat": "Depression"},
    "lost_interest": {"w": 2.5, "cat": "Depression"},
    "sleep_problems": {"w": 1.8, "cat": "Depression/Anxiety"},
    "no_energy": {"w": 1.8, "cat": "Depression"},
    "worthless_feeling": {"w": 2.8, "cat": "Depression"},
    "cannot_concentrate": {"w": 1.5, "cat": "Anxiety"},
    "appetite_change": {"w": 1.5, "cat": "Depression"},
    "excessive_worry": {"w": 2.5, "cat": "Anxiety"},
    "panic_attacks": {"w": 3.0, "cat": "Anxiety"},
    "fear_leaving_home": {"w": 2.2, "cat": "Anxiety"},
    "irritable_angry": {"w": 1.8, "cat": "Stress"},
    "physical_aches_stress": {"w": 1.5, "cat": "Stress"},
    "substance_use": {"w": 2.0, "cat": "Substance Use"},
    "thoughts_of_harm": {"w": 4.0, "cat": "Crisis"},
    "feel_alone": {"w": 2.0, "cat": "Isolation"},
}

@app.route("/api/mental-health", methods=["POST"])
def mental_health():
    data = request.get_json()
    symptoms = set(data.get("symptoms", []))
    gender = data.get("gender", "other")

    score = 0.0
    matched = []
    categories = {}
    crisis = False

    for s in symptoms:
        if s in MH_WEIGHTS:
            score += MH_WEIGHTS[s]["w"]
            matched.append(s)
            cat = MH_WEIGHTS[s]["cat"]
            categories[cat] = categories.get(cat, 0) + 1
            if s == "thoughts_of_harm": crisis = True

    pct = min(round((score / sum(v["w"] for v in MH_WEIGHTS.values())) * 100), 99)
    level = "Crisis" if crisis else "High" if pct >= 50 else "Medium" if pct >= 25 else "Low"

    messages = {
        "Crisis": "You selected thoughts of self-harm. Please reach out for help immediately. You are not alone — help is available.",
        "High": "Your responses indicate significant emotional distress. Please speak to a trusted person or health worker. Professional help makes a real difference.",
        "Medium": "You are showing signs of stress or difficulty. It is okay to feel this way. Talking to someone you trust is a great first step.",
        "Low": "You appear to be managing well. Continue to nurture your mental health through rest, social connection, and physical activity.",
    }

    gender_notes = {
        "female": "Women in rural areas often face extra stress from household duties and social pressure. Your feelings are valid and you deserve support.",
        "male": "Men are often told to 'be strong' and not show feelings. This increases risk of untreated depression. Seeking help is a sign of strength.",
        "other": "Everyone deserves mental health support regardless of gender. Your wellbeing matters.",
    }

    helplines = [
        {"name": "iCall (Free Counseling)", "number": "9152987821"},
        {"name": "Vandrevala Foundation 24/7", "number": "1860-2662-345"},
        {"name": "KIRAN National Helpline", "number": "1800-599-0019"},
        {"name": "NIMHANS Helpline", "number": "080-46110007"},
    ]

    return jsonify({
        "risk_score": pct, "risk_level": level, "is_crisis": crisis,
        "message": messages[level],
        "gender_note": gender_notes.get(gender, gender_notes["other"]),
        "top_categories": sorted(categories.items(), key=lambda x: x[1], reverse=True),
        "helplines": helplines if (crisis or pct >= 40) else [],
        "awareness_facts": [
            {"title": "Mental Health is Real Health", "body": "Depression and anxiety are real medical conditions — NOT weakness or laziness."},
            {"title": "1 in 4 People Struggle", "body": "Across the world, 1 in 4 people face a mental health issue. You are not alone and not 'mad'."},
            {"title": "Talking Helps", "body": "Simply talking to a trusted friend, family member, or ASHA worker can reduce burden significantly."},
            {"title": "Help is Free & Available", "body": "Government PHC/CHC centers have counselors. The KIRAN helpline (1800-599-0019) is free and available 24/7."},
            {"title": "Daily Habits Matter", "body": "Adequate sleep, regular meals, light physical activity, and time with loved ones significantly improve mental health."},
        ],
    })


@app.route("/")
def index():
    return send_from_directory(".", "index.html")

if __name__ == "__main__":
    print("🌿 Rural Health Risk Checker running at http://localhost:5000")
    app.run(debug=True, port=5000)