# -*- coding: UTF-8 -*-
import xml.etree.ElementTree as ET

from exceptions import OpenNebulaException


class WrongNameError(OpenNebulaException):
    pass


class WrongIdError(OpenNebulaException):
    pass


class Template(object):
    def __init__(self, xml_element):
        self.MULTI_TAGS = {
                'DISK' : self.parse_disks,
                'NIC' : self.parse_nics
                }
        self.xml = ET.tostring(xml_element)
        self.xml_element = xml_element
        self.parse()

    def parse(self):
        for element in self.xml_element:
            tag = element.tag
            if tag in self.MULTI_TAGS.keys():
                self.MULTI_TAGS[tag](element)
            else:
                setattr(self, tag.lower(), element.text)

    def parse_disks(self, element):
        self.disks = getattr(self, 'disks', [])
        class Disk(Template):
            pass
        self.disks.append(Disk(element))

    def parse_nics(self, element):
        self.nics = getattr(self, 'nics', [])
        class Nic(Template):
            pass
        self.nics.append(Nic(element))


class XMLElement(object):
    XML_TYPES = {}

    def __init__(self, xml):
        if xml and not ET.iselement(xml):
            xml = ET.fromstring(xml)
        self.xml = xml

    def initialize_xml(self, xml, root_element):
        self.xml = ET.fromstring(xml)
        if self.xml.tag != root_element.upper():
            self.xml = None
        self.convert_types()

    def __getitem__(self, key):
        value = self.xml.find(key.upper())
        if value is not None:
            if value.text:
                return value.text
            else:
                return value
        else:
            raise IndexError()

    def __getattr__(self, name):
        try:
            return self[name]
        except IndexError:
            raise AttributeError(name)

    def convert_types(self):
        for name, fun in self.XML_TYPES.items():
            if isinstance(fun, list):
                tag, cls = fun
                xml = self.xml.find(tag)
                setattr(self, name, cls(xml))
            else:
                setattr(self, name, fun(self[name]))


class XMLPool(XMLElement):
    def __init__(self, xml):
        super(XMLPool, self).__init__(xml)

    def factory(self):
        pass

    def __iter__(self):
        if self.xml:
            return [self.factory(i) for i in self.xml].__iter__()
        else:
            return [].__iter__()


class Pool(XMLPool):
    def __init__(self, pool, element, client):
        super(Pool, self).__init__(None)

        self.pool_name = pool
        self.element_name = element
        self.client = client

    def info(self, *args):
        '''
        Retrives/Refreshes pool information
        '''
        data = self.client.call(self.METHODS['info'], *args)
        self.initialize_xml(data, self.pool_name)

    def get_by_id(self, id):
        for i in self:
            if i.id == id:
                return i
        raise WrongIdError()

    def get_by_name(self, name):
        for i in self:
            if i.name == name:
                return i
        raise WrongNameError()


class PoolElement(XMLElement):
    def __init__(self, xml, client):
        super(PoolElement, self).__init__(xml)
        self.client = client

    def info(self, *args):
        data = self.client.call(self.METHODS['info'], self.id)
        self.initialize_xml(data, self.element_name)

    def delete(self):
        '''
        Deletes current object from the pool
        '''
        self.client.call(self.METHODS['delete'], self.id)

