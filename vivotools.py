#!/usr/bin/env/python
"""vivotools.py -- A library of useful things for working with VIVO

    1.1     2013-03-02 MC
            Added assert_data_property to generate RDF for asserting that an
            entity have a named data property value
            Added update_data property to generate addtion and subtraction RDF
            based on five case logic to update a VIVO data property value with
            a source data property value
            Added hr_abbrev_to_words to fix position and working titles
    1.2     2013-06-11 MC
            Add get_position to return a position object from a position uri
            Add position capability to get_person
            Add repair_phone_number to return IT standard phone numbers
    1.3     2013-07-23 MC
            Fixed make_datetime_rdf to provide datetime string values with
            zeroed time components for datetime precision asserted as
            yearMonthDay
    1.4     2013-08-07 MC
            Changed delimiter in read_csv to "|" was "!"
    1.41    2013-08-11 MC
            support missing grant start and end dates
    1.42    2013-08-22 MC
            added Skip=True to read.csv to skip rows without the number of
            values in the header.  skip=False will throw an exception on
            first such occurance
    1.43    2013-09-02 MC
            get_person now returns preferred_title.
            get_person now returns person['home_dept_uri'] if exists
    1.44    2013-09-04 MC
            Added version variable
    1.45    2013-09-17 MC
            Added debug parameter to vivo_sparql_query to show baseURL and query
    1.46    2013-11-29 MC
            Remove print statements from update_data_property and
            update_resource_property
            Added get_references to return references to a URI
            Added remove_uri to remove all triples citing the URI
            Added get_webpage to return a webpage object from a webpage uri
            Enhancements to get_publication to return pubmed values
            Removed function _values_from_vivo.  Use get_publication
            Renamed get_pubmed_values_from_pubmed to simply
            get_pubmed_values
    1.47    2013-12-10 MC
            Added additional ttributes to get_pubmed and get_publication
    1.48    2013-12-14 MC
            Add retry code to get_pubmed to handle Entrez non-response
    1.49    2014-01-02 MC
            Numerous upgrades to get functions to support biosketches
    1.50    2014-01-11 MC
            Replace all tets for None with is None and is not None
            VIVO URI always appear in rdf:resource assertions
"""

__author__ = "Michael Conlon"
__copyright__ = "Copyright 2014, University of Florida"
__license__ = "BSD 3-Clause license"
__version__ = "1.50"

concept_dictionary = {}

import urllib, urllib2, json, random
import string
from datetime import datetime, date
import time
from xml.dom.minidom import parseString
import sys, httplib
import tempita
import csv
from Bio import Entrez

class UnknownDateTimePrecision(Exception):
    """
    Functions that accept a DateTime Precision will throw this exception if the
    provided value is not one of the known VIVO DateTime precisions.
    """
    pass

def repair_phone_number(phone, debug=False):
    """
    Given an arbitrary string that attempts to represent a phone number,
    return a best attempt to format the phone number according to ITU standards

    If the phone number can not be repaired, the function reurns an empty string
    """
    phone_text = phone.encode('ascii', 'ignore') # encode to ascii
    phone_text = phone_text.lower()
    phone_text = phone_text.strip()
    extension_digits = None
    #
    # strip off US international country code
    #
    if phone_text.find('+1 ') == 0:
        phone_text = phone_text[3:]
    if phone_text.find('+1-') == 0:
        phone_text = phone_text[3:]
    if phone_text.find('(1)') == 0:
        phone_text = phone_text[3:]
    digits = []
    for c in list(phone_text):
        if c in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            digits.append(c)
    if len(digits) > 10:
        # pull off the extension
        i = phone_text.rfind(' ') # last blank
        if i > 0:
            extension = phone_text[i+1:]
            extension_digits = []
            for c in list(extension):
                if c in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    extension_digits.append(c)
            digits = [] # recalc the digits
            for c in list(phone_text[:i+1]):
                if c in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    digits.append(c)
        elif phone_text.rfind('x') > 0:
            i = phone_text.rfind('x')
            extension = phone_text[i+1:]
            extension_digits = []
            for c in list(extension):
                if c in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    extension_digits.append(c)
            digits = [] # recalc the digits
            for c in list(phone_text[:i+1]):
                if c in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    digits.append(c)
        else:
            extension_digits = digits[10:]
            digits = digits[:10]
    if len(digits) == 7:
        if phone[0:5] == '352392':
            updated_phone = '' # Damaged UF phone number, nothing to repair
            extension_digits = None
        elif phone[0:5] == '352273':
            updated_phone = '' # Another damaged phone number, not to repair
            extension_digits = None
        else:
            updated_phone = '(352) ' + "".join(digits[0:3])+'-'+ \
                "".join(digits[3:7])
    elif len(digits) == 10:
        updated_phone = '('+"".join(digits[0:3])+') '+"".join(digits[3:6])+ \
            '-'+"".join(digits[6:10])
    elif len(digits) == 5 and digits[0] == '2': # UF special
        updated_phone = '(352) 392' + "".join(digits[1:5])
    elif len(digits) == 5 and digits[0] == '3': # another UF special
        updated_phone = '(352) 273' + "".join(digits[1:5])
    else:
        updated_phone = '' # no repair
        extension_digits = None
    if extension_digits is not None and len(extension_digits) > 0:
        updated_phone = updated_phone + ' ext. ' + "".join(extension_digits)
    if debug:
        print phone.ljust(25), updated_phone.ljust(25)
    return updated_phone

def hr_abbrev_to_words(s):
    """
    HR uses a series of abbreviations to fit job titles into limited text
    strings.
    Here we attempt to reverse the process -- a short title is turned into a
    longer one
    """

    s = s.lower() # convert to lower
    s = s.title() # uppercase each word
    s = s + ' '   # add a trailing space so we can find these abbreviated
                  # words throughout the string
    t = s.replace(", ,", ",")
    t = t.replace("  ", " ")
    t = t.replace(" & ", " and ")
    t = t.replace(" &", " and ")
    t = t.replace("&", " and ")
    t = t.replace("/", " @")
    t = t.replace("/", " @") # might be two slashes in the input
    t = t.replace(",", " !")
    t = t.replace("-", " #")
    t = t.replace("Aca ", "Academic ")
    t = t.replace("Act ", "Acting ")
    t = t.replace("Advanc ", "Advanced ")
    t = t.replace("Adv ", "Advisory ")
    t = t.replace("Agric ", "Agricultural ")
    t = t.replace("Alumn Aff ", "Alumni Affairs ")
    t = t.replace("Ast #R ", "Research Assistant ")
    t = t.replace("Ast #G ", "Grading Assistant ")
    t = t.replace("Ast #T ", "Teaching Assistant ")
    t = t.replace("Ast ", "Assistant ")
    t = t.replace("Affl ", "Affiliate ")
    t = t.replace("Aso ", "Associate ")
    t = t.replace("Asoc ", "Associate ")
    t = t.replace("Assoc ", "Associate ")
    t = t.replace("Bio ", "Biological ")
    t = t.replace("Prof ", "Professor ")
    t = t.replace("Mstr ", "Master ")
    t = t.replace("Couns ", "Counselor ")
    t = t.replace("Adj ", "Adjunct ")
    t = t.replace("Dist ", "Distinguished ")
    t = t.replace("Chr ", "Chair ")
    t = t.replace("Cio ", "Chief Information Officer ")
    t = t.replace("Coo ", "Chief Operating Officer ")
    t = t.replace("Coord ", "Coordinator ")
    t = t.replace("Co ", "Courtesy ")
    t = t.replace("Clin ", "Clinical ")
    t = t.replace("Dn ", "Dean ")
    t = t.replace("Finan ", "Financial ")
    t = t.replace("Stu ", "Student ")
    t = t.replace("Prg ", "Program ")
    t = t.replace("Dev ", "Development ")
    t = t.replace("Aff ", "Affiliate ")
    t = t.replace("Svcs ", "Services ")
    t = t.replace("Devel ", "Development ")
    t = t.replace("Tech ", "Technician ")
    t = t.replace("Progs ", "Programs ")
    t = t.replace("Facil ", "Facility ")
    t = t.replace("Hlth ", "Health ")
    t = t.replace("Int ", "Interim ")
    t = t.replace("Sctst ", "Scientist ")
    t = t.replace("Supp ", "Support ")
    t = t.replace("Cty ", "County ")
    t = t.replace("Ext ", "Extension ")
    t = t.replace("Emer ", "Emeritus ")
    t = t.replace("Enforce ", "Enforcement ")
    t = t.replace("Environ ", "Environmental ")
    t = t.replace("Gen ", "General ")
    t = t.replace("Jnt ", "Joint ")
    t = t.replace("Eng ", "Engineer ")
    t = t.replace("Ctr ", "Center ")
    t = t.replace("Opr ", "Operator ")
    t = t.replace("Admin ", "Administrative ")
    t = t.replace("Dis ", "Distinguished ")
    t = t.replace("Ser ", "Service ")
    t = t.replace("Rep ", "Representative ")
    t = t.replace("Radiol ", "Radiology ")
    t = t.replace("Technol ", "Technologist ")
    t = t.replace("Pres ", "President ")
    t = t.replace("Pres5 ", "President 5 ")
    t = t.replace("Pres6 ", "President 6 ")
    t = t.replace("Emin ", "Eminent ")
    t = t.replace("Cfo ", "Chief Financial Officer ")
    t = t.replace("Prov ", "Provisional ")
    t = t.replace("Adm ", "Administrator ")
    t = t.replace("Info ", "Information ")
    t = t.replace("It ", "Information Technology ")
    t = t.replace("Mgr ", "Manager ")
    t = t.replace("Mgt ", "Management ")
    t = t.replace("Vis ", "Visiting ")
    t = t.replace("Phas ", "Phased ")
    t = t.replace("Prog ", "Programmer ")
    t = t.replace("Pract ", "Practitioner ")
    t = t.replace("Registr ", "Registration ")
    t = t.replace("Rsch ", "Research ")
    t = t.replace("Rsrh ", "Research ")
    t = t.replace("Ret ", "Retirement ")
    t = t.replace("Sch ", "School ")
    t = t.replace("Sci ", "Scientist ")
    t = t.replace("Svcs ", "Services ")
    t = t.replace("Serv ", "Service ")
    t = t.replace("Tch ", "Teaching ")
    t = t.replace("Tele ", "Telecommunications ")
    t = t.replace("Tv ", "TV ")
    t = t.replace("Univ ", "University ")
    t = t.replace("Educ ", "Education ")
    t = t.replace("Crd ", "Coordinator ")
    t = t.replace("Res ", "Research ")
    t = t.replace("Dir ", "Director ")
    t = t.replace("Pky ", "PK Yonge ")
    t = t.replace("Rcv ", "Receiving ")
    t = t.replace("Sr ", "Senior ")
    t = t.replace("Spec ", "Specialist ")
    t = t.replace("Spc ", "Specialist ")
    t = t.replace("Spv ", "Supervisor ")
    t = t.replace("Supv ", "Supervisor ")
    t = t.replace("Supt ", "Superintendant ")
    t = t.replace("Pky ", "P. K. Yonge ")
    t = t.replace("Ii ", "II ")
    t = t.replace("Iii ", "III ")
    t = t.replace("Iv ", "IV ")
    t = t.replace("Communic ", "Communications ")
    t = t.replace("Postdoc ", "Postdoctoral ")
    t = t.replace("Tech ", "Technician ")
    t = t.replace("Vp ", "Vice President ")
    t = t.replace(" @", "/") # restore /
    t = t.replace(" @", "/")
    t = t.replace(" !", ",") # restore ,
    t = t.replace(" #", "-") # restore -
    return t[:-1] # Take off the trailing space

def assert_data_property(uri, data_property, value):
    from xml.sax.saxutils import escape
    """
    Given a uri and a data_property name, and a value, generate rdf to assert
    the uri has the value of the data property

    Note:
    This function does not check that the data property name is valid
    """
    data_property_template = tempita.Template(
    """
    <rdf:Description rdf:about="{{uri}}">
        <{{data_property}}>{{value}}</{{data_property}}>
    </rdf:Description>
    """)

    # That's one nasty kludge.  Need a smart escape

    if value.find('&amp;') < 0:
        val = escape(value)
    else:
        val = value

    rdf = data_property_template.substitute(uri=uri, \
        data_property=data_property, value=val)
    return rdf

def assert_resource_property(uri, resource_property, resource_uri):
    """
    Given a uri and a resource_property name, and a uri of the resource,
    generate rdf to assert
    assert the uri has the resource_uri for the named resource_property

    Note:
    This function does not check that the resource property name is valid
    This is often called in invertable pairs -- each uri has the other as
    a resource. Example: homeDept and homeDeptFor
    """
    resource_property_template = tempita.Template(
    """
    <rdf:Description rdf:about="{{uri}}">
        <{{resource_property}} rdf:resource="{{resource_uri}}"/>
    </rdf:Description>
    """)
    rdf = resource_property_template.substitute(uri=uri, \
        resource_property=resource_property, resource_uri=resource_uri)
    return rdf

def update_data_property(uri, data_property, vivo_value, source_value):
    """
    Given the URI of an entity, the name of a data_proprty, the current
    vivo value for the data_property and the source (correct) value for
    the property, use five case logic to generate appropriate subtraction
    and addtion rdf to update the data_property

    Note:   we could have shortened the if statements, but they might not have
            been as clear
    """
    srdf = ""
    ardf = ""
    if vivo_value is None and source_value is None:
        pass
    elif vivo_value is None and source_value is not None:
        ardf = assert_data_property(uri, data_property, source_value)
    elif vivo_value is not None and source_value is None:
        srdf = assert_data_property(uri, data_property, vivo_value)
    elif vivo_value is not None and source_value is not None and \
        vivo_value == source_value:
        pass
    elif vivo_value is not None and source_value is not None and \
        vivo_value != source_value:
        srdf = assert_data_property(uri, data_property, vivo_value)
        ardf = assert_data_property(uri, data_property, source_value)
    return [ardf, srdf]

def update_resource_property(uri, resource_property, vivo_value, source_value):
    """
    Given the URI of an entity, the name of a resource_proprty, the current
    vivo value for the resource_property and the source (correct) value for
    the property, use five case logic to generate appropriate subtraction
    and addtion rdf to update the resource_property

    Note:   we could have shortened the if statements, but they might not have
            been as clear
    """
    srdf = ""
    ardf = ""
    if vivo_value is None and source_value is None:
        pass
    elif vivo_value is None and source_value is not None:
        ardf = assert_resource_property(uri, resource_property, source_value)
    elif vivo_value is not None and source_value is None:
        srdf = assert_resource_property(uri, resource_property, vivo_value)
    elif vivo_value is not None and source_value is not None and \
        vivo_value == source_value:
        pass
    elif vivo_value is not None and source_value is not None and \
        vivo_value != source_value:
        srdf = assert_resource_property(uri, resource_property, vivo_value)
        ardf = assert_resource_property(uri, resource_property, source_value)
    return [ardf, srdf]

def remove_uri(uri):
    """
    Given a URI, generate subtraction URI to remove all triples containing
    the URI as either a subject or object
    """
    srdf = ""

    # Remove triples

    triples = get_triples(uri)["results"]["bindings"]
    for triple in triples:
        p = triple["p"]["value"]
        o = triple["o"]["value"]
        if o[:7] == "http://" and p[-3:] != "URI" and p[-4:] != "Text":
            [add, sub] = update_resource_property(uri, p, o, None)
        else:
            [add, sub] = update_data_property(uri, p, o, None)
        srdf = srdf + sub

    # Remove references

    triples = get_references(uri)["results"]["bindings"]
    for triple in triples:
        s = triple["s"]["value"]
        p = triple["p"]["value"]
        [add, sub] = update_resource_property(s, p, uri, None)
        srdf = srdf + sub
    return srdf


def make_datetime_interval_rdf(start_date, end_date):
    """
    Given a start_date and/or end_date in isoformat, create the RDF for
    a datetime interval
    """
    [start_date_rdf, start_date_uri] = make_datetime_rdf(start_date)
    [end_date_rdf, end_date_uri] = make_datetime_rdf(end_date)
    [datetime_interval_rdf, datetime_interval_uri] = \
        make_dt_interval_rdf(start_date_uri, end_date_uri)
    rdf = start_date_rdf + end_date_rdf + datetime_interval_rdf
    return [rdf, datetime_interval_uri]

def make_datetime_rdf(datetime, precision="yearMonthDay"):
    """
    Given a datetime string in isoformat, create the RDF for a datetime object
    """
    datetime_template = tempita.Template(
    """
    <rdf:Description rdf:about="{{datetime_uri}}">
        <rdf:type rdf:resource="http://vivoweb.org/ontology/core#DateTimeValue"/>
        <core:dateTimePrecision rdf:resource="http://vivoweb.org/ontology/core#{{precision}}Precision"/>
        <core:dateTime>{{datetime}}</core:dateTime>
    </rdf:Description>
    """)
    if datetime == "" or datetime is None:
        datetime_uri = None
        rdf = ""
    else:
        if precision == "year" or precision == "yearMonth" or \
            precision == "yearMonthDay":
            datetime = datetime[0:datetime.index('T')]+"T00:00:00"
            datetime_uri = get_vivo_uri()
            rdf = datetime_template.substitute(datetime_uri=datetime_uri,
                                               datetime=datetime,
                                               precision=precision)
        elif precision == "yearMonthDayTime":
            print datetime
            datetime_uri = get_vivo_uri()
            rdf = datetime_template.substitute(datetime_uri=datetime_uri,
                                               datetime=datetime,
                                               precision=precision)
        else:
            print precision
            raise UnknownDateTimePrecision(precision)
    return [rdf, datetime_uri]

def make_dt_interval_rdf(start_uri, end_uri):
    """
    Given a start and end uri, return the rdf for a datetime interval with the
    given start and end uris. Either may be empty.
    """
    dt_interval_template = tempita.Template("""
    <rdf:Description rdf:about="{{interval_uri}}">
        <rdf:type rdf:resource="http://vivoweb.org/ontology/core#DateTimeInterval"/>
        {{if start_uri != "" and start_uri is not None}}
            <core:start rdf:resource="{{start_uri}}"/>
        {{endif}}
        {{if end_uri != "" and end_uri is not None}}
            <core:end rdf:resource="{{end_uri}}"/>
        {{endif}}
    </rdf:Description>
    """)
    if (start_uri == "" or start_uri is None) and \
        (end_uri == "" or end_uri is None):
        rdf = ""
        interval_uri = None
    else:
        interval_uri = get_vivo_uri()
        rdf = dt_interval_template.substitute(interval_uri=interval_uri,
                                              start_uri=start_uri,
                                              end_uri=end_uri)
    return [rdf, interval_uri]

def read_csv(filename, skip=True):
    """
    Given a filename, read the CSV file with that name.  We use "|" as a
    separator in CSV files to allow commas to appear in values.

    CSV files read by this function follow these conventions:
    --  use "|" as a seperator
    --  have a first row that contains column headings.  Columns headings
        must be known to VIVO, typically in the form prefix:name
    --  all elements must have values.  To specify a missing value, use
        the string "None" or "NULL" between separators, that is |None| or |NULL|
    --  leading and trailing whitespace in values is ignored.  | The  | will be
        read as "The"
    -- if skip=True, rows with too many or too few data elements are skipped.
       if Skip=False, a RowError is thrown

    CSV files processed by read_CSV will be returned as a dictionary of
    dictionaries, one dictionary per row with a name of and an
    integer value for the row number of data.

    To Do:
    --  "know" some of the VIVO data elements, checking and converting as
        appropriate.  In particular, handle dates and convert to datetime
    """

    class RowError(Exception):
        pass
    heading = []
    row_number = 0
    data = {}
    csvReader = csv.reader(open(filename, 'rb'), delimiter="|")
    for row in csvReader:
        i = 0
        for r in row:
            # remove white space fore and aft
            row[i] = r.strip(string.whitespace+'\xef\xbb\xbf')
            if row[i] == 'NULL' or row[i] == 'None':
                row[i] = ''
            i = i + 1
        if heading == []:
            heading = row # the first row is the heading
            number_of_columns = len(heading)
            continue
        row_number = row_number + 1
        if len(row) == number_of_columns:
            data[row_number] = {}
            i = 0
            for r in row:
                data[row_number][heading[i]] = r
                i = i + 1
        elif skip == False:
            raise RowError("On row "+str(row_number)+", expecting "+
                           str(number_of_columns)+ " data values. Found "+
                           str(len(row))+" data values. Row contents = "+
                           str(row))
        else:
            pass #  row has wrong number of columns and skip is True
    return data

def get_pmid_from_doi(doi, email='mconlon@ufl.edu', tool='PythonQuery',
                      database='pubmed'):
    """
    Given a DOI, return the PMID of ther corresponding PubMed Article.  If not
    found in PubMed, return None. Adapted from
    http://simon.net.nz/articles/query-pubmed-for-citation-information-
        using-a-doi-and-python/
    """
    params = {'db':database, 'tool':tool, 'email':email, 'term': doi,
        'usehistory':'y', 'retmax':1}
    url = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?' + \
        urllib.urlencode(params)

    # Get data from Entrez.  Retry if Entrez does not respond

    start = 2.0
    retries = 10
    count = 0
    while True:
        try:
            data = urllib.urlopen(url).read()
            xmldoc = parseString(data)
            ids = xmldoc.getElementsByTagName('Id')
            if len(ids) == 0:
                pmid = None
            else:
                pmid = ids[0].childNodes[0].data
            return pmid
        except:
            count = count + 1
            if count > retries:
                return None
            sleep_seconds = start**count
            print "<!-- Failed Entrez PMID query. Count = "+str(count)+ \
                " Will sleep now for "+str(sleep_seconds)+ \
                " seconds and retry -->"
            time.sleep(sleep_seconds) # increase the wait time with each retry


def get_pubmed_values(doi, debug=False):
    """
    Given the doi of a paper, return the current values (if any) for PMID,
    PMCID, Grants Cited, abstract, keywords, nihmsid, and Full_text_uri of
    the paper in PubMed Central.

    Return items in a dictionary.  Grants_cited and keywod_list are
    lists of strings.
    """
    Entrez.email = 'mconlon@ufl.edu'
    values = {}
    grants_cited = []
    keyword_list = []
    pmid = get_pmid_from_doi(doi)
    if pmid is None:
        return {}
    else:
        values['pmid'] = pmid

    # Get record(s) from Entrez.  Retry if Entrez does not respond

    start = 2.0
    retries = 10
    count = 0
    while True:
        try:
            handle = Entrez.efetch(db="pubmed", id=pmid, retmode="xml")
            records = Entrez.parse(handle)
            break
        except:
            count = count + 1
            if count > retries:
                return {}
            sleep_seconds = start**count
            print "<!-- Failed Entrez query. Count = "+str(count)+ \
                " Will sleep now for "+str(sleep_seconds)+ \
                " seconds and retry -->"
            time.sleep(sleep_seconds) # increase the wait time with each retry

    # Find the desired attributes in the record structures returned by Entrez

    for record in records:
        if debug:
            print "Entrez record:", record
        article_id_list = record['PubmedData']['ArticleIdList']
        for article_id in article_id_list:
            attributes = article_id.attributes
            if 'IdType' in attributes:
                if attributes['IdType'] == 'pmc':
                    values["pmcid"] = str(article_id)
                if attributes['IdType'] == 'mid':
                    values["nihmsid"] = str(article_id)
        try:
            values['abstract'] = \
                record['MedlineCitation']['Article']['Abstract']\
                ['AbstractText'][0]
        except:
            pass
        try:
            keywords = record['MedlineCitation']['MeshHeadingList']
            for keyword in keywords:
                keyword_list.append(str(keyword['DescriptorName']))
            values["keyword_list"] = keyword_list
        except:
            pass
        try:
            grants = record['MedlineCitation']['Article']['GrantList']
            for grant in grants:
                grants_cited.append(grant['GrantID'])
            values["grants_cited"] = grants_cited
        except:
            pass

    # If we found a pmcid, construct the full text uri by formula

    if 'pmcid' in values:
        values["full_text_uri"] = \
            "http://www.ncbi.nlm.nih.gov/pmc/articles/" + \
            values["pmcid"].upper()+ "/pdf"
    return values

def rdf_header():
    """
    Return a text string containing the standard VIVO RDF prefixes suitable as
    the beginning of an RDF statement to add or remove RDF to VIVO.

    Note:  This function should be updated for each new release of VIVO and to
        include local ontologies and extensions.
    """
    rdf_header = """<rdf:RDF
    xmlns:rdf     = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:rdfs    = "http://www.w3.org/2000/01/rdf-schema#"
    xmlns:xsd     = "http://www.w3.org/2001/XMLSchema#"
    xmlns:owl     = "http://www.w3.org/2002/07/owl#"
    xmlns:swrl    = "http://www.w3.org/2003/11/swrl#"
    xmlns:swrlb   = "http://www.w3.org/2003/11/swrlb#"
    xmlns:vitro1  = "http://vitro.mannlib.cornell.edu/ns/vitro/0.7#"
    xmlns:bibo    = "http://purl.org/ontology/bibo/"
    xmlns:c4o     = "http://purl.org/spar/c4o/"
    xmlns:dcelem  = "http://purl.org/dc/elements/1.1/"
    xmlns:dcterms = "http://purl.org/dc/terms/"
    xmlns:event   = "http://purl.org/NET/c4dm/event.owl#"
    xmlns:foaf    = "http://xmlns.com/foaf/0.1/"
    xmlns:fabio   = "http://purl.org/spar/fabio/"
    xmlns:geo     = "http://aims.fao.org/aos/geopolitical.owl#"
    xmlns:pvs     = "http://vivoweb.org/ontology/provenance-support#"
    xmlns:ero     = "http://purl.obolibrary.org/obo/"
    xmlns:scires  = "http://vivoweb.org/ontology/scientific-research#"
    xmlns:skos    = "http://www.w3.org/2004/02/skos/core#"
    xmlns:ufVivo  = "http://vivo.ufl.edu/ontology/vivo-ufl/"
    xmlns:vitro2  = "http://vitro.mannlib.cornell.edu/ns/vitro/public#"
    xmlns:core    = "http://vivoweb.org/ontology/core#"
    xmlns:vivo    = "http://vivoweb.org/ontology/core#">"""
    return rdf_header

def rdf_footer():
    """
    Return a text string suitable for edning an RDF statement to add or
    remoe RDF/XML to VIVO
    """
    rdf_footer = """</rdf:RDF>"""
    return rdf_footer

def make_rdf_uri(uri):
    """
    Given a uri of a VIVO profile, generate the URI of the corresponding
    RDF page
    """
    k = uri.rfind("/")
    word = uri[k+1:]
    rdf_uri = uri + "/" + word + ".rdf"
    return rdf_uri

def key_string(s):
    """
    Given a string s, return a string with a bunch of punctuation and special
    characters removed and then everything lower cased.  Useful for matching
    strings in which case, punctuation and special characters should not be
    considered in the match
    """
    k = s.encode("utf-8", "ignore").translate(None,
        """ \t\n\r\f!@#$%^&*()_+:"<>?-=[]\\;',./""")
    k = k.lower()
    return k

def get_triples(uri):
    """
    Given a VIVO URI, return all the triples referencing that URI as subject
    """
    query = tempita.Template("""
    SELECT ?p ?o WHERE
    {
    <{{uri}}> ?p ?o .
    }""")
    query = query.substitute(uri=uri)
    result = vivo_sparql_query(query)
    return result

def get_references(uri):
    """
    Given a VIVO uri, return all the triples that have the given uri as an
    object
    """
    query = tempita.Template("""
    SELECT ?s ?p WHERE
    {
    ?s ?p <{{uri}}> .
    }""")
    query = query.substitute(uri=uri)
    result = vivo_sparql_query(query)
    return result

def get_vivo_value(uri, predicate):
    """
    Given a VIVO URI, and a predicate, get a value for the rpedicate.  Assumes
    the result is single valued.

    Notes:
    --  if the there are mulitple values that meet the criteria, the first one
        is returned
    --  if no values meet the criteria, None is returned
    --  this function is very inefficient, making a SPARQL query for every
        value. Use only when strictly needed!
    """
    query = tempita.Template("""
    SELECT ?o WHERE
    {
    <{{uri}}> {{predicate}} ?o .
    }
    """)
    query = query.substitute(uri=uri, predicate=predicate)
    result = vivo_sparql_query(query)
    try:
        b = result["results"]["bindings"][0]
        o = b['o']['value']
        return o
    except:
        return None


def show_triples(triples):
    """
    Given an object returned by get_triples, print the object
    """
    try:
        count = len(triples["results"]["bindings"])
    except:
        count = 0
    #
    i = 0
    while i < count:
        b = triples["results"]["bindings"][i]
        p = b['p']['value']
        o = b['o']['value']
        print "{0:65}".format(p), o
        i = i + 1
    return

def get_organization(organization_uri):
    """
    Given the URI of an organnization, return an object that contains the
    organization it represents.

    As for most of the access functions, additional attributes can be added.
    """
    organization = {'organization_uri':organization_uri}
    organization['uri'] = organization_uri
    organization['sub_organization_within_uris'] = []
    organization['has_sub_organization_uris'] = []
    triples = get_triples(organization_uri)
    try:
        count = len(triples["results"]["bindings"])
    except:
        count = 0
    i = 0
    while i < count:
        b = triples["results"]["bindings"][i]
        p = b['p']['value']
        o = b['o']['value']
        if p == "http://www.w3.org/2000/01/rdf-schema#label":
            organization['label'] = o
        if p == "http://vivoweb.org/ontology/core#subOrganizationWithin":
            organization['sub_organization_within_uris'].append(o)
        if p == "http://vivoweb.org/ontology/core#hasSubOrganization":
            organization['has_sub_organization_uris'].append(o)
        if p == "http://vivoweb.org/ontology/core#overview":
            organization['overview'] = o
        i = i + 1
    return organization

def get_person(person_uri, get_publications=False, get_grants=False,
               get_positions=False, get_degrees=False):
    """
    Given a person URI, return an object that ccontains the person it
    represents.

    Optionally dereference publications, grants, positions, courses.  Each may
    add significant run time
    """
    person = {'person_uri':person_uri}
    person['authorship_uris'] = []
    person['pi_role_uris'] = []
    person['coi_role_uris'] = []
    person['inv_role_uris'] = []
    person['teaching_role_uris'] = []
    person['position_uris'] = []
    person['degree_uris'] = []
    person['publications'] = []
    person['grants'] = []
    person['positions'] = []
    person['degrees'] = []
    triples = get_triples(person_uri)
    try:
        count = len(triples["results"]["bindings"])
    except:
        count = 0
    i = 0
    while i < count:
        b = triples["results"]["bindings"][i]
        p = b['p']['value']
        o = b['o']['value']
        if p == "http://vivoweb.org/ontology/core#primaryPhoneNumber":
            person['primary_phone_number'] = o
        if p == "http://vivoweb.org/ontology/core#primaryEmail":
            person['primary_email'] = o
        if p == "http://vivoweb.org/ontology/core#faxNumber":
            person['fax_number'] = o
        if p == "http://vivo.ufl.edu/ontology/vivo-ufl/ufid":
            person['ufid'] = o
        if p == "http://vivo.ufl.edu/ontology/vivo-ufl/gatorlink":
            person['gatorlink'] = o
        if p == "http://vivoweb.org/ontology/core#eRACommonsId":
            person['era_commons'] = o
        if p == "http://vivoweb.org/ontology/core#overview":
            person['overview'] = o
        if p == "http://xmlns.com/foaf/0.1/firstName":
            person['first_name'] = o
        if p == "http://xmlns.com/foaf/0.1/lastName":
            person['last_name'] = o
        if p == "http://vivoweb.org/ontology/core#middleName":
            person['middle_name'] = o
        if p == "http://purl.org/ontology/bibo#prefixName":
            person['name_prefix'] = o
        if p == "http://purl.org/ontology/bibo#suffixName":
            person['name_suffix'] = o
        if p == "http://www.w3.org/2000/01/rdf-schema#label":
            person['display_name'] = o
        if p == "http://vivoweb.org/ontology/core#preferredTitle":
            person['preferred_title'] = o
        if p == "http://vivoweb.org/ontology/core#faxNumber":
            person['fax_number'] = o
        if p == "http://vivoweb.org/ontology/core#educationalTraining":
            person['degree_uris'].append(o)
        if p == "http://vivoweb.org/ontology/core#authorInAuthorship":
            person['authorship_uris'].append(o)
        if p == "http://vivoweb.org/ontology/core#hasPrincipalInvestigatorRole":
            person['pi_role_uris'].append(o)
        if p == \
            "http://vivoweb.org/ontology/core#hasCo-PrincipalInvestigatorRole":
            person['coi_role_uris'].append(o)
        if p == "http://vivoweb.org/ontology/core#hasInvestigatorRole":
            person['inv_role_uris'].append(o)
        if p == "http://vivoweb.org/ontology/core#hasTeacherRole":
            person['teaching_role_uris'].append(o)
        if p == "http://vivoweb.org/ontology/core#personInPosition":
            person['position_uris'].append(o)

        # deref the home department

        if p == "http://vivo.ufl.edu/ontology/vivo-ufl/homeDept":
            person['home_dept_uri'] = o
            home_department = get_organization(o)
            if 'label' in home_department: # home department might be incomplete
                person['home_department_name'] = home_department['label']
        i = i + 1

    # deref the authorships

    if get_publications:
        for authorship_uri in person['authorship_uris']:
            authorship = get_authorship(authorship_uri)
            if 'publication_uri' in authorship: # authorship might be incomplete
                publication = get_publication(authorship['publication_uri'])
                person['publications'].append(publication)

    # deref the investigator roles

    if get_grants:
        for role_uri in person['pi_role_uris']:
            role = get_role(role_uri)
            if 'grant_uri' in role:  # some roles are broken
                grant = get_grant(role['grant_uri'])
                grant['role'] = 'pi'
                person['grants'].append(grant)
        for role_uri in person['coi_role_uris']:
            role = get_role(role_uri)
            if 'grant_uri' in role:  # some roles are broken
                grant = get_grant(role['grant_uri'])
                grant['role'] = 'coi'
                person['grants'].append(grant)
        for role_uri in person['inv_role_uris']:
            role = get_role(role_uri)
            if 'grant_uri' in role:  # some roles are broken
                grant = get_grant(role['grant_uri'])
                grant['role'] = 'inv'
                person['grants'].append(grant)

    # deref the positions

    if get_positions:
        for position_uri in person['position_uris']:
            position = get_position(position_uri)
            person['positions'].append(position)

    # deref the degrees

    if get_degrees:
        for degree_uri in person['degree_uris']:
            degree = get_degree(degree_uri)
            person['degrees'].append(degree)

    # deref the teaching roles
    return person

def get_degree(degree_uri):
    """
    Given a URI, return an object that contains the degree (educational
    training) it represents

    """
    degree = {'degree_uri':degree_uri}
    triples = get_triples(degree_uri)
    try:
        count = len(triples["results"]["bindings"])
    except:
        count = 0
    i = 0
    while i < count:
        b = triples["results"]["bindings"][i]
        p = b['p']['value']
        o = b['o']['value']
        if p == "http://vivoweb.org/ontology/core#majorField":
            degree['major_field'] = o

        # deref the academic degree

        if p == "http://vivoweb.org/ontology/core#degreeEarned":
            degree['earned_uri'] = o
            degree['degree_name'] = get_vivo_value(o, 'core:abbreviation')

        # deref the Institution

        if p == "http://vivoweb.org/ontology/core#trainingAtOrganization":
            degree['training_institution_uri'] = o
            institution = get_organization(o)
            if 'label' in institution: # home department might be incomplete
                degree['institution_name'] = institution['label']

        # deref the datetime interval

        if p == "http://vivoweb.org/ontology/core#dateTimeInterval":
            datetime_interval = get_datetime_interval(o)
            degree['datetime_interval'] = datetime_interval
            if 'start_date' in datetime_interval:
                degree['start_date'] = datetime_interval['start_date']
            if 'end_date' in datetime_interval:
                degree['end_date'] = datetime_interval['end_date']
        i = i + 1
    return degree

def get_role(role_uri):
    """
    Given a URI, return an object that contains the role it represents

    To Do:
    Generalize to more types of roles
    """
    role = {'role_uri':role_uri}
    triples = get_triples(role_uri)
    try:
        count = len(triples["results"]["bindings"])
    except:
        count = 0
    i = 0
    while i < count:
        b = triples["results"]["bindings"][i]
        p = b['p']['value']
        o = b['o']['value']
        if p == "http://vivoweb.org/ontology/core#roleIn":
            role['grant_uri'] = o
        if p == "http://vivoweb.org/ontology/core#roleContributesTo":
            role['grant_uri'] = o
        if p == 'http://vivoweb.org/ontology/core#' \
            'co-PrincipalInvestigatorRoleOf':
            role['co_principal_investigator_role_of'] = o
        if p == 'http://vivoweb.org/ontology/core#' \
            'principalInvestigatorRoleOf':
            role['principal_investigator_role_of'] = o
        if p == 'http://vivoweb.org/ontology/core#' \
            'investigatorRoleOf':
            role['investigator_role_of'] = o
        i = i + 1
    return role


def get_authorship(authorship_uri):
    """
    Given a URI, return an object that contains the authorship it represents
    """
    authorship = {'authorship_uri':authorship_uri}
    triples = get_triples(authorship_uri)
    try:
        count = len(triples["results"]["bindings"])
    except:
        count = 0
    i = 0
    while i < count:
        b = triples["results"]["bindings"][i]
        p = b['p']['value']
        o = b['o']['value']
        if p == "http://vivoweb.org/ontology/core#authorRank":
            authorship['author_rank'] = o
        if p == "http://vivoweb.org/ontology/core#linkedAuthor":
            authorship['author_uri'] = o
        if p == "http://vivoweb.org/ontology/core#linkedInformationResource":
            authorship['publication_uri'] = o
        if p == "http://vivoweb.org/ontology/core#isCorrespondingAuthor":
            authorship['corresponding_author'] = o
        i = i + 1
    return authorship

def get_webpage(webpage_uri):
    """
    Given a URI, return an object that contains the webpage it represents
    """
    webpage = {'webpage_uri':webpage_uri}
    triples = get_triples(webpage_uri)
    try:
        count = len(triples["results"]["bindings"])
    except:
        count = 0
    i = 0
    while i < count:
        b = triples["results"]["bindings"][i]
        p = b['p']['value']
        o = b['o']['value']
        if p == "http://vivoweb.org/ontology/core#webpageOf":
            webpage['webpage_of'] = o
        if p == "http://vivoweb.org/ontology/core#rank":
            webpage['rank'] = o
        if p == "http://vivoweb.org/ontology/core#linkURI":
            webpage['link_uri'] = o
        if p == "http://vivoweb.org/ontology/core#rank":
            webpage['rank'] = o
        if p == "http://vivoweb.org/ontology/core#linkAnchorText":
            webpage['link_anchor_text'] = o
        if o == "http://vivoweb.org/ontology/ufVivo#FullTextURI":
            webpage['link_type'] = "full_text"
        i = i + 1
    return webpage

def get_position(position_uri):
    """
    Given a URI, return an object that contains the position it represents
    """
    position = {'position_uri':position_uri} # include position_uri
    triples = get_triples(position_uri)
    try:
        count = len(triples["results"]["bindings"])
    except:
        count = 0
    i = 0
    while i < count:
        b = triples["results"]["bindings"][i]
        p = b['p']['value']
        o = b['o']['value']
        if p == "http://vivoweb.org/ontology/core#positionForPerson":
            position['person_uri'] = o
        if p == "http://vivoweb.org/ontology/core#hrJobTitle":
            position['hr_title'] = o
        if p == "http://www.w3.org/2000/01/rdf-schema#label":
            position['position_label'] = o
        if o == "http://vivoweb.org/ontology/core#FacultyPosition":
            position['position_type'] = 'faculty'
        if o == "http://vivoweb.org/ontology/core#Non-FacultyAcademicPosition":
            position['position_type'] = 'non-faculty'
        if o == "http://vivoweb.org/ontology/ufVivo#ClinicalFacultyPosition":
            position['position_type'] = 'clinical-faculty'
        if o == "http://vivoweb.org/ontology/ufVivo#PostDocPosition":
            position['position_type'] = 'post-doc'
        if o == "http://vivoweb.org/ontology/core#LibrarianPosition":
            position['position_type'] = 'librarian'
        if o == "http://vivoweb.org/ontology/core#Non-AcademicPosition":
            position['position_type'] = 'non-academic'
        if o == "http://vivoweb.org/ontology/ufVivo#StudentAssistant":
            position['position_type'] = 'student-assistant'
        if o == "http://vivoweb.org/ontology/ufVivo#GraduateAssistant":
            position['position_type'] = 'graduate-assistant'
        if o == "http://vivoweb.org/ontology/ufVivo#Housestaff":
            position['position_type'] = 'housestaff'
        if o == "http://vivoweb.org/ontology/ufVivo#TemporaryFaculty":
            position['position_type'] = 'temp-faculty'
        if o == "http://vivoweb.org/ontology/ufVivo#Housestaff":
            position['position_type'] = 'housestaff'
        if o == \
            "http://vivoweb.org/ontology/core#FacultyAdministrativePosition":
            position['position_type'] = 'faculty-administrative'

        # deref the Organization

        if p == "http://vivoweb.org/ontology/core#positionInOrganization":
            position['org_uri'] = o
            org = get_organization(o)
            if 'label' in org: # org might be incomplete
                position['org_name'] = org['label']

        # deref datetime interval

        if p == "http://vivoweb.org/ontology/core#dateTimeInterval":
            datetime_interval = get_datetime_interval(o)
            position['datetime_interval'] = datetime_interval
            if 'start_date' in datetime_interval:
                position['start_date'] = datetime_interval['start_date']
            if 'end_date' in datetime_interval:
                position['end_date'] = datetime_interval['end_date']
        i = i + 1
    return position

def get_publication(publication_uri):
    """
    Given a URI, return an object that contains the publication it represents.
    We have to dereference the publication venue to get the journal name, and
    the datetime value to get the date of publication.  We don't rebuild the
    author list (too dang much work, perhaps the author list should just be
    maintained as a property of the publication)

    The resulting object can be displayed using string_from_document
    """
    publication = {'publication_uri':publication_uri} #include the uri
    triples = get_triples(publication_uri)
    publication['grants_cited'] = []
    publication['keyword_list'] = []
    try:
        count = len(triples["results"]["bindings"])
    except:
        count = 0
    i = 0
    while i < count:
        b = triples["results"]["bindings"][i]
        p = b['p']['value']
        o = b['o']['value']

        if p == "http://purl.org/ontology/bibo/doi":
            publication['doi'] = o
        if p == "http://purl.org/ontology/bibo/pmid":
            publication['pmid'] = o
        if p == "http://purl.org/ontology/bibo/abstract":
            publication['abstract'] = o
        if p == "http://vivoweb.org/ontology/core#pmcid":
            publication['pmcid'] = o
        if p == "http://vivoweb.org/ontology/core#nihmsid":
            publication['nihmsid'] = o
        if o == "http://purl.org/ontology/bibo/AcademicArticle":
            publication['publication_type'] = 'academic-article'
        if o == "http://purl.org/ontology/bibo/Book":
            publication['publication_type'] = 'book'
        if o == "http://purl.org/ontology/bibo/Chapter":
            publication['publication_type'] = 'chapter'
        if o == "http://vivoweb.org/ontology/core#ConferencePaper":
            publication['publication_type'] = 'conference-paper'
        if o == "http://vivoweb.org/ontology/core#ConferencePoster":
            publication['publication_type'] = 'conference-poster'
        if p == "http://vivoweb.org/ontology/core#freeTextKeyword":
            publication['keyword_list'].append(o)
        if p == "http://vivoweb.org/ontology/ufVivo#grantCited":
            person['grants_cited'].append(o)
        if p == "http://vivoweb.org/ontology/core#webPage":
            person['web_page'] = o
        if p == "http://purl.org/ontology/bibo/pageStart":
            publication['page_start'] = o
        if p == "http://purl.org/ontology/bibo/pageEnd":
            publication['page_end'] = o
        if p == "http://www.w3.org/2000/01/rdf-schema#label":
            publication['title'] = o
        if p == "http://purl.org/ontology/bibo/volume":
            publication['volume'] = o
        if p == "http://purl.org/ontology/bibo/number":
            publication['number'] = o

        # deref the web page (does not handle multiple web pages)

        if p == "http://vivoweb.org/ontology/core#webPage":
            publication['web_page'] = get_webpage(o)
            if 'link_type' in web_page and web_page['link_type'] == \
               'full_text_uri':
                publication['full_text_uri'] = web_page['link_uri']

        # deref the publication_venue

        if p == "http://vivoweb.org/ontology/core#hasPublicationVenue":
            publication_venue = get_publication_venue(o)
            try:
                publication['journal'] = publication_venue['label']
            except:
                pass

        # deref the datetime

        if p == "http://vivoweb.org/ontology/core#dateTimeValue":
            datetime_value = get_datetime_value(o)
            try:
                publication['date'] = datetime_value['date']
            except:
                pass
        i = i + 1
    return publication

def get_datetime_value(datetime_value_uri):
    """
    Given a URI, return an object that contains the datetime value it
    represents
    """
    datetime_value = {'datetime_value_uri':datetime_value_uri}
    triples = get_triples(datetime_value_uri)
    try:
        count = len(triples["results"]["bindings"])
    except:
        count = 0
    i = 0
    while i < count:
        b = triples["results"]["bindings"][i]
        p = b['p']['value']
        o = b['o']['value']
        if p == "http://vivoweb.org/ontology/core#dateTime":
            datetime_value['datetime'] = o
            year = o[0:4]
            month = o[5:7]
            day = o[8:10]
        if p == "http://vivoweb.org/ontology/core#dateTimePrecision":
            datetime_value['datetime_precision'] = o
            if datetime_value['datetime_precision'] == \
                "http://vivoweb.org/ontology/core#yearPrecision":
                datetime_value['datetime_precision'] = 'year'
            if datetime_value['datetime_precision'] == \
                "http://vivoweb.org/ontology/core#yearMonthPrecision":
                datetime_value['datetime_precision'] = 'year_month'
            if datetime_value['datetime_precision'] == \
                "http://vivoweb.org/ontology/core#yearMonthDayPrecision":
                datetime_value['datetime_precision'] = 'year_month_day'
        if 'datetime' in datetime_value and 'datetime_precision' in \
            datetime_value:
            if datetime_value['datetime_precision'] == "year":
                datetime_value['date'] = {'year':year}
            if datetime_value['datetime_precision'] == "year_month":
                datetime_value['date'] = {'year':year, 'month':month}
            if datetime_value['datetime_precision'] == "year_month_day":
                datetime_value['date'] = {'year':year, 'month':month, 'day':day}
        i = i + 1
    return datetime_value

def get_datetime_interval(datetime_interval_uri):
    """
    Given a URI, return an object that contains the datetime_interval it
    represents
    """
    datetime_interval = {'datetime_interval_uri':datetime_interval_uri}
    triples = get_triples(datetime_interval_uri)
    try:
        count = len(triples["results"]["bindings"])
    except:
        count = 0
    i = 0
    while i < count:
        b = triples["results"]["bindings"][i]
        p = b['p']['value']
        o = b['o']['value']
        if p == "http://vivoweb.org/ontology/core#start":
            datetime_value = get_datetime_value(o)
            datetime_interval['start_date'] = datetime_value
        if p == "http://vivoweb.org/ontology/core#end":
            datetime_value = get_datetime_value(o)
            datetime_interval['end_date'] = datetime_value
        i = i + 1
    return datetime_interval


def get_publication_venue(publication_venue_uri):
    """
    Given a URI, return an object that contains the publication venue it
    represents
    """
    publication_venue = {'publication_venue_uri':publication_venue_uri}
    triples = get_triples(publication_venue_uri)
    try:
        count = len(triples["results"]["bindings"])
    except:
        count = 0
    i = 0
    while i < count:
        b = triples["results"]["bindings"][i]
        p = b['p']['value']
        o = b['o']['value']
        if p == "http://purl.org/ontology/bibo/issn":
            publication_venue['issn'] = o
        if p == "http://www.w3.org/2000/01/rdf-schema#label":
            publication_venue['label'] = o
        i = i + 1
    return publication_venue

def get_grant(grant_uri, get_investigators=False):
    """
    Given a URI, return an object that contains the grant it represents
    """
    grant = {'grant_uri':grant_uri}
    grant['contributing_role_uris'] = []
    grant['pi_uris'] = []
    grant['coi_uris'] = []
    grant['inv_uris'] = []
    grant['role_uris'] = {}
    grant['investigators'] = []
    triples = get_triples(grant_uri)
    try:
        count = len(triples["results"]["bindings"])
    except:
        count = 0
    i = 0
    while i < count:
        b = triples["results"]["bindings"][i]
        p = b['p']['value']
        o = b['o']['value']
        if p == "http://www.w3.org/2000/01/rdf-schema#label":
            grant['title'] = o
        if p == "http://vivoweb.org/ontology/core#totalAwardAmount":
            grant['total_award_amount'] = o
        if p == "http://vivoweb.org/ontology/core#grantDirectCosts":
            grant['grant_direct_costs'] = o
        if p == "http://purl.org/ontology/bibo/abstract":
            grant['abstract'] = o
        if p == "http://vivoweb.org/ontology/core#sponsorAwardId":
            grant['sponsor_award_id'] = o
        if p == "http://vivo.ufl.edu/ontology/vivo-ufl/dsrNumber":
            grant['dsr_number'] = o
        if p == "http://vivo.ufl.edu/ontology/vivo-ufl/psContractNumber":
            grant['pcn'] = o
        if p == "http://vivo.ufl.edu/ontology/vivo-ufl/dateHarvested":
            grant['date_harvested'] = o
        if p == "http://vivo.ufl.edu/ontology/vivo-ufl/harvestedBy":
            grant['harvested_by'] = o
        if p == "http://vivo.ufl.edu/ontology/vivo-ufl/localAwardId":
            grant['local_award_id'] = o
        if p == "http://vivoweb.org/ontology/core#contributingRole":
            grant['contributing_role_uris'].append(o)
        
        # deref administered by

        if p == "http://vivoweb.org/ontology/core#administeredBy":
            grant['administered_by_uri'] = o
            administered_by = get_organization(o)
            grant['administered_by'] = administered_by['label']

        # deref awarded by

        if p == "http://vivoweb.org/ontology/core#grantAwardedBy":
            grant['sponsor_uri'] = o
            awarded_by = get_organization(o)
            grant['awarded_by'] = awarded_by['label']

        # deref the datetime interval

        if p == "http://vivoweb.org/ontology/core#dateTimeInterval":
            grant['dti_uri'] = o
            datetime_interval = get_datetime_interval(o)
            grant['datetime_interval'] = datetime_interval
            if 'start_date' in datetime_interval:
                grant['start_date'] = datetime_interval['start_date']
            if 'end_date' in datetime_interval:
                grant['end_date'] = datetime_interval['end_date']

        i = i + 1

    # deref the roles

    for role_uri in grant['contributing_role_uris']:
        role = get_role(role_uri)
        if 'principal_investigator_role_of' in role:
            pi_uri = role['principal_investigator_role_of']
            if pi_uri not in grant['pi_uris']:
                grant['pi_uris'].append(pi_uri)
                grant['role_uris'][pi_uri] = role_uri
        if 'co_principal_investigator_role_of' in role:
            coi_uri = role['co_principal_investigator_role_of']
            if coi_uri not in grant['coi_uris']:
                grant['coi_uris'].append(coi_uri)
                grant['role_uris'][coi_uri] = role_uri
        if 'investigator_role_of' in role:
            inv_uri = role['investigator_role_of']
            if inv_uri not in grant['inv_uris']:
                grant['inv_uris'].append(inv_uri)
                grant['role_uris'][inv_uri] = role_uri

    # deref the investigators

    if get_investigators == True:
        for role_uri in grant['contributing_role_uris']:
            role = get_role(role_uri)
            if 'co_principal_investigator_role_of' in role:
                person = \
                    get_person(role['co_principal_investigator_role_of'])
                person['role'] = 'co_principal_investigator'
                grant['investigators'].append(person)
            if 'principal_investigator_role_of' in role:
                person = \
                    get_person(role['principal_investigator_role_of'])
                person['role'] = 'principal_investigator'
                grant['investigators'].append(person)
            if 'investigator_role_of' in role:
                person = \
                    get_person(role['investigator_role_of'])
                person['role'] = 'investigator'
                grant['investigators'].append(person)
    return grant

def string_from_grant(grant):
    """
    Given a grant object, return a string representing the grant

    To Do
    Need the PI and the dates
    """
    s = ""
    if 'awarded_by' in grant:
        s = s + grant['awarded_by'] + '\n'
    if 'sponsor_award_id' in grant:
        s = s + grant['sponsor_award_id']
    if 'pi_name' in grant:
        s = s + '          ' + grant['pi_name']
    if 'award_amount' in grant:
        s = s + ' $' + grant['award_amount']
    if 'start_date' in grant:
        s = s + '          ' + grant['start_date']['date']['month'] + '/' + \
            grant['start_date']['date']['day'] + '/' + \
            grant['start_date']['date']['year']
    if 'end_date' in grant:
        s = s + ' - ' + grant['end_date']['date']['month'] + '/' + \
            grant['end_date']['date']['day'] + '/' + \
            grant['end_date']['date']['year']
    if 'title' in grant:
        s = s + '\n' + grant['title']
    return s

def make_concept_dictionary(debug=False):
    """
    Make a dictionary for concepts in UF VIVO.  Key is label.  Value is URI.
    """

    global concept_dictionary
    concept_dictionary = {}

    query = tempita.Template("""
        SELECT ?uri ?label WHERE
        {
        ?uri a skos:Concept .
        ?uri rdfs:label ?label .
        }""")
    query = query.substitute()
    result = vivo_sparql_query(query)
    try:
        count = len(result["results"]["bindings"])
    except:
        count = 0
    if debug:
        print query, count, result["results"]["bindings"][0], \
            result["results"]["bindings"][1]
    i = 0
    while i < count:
        b = result["results"]["bindings"][i]
        label = b['label']['value']
        uri = b['uri']['value']
        concept_dictionary[label] = uri
        i = i + 1
    return concept_dictionary


def make_concept_rdf(label):
    """
    Given a concept label, create a concept in VIVO
    """
    concept_template = tempita.Template("""
    <rdf:Description rdf:about="{{concept_uri}}">
        <rdf:type rdf:resource="http://www.w3.org/2004/02/skos/core#Concept"/>
        <rdfs:label>{{label}}</rdfs:label>
    </rdf:Description>""")
    concept_uri = get_vivo_uri()
    rdf = concept_template.substitute(concept_uri=concept_uri, \
        label=label)
    return [rdf, concept_uri]

def make_deptid_dictionary(debug=False):
    """
    Make a dictionary for orgs in UF VIVO.  Key is DeptID.  Value is URI.
    """
    query = tempita.Template("""
    SELECT ?x ?deptid WHERE
    {
    ?x rdf:type foaf:Organization .
    ?x ufVivo:deptID ?deptid .
    }""")
    query = query.substitute()
    result = vivo_sparql_query(query)
    try:
        count = len(result["results"]["bindings"])
    except:
        count = 0
    if debug:
        print query, count, result["results"]["bindings"][0], \
            result["results"]["bindings"][1]
    #
    deptid_dictionary = {}
    i = 0
    while i < count:
        b = result["results"]["bindings"][i]
        deptid = b['deptid']['value']
        uri = b['x']['value']
        deptid_dictionary[deptid] = uri
        i = i + 1
    return deptid_dictionary

def find_deptid(deptid, deptid_dictionary):
    """
    Given a deptid, find the org with that deptid.  Return True and URI
    if found.  Return false and None if not found
    """
    try:
        uri = deptid_dictionary[deptid]
        found = True
    except:
        uri = None
        found = False
    return [found, uri]


def make_ufid_dictionary(debug=False):
    """
    Make a dictionary for people in UF VIVO.  Key is UFID.  Value is URI.
    """
    query = tempita.Template("""
    SELECT ?x ?ufid WHERE
    {
    ?x rdf:type foaf:Person .
    ?x ufVivo:ufid ?ufid .
    }""")
    query = query.substitute()
    result = vivo_sparql_query(query)
    try:
        count = len(result["results"]["bindings"])
    except:
        count = 0
    if debug:
        print query, count, result["results"]["bindings"][0], \
            result["results"]["bindings"][1]
    #
    ufid_dictionary = {}
    i = 0
    while i < count:
        b = result["results"]["bindings"][i]
        ufid = b['ufid']['value']
        uri = b['x']['value']
        ufid_dictionary[ufid] = uri
        i = i + 1
    return ufid_dictionary

def find_person(ufid, ufid_dictionary):
    """
    Given a UFID, and a dictionary, find the person with that UFID.  Return True
    and URI if found. Return False and None if not found
    """
    try:
        uri = ufid_dictionary[ufid]
        found = True
    except:
        uri = None
        found = False
    return [found, uri]

def make_doi_dictionary(debug=False):
    """
    Extract all the dois of documents in VIVO and organize them into a
    dictionary keyed by prepared label with value URI
    """
    query = tempita.Template("""
    SELECT ?x ?doi WHERE
    {
    ?x rdf:type bibo:Document .
    ?x bibo:doi ?doi .
    }""")
    doi_dictionary = {}
    query = query.substitute()
    result = vivo_sparql_query(query)
    try:
        count = len(result["results"]["bindings"])
    except:
        count = 0
    if debug:
        print query, count, result["results"]["bindings"][0], \
            result["results"]["bindings"][1]
    #
    doi_dictionary = {}
    i = 0
    while i < count:
        b = result["results"]["bindings"][i]
        doi = b['doi']['value']
        uri = b['x']['value']
        doi_dictionary[doi] = uri
        i = i + 1
    return doi_dictionary

def make_title_dictionary(debug=False):
    """
    Extract all the titles of documents in VIVO and organize them into a
    dictionary keyed by prepared label with value URI
    """
    query = tempita.Template("""
    SELECT ?x ?label WHERE
    {
    ?x rdf:type bibo:Document .
    ?x rdfs:label ?label .
    }""")
    title_dictionary = {}
    query = query.substitute()
    result = vivo_sparql_query(query)
    try:
        count = len(result["results"]["bindings"])
    except:
        count = 0
    if debug:
        print query, count, result["results"]["bindings"][0], \
            result["results"]["bindings"][1]
    #
    title_dictionary = {}
    i = 0
    while i < count:
        b = result["results"]["bindings"][i]
        title = b['label']['value']
        key = key_string(title)
        uri = b['x']['value']
        title_dictionary[key] = uri
        i = i + 1
    return title_dictionary

def find_title(title, title_dictionary):
    """
    Given a title, and a title dictionary, find the document in VIVO with that
    title.  Return True and URI if found.  Return False and None if not found
    """
    key = key_string(title)
    try:
        uri = title_dictionary[key]
        found = True
    except:
        uri = None
        found = False
    return [found, uri]

def make_publisher_dictionary(debug=False):
    """
    Extract all the publishers from VIVO and organize them into a dictionary
    keyed by prepared label with value URI
    """
    query = tempita.Template("""
    SELECT ?x ?label WHERE
    {
    ?x rdf:type core:Publisher .
    ?x rdfs:label ?label .
    }""")
    query = query.substitute()
    result = vivo_sparql_query(query)
    try:
        count = len(result["results"]["bindings"])
    except:
        count = 0
    if debug:
        print query, count, result["results"]["bindings"][0], \
            result["results"]["bindings"][1]
    #
    publisher_dictionary = {}
    i = 0
    while i < count:
        b = result["results"]["bindings"][i]
        publisher = b['label']['value']
        key = key_string(publisher)
        uri = b['x']['value']
        publisher_dictionary[key] = uri
        i = i + 1
    return publisher_dictionary

def find_publisher(publisher, publisher_dictionary):
    """
    Given a publisher label, and a publisher dictionary, find the publisher in
    VIVO with that label.  Return True and URI if found.  Return False and
    None if not found
    """
    key = key_string(publisher)
    try:
        uri = publisher_dictionary[key]
        found = True
    except:
        uri = None
        found = False
    return [found, uri]

def make_journal_dictionary(debug=False):
    """
    Extract all the journals from VIVO and organize them into a dictionary
    keyed by ISSN with value URI
    """
    query = tempita.Template("""
    SELECT ?x ?issn WHERE
    {
    ?x rdf:type bibo:Journal .
    ?x bibo:issn ?issn .
    }""")
    query = query.substitute()
    result = vivo_sparql_query(query)
    try:
        count = len(result["results"]["bindings"])
    except:
        count = 0
    if debug:
        print query, count, result["results"]["bindings"][0], \
            result["results"]["bindings"][1]
    #
    journal_dictionary = {}
    i = 0
    while i < count:
        b = result["results"]["bindings"][i]
        issn = b['issn']['value']
        uri = b['x']['value']
        journal_dictionary[issn] = uri
        i = i + 1
    return journal_dictionary

def find_journal(issn, journal_dictionary):
    """
    Given an issn, and a journal_dictinary, find the journal in VIVO with that
    UFID. Return True and URI if found.  Return False and None if not found
    """
    try:
        uri = journal_dictionary[issn]
        found = True
    except:
        uri = None
        found = False
    return [found, uri]

def make_webpage_rdf(full_text_uri, \
    uri_type="http://vivo.ufl.edu/ontology/vivo-ufl/FullTextURL", \
    link_anchor_text="PubMed Central Full Text Link", rank="1", \
    harvested_by="Python PubMed 1.0"):
    """
    Given a uri, create a web page entity with the uri, rank and
    anchor text, harvested_by specified
    """
    if full_text_uri is None:
        return ["", None]
    full_text_url_rdf_template = tempita.Template("""
    <rdf:Description rdf:about="{{webpage_uri}}">
        <rdf:type rdf:resource="http://vivoweb.org/ontology/core#URLLink"/>
        <rdf:type rdf:resource="{{uri_type}}"/>
        <vivo:linkURI>{{full_text_uri}}</vivo:linkURI>
        <vivo:rank>{{rank}}</vivo:rank>
        <vivo:linkAnchorText>{{link_anchor_text}}</vivo:linkAnchorText>
        <ufVivo:harvestedBy>{{harvested_by}}</ufVivo:harvestedBy>
        <ufVivo:dateHarvested>{{harvest_datetime}}</ufVivo:dateHarvested>
    </rdf:Description>""")
    webpage_uri = get_vivo_uri()
    harvest_datetime = make_harvest_datetime()
    rdf = full_text_url_rdf_template.substitute(webpage_uri=webpage_uri, \
        full_text_uri=full_text_uri, \
        rank=rank, \
        uri_type=uri_type, \
        link_anchor_text=link_anchor_text, \
        harvested_by=harvested_by, \
        harvest_datetime=harvest_datetime)
    return [rdf, webpage_uri]

def catalyst_pmid_request(first, middle, last, email, debug=False):
    """
    Give an author name at the University of Florida, return the PMIDs of
    papers that are likely to be the works of the author.  The Harvard
    Catalyst GETPMIDS service is called.

    Uses HTTP XML Post request, by www.forceflow.be
    """
    request = tempita.Template("""
        <?xml version="1.0"?>
        <FindPMIDs>
            <Name>
                <First>{{first}}</First>
                <Middle>{{middle}}</Middle>
                <Last>{{last}}</Last>
                <Suffix/>
            </Name>
            <EmailList>
                <email>{{email}}</email>
            </EmailList>
            <AffiliationList>
                <Affiliation>%university of florida%</Affiliation>
                <Affiliation>%@ufl.edu%</Affiliation>
            </AffiliationList>
            <LocalDuplicateNames>1</LocalDuplicateNames>
            <RequireFirstName>false</RequireFirstName>
            <MatchThreshold>0.98</MatchThreshold>
        </FindPMIDs>""")
    HOST = "profiles.catalyst.harvard.edu"
    API_URL = "/services/GETPMIDs/default.asp"
    request = request.substitute(first=first, middle=middle, last=last, \
        email=email)
    webservice = httplib.HTTP(HOST)
    webservice.putrequest("POST", API_URL)
    webservice.putheader("Host", HOST)
    webservice.putheader("User-Agent", "Python post")
    webservice.putheader("Content-type", "text/xml; charset=\"UTF-8\"")
    webservice.putheader("Content-length", "%d" % len(request))
    webservice.endheaders()
    webservice.send(request)
    statuscode, statusmessage, header = webservice.getreply()
    result = webservice.getfile().read()
    if debug:
        print "Request", request
        print "StatusCode, Messgage,header", statuscode, statusmessage, header
        print "result", result
    return result

def document_from_pubmed(record):
    """
    Given a record returned by Entrez for a document in pubmed, pull it apart
    keeping only the data elements useful for VIVO
    """
    d = {}
    d['title'] = record['MedlineCitation']['Article']['ArticleTitle']
    d['date'] = {'month': record['PubmedData']['History'][0]['Month'],
        'day'  : record['PubmedData']['History'][0]['Day'],
        'year' : record['PubmedData']['History'][0]['Year']}
    d['journal'] = record['MedlineCitation']['Article']['Journal']['Title']

    author_list = list(record['MedlineCitation']['Article']['AuthorList'])
    authors = {}
    i = 0
    for author in author_list:
        i = i + 1
        first = author['ForeName']
        if first.find(' ') >= 0:
            first = first[:first.find(' ')]
        last = author['LastName']
        middle = author['Initials']
        if len(middle) == 2:
            middle = str(middle[1])
        else:
            middle = ""
        key = str(i)
        authors[key] = {'first':first, 'middle':middle, 'last':last}
    d['authors'] = authors

    d['volume'] = record['MedlineCitation']['Article']\
        ['Journal']['JournalIssue']['Volume']
    d['issue'] = record['MedlineCitation']['Article']['Journal']\
        ['JournalIssue']['Issue']
    d['issn'] = str(record['MedlineCitation']['Article']['Journal']['ISSN'])

    article_id_list = record['PubmedData']['ArticleIdList']
    for article_id in article_id_list:
        attributes = article_id.attributes
        if 'IdType' in attributes:
            if attributes['IdType'] == 'pubmed':
                d['pmid'] = str(article_id)
            elif attributes['IdType'] == 'doi':
                d['doi'] = str(article_id)

    pages = record['MedlineCitation']['Article']['Pagination']['MedlinePgn']
    pages_list = pages.split('-')
    try:
        start = pages_list[0]
        try:
            istart = int(start)
        except:
            istart = -1
    except:
        start = ""
        istart = -1
    try:
        end = pages_list[1]
        if end.find(';') > 0:
            end = end[:end.find(';')]
    except:
        end = ""
    if start != "" and istart > -1 and end != "":
        if int(start) > int(end):
            if int(end) > 99:
                end = str(int(start) - (int(start) % 1000) + int(end))
            elif int(end) > 9:
                end = str(int(start) - (int(start) % 100) + int(end))
            else:
                end = str(int(start) - (int(start) % 10) + int(end))
    d['page_start'] = start
    d['page_end'] = end
    return d

def string_from_document(doc):
    """
    Given a doc structure, create a string representation for printing
    """
    s = ""
    if 'authors' in doc:
        author_list = doc['authors']
        for key in sorted(author_list.keys()):
            value = author_list[key]
            s = s + value['last']
            if value['first'] == "":
                s = s + ', '
                continue
            else:
                s = s + ', ' + value['first']
            if value['middle'] == "":
                s = s + ', '
            else:
                s = s + ' ' + value['middle'] + ', '
    if 'title' in doc:
        s = s + '"' + doc['title']+'"'
    if 'journal' in doc:
        s = s + ', ' + doc['journal']
    if 'volume' in doc:
        s = s + ', ' + doc['volume']
    if 'issue' in doc:
        s = s + '(' + doc['issue'] + ')'
    if 'number' in doc:
        s = s + '(' + doc['number'] + ')'
    if 'date' in doc:
        s = s + ', ' + doc['date']['year']
    if 'page_start' in doc:
        s = s + ', pp ' + doc['page_start']
    if 'page_end' in doc:
        s = s + '-' + doc['page_end'] + '.'
    if 'doi' in doc:
        s = s + ' doi: ' + doc['doi']
    if 'pmid' in doc:
        s = s + ' pmid: ' + doc['pmid']
    if 'pmcid' in doc:
        s = s + ' pmcid: ' + doc['pmcid']
    return s


def make_harvest_datetime():
    dt = datetime.now()
    return dt.isoformat()

def update_pubmed(pub_uri, doi=None):
    """
    Given the uri of a pub in VIVO and a module concept dictionary,
    update the PubMed attributes for the paper, and include RDF
    to add to the concept dictionary if necessary
    """

    ardf = ""
    srdf = ""

    # Get the paper's attributes from VIVO

    pub = get_publication(pub_uri)
    if 'doi' not in pub and doi is None:
        return ["", ""]
    elif doi is None:
        doi = pub['doi']
    if 'pmid' not in pub:
        pub['pmid'] = None
    if 'pmcid' not in pub:
        pub['pmcid'] = None
    if 'nihmsid' not in pub:
        pub['nihmsid'] = None
    if 'abstract' not in pub:
        pub['abstract'] = None

    # Get the paper's attributes from PubMed

    try:
        values = get_pubmed_values(doi)
        pass
    except:
        return {}

    if values == {}:
        return ["", ""]

    if 'pmid' not in values:
        values['pmid'] = None
    if 'pmcid' not in values:
        values['pmcid'] = None
    if 'nihmsid' not in values:
        values['nihmsid'] = None
    if 'abstract' not in values:
        values['abstract'] = None

    [add, sub] = update_data_property(pub_uri, "bibo:pmid", pub['pmid'],
                                          values['pmid'])
    ardf = ardf + add
    srdf = srdf + sub

    [add, sub] = update_data_property(pub_uri, "vivo:pmcid", pub['pmcid'],
                                          values['pmcid'])
    ardf = ardf + add
    srdf = srdf + sub

    [add, sub] = update_data_property(pub_uri, "vivo:nihmsid", pub['nihmsid'],
                                          values['nihmsid'])
    ardf = ardf + add
    srdf = srdf + sub

    [add, sub] = update_data_property(pub_uri, "bibo:abstract", pub['abstract'],
                                          values['abstract'])
    ardf = ardf + add
    srdf = srdf + sub

    # Process the keyword_list and link to concepts in VIVO. If the
    # concept is not in VIVO, add it

    if 'keyword_list' in values:
        for keyword in values['keyword_list']:
            if keyword in concept_dictionary:
                keyword_uri = concept_dictionary[keyword]
                [add, sub] = update_resource_property(pub_uri, \
                    "vivo:hasSubjectArea", None, keyword_uri)
                ardf = ardf + add
                srdf = srdf + sub
            else:
                [add, keyword_uri] = make_concept_rdf(keyword)
                ardf = ardf + add
                concept_dictionary[keyword] = keyword_uri
                [add, sub] = update_resource_property(pub_uri, \
                    "vivo:hasSubjectArea", None, keyword_uri)
                ardf = ardf + add
                srdf = srdf + sub

    # Process the grants cited lists -- VIVO and PubMed

    if 'grants_cited' in values:
        pubmed_grants_cited = values['grants_cited']
    else:
        pubmed_grants_cited = None

    if 'grants_cited' in pub:
        if pubmed_grants_cited is None:    # Remove grants cited from VIVO
            for grant in pub['grants_cited']:
                [add, sub] = update_data_property(pub_uri, 'ufVivo:grantCited',
                                                    grant, None)
                ardf = ardf + add
                srdf = srdf + sub
        else:                                # Compare lists
            for grant in pub['grants_cited']:
                if grant not in pubmed_grants_cited:
                    [add, sub] = update_data_property(pub_uri, \
                        'ufVivo:grantCited', grant, None) # remove from VIVO
                    ardf = ardf + add
                    srdf = srdf + sub
            for grant in pubmed_grants_cited:
                if grant not in pub['grants_cited']:
                    [add, sub] = update_data_property(pub_uri, \
                        'ufVivo:grantCited', None, grant) # add to VIVO
                    ardf = ardf + add
                    srdf = srdf + sub
    else:
        if pubmed_grants_cited is None:    # No grants cited
            pass
        else:                                # Add Pubmed grants cited to VIVO
            for grant in pubmed_grants_cited:
                [add, sub] = update_data_property(pub_uri, 'ufVivo:grantCited',
                                                    None, grant)
                ardf = ardf + add
                srdf = srdf + sub

    #  Web page for full text

    if 'full_text_uri' in pub and 'full_text_uri' in values:
        # both have URI
        if pub['full_text_uri'] == values['full_text_uri']:
            pass # both have same URI for full text, nothing to do
        else:
            sub = remove_uri(pub['webpage']['webpage_uri'])
            srdf = srdf + sub

    elif 'full_text_uri' in pub and 'full_text_uri' not in values:
        pass  # keep the VIVO full text URI, might not be PubMed Central

    elif 'full_text_uri' not in pub and 'full_text_uri' in values:

        # Add web page

        [add, webpage_uri] = \
            make_webpage_rdf(values['full_text_uri'])
        ardf = ardf + add

        # Point the pub at the web page

        [add, sub] = update_resource_property(pub_uri, 'vivo:webpage', None,
            webpage_uri)
        ardf = ardf + add
        srdf = srdf + sub

        # Point the web page at the pub

        [add, sub] = update_resource_property(webpage_uri, 'vivo:webpageOf',
            None, pub_uri)
        ardf = ardf + add
        srdf = srdf + sub

    else:
        pass # Full text URI is not in VIVO and not in PubMed

    return [ardf, srdf]


def vivo_find_result(type="core:Publisher", label="Humana Press", debug=False):
    """
    Look for entities having the specified type and the specifed label.
    If you find any, return the json object
    """
    query_template = Template(
    """
    SELECT ?x WHERE {
      ?x rdf:type $type .
      ?x rdfs:label '''$label''' .
      }
    """
    )
    query = query_template.substitute(type=type, label=label)
    if debug:
        print query
    result = vivo_sparql_query(query)
    if debug:
        print result
    return result


def vivo_find(type="core:Publisher", label="Humana Press", debug=False):
    """
    Look for entities having the specified type and the specifed label.
    If you find any, return true (found).  Otherwise return false (not found)
    """
    query_template = Template(
    """
    SELECT COUNT(?s) WHERE {
      ?s rdf:type $type .
      ?s rdfs:label '''$label''' .
      }
    """
    )
    query = query_template.substitute(type=type, label=label)
    if debug:
        print query
    response = vivo_sparql_query(query)
    if debug:
        print response
    try:
        return int(response["results"]["bindings"][0]['.1']['value']) != 0
    except:
        return False

def get_vivo_uri(prefix="http://vivo.ufl.edu/individual/n"):
    """
    Find an unused VIVO URI at the site with the specified prefix
    """
    test_uri = prefix + str(random.randint(1, 9999999999))
    query = """
	SELECT COUNT(?z) WHERE {
	<""" + test_uri + """> ?y ?z
	}"""
    response = vivo_sparql_query(query)
    while int(response["results"]["bindings"][0]['.1']['value']) != 0:
        test_uri = prefix + str(random.randint(1, 9999999999))
        query = """
            SELECT COUNT(?z) WHERE {
            <""" + test_uri + """> ?y ?z
            }"""
        response = vivo_sparql_query(query)
    return test_uri

def vivo_sparql_query(query,
    baseURL="http://sparql.vivo.ufl.edu:3030/VIVO/sparql",
    format="application/sparql-results+json", debug=False):

    """
    Given a SPARQL query string return result set of the SPARQL query.  Default
    is to call the UF VIVO SPAQRL endpoint and receive results in JSON format
    """

    prefix = """
    PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd:     <http://www.w3.org/2001/XMLSchema#>
    PREFIX owl:     <http://www.w3.org/2002/07/owl#>
    PREFIX swrl:    <http://www.w3.org/2003/11/swrl#>
    PREFIX swrlb:   <http://www.w3.org/2003/11/swrlb#>
    PREFIX vitro:   <http://vitro.mannlib.cornell.edu/ns/vitro/0.7#>
    PREFIX bibo:    <http://purl.org/ontology/bibo/>
    PREFIX dcelem:  <http://purl.org/dc/elements/1.1/>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX event:   <http://purl.org/NET/c4dm/event.owl#>
    PREFIX foaf:    <http://xmlns.com/foaf/0.1/>
    PREFIX geo:     <http://aims.fao.org/aos/geopolitical.owl#>
    PREFIX pvs:     <http://vivoweb.org/ontology/provenance-support#>
    PREFIX ero:     <http://purl.obolibrary.org/obo/>
    PREFIX scires:  <http://vivoweb.org/ontology/scientific-research#>
    PREFIX skos:    <http://www.w3.org/2004/02/skos/core#>
    PREFIX ufVivo:  <http://vivo.ufl.edu/ontology/vivo-ufl/>
    PREFIX vitro:   <http://vitro.mannlib.cornell.edu/ns/vitro/public#>
    PREFIX vivo:    <http://vivoweb.org/ontology/core#>
    PREFIX core:    <http://vivoweb.org/ontology/core#>
    """
    params = {
        "default-graph":"",
        "should-sponge":"soft",
        "query":prefix+query,
        "debug":"on",
        "timeout":"7000",  # 7 seconds
        "format":format,
        "save":"display",
        "fname":""
    }
    querypart = urllib.urlencode(params)
    if debug:
        print "Base URL", baseURL
        print "Query:", querypart
    start = 2.0
    retries = 10
    count = 0
    while True:
        try:
            response = urllib.urlopen(baseURL, querypart).read()
            break
        except:
            count = count + 1
            if count > retries:
                break
            sleep_seconds = start**count
            print "<!-- Failed query. Count = "+str(count)+\
                " Will sleep now for "+str(sleep_seconds)+\
                " seconds and retry -->"
            time.sleep(sleep_seconds) # increase the wait time with each retry
    try:
        return json.loads(response)
    except:
        return None
