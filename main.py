
import sys

import wikipedia as wp

from typing import List
from wikipedia.exceptions import WikipediaException

NO_ITERATIONS = 10
SEED_ENTITIES = ["stone age flint arrowhead", "genius"]


def _get_search_candidates(s: str) -> List[str]:
    """
        Generates wikipedia page title candidates from a given string
    """
    words = s.split(" ")
    return [
        " ".join(words[i:])
        for i in range(len(words)-1, -1, -1)
    ][::-1]


def _retrieve_article(entity: str) -> str:
    """
        Retrieves the best article matched for a given an entity
    """
    candidates = _get_search_candidates(entity)
    for candidate in candidates:
        needs_retry = True
        while needs_retry:
            needs_retry = False
            try:
                p = wp.page(candidate)
                if p.title.lower() == candidate.lower():
                    return p
            except Exception as e:
                if "busy" in str(e):
                    needs_retry = True
    return None


def matching(seed_entities):
    P = []
    for entity in seed_entities:
        p = _retrieve_article(entity)
        if p is not None:
            P.append(p)
    return P


def classification():
    pass


def expansion():
    pass


for itr in range(NO_ITERATIONS):
    # matching()
    classification()
    expansion()


print(matching(SEED_ENTITIES))
