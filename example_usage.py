from client import KDTree

data_pts = [
    ((2, 3), "Sensor-A"),
    ((5, 4), "Sensor-B"),
    ((9, 6), "Sensor-C"),
    ((4, 7), "Sensor-D"),
    ((8, 1), "Sensor-E"),
    ((7, 2), "Sensor-F")
]
tree = KDTree(data_pts, k=2)

query = (9, 2)
pt, tag, dist = tree.nearest_neighbor(query)
print(f"Query {query} -> 1-NN: {tag} at {pt}, Distance: {dist:.4f}")

knn = tree.k_nearest_neighbors(query, k=3)
print(f"3-NN Results:")
for p, t, d in knn:
    print(f"  {t} @ {p} - dist={d:.4f}")
