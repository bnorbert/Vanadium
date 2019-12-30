
import sys

import wikipedia as wp
import pywikibot as pw

from typing import List, Set
from wikipedia.exceptions import WikipediaException
from wikipedia import WikipediaPage

NO_ITERATIONS = 10
SEED_ENTITIES = [
    "stone age flint arrowhead",
    "genius", "archery", "python", "java", "star wars", "movie", "apple", "pear"]
SEED_ENTITIES = ["Iron Age"]
SITE = pw.Site("en", "wikipedia")


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
    # TODO: I think at this point we might need to keep track of redirecting links
    # and maybe consider a synonimy relationship for them
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


def _extract_fgcc(article: WikipediaPage) -> List[str]:
    # TODO: change the logic of this to enable tight category structure (>2 counts per category)
    global SITE

    # return article.categories
    return [
        cat.title().split(":")[1]
        for cat in pw.Page(SITE, article.title).categories()
        if "hidden" not in cat.categoryinfo
    ]


def matching(seed_entities: List[str]) -> List[WikipediaPage]:
    P = []
    for entity in seed_entities:
        p = _retrieve_article(entity)
        if p is not None:
            P.append(p)
    return P


def classification(P: List[WikipediaPage]) -> Set[str]:
    L = set()
    for p in P:
        L.update(set(_extract_fgcc(p)))
    return L


def expansion(articles: List[WikipediaPage], fgcs: Set[str]) -> List[str]:
    HL = set()
    for article in articles:
        HL.update(set(article.links))
    external_entities = [wp.Page(hl) for hl in HL]

    ret = set()
    for hl in HL:
        p = wp.page(hl)
        p_fgcs = set(_extract_fgcc(p))
        if len(fgcs.intersection(p_fgcs)) > 0:
            ret.add(hl)
    return hl


for itr in range(NO_ITERATIONS):
    # P = matching()
    # L = classification()
    # expansion(P, L)

    # THE NEXT SECTION WILL PROBABLY NEED SOME CLEANING UP

print(matching(SEED_ENTITIES))
res = classification(matching(SEED_ENTITIES))
for cat in res:
    print(cat)
print("N_CATEGORIES:")
print(len(res))
