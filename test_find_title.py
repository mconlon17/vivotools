"""
    test_find_title.py -- from a title dictionary, find titles and return
    their URIs.

    Version 0.1 MC 2013-12-28
    --  Initial version.  Make a dictionary and make a dictionary with
        debug=True
"""

__author__      = "Michael Conlon"
__copyright__   = "Copyright 2013, University of Florida"
__license__     = "BSD 3-Clause license"
__version__     = "0.1"

import vivotools as vt
from datetime import datetime

print datetime.now(),"Start"
print datetime.now(),"Making title dictionary"
title_dictionary = vt.make_title_dictionary(debug=True)
print datetime.now(),"title dictionary has ",len(title_dictionary),"entries"
titles = [
    "A New Confidence Interval for the Difference of Two Binomial Proportions",
    "A New Cytolytic Protein From the Sea Anemone Urticina Crassicornis That Binds To Cholesterol- and Sphingomyelin-Rich Membranes",
    "A New Deletion Refines the Boundaries of the Murine Prader-Willi Syndrome Imprinting Center",
    "A New Derivative of Roxithromycin Modulates Immunological Responses and Ameliorates Collagen-Induced Arthritis",
    "A New Digitized Method of the Compulsive Gnawing Test Revealed Dopaminergic Activity of Salvinorin a in Vivo",
    "A New Discourse Theory of the Firm After Citizens United",
    "A New Discovery in Unfindable Titles",
    "A New Disease of Syzygium Paniculatum (Myrtaceae)",
    "A New Dosing Protocol Reduces Dexmedetomidine-Associated Hypotension in Critically Ill Surgical Patients",
    "A New Drug-Sensing Paradigm Based On Ion-Current Rectification in a Conically Shaped Nanopore",
    "A New Elasticity Element Made for Enforcing Weak Stress Symmetry"
    ]
for title in titles:
    [found,uri] = vt.find_title(title,title_dictionary)
    print str(found).ljust(5),title,uri

print datetime.now(),"Finished"
