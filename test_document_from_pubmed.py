"""
    test_document_from_pubmed.py -- use Entrez to retrive a document entry from
    Pubmed, and format it as a reusable python structure

    Version 0.1 MC 2013-12-28
    --  Initial version.
"""

__author__      = "Michael Conlon"
__copyright__   = "Copyright 2013, University of Florida"
__license__     = "BSD 3-Clause license"
__version__     = "0.1"

import vivotools as vt
from datetime import datetime
from Bio import Entrez

print datetime.now(),"Start"

pmids = [
    "18068940",
    "18089571",
    "19206997",
    "21822356",
    "19247798",
    "21493414",
    "12099768",
    "11410031",
    "20143936",
    "16934145"
    ]

for pmid in pmids:
    handle = Entrez.efetch(db="pubmed", id=pmid, retmode="xml")
    records = Entrez.parse(handle)
    for record in records:
        print "\n",pmid,vt.document_from_pubmed(record)

print datetime.now(),"Finish"
