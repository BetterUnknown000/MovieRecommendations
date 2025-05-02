import pandas as pd

def bulk_replace_tags(file_path, replacements_dict, output_file):
    # Load the CSV
    df = pd.read_csv(file_path)

    def replace_tags(cell):
        if pd.isna(cell):
            return cell
        tags = [tag.strip() for tag in cell.split(',')]
        updated_tags = []
        for tag in tags:
            replaced = False
            for target_word, replacement in replacements_dict.items():
                if target_word.lower() in tag.lower():
                    if replacement not in updated_tags:
                        updated_tags.append(replacement)
                    replaced = True
                    break  # Stop checking other words once one matches
            if not replaced:
                updated_tags.append(tag)
        return ', '.join(updated_tags)

    # Apply the replacement function
    df['tags'] = df['tags'].apply(replace_tags)

    # Save the updated CSV
    df.to_csv(output_file, index=False)
    print(f"Updated CSV saved to {output_file}")

# Example usage:
replacements = {
    "boy": "Child",
    "boy next door": "Child",
    "teenage boy": "Child",
    "girl": "Child",
    "children": "Child",
    "childhood": "Child",
    "toy": "Toy",
    "new toy": "Toy",
    "toy comes to life": "Toy",
    "dog": "Animal",
    "wolf": "Animal",
    "bat": "Animal",
    "goose": "Animal",
    "cat": "Animal",
    "animal": "Animal",
    "jealousy": "Emotion",
    "rage and hate": "Emotion",
    "lovesickness": "Emotion",
    "friendship": "Friendship",
    "friends": "Friendship",
    "best friend": "Friendship",
    "brother brother relationship": "Family",
    "mother daughter relationship": "Family",
    "interracial relationship": "Relationship",
    "teacher student relationship": "School",
    "alcoholism": "Addiction",
    "alcohol abuse": "Addiction",
    "drug abuse": "Addiction",
    "based on novel": "Adaptation",
    "based on children's book": "Adaptation",
    "serial killer": "Crime",
    "crime": "Crime",
    "murder": "Crime",
    "bank robbery": "Crime",
    "police": "Law Enforcement",
    "detective": "Law Enforcement",
    "shootout": "Violence",
    "gun fight": "Violence",
    "rape": "Crime",
    "violence": "Violence",
    "chase": "Exciting",
    "explosion": "Exciting",
    "heist": "Crime",
    "money": "Wealth",
    "mafia": "Crime",
    "gang": "Crime",
    "casino": "Gambling",
    "hotel room": "Hotel",
    "los angeles": "USA",
    "paris": "France",
    "seattle": "USA",
    "new york city": "USA",
    "st. petersburg russia": "Russia",
    "detroit michigan": "USA",
    "space": "Science",
    "time travel": "Science",
    "virus": "Science",
    "post-apocalyptic": "Apocalypse",
    "teacher": "School",
    "hitman": "Crime",
    "cop": "Law Enforcement",
    "president": "Political",
    "usa president": "Political",
    "election": "Political",
    "white house": "Political",
    "mother": "Family",
    "father": "Family",
    "brother": "Family",
    "sister": "Family",
    "cousin": "Family",
    "uncle": "Family",
    "aunt": "Family",
    "marriage": "Relationship",
    "divorce": "Relationship",
    "widow": "Relationship",
    "widower": "Relationship",
    "miami": "USA",
    "cia": "Law Enforcement",
    "poker": "Gambling",
    "shot": "Violence",
    "shoot": "Violence",
    "gun": "Violence",
    "knife": "Violence",
    "stab": "Violence",
    "bank": "Wealth",
    "philadelphia": "USA",
    "terrorist": "Crime",
    "island": "Tropical",
    "love": "Relationship",
    "dying": "Death",
    "die": "Death",
    "death": "Death",
    "music": "Musical",
    "musician": "Musical",
    "monster": "Scary",
    "beast": "Scary",
    "vampire": "Scary",
    "political": "Political",
    "family": "Family",
    "true story": "Adaptation",

    # Add more mappings as needed
}

bulk_replace_tags("cleaned_movies.csv", replacements, "final_movies.csv")
