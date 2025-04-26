from tree.Tree import root
class GenreTree:

    def __init__(self, root):
        self.root = root

    def find_node(self, current, genre):
        if current.name == genre:
            return current
        for child in current.children:
            result = self.find_node(child, genre)
            if result:
                return result
        return None

    def find_genre_distance(self, start_genre, target_genre):
        start_node = self.find_node(self.root, start_genre)
        if not start_node:
            return None
        return self._dfs_distance(start_node, target_genre, 0)

    def _dfs_distance(self, current, target_genre, distance): # Recursive call
        if current.name == target_genre:
            return distance
        for child in current.children:
            found_distance = self._dfs_distance(child, target_genre, distance + 1)
            if found_distance is not None:
                return found_distance
        return None
genre_tree = GenreTree(root)