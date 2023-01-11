from heapq import heappop, heappush
from itertools import count

def dijkstra_path(G, source, target, weight="weight"):
    (length, path) = single_source_dijkstra(G, source, target=target, weight=weight)
    return path

def dijkstra_path_length(G, source, target, weight="weight"):
    (length, path) = single_source_dijkstra(G, source, target=target, weight=weight)
    return length

def single_source_dijkstra(G, source, target, cutoff=None, weight="weight"):
    return multi_source_dijkstra(G, {source}, cutoff=cutoff, target=target, weight=weight)

def multi_source_dijkstra(G, sources, target=None, cutoff=None, weight="weight"):
    if not sources:
        raise ValueError("sources must not be empty")
    if target in sources:
        return (0, [target])
    weight = _weight_function(G, weight)
    paths = {source: [source] for source in sources}  # dictionary of paths
    dist = _dijkstra_multisource(G, sources, weight, paths=paths, cutoff=cutoff, target=target)
    if target is None:
        return (dist, paths)
    return (dist[target], paths[target])


def _weight_function(G, weight):
    if callable(weight):
        return weight
    return lambda u, v, data: data.get(weight, 1)

def _dijkstra_multisource(G, sources, weight, pred=None, paths=None, cutoff=None, target=None):
    G_succ = G._adj  # For speed-up (and works for both directed and undirected graphs)

    push = heappush
    pop = heappop
    dist = {}  # dictionary of final distances
    seen = {}
    # fringe is heapq with 3-tuples (distance,c,node)
    # use the count c to avoid comparing nodes (may not be able to)
    c = count()
    fringe = []
    for source in sources:
        seen[source] = 0
        push(fringe, (0, next(c), source))
    while fringe:
        (d, _, v) = pop(fringe)
        if v in dist:
            continue  # already searched this node.
        dist[v] = d
        if v == target:
            break
        for u, e in G_succ[v].items():
            cost = weight(v, u, e)
            if cost is None:
                continue
            vu_dist = dist[v] + cost
            if cutoff is not None:
                if vu_dist > cutoff:
                    continue
            if u in dist:
                u_dist = dist[u]
                if vu_dist < u_dist:
                    raise ValueError("Contradictory paths found:", "negative weights?")
                elif pred is not None and vu_dist == u_dist:
                    pred[u].append(v)
            elif u not in seen or vu_dist < seen[u]:
                seen[u] = vu_dist
                push(fringe, (vu_dist, next(c), u))
                if paths is not None:
                    paths[u] = paths[v] + [u]
                if pred is not None:
                    pred[u] = [v]
            elif vu_dist == seen[u]:
                if pred is not None:
                    pred[u].append(v)
    return dist