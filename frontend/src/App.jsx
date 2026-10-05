import { useEffect, useState } from "react";
import { getDestinations } from "./services/api";

export default function App() {
  const [items, setItems] = useState([]);

  useEffect(() => {
    getDestinations().then((res) => setItems(res.data));
  }, []);

  return (
    <div style={{ padding: 24 }}>
      <h1>Voyager</h1>
      <ul>
        {items.map((d) => (
          <li key={d.id}>{d.name}, {d.state}</li>
        ))}
      </ul>
    </div>
  );
}