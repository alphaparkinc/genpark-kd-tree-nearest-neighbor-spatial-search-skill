"""k-Dimensional Tree (KD-Tree) Spatial Search Engine.
100% Python Standard Library.
"""

import math
import heapq

class KDTree:
    """k-Dimensional Tree for nearest neighbor and radius spatial queries."""
    class Node:
        def __init__(self, point, axis, left=None, right=None, data=None):
            self.point = tuple(point)
            self.axis = axis
            self.left = left
            self.right = right
            self.data = data

    def __init__(self, points_with_data=None, k=2):
        self.k = k
        self.root = self._build(points_with_data or [], depth=0)

    def _build(self, points, depth):
        if not points:
            return None
        axis = depth % self.k
        points.sort(key=lambda item: item[0][axis])
        median_idx = len(points) // 2
        pt, data = points[median_idx]
        return self.Node(
            point=pt,
            axis=axis,
            left=self._build(points[:median_idx], depth + 1),
            right=self._build(points[median_idx + 1:], depth + 1),
            data=data
        )

    def nearest_neighbor(self, target):
        target = tuple(target)
        best = {"node": None, "dist_sq": float("inf")}

        def search(node):
            if node is None:
                return
            d_sq = sum((a - b)**2 for a, b in zip(target, node.point))
            if d_sq < best["dist_sq"]:
                best["dist_sq"] = d_sq
                best["node"] = node

            axis = node.axis
            diff = target[axis] - node.point[axis]
            first = node.left if diff < 0 else node.right
            second = node.right if diff < 0 else node.left

            search(first)
            if diff**2 < best["dist_sq"]:
                search(second)

        search(self.root)
        if best["node"]:
            return best["node"].point, best["node"].data, math.sqrt(best["dist_sq"])
        return None, None, float("inf")

    def k_nearest_neighbors(self, target, k=3):
        target = tuple(target)
        heap = []

        def search(node):
            if node is None:
                return
            d_sq = sum((a - b)**2 for a, b in zip(target, node.point))
            if len(heap) < k:
                heapq.heappush(heap, (-d_sq, node.point, node.data))
            elif d_sq < -heap[0][0]:
                heapq.heapreplace(heap, (-d_sq, node.point, node.data))

            axis = node.axis
            diff = target[axis] - node.point[axis]
            first = node.left if diff < 0 else node.right
            second = node.right if diff < 0 else node.left

            search(first)
            worst_d_sq = -heap[0][0] if len(heap) >= k else float("inf")
            if diff**2 < worst_d_sq:
                search(second)

        search(self.root)
        results = sorted([(-item[0], item[1], item[2]) for item in heap])
        return [(pt, data, math.sqrt(d_sq)) for d_sq, pt, data in results]
