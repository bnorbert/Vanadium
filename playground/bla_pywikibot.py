import sys
import pywikibot as pw

site = pw.Site('en', 'wikipedia')

l = [
    cat.title()
    for cat in pw.Page(site, 'arrowhead').categories()
    if 'hidden' not in cat.categoryinfo
    ]
print([cat.split(":")[1] for cat in l])




