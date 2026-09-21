import nltk
from nltk.corpus import wordnet as wn

print("Downloading WordNet database...")
nltk.download('wordnet')

print("Filtering physical items/artifacts...")
a_items = set()

# Get the base category for physical artifacts/objects
artifact_root = wn.synset('artifact.n.01')

# Loop through all noun synsets starting with 'a'
for synset in wn.all_synsets(wn.NOUN):
    name = synset.name().split('.')[0]
    if name.startswith('z'):
        # Check if the noun is a subclass of a physical artifact/object
        hypernyms = synset.closure(lambda s: s.hypernyms())
        if artifact_root in hypernyms or synset == artifact_root:
            for lemma in synset.lemmas():
                clean_word = lemma.name().replace('_', ' ').strip().title()
                if clean_word.lower().startswith('z'):
                    a_items.add(clean_word)

# Save formatted list to text file
filename = "a_items_formatted.txt"
sorted_items = sorted(a_items)

with open(filename, "w", encoding="utf-8") as f:
    for item in sorted_items:
        f.write(f'"{item}",\n')

print(f"DONE! Saved {len(sorted_items)} formatted items to '{filename}'.")
