import pytest
from prompts import get_urgency_assessment, HEALTHCARE_DISCLAIMER, EMERGENCY_KEYWORDS
from main import get_user_context, log_health_interaction
from models import User, HealthLog
from database import get_db
from sqlalchemy.orm import Session

def test_emergency_detection():
    """Test emergency keyword detection"""
    emergency_cases = [
        "I have chest pain",
        "can't breathe",
        "severe bleeding",
        "unconscious"
    ]

    for case in emergency_cases:
        result = get_urgency_assessment(case)
        assert result["level"] == "emergency"
        assert "emergency" in result["response"].lower()

def test_urgency_assessment():
    """Test different urgency levels"""
    # Low urgency
    low_result = get_urgency_assessment("I have a mild headache")
    assert low_result["level"] == "low"

    # Medium urgency
    medium_result = get_urgency_assessment("I have persistent vomiting")
    assert medium_result["level"] == "medium"

def test_healthcare_disclaimer():
    """Test that disclaimer is always present"""
    assert "not a doctor" in HEALTHCARE_DISCLAIMER.lower()
    assert "consult" in HEALTHCARE_DISCLAIMER.lower()

def test_emergency_keywords():
    """Test emergency keyword list"""
    assert "chest pain" in EMERGENCY_KEYWORDS
    assert "shortness of breath" in EMERGENCY_KEYWORDS
    assert len(EMERGENCY_KEYWORDS) > 5

def test_user_context_generation(db: Session):
    """Test user context retrieval"""
    # Create test user
    test_user = User(
        email="test@example.com",
        hashed_password="hashed",
        full_name="Test User",
        phone="+1234567890"
    )
    db.add(test_user)
    db.commit()

    # Add health logs
    log1 = HealthLog(
        user_id=test_user.id,
        log_type="symptom",
        data={"symptom": "headache", "severity": "mild"}
    )
    log2 = HealthLog(
        user_id=test_user.id,
        log_type="medication",
        data={"medication": "aspirin", "dosage": "100mg"}
    )
    db.add(log1)
    db.add(log2)
    db.commit()

    # Test context generation
    context = get_user_context(test_user.id, db)
    assert "headache" in context
    assert "aspirin" in context

def test_health_interaction_logging(db: Session):
    """Test logging of health interactions"""
    # Create test user
    test_user = User(
        email="logtest@example.com",
        hashed_password="hashed",
        full_name="Log Test User",
        phone="+1234567890"
    )
    db.add(test_user)
    db.commit()

    # Log interaction
    log_health_interaction(
        db=db,
        user_id=test_user.id,
        user_input="I have a headache",
        ai_response="Please consult a doctor",
        urgency="low"
    )

    # Verify log was created
    logs = db.query(HealthLog).filter(
        HealthLog.user_id == test_user.id,
        HealthLog.log_type == "voice_interaction"
    ).all()

    assert len(logs) == 1
    assert logs[0].data["user_input"] == "I have a headache"
    assert logs[0].data["urgency_level"] == "low"

if __name__ == "__main__":
    pytest.main([__file__])
