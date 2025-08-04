# Design Constraints for UrbanInfraAI

## 1. Data Availability

- Must work with incomplete or outdated data (esp. for small towns).
- Use default assumptions or proxy models when needed.

## 2. Low Resource Requirements

- Should run on low-bandwidth networks or old machines (e.g., in municipal offices).

## 3. Explainability

- Every recommendation must include clear reasoning (e.g., "this site covers 5K more people within 10 mins").

## 4. Privacy & Ethics

- Must avoid using any personally identifiable data.
- Work only with aggregated or anonymized data layers.

## 5. Regulatory Compliance

- Must encode local planning norms (zoning rules, road width limits, FARs).

## 6. Modular Architecture

- Different cities should adopt modules independently (traffic, water, etc).

## 7. Human-in-the-loop

- Planners must be able to adjust weights, override decisions, and simulate alternatives.

## 8. Sustainability Awareness

- All plans must consider long-term environmental impact (flood risk, deforestation, etc).

## 9. Equity First

- Underserved communities must be prioritized when proposing new infrastructure.

## 10. Long-Term Usability

- Exportable formats, simple UI, and documentation are critical for adoption beyond initial pilots.
