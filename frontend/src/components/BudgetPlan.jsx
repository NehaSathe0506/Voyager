import { useState } from "react";
import { getBudgetPlan } from "../services/api";

const inr = (n) => `₹${Number(n).toLocaleString("en-IN")}`;

export default function BudgetPlan({ destinationId, form }) {
  const [plan, setPlan] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const load = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await getBudgetPlan({
        destination_id: destinationId,
        start_city: form.start_city,
        budget: Number(form.budget),
        days: Number(form.days),
        travel_style: form.travel_style,
      });
      setPlan(res.data);
    } catch {
      setError("Could not load the budget plan.");
    } finally {
      setLoading(false);
    }
  };

  if (!plan) {
    return (
      <>
        <button onClick={load} disabled={loading}>
          {loading ? "Calculating..." : "Plan budget"}
        </button>
        {error && <p style={{ color: "crimson" }}>{error}</p>}
      </>
    );
  }

  return (
    <div style={{ marginTop: 12, background: "#f7f7f7", padding: 12, borderRadius: 8 }}>
      <h3 style={{ marginTop: 0 }}>Budget plan: {inr(plan.budget)}</h3>

      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr style={{ textAlign: "left" }}>
            <th>Category</th>
            <th>Allocated</th>
            <th>Estimated</th>
          </tr>
        </thead>
        <tbody>
          {Object.keys(plan.allocation).map((cat) => (
            <tr key={cat}>
              <td>{cat}</td>
              <td>{inr(plan.allocation[cat])}</td>
              <td>{plan.estimated_costs[cat] !== undefined ? inr(plan.estimated_costs[cat]) : "-"}</td>
            </tr>
          ))}
          <tr style={{ fontWeight: "bold" }}>
            <td>Total spend (without buffer)</td>
            <td>{inr(plan.spend_limit)}</td>
            <td>{inr(plan.estimated_total)}</td>
          </tr>
        </tbody>
      </table>

      {plan.within_budget ? (
        <p style={{ color: "green" }}>✅ This trip fits your budget.</p>
      ) : (
        <>
          <p style={{ color: "darkorange" }}>⚠️ Over budget by {inr(plan.over_by)}</p>
          <p>Suggested changes:</p>
          <ul>
            {plan.suggestions.map((s, i) => (
              <li key={i}>{s.action}: save {inr(s.saves)}</li>
            ))}
          </ul>
          <p>
            New estimated cost: <b>{inr(plan.optimized_total)}</b>{" "}
            {plan.fits_after_optimization
              ? "✅ now within budget"
              : "❌ still over. Try fewer days or a lower-cost destination"}
          </p>
        </>
      )}
    </div>
  );
}