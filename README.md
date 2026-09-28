# genpark-kd-tree-nearest-neighbor-spatial-search-skill

Agent Skill implementing **k-Dimensional Tree (KD-Tree)** spatial partitioning with median hyperplane splitting and branch-and-bound k-NN search.

## Architectural Overview
```mermaid
flowchart TD
    Data["Spatial Points"] --> Median["Recursive Median Split (X / Y Alternating)"]
    Median --> KDTree["Binary KD-Tree Index"]
    Query["Target Query Point"] --> Branch["Branch-and-Bound Traversal"]
    KDTree & Query --> Branch
    Branch --> Prune["Hyperplane Distance Pruning"]
    Prune --> MaxHeap["k-NN Bounded Max-Heap"]
    MaxHeap --> Neighbors["k-Nearest Neighbors + Distances"]
```
