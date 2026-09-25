def classify(data):
    intended = data.intended_use.lower()
    classical = data.classical_text.lower()
    modification = data.modification.lower()
    if classical == "yes" and modification in ("no", "none"):
        category = "Classical / generic Ayurvedic medicine"
        reason = "The user indicates an authoritative classical-text basis with no reported modification."
    elif "cosmetic" in intended:
        category = "Cosmetic — preliminary"
        reason = "Intended use indicates cosmetic positioning."
    elif any(x in intended for x in ["food", "beverage", "nutraceutical", "nutrition"]):
        category = "Ayurveda-Aahar / food — preliminary"
        reason = "Intended use indicates food/nutritional positioning."
    elif classical == "no" or modification in ("yes", "modified"):
        category = "Proprietary / non-classical Ayurvedic product — preliminary"
        reason = "The product is reported as non-classical or modified."
    else:
        category = "Uncertain — clarification required"
        reason = "The available facts are insufficient to classify the formulation reliably."
    confidence = 0.9 if category != "Uncertain — clarification required" else 0.45
    return {"category": category, "reason": reason, "confidence": confidence}
