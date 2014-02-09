"""
    test_repair_phone_number.py -- given a phone number, attempt to improve it

    Version 0.1 MC 2013-12-121
    --  Initial version.
"""

__author__      = "Michael Conlon"
__copyright__   = "Copyright 2013, University of Florida"
__license__     = "BSD 3-Clause license"
__version__     = "0.1"

import vivotools as vt
from datetime import datetime

print datetime.now(),"Start"
befores = [
    "27737",
    "352 484 2999",
    "377 9999",
    "3-48812 X 9943",
    "+1 352 388 2888",
    "888388",
    "272 2822 ext. 2999",
    "bd282"
    ]
for before in befores:
    print "Before",before.ljust(20),"After", \
        vt.repair_phone_number(before).ljust(20)
print datetime.now(),"Finish"

