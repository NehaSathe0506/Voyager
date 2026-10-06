from services.recommendation import CITY_COORDS, haversine_km

# How the total budget is split. Must add up to 1.0
ALLOCATION = {
    "Transportation": 0.27,
    "Accommodation": 0.23,
    "Food": 0.17,
    "Activities": 0.13,
    "Local transport": 0.10,
    "Emergency buffer": 0.10,
}

# How a destination's average daily cost is split
DAILY_SPLIT = {
    "Accommodation": 0.45,
    "Food": 0.25,
    "Activities": 0.15,
    "Local transport": 0.15,
}

TRANSPORT_RATE_PER_KM = 2.0   # INR per km, per person, one way (bus/train mix)

STYLE_MULTIPLIER = {"budget": 0.85, "standard": 1.0, "luxury": 1.4}

# Cuts applied in this order until the plan fits: (category, action, share of that category saved)
SAVINGS_STEPS = [
    ("Accommodation", "Switch to a cheaper hotel or hostel", 0.25),
    ("Local transport", "Use public transport instead of taxis", 0.30),
    ("Food", "Eat at local restaurants instead of tourist spots", 0.20),
    ("Activities", "Drop one paid activity", 0.30),
    ("Transportation", "Choose a cheaper travel option (sleeper bus or train)", 0.15),
]


def estimate_costs(dest, req):
    coords = CITY_COORDS.get(req.start_city.strip().lower())
    if coords and dest.latitude is not None and dest.longitude is not None:
        distance = haversine_km(coords[0], coords[1], dest.latitude, dest.longitude)
    else:
        distance = 800  # fallback guess

    daily = float(dest.average_budget_per_day or 0) * STYLE_MULTIPLIER[req.travel_style]
    costs = {"Transportation": distance * 2 * TRANSPORT_RATE_PER_KM}   # round trip
    for category, share in DAILY_SPLIT.items():
        costs[category] = daily * share * req.days
    return {k: round(v) for k, v in costs.items()}, round(distance)


def optimize(costs, spend_limit):
    costs = dict(costs)
    suggestions = []
    for category, action, share in SAVINGS_STEPS:
        if sum(costs.values()) <= spend_limit:
            break
        saved = round(costs[category] * share)
        if saved <= 0:
            continue
        costs[category] -= saved
        suggestions.append({"category": category, "action": action, "saves": saved})
    return costs, suggestions


def plan_budget(dest, req):
    allocation = {k: round(req.budget * v) for k, v in ALLOCATION.items()}
    buffer_amount = allocation["Emergency buffer"]
    spend_limit = req.budget - buffer_amount

    costs, distance = estimate_costs(dest, req)
    total = sum(costs.values())
    over_by = max(0, round(total - spend_limit))

    result = {
        "destination": dest.name,
        "distance_km": distance,
        "budget": round(req.budget),
        "allocation": allocation,
        "estimated_costs": costs,
        "estimated_total": total,
        "spend_limit": round(spend_limit),
        "emergency_buffer": buffer_amount,
        "within_budget": over_by == 0,
        "over_by": over_by,
        "suggestions": [],
        "optimized_costs": costs,
        "optimized_total": total,
        "fits_after_optimization": over_by == 0,
    }

    if over_by > 0:
        optimized, suggestions = optimize(costs, spend_limit)
        optimized_total = sum(optimized.values())
        result["suggestions"] = suggestions
        result["optimized_costs"] = optimized
        result["optimized_total"] = optimized_total
        result["fits_after_optimization"] = optimized_total <= spend_limit

    return result