#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
1. Execute a python interpreter, ipython for example, in the same
   directory as this script.

2. Change path and names of the n3 files from which you want to
   generate the html file. See below annotation in code.

3. Run the script (or import all)

   [1] run extractor.py

4. Change the template "vocabulario.html" to one that fits your
   needs.

5. Use the function save_template() to generate the html file:

   [2] save_template("vocabulario.html", "20100626.html")

6. You will then have a file named "20100626.html" saved in the
   path directory where you executed this script.

"""
import rdflib

from os import path
from rdflib.graph import ConjunctiveGraph
from jinja2 import Environment, FileSystemLoader
from rdflib import ConjunctiveGraph
from rdflib import URIRef
from rdflib import Namespace
from rdflib import RDF, RDFS

# Change following lines as per your configuration:
TEMPLATE_PATH = path.join(path.dirname(__file__), 'templates')

f1 = '/home/jdelacueva/proyectos/kelsen/trunk/rdf/informacion_poder_judicial.n3'
f2 = '/home/jdelacueva/proyectos/kelsen/trunk/rdf/informacion_poder_legislativo.n3'
f3 = '/home/jdelacueva/proyectos/kelsen/trunk/rdf/organizacion_territorial.n3'
f4 = '/home/jdelacueva/proyectos/kelsen/trunk/rdf/organos_administracion_local.n3'
f5 = '/home/jdelacueva/proyectos/kelsen/trunk/rdf/organos_autonomicos_legislativos.n3'
f6 = '/home/jdelacueva/proyectos/kelsen/trunk/rdf/organos_constitucionales.n3'
f7 = '/home/jdelacueva/proyectos/kelsen/trunk/rdf/organos_poder_judicial.n3'
f8 = '/home/jdelacueva/proyectos/kelsen/trunk/rdf/vocabulario.n3'

g = ConjunctiveGraph()

g.parse(f1, format='n3')
g.parse(f2, format='n3')
g.parse(f3, format='n3')
g.parse(f4, format='n3')
g.parse(f5, format='n3')
g.parse(f6, format='n3')
g.parse(f7, format='n3')
g.parse(f8, format='n3')

def get_list_ns(g):
    "Returns a list of dictionaries with the namespaces used in the n3 file"
    result = list()
    for item in g.namespaces():
        prefix, iri = item[0].encode(), item[1].expandtabs()
        d = {"prefix":prefix, "iri":iri}
        result.append(d)
    return result

def get_list_classes(g):
    result = list()
    l = list(g.triples((None, None, rdflib.term.URIRef('http://www.w3.org/2000/01/rdf-schema#Class'))))
    subjects = [item[0] for item in l]
    subjects.sort()
    for item in subjects:
        lista = list()
        po = list(g.triples((item, None, None)))
        for element in po:
            d = {'predicate':element[1].expandtabs(), 'object': element[2].expandtabs()}
            lista.append(d)
        clases = {'subject':item.partition('#')[2], 'po': lista}
        result.append(clases)
    return result

def get_list_classes(g):
    result = list()
    l = list(g.triples((None, None, RDFS.Class)))
    subjects = [item[0] for item in l]
    subjects.sort()
    for item in subjects:
        lista = list()
        po = list(g.triples((item, None, None)))
        for element in po:
            d = {'predicate':element[1].expandtabs(), 'object': element[2].expandtabs()}
            lista.append(d)
        clases = {'subject':item.partition('#')[2], 'po': lista}
        result.append(clases)
    return result

def get_list_properties(g):
    result = list()
    l = list(g.triples((None, None, RDF.Property)))
    subjects = [item[0] for item in l]
    subjects.sort()
    for item in subjects:
        lista = list()
        po = list(g.triples((item, None, None)))
        for element in po:
            d = {'predicate':element[1].expandtabs(), 'object': element[2].expandtabs()}
            lista.append(d)
        clases = {'subject':item.partition('#')[2], 'po': lista}
        result.append(clases)
    return result

all_ns = get_list_ns(g)
all_classes = get_list_classes(g)
all_properties = get_list_properties(g)

jinja_env = Environment(loader=FileSystemLoader(TEMPLATE_PATH))

jinja_env.globals['referencias'] = all_ns
jinja_env.globals['clases'] = all_classes
jinja_env.globals['properties'] = all_properties

def render_template(template, **context):
    return jinja_env.get_template(template).render(**context)

def save_template(template, filename, **context):
    "Saves a html file using the template and variables"
    html = jinja_env.get_template(template).render(**context).encode('utf-8')
    f = open(filename, 'w')
    f.write(html)
    f.close()

def save_format_xml(destination):
    g.serialize(destination, format='xml')
