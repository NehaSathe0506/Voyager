import math

CITY_COORDS = {
    "mumbai": (19.0760, 72.8777),
    "pune": (18.5204, 73.8567),
    "delhi": (28.6139, 77.2090),
    "bangalore": (12.9716, 77.5946),
    "chennai": (13.0827, 80.2707),
    "hyderabad": (17.3850, 78.4867),
    "kolkata": (22.5726, 88.3639),
}

WEIGHTS = {
    "budget": 0.25,
    "interest": 0.25,
    "season": 0.15,
    "duration": 0.15,
    "style": 0.10,
    "distance": 0.10,
}

STYLE_IDEAL_PER_DAY = {"budget": 2000, "standard": 3500, "luxury": 6000}

INTEREST_COLUMNS = {
    "nature": "nature_score",
    "adventure": "adventure_score",
    "culture": "culture_score",
    "nightlife": "nightlife_score",
    "relaxation": "relaxation_score",
}


def haversine_km(lat1, lon1, lat2, lon2):
    r = 6371
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = p2 - p1
    dlmb = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlmb / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def estimated_cost(dest, prefs):
    return float(dest.average_budget_per_day or 0) * prefs.days


def budget_match(dest, prefs):
    cost = estimated_cost(dest, prefs)
    if cost <= prefs.budget:
        return 1.0
    return max(0.0, 1 - (cost - prefs.budget) / prefs.budget)


def interest_match(dest, prefs):
    chosen = [i.lower() for i in prefs.interests if i.lower() in INTEREST_COLUMNS]
    if not chosen:
        return 0.5
    values = [getattr(dest, INTEREST_COLUMNS[i]) or 0 for i in chosen]
    return sum(values) / (len(values) * 10)


def season_match(dest, prefs):
    months = [m.strip().title() for m in (dest.best_months or "").split(",")]
    return 1.0 if prefs.month[:3].title() in months else 0.4


def duration_match(prefs):
    d = prefs.days
    if 3 <= d <= 7:
        return 1.0
    if d < 3:
        return d / 3
    return max(0.4, 7 / d)


def style_match(dest, prefs):
    ideal = STYLE_IDEAL_PER_DAY[prefs.travel_style]
    avg = float(dest.average_budget_per_day or 0)
    return max(0.0, 1 - abs(avg - ideal) / ideal)


def distance_km(dest, prefs):
    coords = CITY_COORDS.get(prefs.start_city.strip().lower())
    if not coords or dest.latitude is None or dest.longitude is None:
        return None
    return haversine_km(coords[0], coords[1], dest.latitude, dest.longitude)


def distance_match(distance):
    if distance is None:
        return 0.5
    return max(0.0, 1 - distance / 2500)


def build_reasons(prefs, parts, cost, distance):
    reasons = []
    if parts["budget"] == 1.0:
        reasons.append(f"Fits your budget (about ₹{cost:,.0f} per person)")
    elif parts["budget"] < 0.6:
        reasons.append(f"May exceed your budget (about ₹{cost:,.0f} per person)")
    if parts["interest"] >= 0.7:
        reasons.append("Strong match for your interests")
    if parts["season"] == 1.0:
        reasons.append(f"{prefs.month} is a good time to visit")
    else:
        reasons.append(f"{prefs.month} is not the ideal season")
    if parts["duration"] >= 0.9:
        reasons.append(f"Well suited to a {prefs.days}-day trip")
    if distance is not None:
        reasons.append(f"About {distance:,.0f} km from {prefs.start_city}")
    return reasons


def recommend(destinations, prefs, top_n=3):
    results = []
    for dest in destinations:
        distance = distance_km(dest, prefs)
        cost = estimated_cost(dest, prefs)
        parts = {
            "budget": budget_match(dest, prefs),
            "interest": interest_match(dest, prefs),
            "season": season_match(dest, prefs),
            "duration": duration_match(prefs),
            "style": style_match(dest, prefs),
            "distance": distance_match(distance),
        }
        total = sum(parts[k] * WEIGHTS[k] for k in WEIGHTS)
        results.append({
            "id": dest.id,
            "name": dest.name,
            "state": dest.state,
            "description": dest.description,
            "match_score": round(total * 100),
            "estimated_cost_per_person": round(cost),
            "distance_km": round(distance) if distance is not None else None,
            "breakdown": {k: round(v * 100) for k, v in parts.items()},
            "reasons": build_reasons(prefs, parts, cost, distance),
        })
    results.sort(key=lambda r: r["match_score"], reverse=True)
    return results[:top_n]