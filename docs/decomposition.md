# Problem Decomposition (Hour 5)

```
Route Optimizer
│
├── Data Management
│   ├── stops
│   └── routes (route to stop associations, with ordering)
│
├── Validation
│   ├── coordinate range/type validation
│   ├── duplicate-stop-in-route validation
│   └── foreign-key validation
│
├── Route Engine
│   ├── pairwise distance calculation
│   ├── total route distance
│   ├── nearest-neighbor construction
│   ├── 2-opt improvement
│   └── naive-vs-optimized comparison
│
├── API
│   ├── stop retrieval/creation/modification/deletion
│   ├── route retrieval/creation/modification/deletion
│   └── optimize + compare endpoint
│
├── User Interface
│   ├── stop entry (map click or manual coordinates)
│   ├── route builder
│   ├── map visualization (naive vs optimized)
│   └── route list
│
└── Testing
    ├── correctness
    ├── reliability
    └── efficiency
```

## SC mapping

| Branch | Primary SC |
|---|---|
| Data Management | SC1 |
| Validation | SC1, SC6 |
| Route Engine | SC2, SC3, SC4, SC7 |
| API | SC1, SC5 |
| User Interface | SC7 |
| Testing | SC1 through SC7 |
