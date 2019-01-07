#!/usr/bin/python
# -*- coding: UTF-8 -*-

from queue import PriorityQueue
from typing import List, IO
import pygraphviz as pgv

OUTPUT_PATH = 'C:/Users/gz1301/'


class Graph:
    def __init__(self, vertex_count: int) -> None:
        self.adj = [[] for _ in range(vertex_count)]

    def add_edge(self, s: int, t: int, w: int) -> None:
        edge = Edge(s, t, w)
        self.adj[s].append(edge)

    def draw_graph(self) -> None:
        graph = pgv.AGraph(strict=False, directed=True, rankdir='LR')
        for vertex, edges in enumerate(self.adj):
            graph.add_node(vertex, style='filled', fillcolor='red', fontcolor='white')
            for e in edges:
                graph.add_edge(e.s, e.t, label=e.w)

        graph.graph_attr['epsilon'] = '0.01'
        graph.layout('dot')
        graph.draw(OUTPUT_PATH + 'directed_graph_with_weight.png')

    def __len__(self):
        return len(self.adj)


class Vertex:
    def __init__(self, v: int, dist: int) -> None:
        self.id = v
        self.dist = dist

    def __gt__(self, other):
        return self.dist > other.dist

    def __repr__(self):
        return str((self.id, self.dist))


class Edge:
    def __init__(self, source: int, target: int, weight: int) -> None:
        self.s = source
        self.t = target
        self.w = weight


def dijkstra(g: Graph, s: int, t: int) -> int:
    """
    dijkstra = 穷举 + 优先级队列
    :param g:
    :param s:
    :param t:
    :return:
    """
    size = len(g)

    pq = PriorityQueue(size)    # 节点队列
    in_queue = [False] * size   # 已入队标记
    vertices = [                # 需要随时更新离s的最短距离的节点列表
        Vertex(v, float('inf')) for v in range(size)
    ]
    predecessor = [-1] * size   # 先驱

    vertices[s].dist = 0
    pq.put(vertices[s])
    in_queue[s] = True

    while not pq.empty():
        print('cur queue: ', pq)
        v = pq.get()
        print('get vertex: ', v)
        if v.id == t:
            break
        for edge in g.adj[v.id]:
            if v.dist + edge.w < vertices[edge.t].dist:
                # TODO: pq更新了队列中的元素的优先级之后，不会堆化
                # TODO: 需要自己维护一个小顶堆
                vertices[edge.t].dist = v.dist + edge.w
                predecessor[edge.t] = v.id
            if not in_queue[edge.t]:
                pq.put(vertices[edge.t])
                in_queue[edge.t] = True

    for n in print_path(s, t, predecessor):
        if n == t:
            print(t)
        else:
            print(n, end=' -> ')
    return vertices[t].dist


def print_path(s: int, t: int, p: List[int]) -> IO[str]:
    if t == s:
        yield s
    else:
        yield from print_path(s, p[t], p)
        yield t


if __name__ == '__main__':
    g = Graph(6)
    g.add_edge(0, 1, 10)
    g.add_edge(0, 4, 15)
    g.add_edge(1, 2, 15)
    g.add_edge(1, 3, 2)
    g.add_edge(2, 5, 5)
    g.add_edge(3, 2, 1)
    g.add_edge(3, 5, 12)
    g.add_edge(4, 5, 10)
    g.draw_graph()
    print(dijkstra(g, 0, 5))
