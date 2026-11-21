# Requirements (Hour 3)

## Essential

| ID | Requirement |
|---|---|
| R1 | Store stop information (name, coordinates) |
| R2 | Store route information (a named collection of stops for one trip) |
| R3 | Retrieve stops and routes |
| R4 | Modify and delete stops/routes while maintaining valid relationships |
| R5 | Calculate the distance between any two stops |
| R6 | Calculate the total distance of a given ordered route |
| R7 | Construct an initial route automatically (nearest-neighbor heuristic) |
| R8 | Improve a constructed route (2-opt local search) |
| R9 | Compare the naive/input order against the optimized order |
| R10 | Visualize a route on a map |
| R11 | Handle a realistic number of stops (tens to low hundreds) efficiently |

## Supporting

Validate coordinate input. Reject duplicate stops within one route. Handle trivial cases (0 or 1 stop) gracefully. Clear error messages. Filter/list routes.

## Out of scope (and why)

- **Real-time traffic / live GPS.** Needs external, paid, rate-limited APIs. Out of scope for a 35-hour solo build.
- **True optimal TSP solving (exact algorithms).** Factorial time complexity, infeasible past roughly 12 stops. This is why a heuristic is the right technique, not a limitation to apologize for, good Criterion D material.
- **Multi-vehicle routing (VRP).** A real extension, good material for Criterion E's future improvements, not something to build now.
- **Real road-network distances (via OSRM/Google Directions).** External API dependency. Straight-line distance is a standard, accepted simplification at this scope (see technology-decisions.md).
- Authentication, accounts, live tracking.
