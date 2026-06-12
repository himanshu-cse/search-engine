import json

with open("indexing/vocabulary.json") as f:
    vocabulary = json.load(f)

trie = {}

for word in vocabulary.keys():
    node = trie
    for char in word:
        if char not in node:
            node[char] = {}
        node = node[char]
    node["_end"] = True

with open("indexing/trie.json", "w") as f:
    json.dump(trie, f)

print(f"built trie with {len(vocabulary)} words")
        