import codecs
import os
import xmlschema
from lxml import etree


def create_dir(filename):
    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory)


def save_file(filename, content):
    create_dir(filename)
    file = codecs.open(filename, "w", "utf-8")
    file.write(content)
    file.close()


def read_file(filename):
    create_dir(filename)
    if os.path.isfile(filename):
        file = codecs.open(filename, "r", "utf-8")
        content = file.read()
        file.close()
        return content


def validar_schema(file_schema_xsd, file_xml):
    try:
        etree.parse(file_xml)
    except etree.XMLSyntaxError as e:
        return e
    schema = xmlschema.XMLSchema(file_schema_xsd)
    is_valid = schema.is_valid(file_xml)
    if not is_valid:
        return schema.iter_errors(file_xml)
