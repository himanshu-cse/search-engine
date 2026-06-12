import json

with open("indexing/vocabulary.json") as f:
    vocabulary = json.load(f)

with open("indexing/trie.json") as f:
    trie = json.load(f)

def find_node(prefix):
    node = trie
    for char in prefix:
        if char not in node:
            return None
        node = node[char]

    return node

def collect_words(node, prefix, results):
    if "_end" in node:
        results.append(prefix)

    for char, child in node.items():
        if char == "_end":
            continue

        collect_words(child, prefix+char, results)

def autocomplete(prefix, limit=10):
    prefix = prefix.lower()
    node = find_node(prefix)

    if node is None:
        return []
    
    results = []
    collect_words(node, prefix, results)
    results.sort(key=lambda word: vocabulary.get(word, 0), reverse=True)
    return results[:limit]