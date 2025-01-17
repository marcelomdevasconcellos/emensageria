import codecs
import os
from urllib.parse import urlparse

import xmlschema  # type: ignore
from django.utils.http import url_has_allowed_host_and_scheme
from lxml import etree

from config.settings import ALLOWED_HOSTS


def verify_domain(referer):
    domain = ''
    if referer:
        parsed_url = urlparse(referer)
        domain = parsed_url.netloc.split(':')[0]
    return url_has_allowed_host_and_scheme(domain, allowed_hosts=ALLOWED_HOSTS)


def create_dir(filename):
    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory)
    if not os.path.exists(directory):
        raise NameError(
            f'Não foi possivel criar a pasta {filename}, verifique se a pasta está '
            'com permissão de escrita para o usuário do sistema.')


def save_file(filename, content):
    create_dir(filename)
    file = codecs.open(filename, "w", "utf-8")
    file.write(content)
    file.close()
    if not os.path.exists(filename):
        raise NameError('''Não foi possivel salvar o arquivo %s, verifique se a pasta
                           está com permissão de escrita para o usuário do sistema.''' % filename)


def read_file(filename):
    create_dir(filename)
    if os.path.isfile(filename):
        file = codecs.open(filename, "r", "utf-8")
        content = file.read()
        file.close()
        return content
    else:
        raise NameError('Não foi possivel ler o arquivo %s.' % filename)


def validar_schema(file_schema_xsd, file_xml):
    try:
        etree.parse(file_xml)
    except etree.XMLSyntaxError as e:
        return e
    schema = xmlschema.XMLSchema(file_schema_xsd)
    is_valid = schema.is_valid(file_xml)
    if not is_valid:
        return schema.iter_errors(file_xml)
