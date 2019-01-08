#!/usr/bin/python
# -*- coding: UTF-8 -*-

from typing import List, IO
from queue import Queue


class Graph:
    # 有向无环图
    def __init__(self, vertex_count: int) -> None:
        self.adj: List[List[int]] = [[] for _ in range(vertex_count)]

    def add_edge(self, s: int, t: int) -> None:
        self.adj[s].append(t)

    def __len__(self):
        return len(self.adj)


def topological_sort(g: Graph) -> IO[str]:
    size = len(g)
    in_degree: List[int] = [0] * size  # 记录每个顶点的入度
    for neighbors in g.adj:
        for n in neighbors:
            in_degree[n] += 1

    q = Queue()
    for vertex, neighbors_count in enumerate(in_degree):
        if neighbors_count == 0:
            q.put(vertex)

    while not q.empty():
        vertex = q.get()
        print(vertex, end=' ')
        for n in g.adj[vertex]:
            in_degree[n] -= 1
            if in_degree[n] == 0:
                q.put(n)


if __name__ == '__main__':
    g = Graph(5)
    g.add_edge(0, 3)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(1, 3)
    g.add_edge(2, 4)
    g.add_edge(3, 2)
    g.add_edge(3, 4)
    topological_sort(g)
