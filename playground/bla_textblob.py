import sys

import wikipedia as wp

from textblob import TextBlob

S = sys.argv[1]


def extract_noun_phrase(entity):
    
    print(entity)
    first_sentence = wp.page(entity).content.split(".")[0]
    print(first_sentence)
    blob = TextBlob(first_sentence)
    print("pos tags:")
    print(blob.pos_tags)
    print("tags:")
    print(blob.tags)
    print("noun phrases:")
    print(blob.noun_phrases)
    return blob.noun_phrases

result = extract_noun_phrase(S)
#print("FINAL RESULT:")
#print(result)


