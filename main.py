MAX_USERS = 100


class AdjNode:
    def __init__(self, vertex, next_node=None):
        self.vertex = vertex
        self.next = next_node


class SocialGraph:
    def __init__(self, num_vertices):
        if num_vertices > MAX_USERS:
            raise ValueError(f"num_vertices must be <= {MAX_USERS}")

        self.num_vertices = num_vertices
        self.adj_lists = [None for _ in range(num_vertices)]

    def insert_sorted(self, u, v):
        new_node = AdjNode(v)

        if self.adj_lists[u] is None or v < self.adj_lists[u].vertex:
            new_node.next = self.adj_lists[u]
            self.adj_lists[u] = new_node
            return

        prev = self.adj_lists[u]
        current = self.adj_lists[u].next

        while current is not None and current.vertex < v:
            prev = current
            current = current.next

        new_node.next = current
        prev.next = new_node

    def add_friendship(self, u, v):
        if not self.has_edge(u, v):
            self.insert_sorted(u, v)
            self.insert_sorted(v, u)

    def has_edge(self, u, v):
        current = self.adj_lists[u]

        while current is not None:
            if current.vertex == v:
                return True
            if current.vertex > v:
                return False
            current = current.next

        return False

    def neighbors(self, u):
        result = []
        current = self.adj_lists[u]

        while current is not None:
            result.append(current.vertex)
            current = current.next

        return result


def dfs_recursive_util(graph, u, visited, order):
    visited[u] = True
    order.append(u)

    current = graph.adj_lists[u]
    while current is not None:
        if not visited[current.vertex]:
            dfs_recursive_util(graph, current.vertex, visited, order)
        current = current.next


def dfs_recursive(graph, start_user):
    visited = [False] * graph.num_vertices
    order = []
    dfs_recursive_util(graph, start_user, visited, order)
    return order


def dfs_iterative(graph, start_user):
    visited = [False] * graph.num_vertices
    order = []
    stack = [start_user]

    while stack:
        u = stack.pop()
        if not visited[u]:
            visited[u] = True
            order.append(u)

            for vertex in graph.neighbors(u):
                if not visited[vertex]:
                    stack.append(vertex)

    return order


def find_connected_components(graph):
    components = []
    visited = [False] * graph.num_vertices

    for i in range(graph.num_vertices):
        if not visited[i]:
            component_order = []
            dfs_recursive_util(graph, i, visited, component_order)
            components.append(component_order)

    return components


def is_connected(graph):
    if graph.num_vertices <= 1:
        return True

    return len(dfs_recursive(graph, 0)) == graph.num_vertices


def has_path_util(graph, u, target, visited):
    if u == target:
        return True

    visited[u] = True
    current = graph.adj_lists[u]

    while current is not None:
        if not visited[current.vertex]:
            if has_path_util(graph, current.vertex, target, visited):
                return True
        current = current.next

    return False


def has_path(graph, start_user, target_user):
    visited = [False] * graph.num_vertices
    return has_path_util(graph, start_user, target_user, visited)


def find_path_util(graph, u, target, visited, path):
    visited[u] = True
    path.append(u)

    if u == target:
        return True

    current = graph.adj_lists[u]
    while current is not None:
        if not visited[current.vertex]:
            if find_path_util(graph, current.vertex, target, visited, path):
                return True
        current = current.next

    path.pop()
    return False


def find_path(graph, start_user, target_user):
    visited = [False] * graph.num_vertices
    path = []
    find_path_util(graph, start_user, target_user, visited, path)
    return path


def get_connected_components_sizes(graph):
    return [len(component) for component in find_connected_components(graph)]


def find_largest_component(graph):
    largest = []

    for component in find_connected_components(graph):
        if len(component) > len(largest):
            largest = component

    return largest


def find_isolated_users(graph):
    isolated = []

    for i in range(graph.num_vertices):
        if graph.adj_lists[i] is None:
            isolated.append(i)

    return isolated


graph = SocialGraph(8)
graph.add_friendship(0, 1)
graph.add_friendship(1, 2)
graph.add_friendship(2, 3)
graph.add_friendship(4, 5)
graph.add_friendship(5, 6)

print("Adjacency lists:")
for user in range(graph.num_vertices):
    print(f"{user}: {graph.neighbors(user)}")

print("\nDFS recursive from 0:", dfs_recursive(graph, 0))
print("DFS iterative from 0:", dfs_iterative(graph, 0))

components = find_connected_components(graph)
print("\nConnected components:", components)
print("Connected component sizes:", get_connected_components_sizes(graph))
print("Largest component:", find_largest_component(graph))
print("Is graph connected?", is_connected(graph))
print("Isolated users:", find_isolated_users(graph))

print("\nPath checks:")
print("Has path from 0 to 3?", has_path(graph, 0, 3))
print("Has path from 0 to 6?", has_path(graph, 0, 6))
print("Find path from 0 to 3:", find_path(graph, 0, 3))
print("Find path from 4 to 6:", find_path(graph, 4, 6))
