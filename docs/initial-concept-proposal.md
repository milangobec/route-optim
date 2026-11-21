# IB Computer Science
## IA Initial Concept Proposal

## Part 1 — Identify Your Client

**Client name:** Jimothy

**Client Description:**
Jimothy runs a small, one-person local delivery and errand-running service. Each day he has a list of stops to visit: dropping off packages, picking up items for regular customers, and running small errands around town. On a typical day this ranges from a handful of stops up to 20 or 30 on busier days. (Client is fictional, with teacher approval. The problem and solution below don't depend on this being a real, contactable person.)

---

## Part 2 — Identify the Problem

**2. What problem does your client currently have?**

Every day, Jimothy has to decide what order to visit his stops in. Right now he has no systematic way to do this: he just goes in whatever order the requests came in, or whatever feels convenient that morning. As the number of stops grows, working out a good order by hand becomes practically impossible. The number of possible orderings grows factorially, so a route with just 10 stops already has over 3.6 million possible sequences. Because of this, Jimothy has no way of knowing whether the route he's driving is efficient or wasteful, or how much time and fuel a better-planned route would save him. On busier days this costs him time and fuel, and he can't give customers a confident estimate of when he'll arrive.

**3. How does the client currently solve this problem?**

Jimothy does this entirely by hand. He keeps a running list of addresses for the day, usually built from text messages and memory, and visits them in whatever order they arrived or however he remembers them. There's no spreadsheet, app, or calculation involved at any point. It's memory and instinct.

**4. What are the limitations of the current process?**

- No way to measure whether a chosen order is actually good. It's a guess, not a calculation.
- Doesn't scale. Manageable for a handful of stops, unworkable once the list gets long.
- No baseline for comparison. There's no way to know how much better a smarter route would be.
- Wasted time and fuel from avoidable backtracking.
- Working from memory risks a stop being missed or visited twice.

---

## Part 3 — Proposed Computational Solution

**5. What do you propose to create?**

A route optimization web application. Jimothy enters his stops for the day by clicking their locations on an interactive map. The system builds a starting route using a nearest-neighbor construction algorithm, then improves that route using a 2-opt local search algorithm. It shows both the original (naive) order and the optimized order side by side on the map, along with each route's total distance and the percentage improvement, so Jimothy can see, in concrete numbers, how much better the computed route is before he leaves for the day.

**6. Potential features**

| # | Potential Feature |
|---|---|
| 1 | Add, edit, and delete stops (name and map location) |
| 2 | Group stops into a named route for a given day or trip |
| 3 | Automatically construct an initial route order (nearest-neighbor algorithm) |
| 4 | Automatically improve a constructed route to reduce total distance (2-opt algorithm) |
| 5 | Visualize the naive and optimized routes on an interactive map, togglable |
| 6 | Calculate and display total distance and percentage improvement between the two |

---

## Part 4 — How Will Your Solution Help?

**7. How will your proposed solution improve the client's current situation?**

Right now, Jimothy has to guess at a stop order with no way to check or improve it. The system instead calculates a near-optimal order using established routing algorithms and works out exactly how much shorter it is than the naive order. The result is that Jimothy leaves with a better route each day, backed by real numbers (kilometers saved, percentage improvement), instead of a guess.

**8. Why would your client actually use this solution?**

- Saves time and fuel on every route, which adds up over weeks of daily use.
- Removes the guesswork of deciding stop order every morning.
- Scales to busy days with many stops, where manual planning wasn't practical before.
- Gives a visual before-and-after comparison, so it's clear the route actually improved rather than just changed.

---

## Part 5 — Initial Requirements

| # | Initial Requirement |
|---|---|
| 1 | The client will be able to add, view, update, and delete stops (name and location). |
| 2 | The client will be able to group a set of stops into a named route for a trip. |
| 3 | The system will automatically construct an initial visiting order for a route using a nearest-neighbor algorithm. |
| 4 | The system will improve a constructed route using a 2-opt algorithm, and will never return a route longer than the one it started from. |
| 5 | The system will calculate and display each route's total distance and the percentage improvement between the naive and optimized orders. |
| 6 | The system will display routes visually on a map, showing both the naive and optimized paths. |
| 7 | The system will reject invalid stop data (for example, out-of-range coordinates or duplicate stops) without corrupting existing records. |

*(These are initial requirements and may be refined once success criteria are locked.)*

---

## Part 6 — Computer Science

**9. What computer science concepts might your solution require?**

☑ Algorithms
☑ Searching *(finding the nearest unvisited stop at each construction step)*
☐ Sorting
☑ Data structures *(distance matrix / graph representation of stops)*
☑ Object-oriented programming *(data models for Stop, Route, RouteStop)*
☑ Databases
☑ Data validation
☐ File processing
☑ User interface
☑ Calculations
☑ Decision-making *(which candidate swap improves a route; which stop is nearest)*
☑ Data visualization
☐ Other: ______________________________

**10. What part of your solution do you think will be the most challenging?**

Implementing the 2-opt algorithm correctly. Specifically: getting the segment-reversal swap logic right, making sure the fixed depot or start point is excluded from the swappable range so a swap can't produce a route that doesn't start and end at the depot, and making sure the algorithm stops correctly once no improving swap remains. To catch mistakes early, I plan to check the implementation against a small, hand-built test case where the true optimal route is found by brute force, so I have an exact, independently known answer to compare against.

---

## Part 7 — Technology

**Programming language:** Python (backend and algorithm engine), HTML/JavaScript (frontend)

**Database (if applicable):** SQLite, accessed through the SQLAlchemy ORM

**Other technology/tools:** FastAPI (REST API layer), Tailwind CSS (styling), Leaflet.js (interactive map rendering, free and open-source, needs no API key), pytest (testing)

---

## Part 8 — Feasibility

**12. Can you realistically complete this solution?**

Yes. I've already built and tested a full application in this stack (FastAPI, SQLAlchemy, SQLite) for an earlier project attempt, so the setup and workflow are proven and quick to redo. The computational core here is a single, well-established algorithm family (nearest-neighbor construction plus 2-opt improvement), and both parts are deterministic and don't need empirical parameter tuning. That's a narrower, more provable scope than an earlier project idea I moved away from, which needed several separately tuned analytical parameters. The stop data will be synthetic (randomly generated coordinates within a bounding box), so there's no data collection bottleneck or privacy concern. The 35-hour computational solution budget is already mapped hour by hour, from problem definition through final evaluation, with dedicated time set aside for testing and optimization. Since the client is fictional and teacher-approved, there's also no dependency on an outside person's availability.

**13. What concerns or questions do you currently have?**

- Is the nearest-neighbor plus 2-opt pairing enough computational depth on its own, or would adding one more distinct technique (like a priority structure for managing stops) strengthen Criterion D?
- What's a reasonable efficiency target (for example, under a certain number of seconds for 100 stops)? I plan to benchmark on my own machine once it's built and set the real number then, instead of guessing now.
- Is using straight-line (Haversine) distance instead of real road-network distance an acceptable, well-justified simplification, given that a real routing API would add an external dependency outside the project's scope?

---

## Final Submission Checklist

☑ Identified a client (fictional, teacher-approved)
☑ Identified a genuine real-world problem
☑ Explained the client's current process
☑ Explained the limitations of the current process
☑ Proposed a computational solution
☑ Identified at least 5 potential features
☑ Identified at least 5 initial requirements
☑ Explained how the solution will benefit the client
☑ Considered the computer science involved
☑ Considered whether the project is realistic

---

## Teacher Review

**Initial Decision**

☐ Approved — Begin development of the concept
☐ Approved with revisions
☐ Revise and resubmit

**Teacher Comments:**

*(left blank for teacher completion)*
