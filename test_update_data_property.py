"""
    test_update_data_property.py -- Given a VIVO URI, an predicate, and two
    vaues -- VIVO value and Source value, generate the add and subtract RDF
    necessary to execute "five case logic" in updating VIVO with an
    authoritative source value

    Version 0.1 MC 2013-12-27
    --  Initial version.
    Version 0.2 MC 2014-03-28
    --  Support for dictionary values
"""

__author__ = "Michael Conlon"
__copyright__ = "Copyright 2014, University of Florida"
__license__ = "BSD 3-Clause license"
__version__ = "0.2"

import vivotools as vt
from datetime import datetime

print datetime.now(), "Start"
cases = {
    "01.  VIVO has A, Source Has B": ["A","B"],
    "02.  VIVO has A and Source also has A": ["A","A"],
    "03.  VIVO has A, source has no value": ["A",None],
    "04.  VIVO has no value, Source has B": [None,"B"],
    "05.  VIVO has no value and Source also has no value": [None,None],
    "06.  Both have values as equal dictionaries": [{'value':'A',
        'xml:lang':'en-US', 'datatype': 'http://something'},
        {'value':'A','xml:lang':'en-US', 'datatype': 'http://something'}],
    "07.  Both have values as unequal dictionaries": [{'value':'A',
        'xml:lang':'en-US', 'datatype': 'http://something'},
        {'value':'B','xml:lang':'en-US', 'datatype': 'http://something'}],
    "08.  Both have values as unequal dictionaries": [{'value':'A',
        'xml:lang':'en-US', 'datatype': 'http://something'},
        {'value':'B'}],
    "09.  Both have values as unequal dictionaries": [{'value':'A',
        'xml:lang':'en-US', 'datatype': 'http://something'},
        {'value':'A', 'xml:lang':'en-US', 'datatype': 'http://else'}],
    "10. A a dict, B a string": [{'value':'A',
        'xml:lang':'en-US', 'datatype': 'http://something'},
        'A'],
    "11. A a dict, B a string": [{'value':'A',
        'other': 'ignore', 'whatever': 'ignore'},
        'A'],
    "12. A a dict, B a string": [{'value':'A',
        'xml:lang':'en-US', 'datatype': 'http://something'},
        'B'],
    "13. A a dict, B a string": [{'value':'A'},'A'],
    "14. A a dict, B a string": [{'value':'A'},'B'],
    "15. A a string, B a dict": ['A',{'value':'A'}],
    "16. A a string, B a dict": ['A',{'value':'B'}],
    "17. A a string, B a dict": ['A',{'value':'A',
        'xml:lang':'en-US', 'datatype': 'http://something'}],
    "18. A a string, B a dict": ['B',{'value':'A',
        'xml:lang':'en-US', 'datatype': 'http://something'}]
    }

for case in sorted(cases.keys()):
    print "\n",case,":"
    [vivo,source] = cases[case]
    [add,sub] = vt.update_data_property("http://vivo.uri","http://pred.uri",
                                        vivo,source)
    print "    Add:"
    print add
    print "    Subtract:"
    print sub
print datetime.now(),"Finish"

