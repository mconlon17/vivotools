# VIVO Tools

Simple python functions for managing data in VIVO

See the test scripts for examples of use.


## Plans for VIVO Tools

### Version 2.0

Version 2.0 will support VIVO 1.6 and VIVO-ISF. We expect to 
complete VIVO Tools 2.0 by September 2015.  

Additionally,
VIVO Tools 2.0 will have modules and a setup.py.  We tried hard
to keep everything very simple -- one file, no install procedure,
one import statement -- but best practice is to organize the
code into smaller modules and use only the modules one needs.

#### Planned modules

Each module will have the input/output functions for managing entities
in the domain

1. Grants -- grants, studies, roles, and related entities
1. People -- contact information, positions, education, overviews, service
1. Courses -- courses, course sections, academic terms, roles
1. Organizations -- departments, universities, publishers and many more
1. Publications -- including all scholarly works, authorships 
1. Foundation -- uri, rdf, assertion level processing, including input/output
to and from the VIVO triple store

#### Design Goals

1. Minimize requirements for additional libraries.  Keep it simple.
1. Consistent use of functions and identifiers
1. Improve separation of assertion level (triples, rdf, uri, ontology) and
domain level (person, grant, pub, org, course, role)
1. Increased emphasis on output functions for visualization and reporting
1. Isolation of UF specific features and dependencies

### Version 3.0

VIVO Tools will move toward an object-oriented representation of domain
entities.  We expect to collaborate with other emerging VIVO apps and tools
projects to provide useful functionality for others.
