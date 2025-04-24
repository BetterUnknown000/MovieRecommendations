# basic idea of tree structure
# Code made by Jack Demtshuk
#
class FeatureNode:
    def __init__(self, name):
        self.name = name
        self.children = []
        self.movies = []

    def __repr__(self):
        return "Feature Node: " + str(self.name)

    def add_child(self, child):
        self.children.append(child)

    def add_movie(self, movie):
        self.movies.append(movie)


# root node is based off what the current feature is (genre, director)
root = FeatureNode("Genre")

#starting branches
action = FeatureNode("Action")
drama = FeatureNode("Drama")
comedy = FeatureNode("Comedy")

#children
scifi = FeatureNode("Sci-Fi")
adventure = FeatureNode("Adventure")
romcom = FeatureNode("Romantic Comedy")
spaceOpera = FeatureNode("Space Opera")

#building time
root.add_child(action)
root.add_child(drama)
root.add_child(comedy)

action.add_child(scifi)
action.add_child(adventure)
comedy.add_child(romcom)

scifi.add_child(spaceOpera)

# assign movies to connect to the genres

spaceOpera.add_movie("Star Wars")
romcom.add_movie("The Proposal")
adventure.add_movie("Indiana Jones")

# basically we are building this
#           Genre
#       /     |      \
#     Action   Drama   Comedy
#    /    \              |
#  Sci-Fi  Adventure     Romcom
#     |
# Space Opera

def find_genre(root, movie):
    if movie in root.movies:
        return root
    for child in root.children:
        result = find_genre(child, movie)
        if result:
            return result
    return None

def recommend(root, movie):
    genre = find_genre(root, movie)
    if not genre:
        return []
    parent = find_parent(root, genre)
    recommendations = []
    for sibling in parent.children:
        if sibling != genre:
            recommendations.extend(sibling.movies)
    return recommendations

def find_parent(current, target, parent = None):
    if current == target:
        return parent
    for child in current.children:
        found = find_parent(child, target, current)
        if found:
            return found
    return None

print(recommend(root, "Star Wars"))
