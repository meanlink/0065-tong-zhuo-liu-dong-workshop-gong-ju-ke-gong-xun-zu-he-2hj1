from itertools import combinations

def communities(sets, threshold, pair_count):
    graph={key:set() for key in sets}
    edges=[]
    for (a,left),(b,right) in combinations(sets.items(),2):
        overlap=len(left&right)
        union=len(left|right)
        if not union or overlap<pair_count or overlap/union < threshold:
            continue
        ratio=round(overlap/union,4)
        graph[a].add(b)
        graph[b].add(a)
        edges.append({"left":a,"right":b,"shared":overlap,"union":union,"ratio":ratio})
    remaining=set(graph)
    groups=[]
    while remaining:
        unseen=[min(remaining)]
        component=set()
        while unseen:
            current=unseen.pop()
            if current not in remaining:
                continue
            remaining.remove(current)
            component.add(current)
            unseen.extend(graph[current]&remaining)
        if len(component)>1:
            groups.append((sorted(component), [e for e in edges if {e["left"],e["right"]}<=component]))
    return groups
