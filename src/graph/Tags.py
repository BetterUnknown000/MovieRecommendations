#
# Code made by Nick Taweel
# 
class Tag:
    def __init__(self, name, description=None):
        self.name = name
        self.description = description

    def __repr__(self):
        return f"Tag(name={self.name}, description={self.description})"


class TagGraph:
    def __init__(self):
        self.tags = {}
        self.graph = {}

    def add_tag(self, tag):
        if tag.name not in self.tags:
            self.tags[tag.name] = tag
            self.graph[tag.name] = {}
        else:
            print(f"Tag '{tag.name}' already exists.")

    def remove_tag(self, tag_name):
        if tag_name not in self.tags:
            print(f"Tag '{tag_name}' does not exist.")
            return

        for connected_tag in list(self.graph[tag_name].keys()):
            del self.graph[connected_tag][tag_name]

        del self.graph[tag_name]
        del self.tags[tag_name]

    def get_tag_likeness_percentage(self, movie1_tags, movie2_tags):
        score = 0
        comparisons = 0

        tags1 = set(movie1_tags)
        tags2 = set(movie2_tags)

        for tag1 in tags1:
            comparisons += 1
            if tag1 in tags2:
                score += 3
            else:
                # check if any of tag1's neighbors are in tags2
                neighbors = self.graph.get(tag1, {})
                if any(neighbor in tags2 for neighbor in neighbors):
                    score += 1

        for tag2 in tags2:
            if tag2 not in tags1:
                comparisons += 1
                neighbors = self.graph.get(tag2, {})
                if any(neighbor in tags1 for neighbor in neighbors):
                    score += 1

        if comparisons == 0:
            return 0.0

        max_score = comparisons * 3.0
        return (score / max_score) * 100.0

    def __repr__(self):
        return f"TagGraph(tags={list(self.tags.keys())}, graph={self.graph})"
