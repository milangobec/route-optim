# Problem Definition (Hour 1)

**Who has the problem?**

A small operator who has to visit multiple stops in one trip, a local delivery service, a fundraiser drop-off run, a mobile pet-sitting or tutoring round. Client is fictional per teacher approval (Jimothy).

**What do they currently have?**

A list of addresses or stops for the day, visited in whatever order they were requested or remembered. No systematic way to decide a good order.

**What is difficult?**

- As the number of stops grows, manually judging a good order becomes infeasible, since the number of possible orderings grows factorially.
- There's no way to know how much better a smarter order would be. No baseline to compare against.
- Fuel, time, and reliability all suffer from an arbitrary visiting order.

**What does the computer need to do?**

Store stops and their locations, calculate distances between them, construct a reasonable initial visiting order automatically, improve that order algorithmically, and show the improvement, numerically and visually, against the naive order.
