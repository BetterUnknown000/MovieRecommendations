# basic idea of tree structure
# Code made by Jack Demtshuk

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

# Hard coded tree
root = FeatureNode("Genre")

# Three generic branches
action = FeatureNode("Action")
drama = FeatureNode("Drama")
comedy = FeatureNode("Comedy")

# Three main children of the main root - Genre. This will be most generic.
root.add_child(action)
root.add_child(drama)
root.add_child(comedy)

# All the nodes included in the action subbranch
adventure = FeatureNode("Adventure")
thriller = FeatureNode("Thriller")
western = FeatureNode("Western")
war = FeatureNode("War")
scifi = FeatureNode("Sci-Fi")
fantasy = FeatureNode("Fantasy")

# Adding the connections
action.add_child(adventure)
action.add_child(thriller)
action.add_child(western)
action.add_child(war)
# Adventure subbranch
adventure.add_child(scifi)
adventure.add_child(fantasy)

# All the nodes included in the drama subbranch
romance = FeatureNode("Romance")
crime = FeatureNode("Crime")
mystery = FeatureNode("Mystery")
foreign = FeatureNode("Foreign")
documentary = FeatureNode("Documentary")
history = FeatureNode("History")

# Adding the connections
drama.add_child(romance)
drama.add_child(crime)
drama.add_child(mystery)
drama.add_child(foreign)
# Foreign subbranch
foreign.add_child(documentary)
foreign.add_child(history)


# All the nodes included in the comedy subbranch
animation = FeatureNode("Animation")
music = FeatureNode("Music")
horror = FeatureNode("Horror")
tv_movie = FeatureNode("TV Movie")
family = FeatureNode("Family")

# Adding the connections
comedy.add_child(animation)
# Animation subbranch
animation.add_child(music)
animation.add_child(horror)
# Horror subbranch
horror.add_child(tv_movie)
horror.add_child(family)

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

def find_parent(current, target, parent=None):
    if current == target:
        return parent
    for child in current.children:
        found = find_parent(child, target, current)
        if found:
            return found
    return None