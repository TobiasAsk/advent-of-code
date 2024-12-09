'''
Very much thought that topological sorting was the way to go here,
but to my disappointment the graph has cycles, which took me some time to
figure out. Instead, the approach is to check whether any number appears before it
should, i.e., that it is listed as a successor of the next number in the sequence.
'''

import sys
from collections import defaultdict
import pygraphviz as pgv


def make_graph(ordering_rules: list[str]) -> tuple[dict[int, list[int]], set[int]]:
    edges = defaultdict(list)
    graph_vis = pgv.AGraph(directed=True)

    for rule in ordering_rules:
        precursor_page, other_page = map(int, rule.split('|'))
        # graph_vis.add_nodes_from(nodes)
        # graph_vis.add_edge(precursor_page, other_page)
        edges[precursor_page].append(other_page)

    # graph_vis.draw('graph.png', prog='dot')

    return edges


# def topological_sort(edges: dict, nodes: set) -> list[int]:
#     sorted_pages = []
#     visited = {n: False for n in nodes}
#     unvisited = list(nodes)

#     while unvisited:
#         node = unvisited.pop()

#         if visited[node]:
#             continue

#         q = [node]

#         while q:
#             node_in_search = q.pop()
#             if not visited[node_in_search]:
#                 visited[node_in_search] = True

#                 if edges[node_in_search]:
#                     q.extend(n for n in edges[node_in_search] if not visited[n])
#                 else:
#                     sorted_pages.insert(0, node_in_search)

#         sorted_pages.insert(0, node)

#     return sorted_pages


# def is_subsequence(s1, s2):
#     n, m = len(s1), len(s2)
#     i, j = 0, 0
#     while (i < n and j < m):
#         if (s1[i] == s2[j]):
#             i += 1
#         j += 1

#     return i == n

def fix_order(numbers: list[int], graph: dict) -> list[int]:
    ordered_nums = list(numbers)

    found_offender = True
    while found_offender:
        found_offender = False
        for i in range(len(numbers)-1):
            num = ordered_nums[i]
            next_num = ordered_nums[i+1]
            if num in graph[next_num]:
                ordered_nums[i], ordered_nums[i+1] = ordered_nums[i+1], ordered_nums[i]
                found_offender = True

    return ordered_nums


def main():
    filename = sys.argv[1]
    with open(filename) as printing_instructions_file:
        ordering_rules, updates = tuple(p.splitlines() for p in
                                        printing_instructions_file.read().split('\n\n'))

    graph = make_graph(ordering_rules)

    mid_page_sum = 0
    for update in updates:
        numbers = list(map(int, update.split(',')))
        for i in range(len(numbers)-1):
            num = numbers[i]
            next_num = numbers[i+1]
            if num in graph[next_num]:
                ordered_nums = fix_order(numbers, graph)
                mid_page_sum += ordered_nums[len(ordered_nums)//2]
                break

    print(mid_page_sum)


if __name__ == '__main__':
    main()
