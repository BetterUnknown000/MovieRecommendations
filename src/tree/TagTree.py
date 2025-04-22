from src.data.DatasetLoader import DatasetLoader

loader = DatasetLoader("C:/cleaned_movies.csv")
movies = loader.load_dataset()

all_tags = set()
for movie in movies:
    all_tags.update(movie.tags)

class TagNode:
    def __init__(self, tag):
        self.tag = tag
        self.left = None
        self.right = None

class TagTree:
    def __init__(self, tags):
        sorted_tags = sorted(tags)
        self.root = self.build_tree(sorted_tags)

    def build_tree(self, tags):
        if not tags:
            return None
        mid = len(tags) // 2
        node = TagNode(tags[mid])
        node.left = self.build_tree(tags[:mid])
        node.right = self.build_tree(tags[mid+1:])
        return node

    def search(self, tag):
        current = self.root
        while current is not None:

            if tag == current.tag:
                return True
            elif tag < current.tag:
                current = current.left
            else:
                current = current.right
        return False

    def in_order_traversal(self):
        result = []
        stack = []
        current = self.root

        while stack or current:
            while current:
                stack.append(current)
                current = current.left
            current = stack.pop()
            result.append(current.tag)
            current = current.right

        return result

    def compare_movie_tags(self, movie1, movie2):
        tags1 = set(movie1.tags) if hasattr(movie1, 'tags') and movie1.tags else set()
        tags2 = set(movie2.tags) if hasattr(movie2, 'tags') and movie2.tags else set()

        common_tags = tags1.intersection(tags2)
        all_tags = tags1.union(tags2)

        similarity_score = len(common_tags) / len(all_tags) if all_tags else 0.0

        return {
            "common_tags": list(common_tags),
            "similarity_score": similarity_score
        }

