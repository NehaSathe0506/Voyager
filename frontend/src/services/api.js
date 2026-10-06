import axios from "axios";

const api = axios.create({ baseURL: "http://127.0.0.1:8000/api" });

export const getDestinations = () => api.get("/destinations/");
export const getRecommendations = (prefs) => api.post("/recommendations", prefs);
export const getBudgetPlan = (payload) => api.post("/budget", payload);
export const getItinerary = (payload) => api.post("/itinerary", payload);
export default api;