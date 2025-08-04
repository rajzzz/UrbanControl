# Agile Development Phases for UrbanInfraAI

## Phase 1: Discovery & Prototyping (1–2 Sprints)

- Define key use case (e.g., school placement).
- Identify available datasets (e.g., census, OSM).
- Create clickable Figma prototype.
- Conduct 3–5 expert interviews (if time permits).

## Phase 2: Core MVP Engine (2–3 Sprints)

- Build ingestion pipeline (Census + OSM).
- Implement simple recommendation logic.
- Create backend engine for one domain (e.g., education).
- Export recommendations to JSON/GeoJSON.

## Phase 3: Dashboard UI (2–3 Sprints)

- Build web dashboard (React + Mapbox/Folium).
- Add filters (budget, accessibility, equity weighting).
- Visualize output with basic interactivity.

## Phase 4: Multi-Domain Expansion (3–4 Sprints)

- Add new domains (roads, water, green spaces).
- Enable "what-if" simulations for future population growth.
- Incorporate sustainability scoring (green coverage, carbon).

## Phase 5: Pilot + Validation (2–4 Sprints)

- Deploy in one ward or city district.
- Measure before vs after KPIs (access rate, congestion, equity).
- Adjust models based on planner feedback.

## Phase 6: Modularization + Scaling (Ongoing)

- Plug-in system (choose only needed modules).
- Localization (language, zoning norms).
- Optimize for edge/offline use (gov laptops).
