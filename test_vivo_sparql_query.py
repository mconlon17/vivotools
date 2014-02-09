"""
    test_vivo_sparql_query.py -- issue a SPARQL query to VIVO and return
    the result as a JSON object

    Version 0.1 MC 2013-12-28
    --  Initial version.

"""

__author__      = "Michael Conlon"
__copyright__   = "Copyright 2013, University of Florida"
__license__     = "BSD 3-Clause license"
__version__     = "0.1"

import vivotools as vt
import json
from datetime import datetime

print datetime.now(),"Start"

query = """
    SELECT ?p ?o
    WHERE {
      <http://vivo.ufl.edu/individual/n25562> ?p ?o
    }
    ORDER BY ?p
    """

data=vt.vivo_sparql_query(query,debug=True) # show the encoded query                                # issue the query, return the data
print "Retrieved data:\n" + json.dumps(data, sort_keys=True, indent=4)
print "Items found = ",len(data["results"]["bindings"])
print datetime.now(),"Finish"
