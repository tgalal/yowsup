from .protocoltreenode import ProtocolTreeNode
import unittest, time
from lxml import etree
import os

class ProtocolEntityMeta(type):
    __BASE_SCHEMA = """<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
    <xs:complexType name="yowsup_encodable" xml:base="xs:string" mixed="true">
            <xs:attribute name="meta-yowsup-encoding" use="optional" type="xs:string" />
        </xs:complexType>
        </xs:schema>
"""
    def __new__(cls, clsname, bases, dct):
        if "schema" not in dct:
            dct["schema"] = bases[0].schema

        elif dct["schema"] is not None:
            schemaXML = cls.getSchemaXML(dct["schema"])
            baseSCHEMA = etree.XML(ProtocolEntityMeta.__BASE_SCHEMA)
            for i in range(len(baseSCHEMA) -1, -1, -1):
                schemaXML.append(baseSCHEMA[i])

            parentSchemaNode = schemaXML.find("xs:redefine", namespaces={"xs": "http://www.w3.org/2001/XMLSchema"})
            if parentSchemaNode is not None:
                parentSchemaPath = parentSchemaNode.get("schemaLocation")
                originalSchemaPathDir = os.path.dirname(dct["schema"])
                targetPath = os.path.join(originalSchemaPathDir, parentSchemaPath)
                parentSchemaNode.set("schemaLocation", targetPath)
            dct["schema"] = etree.XMLSchema(schemaXML)

        originalToProtocolTreeNode = dct["toProtocolTreeNode"] if "toProtocolTreeNode" in dct else None
        def toProtocolTreeNodeWrapper(instance):
            result = originalToProtocolTreeNode(instance)

            if dct["schema"] and not cls.isValid(result.__str__(True), dct["schema"]):
                raise ValueError("Schema and XML don't match")

            return result


        originalFromProtocolTreeNode = dct["fromProtocolTreeNode"] if "fromProtocolTreeNode" in dct else None
        @staticmethod
        def fromProtocolTreeNodeWrapper(node):
            if dct["schema"] and not cls.isValid(node, dct["schema"]):
                raise ValueError("ProtocolTreeNode does not match Schema")
            # print(vars(originalFromProtocolTreeNode))
            return originalFromProtocolTreeNode.__func__(node)

        if originalToProtocolTreeNode:
            dct["toProtocolTreeNode"] = toProtocolTreeNodeWrapper

        if originalFromProtocolTreeNode:
            dct["fromProtocolTreeNode"] = fromProtocolTreeNodeWrapper

        return super(ProtocolEntityMeta, cls).__new__(cls, clsname, bases, dct)

    @classmethod
    def isValid(cls, xml, schema):
        parsedXML = etree.fromstring(xml) if type(xml) in (str,unicode) else xml
        return schema.validate(parsedXML)

    @classmethod
    def getSchemaXML(cls, absPathOrTuple):
        if type(absPathOrTuple) is tuple:
            path = os.path.join(os.path.abspath(os.path.dirname(absPathOrTuple[0])), absPathOrTuple[1])
        else:
            path = absPathOrTuple

        if not os.path.exists(path):
            raise ValueError("%s does not exist" % path)

        with open(path) as schemaFile:
            schemaData = schemaFile.read()

        return etree.XML(schemaData)

class ProtocolEntity(object):
    __metaclass__ = ProtocolEntityMeta
    schema = None
    __ID_GEN = 0

    def __init__(self, tag):
        self.tag = tag

    def getTag(self):
        return self.tag

    def isType(self,  typ):
        return self.tag == typ

    def _createProtocolTreeNode(self, attributes, children = None, data = None, ns = None, dataEncoding = None):
        return ProtocolTreeNode(self.getTag(), attributes, children, data, ns, dataEncoding=dataEncoding)


    def _getCurrentTimestamp(self):
        return int(time.time())

    def _generateId(self, short = False):
        ProtocolEntity.__ID_GEN += 1
        return str(ProtocolEntity.__ID_GEN) if short else str(int(time.time())) + "-" + str(ProtocolEntity.__ID_GEN)


    def toProtocolTreeNode(self):
        pass

    @staticmethod
    def fromProtocolTreeNode(self, protocolTreeNode):
        pass

    @classmethod
    def fromXML(cls, xml):
        if cls.isValid(xml):
            return cls.fromProtocolTreeNode(ProtocolTreeNode(xmlString = xml))
        else:
            raise ValueError("Invalid XML for this schema")

    @classmethod
    def isValid(cls, xml):
        if not cls.schema:
            return False
        #parser = etree.XMLParser(schema = cls.schema)
        #etree.fromstring(xml, parser)
        parsedXML = etree.XML(xml) if type(xml) in (str,unicode) else xml
        return cls.schema.validate(parsedXML)


class ProtocolEntityTest(object):
    def setUp(self):
        self.ProtocolEntity = None
        self.node = None
        self.xml = None

    # def assertEqual(self, entity, node):
    #     raise AssertionError("Should never execute that")

    def test_forward_backward_converstion(self):
        if self.ProtocolEntity is None:
            raise ValueError("Test case not setup!")

        node = ProtocolTreeNode(xmlString = self.xml) if self.___hasXmlDefined() else self.node

        entity = self.ProtocolEntity.fromProtocolTreeNode(node)
        try:
            self.assertEqual(entity.toProtocolTreeNode(), node)
        except:
            print(entity.toProtocolTreeNode())
            print("\nNOTEQ\n")
            print(node)
            raise

    def ___hasXmlDefined(self):
        """
        temporary check if xml instance variable
        until all eentities are migrated to schema bades
        """
        try:
            return self.xml is not None
        except AttributeError:
            return False

    def test_valid(self):
        if self.___hasXmlDefined():
            self.assertTrue(self.ProtocolEntity.isValid(self.xml))

