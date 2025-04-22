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