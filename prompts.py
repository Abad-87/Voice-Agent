# Healthcare Voice AI - Safety Guardrails and Prompts

HEALTHCARE_DISCLAIMER = """
⚠️ MEDICAL DISCLAIMER: I am an AI assistant, not a doctor. I cannot diagnose, prescribe medication, or provide medical treatment. All information is for educational purposes only. Please consult a qualified healthcare professional for medical advice, diagnosis, or treatment.
"""

EMERGENCY_WARNING = """
🚨 EMERGENCY: If you are experiencing a medical emergency (chest pain, difficulty breathing, severe bleeding, etc.), call emergency services immediately (911 in US, 112 in Europe, 108 in India) or go to the nearest emergency room. Do not wait for a response.
"""

# Emergency Detection Keywords
EMERGENCY_KEYWORDS = [
    "chest pain", "heart attack", "shortness of breath", "can't breathe",
    "severe bleeding", "unconscious", "stroke", "seizure", "high fever",
    "confusion", "dizziness", "fainting", "allergic reaction", "anaphylaxis"
]

# Main LLM Prompt Template
MAIN_HEALTHCARE_PROMPT = f"""
{HEALTHCARE_DISCLAIMER}

You are a healthcare voice assistant. Your role is to:
1. Provide general health information and education
2. Help manage appointments and medications (reminders only)
3. Conduct basic symptom screening (no diagnosis)
4. Support mental health check-ins (no therapy)
5. Assist with daily health monitoring
6. Direct to appropriate care when needed

{EMERGENCY_WARNING}

STRICT RULES:
- NEVER diagnose conditions
- NEVER prescribe or suggest medication changes
- NEVER provide treatment plans
- ALWAYS recommend consulting healthcare professionals
- ALWAYS include appropriate disclaimers
- If emergency symptoms detected, immediately advise seeking emergency care

User input: {{user_input}}

Context: {{context}}

Respond empathetically, clearly, and safely.
"""

def get_emergency_response(symptoms: str) -> str:
    """Generate emergency response"""
    return f"{EMERGENCY_WARNING}\n\nBased on your description of '{symptoms}', this sounds like it may require immediate medical attention. Please seek emergency care right away or contact emergency services."

def get_urgency_assessment(symptoms: str) -> dict:
    """Assess symptom urgency"""
    symptoms_lower = symptoms.lower()

    # Check for emergency keywords
    for keyword in EMERGENCY_KEYWORDS:
        if keyword in symptoms_lower:
            return {
                "level": "emergency",
                "response": get_emergency_response(symptoms),
                "action": "escalate_immediately"
            }

    # Medium urgency indicators
    medium_indicators = ["persistent", "severe", "worsening", "high fever", "vomiting"]
    if any(indicator in symptoms_lower for indicator in medium_indicators):
        return {
            "level": "medium",
            "response": "These symptoms should be evaluated by a healthcare provider within 24-48 hours. Please consult your doctor.",
            "action": "schedule_appointment"
        }

    # Default to low urgency
    return {
        "level": "low",
        "response": "These symptoms may be minor, but monitor them closely. If they persist or worsen, consult a healthcare provider.",
        "action": "monitor_symptoms"
    }
