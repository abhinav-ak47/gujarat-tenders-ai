"""
Company Profile – Eligibility Gate Configuration
Represents YOUR company's current credentials and capacity
"""

COMPANY_PROFILE = {
    "name": "Deloitte Skill Development & Livelihoods Practice",
    "established_year": 2004,
    "annual_turnover_crores": 120.0,          # Above ₹100 Crores
    "years_of_experience": 22,                 # More than 20 years
    "certifications": [
        "ISO 9001",
        "MSME Registered",
        "Government Empanelled",
        "NSDC Partner",
        "State Skill Mission",
        "NSQF Aligned"
    ],
    "geographic_presence": ["Gujarat"],        # Gujarat-only
    "daily_training_capacity": 200,            # 200 trainees/day
    "similar_projects_completed": 18,          # Strong project history
}

# ─── Eligibility Gate Logic ────────────────────────────────────────────────────

CERT_ALIASES = {
    "ISO 9001":              "ISO 9001",
    "MSME Registered":       "MSME Registered",
    "MSME":                  "MSME Registered",
    "Government Empanelled": "Government Empanelled",
    "NSDC Partner":          "NSDC Partner",
    "State Skill Mission":   "State Skill Mission",
    "NSQF Aligned":          "NSQF Aligned",
}

BORDERLINE_RATIO = 0.15   # If tender requires X and company has X ± 15% → Manual Check


def check_tender_eligibility(tender: dict, company: dict) -> dict:
    """
    Run all eligibility checks on a tender against company profile.
    Returns a result dict with: status, checks (list of individual check results)
    """
    checks = []

    # ── 1. Turnover Check ─────────────────────────────────────────────────────
    min_t = tender["eligibility"]["min_turnover_crores"]
    co_t  = company["annual_turnover_crores"]
    ratio_t = (co_t - min_t) / max(min_t, 0.01)
    if co_t >= min_t:
        if ratio_t < BORDERLINE_RATIO:
            c_status = "manual"
            c_reason = (f"Company turnover ₹{co_t}Cr is only {ratio_t*100:.1f}% above the "
                        f"minimum required ₹{min_t}Cr – borderline, needs verification")
        else:
            c_status = "pass"
            c_reason = f"Company turnover ₹{co_t}Cr exceeds minimum requirement of ₹{min_t}Cr"
    else:
        c_status = "fail"
        c_reason = (f"Company turnover ₹{co_t}Cr is below minimum required ₹{min_t}Cr "
                    f"(shortfall: ₹{min_t - co_t:.1f}Cr)")
    checks.append({"criterion": "Annual Turnover", "status": c_status, "reason": c_reason,
                   "required": f"₹{min_t}Cr", "company": f"₹{co_t}Cr"})

    # ── 2. Experience Check ───────────────────────────────────────────────────
    min_exp = tender["eligibility"]["min_experience_years"]
    co_exp  = company["years_of_experience"]
    if co_exp >= min_exp:
        c_status = "pass"
        c_reason = f"Company has {co_exp} years of experience, meets minimum of {min_exp} years"
    else:
        c_status = "fail"
        c_reason = f"Company has {co_exp} years of experience, below minimum of {min_exp} years"
    checks.append({"criterion": "Experience / Company Age", "status": c_status, "reason": c_reason,
                   "required": f"{min_exp} yrs", "company": f"{co_exp} yrs"})

    # ── 3. Certifications Check ───────────────────────────────────────────────
    required_certs = tender["eligibility"]["required_certifications"]
    company_certs  = set(company["certifications"])
    missing_certs  = []
    for rc in required_certs:
        normalized = CERT_ALIASES.get(rc, rc)
        if normalized not in company_certs and rc not in company_certs:
            missing_certs.append(rc)
    if not missing_certs:
        c_status = "pass"
        c_reason = f"All required certifications present: {', '.join(required_certs)}"
    else:
        c_status = "fail"
        c_reason = f"Missing certifications: {', '.join(missing_certs)}"
    checks.append({"criterion": "Registrations & Certifications", "status": c_status, "reason": c_reason,
                   "required": ", ".join(required_certs), "company": ", ".join(company["certifications"])})

    # ── 4. Geographic Eligibility ─────────────────────────────────────────────
    geo_required = tender["eligibility"].get("location_restricted_to")
    geo_scope    = tender["eligibility"].get("geographic_scope", "Gujarat")
    co_geo       = company["geographic_presence"]
    if geo_scope == "Pan-India" or geo_required is None:
        # Tender is pan-India; company is Gujarat-only → manual check
        c_status = "manual"
        c_reason = ("Tender has Pan-India scope requiring multi-state delivery capacity. "
                    "Company's current presence is Gujarat-only – verify if consortium/partnership is allowed")
    elif geo_required in co_geo or geo_required == "Gujarat":
        c_status = "pass"
        c_reason = f"Tender is restricted to {geo_required}, company operates in Gujarat"
    else:
        c_status = "fail"
        c_reason = f"Tender requires operations in {geo_required}, company does not have presence there"
    checks.append({"criterion": "Geographic / Location Eligibility", "status": c_status, "reason": c_reason,
                   "required": geo_scope, "company": ", ".join(co_geo)})

    # ── 5. Prior Similar Projects ─────────────────────────────────────────────
    min_proj = tender["eligibility"]["min_similar_projects"]
    co_proj  = company["similar_projects_completed"]
    if co_proj >= min_proj:
        c_status = "pass"
        c_reason = f"Company has completed {co_proj} similar projects, requirement is {min_proj}"
    else:
        c_status = "fail"
        c_reason = f"Company has only {co_proj} similar projects; minimum required is {min_proj}"
    checks.append({"criterion": "Prior Similar Projects", "status": c_status, "reason": c_reason,
                   "required": f"{min_proj} projects", "company": f"{co_proj} projects"})

    # ── 6. Daily Training Capacity ────────────────────────────────────────────
    min_cap = tender["eligibility"]["min_daily_capacity"]
    co_cap  = company["daily_training_capacity"]
    ratio_c = (min_cap - co_cap) / max(min_cap, 1)
    if co_cap >= min_cap:
        c_status = "pass"
        c_reason = f"Company capacity of {co_cap} trainees/day meets minimum of {min_cap}/day"
    elif ratio_c <= BORDERLINE_RATIO:
        c_status = "manual"
        c_reason = (f"Company capacity {co_cap}/day is {ratio_c*100:.1f}% below required {min_cap}/day – "
                    f"borderline, consider temporary scale-up or partnership")
    else:
        c_status = "fail"
        c_reason = (f"Company capacity {co_cap}/day is below required {min_cap}/day "
                    f"(gap: {min_cap - co_cap}/day). Significant scale-up needed.")
    checks.append({"criterion": "Daily Training Capacity", "status": c_status, "reason": c_reason,
                   "required": f"{min_cap}/day", "company": f"{co_cap}/day"})

    # ── Final Status Determination ────────────────────────────────────────────
    statuses = [c["status"] for c in checks]
    if "fail" in statuses:
        overall = "FAILED"
    elif "manual" in statuses:
        overall = "MANUAL CHECK"
    else:
        overall = "PASSED"

    fail_reasons   = [c for c in checks if c["status"] == "fail"]
    manual_reasons = [c for c in checks if c["status"] == "manual"]
    pass_count     = sum(1 for c in checks if c["status"] == "pass")

    return {
        "tender_id":     tender["id"],
        "tender_title":  tender["title"],
        "department":    tender["department"],
        "deadline":      tender["deadline"],
        "value_lakhs":   tender["estimated_value_lakhs"],
        "location":      tender["location"],
        "scope":         tender["scope"],
        "duration_days": tender["duration_days"],
        "status":        overall,
        "checks":        checks,
        "fail_count":    len(fail_reasons),
        "manual_count":  len(manual_reasons),
        "pass_count":    pass_count,
        "fail_reasons":  [c["reason"] for c in fail_reasons],
        "manual_reasons":[c["reason"] for c in manual_reasons],
    }
