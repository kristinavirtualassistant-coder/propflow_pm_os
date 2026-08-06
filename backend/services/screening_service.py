from typing import Dict, Any

def score_lead(income: float, rent: float, credit_score: int) -> Dict[str, Any]:
    score = 0
    if rent > 0 and (income / rent) >= 3.0:
        score += 50
        
    if credit_score >= 700:
        score += 50
    elif credit_score >= 650:
        score += 30
        
    qualification = "UNQUALIFIED"
    if score >= 80:
        qualification = "HOT"
    elif score >= 50:
        qualification = "WARM"
        
    return {
        "income": income,
        "rent_target": rent,
        "credit_score": credit_score,
        "lead_score": score,
        "qualification_tier": qualification
    }
