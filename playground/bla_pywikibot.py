import sys
import pywikibot as pw

site = pw.Site('en', 'wikipedia')

print([
    cat.title()
    for cat in pw.Page(site, 'arrowhead').categories()
    if 'hidden' not in cat.categoryinfo
])



