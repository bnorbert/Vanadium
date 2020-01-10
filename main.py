
import sys
import time
import random

import wikipedia as wp
import pywikibot as pw

from typing import List, Set
from wikipedia.exceptions import WikipediaException
from wikipedia import WikipediaPage
from seeds import SEED_ENTITIES

NO_ITERATIONS = 3
SITE = pw.Site("en", "wikipedia")
clarifier = {
    "european": "Europe",
    "nam": "Vietnam War",
}


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
    N_SAMPLE = 30
    HL = set()
    for article in articles:
        HL.update(set(article.links))
    HL = set(random.sample(HL, N_SAMPLE))

    ret = set()
    print(list(HL))
    for hl in HL:
        p = _fetch_page(hl)
        p_fgcs = set(_extract_fgcc(p))
        if len(fgcs.intersection(p_fgcs)) > 0:
            ret.add(hl)
    return hl


def _retrieve_article(entity: str) -> str:
    """
        Retrieves the best article matched for a given an entity
    """
    # TODO: I think at this point we might need to keep track of redirecting links
    # and maybe consider a synonimy relationship for them
    candidates = _get_search_candidates(entity)
    for candidate in candidates:
        p = _fetch_page(candidate)
        if p == None:
            continue
        if p.title.lower() == candidate.lower():
            return p
    last_candidate = clarify(candidates[-1])
    return _fetch_page(last_candidate)


def _get_search_candidates(s: str) -> List[str]:
    """
        Generates wikipedia page title candidates from a given string
    """
    words = s.split(" ")
    return [
        " ".join(words[i:])
        for i in range(len(words)-1, -1, -1)
    ][::-1]


def _fetch_page(page_name: str) -> WikipediaPage:
    needs_retry = True
    while needs_retry:
        needs_retry = False
        try:
            p = wp.page(page_name)
            return p
        except Exception as e:
            if "busy" in str(e):
                needs_retry = True
                time.sleep(.1)
            else:
                print(e)


def _extract_fgcc(article: WikipediaPage) -> List[str]:
    # TODO: change the logic of this to enable tight category structure (>2 counts per category)
    global SITE
    ret = []
    if article == None:
        return []
    for cat in pw.Page(SITE, article.title).categories():
        if cat == None:
            continue
        if "hidden" not in cat.categoryinfo:
            ret.append(cat.title().split(":")[1])

    return ret


def clarify(entity):
    global clarifier
    if entity.lower() in clarifier.keys():
        return clarifier[entity]
    return entity


# __________________________ MAIN _______________________________
ALL_ENTITIES = set()


def update_all_entities(entities):
    global ALL_ENTITIES
    for entity in entities:
        ALL_ENTITIES.add(entity)


update_all_entities(SEED_ENTITIES)

for _ in range(NO_ITERATIONS):
    P = matching(SEED_ENTITIES)
    print("P:")
    print(P)
    print()
    L = classification(P)
    print("L:")
    print(list(L))
    print()
    HL = expansion(P, L)
    print("HL:")
    print(HL)
    print("-" * 30)
    SEED_ENTITIES = list(set(L))
    update_all_entities(L)

# THE NEXT SECTION WILL PROBABLY NEED SOME CLEANING UP

print("ENDDDDDDD")
print("-" * 40)
print(ALL_ENTITIES)

sys.exit(0)

print(matching(SEED_ENTITIES))
res = classification(matching(SEED_ENTITIES))
for cat in res:
    print(cat)
print("N_CATEGORIES:")
print(len(res))
