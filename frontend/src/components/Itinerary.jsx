import { useState } from "react";
import { getItinerary } from "../services/api";

const inr = (n) => `₹${Number(n).toLocaleString("en-IN")}`;

export default function Itinerary({ destinationId, form }) {
  const [plan, setPlan] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const load = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await getItinerary({
        destination_id: destinationId,
        days: Number(form.days),
        interests: form.interests,
        travelers: Number(form.travelers),
      });
      setPlan(res.data);
    } catch (e) {
      setError(e.response?.data?.detail || "Could not build the itinerary.");
    } finally {
      setLoading(false);
    }
  };

  if (!plan) {
    return (
      <div style={{ marginTop: 8 }}>
        <button onClick={load} disabled={loading}>
          {loading ? "Building..." : "Plan itinerary"}
        </button>
        {error && <p style={{ color: "crimson" }}>{error}</p>}
      </div>
    );
  }

  return (
    <div style={{ marginTop: 12, background: "#eef6ee", padding: 12, borderRadius: 8 }}>
      <h3 style={{ marginTop: 0 }}>Itinerary for {plan.destination}</h3>
      <p>
        🗺️ {plan.message} Total {plan.total_km} km · local transport about{" "}
        {inr(plan.total_local_transport_cost)} · activities{" "}
        {inr(plan.total_activity_cost_per_person)} per person
      </p>
      {plan.note && <p style={{ color: "darkorange" }}>{plan.note}</p>}

      {plan.days.map((d) => (
        <div key={d.day} style={{ marginBottom: 12 }}>
          <b>Day {d.day}</b>{" "}
          <span style={{ color: "#555" }}>
            · {d.total_km} km · {d.travel_minutes} min travel
            {d.saved_minutes > 0 && ` · saved ${d.saved_minutes} min`}
          </span>
          <ul style={{ margin: "4px 0" }}>
            {d.stops.map((s, i) => (
              <li key={i}>
                {s.time} → {s.name}
                {s.category !== "meal" && s.category !== "rest" && ` (${s.category})`}
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
}