# Architecturally and Scientifically Recommended Practices in UrbanInfraAI

UrbanInfraAI incorporates evidence-based architectural and urban planning standards to ensure its recommendations are efficient, sustainable, and policy-aligned. Below are core planning principles and their integration into the system.

---

## 1. Urban Design & Land Use

### 🏙️ Practices

- Compact City Planning: Mixed-use, high-density clusters
- Transit-Oriented Development (TOD)
- Street Width Standards (IRC:86-1983): Min 12m for collector roads
- FAR and Setback Compliance
- Walkable Block Sizes (80–120m)

### 🔧 Integration

- Road width and FAR become constraints in location recommendation logic
- Proximity to transit boosts priority score

---

## 2. Public Service Access

### 🏫 Practices

- School: 1 primary school per 2,000–3,000 people, within 1km
- Health: PHC within 5km; emergency within 8–10 min reach
- Barrier-Free Design

### 🔧 Integration

- Demand-based scoring for services using population raster
- Catchment area modeling for underserved zones

---

## 3. Infrastructure Efficiency

### 🚰 Practices

- Road: IRC lane width, curvature, RoW
- Water: CPHEEO norms (135 lpcd, 24x7 design)
- Drainage slope: 1:1000 min
- Power: Underground cabling in dense cores

### 🔧 Integration

- Infra suggestions constrained by slope, road size, water grid layout
- Evaluate power distribution nodes for load balancing

---

## 4. Sustainability Metrics

### 🌱 Practices

- Green Space: Minimum 10–12 sqm per person (WHO)
- Solar Potential: South-facing, unshaded rooftops
- Water Harvesting: Required in >100 sqm plots
- Environmental Impact: Avoid eco-sensitive zones

### 🔧 Integration

- Sustainability score includes greenery ratio, solar index
- Sites in flood plains auto-flagged

---

## 5. Equity and Inclusion

### 🧑‍🤝‍🧑 Practices

- Accessibility: SC/ST, income, disability-aware planning
- Gender-Sensitive Design: Lighting, safety, restrooms
- Prioritize Underserved Areas (slums, peri-urban)

### 🔧 Integration

- Equity Score = distance to services + demographic weights
- Visualize neglected zones on map overlays

---

## Sources

- URDPFI Guidelines (India)
- IRC Codes (Indian Road Congress)
- CPHEEO Manuals
- WHO Urban Health Guidelines
- UN-Habitat Principles
- Smart Cities Mission Toolkit
- CEPT/SPA Delhi Research
