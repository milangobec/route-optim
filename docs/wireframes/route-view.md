# Wireframe: Route View, the Centerpiece (Hour 9)

One map, two togglable overlays: naive order (dashed line, input sequence) and optimized order (solid line). A stats panel alongside shows both total distances and the percentage improvement. This is the payoff screen, watching the line visibly shorten when toggling to optimized is the strongest thing to put in the demonstration video.

```
+---------------------------------------------+
|  Route: Tuesday Deliveries                   |
+---------------------------------------------+
|   ( Naive )  [ Optimized ]  <- toggle        |
|                                               |
|   +-------------------------------------+   |
|   |        map with route line          |   |
|   |   - - - naive    solid = optimized  |   |
|   +-------------------------------------+   |
|  ---------------------------------------    |
|   Naive distance:       13.77 km             |
|   Optimized distance:   12.66 km             |
|   Improvement:          8.1%                 |
+---------------------------------------------+
```

Numbers here match the verified worked example exactly (see docs/algorithms/worked-example.md), so this mockup is already testable against real output, not invented placeholder data.
