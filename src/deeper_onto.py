import sys
import pprint
import wikipedia as wp
import nltk

seeds = ["arrow", "axe", "sword", "warrior"]
graph = {}
clarifier = {
    "sword": "Sword_(Weapon)",
    "thrown": "object",
    "implement": "Tool",
    "reason": "being",
    "material": "thing",
    "object": "thing",
}


def _get_be_index(tags):
    # is | are
    idx = 0
    while tags[idx][0].lower() not in ['is', 'are', "means"]:
        idx = idx + 1
    if idx == len(tags):
        raise Exception("Is/are not found!")
    return idx


def _get_first_NN_after_idx(idx, tags):
    for i in range(idx, len(tags)):
        if tags[i][1] == 'NN':
            return tags[i][0]
    raise Exception("NN not found after be")


def _get_super_class(tags):
    idx = _get_be_index(tags)
    return _get_first_NN_after_idx(idx, tags)


def clarify(entity):
    global clarifier
    if entity.lower() in clarifier.keys():
        return clarifier[entity.lower()]
    return entity


itr_elems = seeds
all_elems = set(seeds)
while len(itr_elems) > 0:

    new_itr_elems = []

    for entity in itr_elems:
        entity = clarify(entity)
        if entity.lower() == "thing" or entity.lower() == "object":
            continue

        # get tags from the first sentence on wikipedia
        try:
            first_sentence = wp.page(entity).content.split(".")[0]
        except Exception as e:
            print(e)
            print(graph)
            sys.exit(0)
        tags = nltk.pos_tag(nltk.word_tokenize(first_sentence))

        # actually get super_class
        super_class = _get_super_class(tags)

        # keep track of data
        clarified_super_class = clarify(super_class)
        graph[entity] = clarified_super_class

        # do consistency checks
        if super_class not in all_elems:
            new_itr_elems.append(super_class)
            all_elems.add(super_class)

    itr_elems = new_itr_elems

print(graph)

# don't handle exceptions but throw them
