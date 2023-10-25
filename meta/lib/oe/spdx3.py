#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: GPL-2.0-only
#

#
# This library is intended to set the data types for the SPDX3 specification. It
# is not intended to encode any particular OE specific behaviors, see the
# sbom.py for that.
#

from oe.spdx import _String, _StringList, _Object, _ObjectList
from oe.spdx import SPDXObject

import json
import hashlib

class SPDX3Tool(SPDXObject):
    pass

class SPDX3Agent(SPDXObject):
    pass

#
# Profile: Core - Enumerations
#
SPDX3HashAlgorithm = [
    "blake2b256",
    "blake2b384",
    "blake2b512",
    "blake3",
    "crystalsKyber",
    "crystalsDilithium",
    "falcon",
    "md2",
    "md4",
    "md5",
    "md6",
    "other",
    "sha1",
    "sha224",
    "sha256",
    "sha3_224",
    "sha3_256",
    "sha3_384",
    "sha3_512",
    "sha384",
    "sha512",
    "spdxPvcSha1",
    "spdxPvcSha256",
    "sphincsPlus"
]

#
# Profile: Core - Datatypes
#

class SPDX3IntegrityMethod(SPDXObject):
    comment = _String()

class SPDX3Hash(SPDX3IntegrityMethod):
    hashValue = _String()
    algorithm = _String()

#
# Profile: Core - Classes
#
class SPDX3CreationInfo(SPDXObject):
    specVersion = _String(default="3.0.0")
    comment = _String(default="")
    created = _String()
    createdBy = _ObjectList(SPDX3Agent)
    profile = _StringList(default=["core", "software"])  # TODO: not in creationInfo in spec
    createdUsing = _ObjectList(SPDX3Tool)
    dataLicense = _String(default="CC0-1.0")

    def serializer(self):
        """
        Serialize a creationInfo element.
        createdBy and createdUsing are only stored with their spdxId.
        other attributes are ordinary serialized
        """
        main = {"type": self.__class__.__name__[len("SPDX3"):],
                "createdBy": []}

        main["createdBy"] = [c.spdxId for c in self._spdx["createdBy"]]
        if "createdUsing" in self._spdx and len(self._spdx["createdUsing"]):
            main["createdUsing"] = [c.spdxId for c in self._spdx["createdUsing"]]

        for (key, value) in self._spdx.items():
            if not key in ["createdBy", "createdUsing"] \
               and value is not None and value is not "":
                main.update({key: value})
        return main

class SPDX3ExternalMap(SPDXObject):
    externalId = _String()
    verifiedUsing = _ObjectList(SPDX3IntegrityMethod)
    definingDocument = _String()

class SPDX3Element(SPDXObject):
    spdxId = _String(default="SPDXRef-DOCUMENT")
    name = _String()
    summary = _String()
    description = _String()
    creationInfo = _String()
    verifiedUsing = _ObjectList(SPDX3IntegrityMethod)
#    packages = _ObjectList(SPDXPackage)
#    files = _ObjectList(SPDXFile)
#    relationships = _ObjectList(SPDXRelationship)
#    externalDocumentRefs = _ObjectList(SPDXExternalDocumentRef)
#    hasExtractedLicensingInfos = _ObjectList(SPDXExtractedLicensingInfo)

    def serializer(self, rootElement, ignorekeys=[]):
        """
        Default serialization of an Element
        creationInfo is moved to the root and refered with its id
        context and element defined in ElementCollection and Bundle are ignored
        Element objects are ignored
        other attributes are ordinary serialized
        """
        main = {"type": self.__class__.__name__[len("SPDX3"):]}

        for (key, value) in self._spdx.items():
            if key == "creationInfo":
                _id = rootElement.creationinfo(value)
                main["creationInfo"] = _id
            elif key not in ignorekeys \
                and not isinstance(value, SPDX3Element):
                if key[0] == '_':
                    main.update({key[1:]: value})
                else:
                    main.update({key: value})
        return main

    def add_relationship(self, _from, relationship, _to):
        if isinstance(_from, SPDX3Element):
            from_spdxid = _from.spdxId
        else:
            from_spdxid = _from

        if isinstance(_to, SPDX3Element):
            to_spdxid = _to.spdxId
        else:
            to_spdxid = _to

        for element in self.element:
            if isinstance(element, SPDX3Relationship) \
            and element._from == from_spdxid \
            and element.relationshipType == relationship:
                element.to.append(to_spdxid)
                return element.spdxId

        r = SPDX3Relationship(
            _from=from_spdxid,
            relationshipType=relationship,
            to = [to_spdxid]
        )

        self.element.append(r)
        return r.spdxId

    def find_external_map(self, sourceDocumentNamespace):
        for i in self.imports:
            if i.definingDocument == sourceDocumentNamespace:
                return i

class SPDX3Relationship(SPDX3Element):
    spdxId = _String(default="SPDXRef-Relationship") # TODO: increment id
    _from = _String()
    to = _StringList()
    relationshipType = _String()

class SPDX3Annotation(SPDX3Element):
    spdxId = _String(default="SPDXRef-Annotation") # TODO: increment id
    annotationType = _String()
    statement = _String()
    subject = _String()

class SPDX3Agent(SPDX3Element):
    pass

class SPDX3Person(SPDX3Agent):
    pass

class SPDX3Organization(SPDX3Agent):
    pass

class SPDX3Tool(SPDX3Element):
    pass

class SPDX3Artifact(SPDX3Element):
    suppliedBy = _ObjectList(SPDX3Agent)

class SPDX3ElementCollection(SPDX3Element):
    element = _ObjectList(SPDX3Element)
    imports = _ObjectList(SPDX3ExternalMap)

class SPDX3Bundle(SPDX3ElementCollection):
    context = _String(default="")

class SPDX3SpdxDocument(SPDX3Bundle):
    documentNamespace = _String()  # TODO: where is this definition ?
    creationInfo = _Object(SPDX3CreationInfo)

    _spdxcounter = 1

    def __init__(self):
        self._spdxcreationinfo = {}
        super().__init__()

    def creationinfo(self, c):
        """
        Look for a creationInfo in the dictionary. If it does not exist,
        create a unique id and append it if it does not exist.
        Return the id.
        """
        for (_id, info) in self._spdxcreationinfo.items():
            if c == info:
                return _id
        _id = "_:CreationInfo{}".format(SPDX3SpdxDocument._spdxcounter)
        SPDX3SpdxDocument._spdxcounter += 1
        self._spdxcreationinfo[_id] = c
        return _id

    def serializer(self, rootElement):
        """
        Serialize a SpdxDocument element.
        context has a specific serialization
        attributes of type Element are moved to root
        attributes are are ordinary serialized (context and element are ignored)
        all elements are moved to root
        """
        chunk = {"@context": [self.context, {}]}
        root = super().serializer(rootElement)
        chunk["@graph"] = []

        body = []
        for (_, value) in self._spdx.items():
            if isinstance(value, SPDX3Element):
                body.append(value.serializer(rootElement, ignorekeys=["context", "element"]))

        if len(self.element):
            root["element"] = []
            for e in self.element:
                root["element"].append(e.spdxId)
                body.append(e.serializer(rootElement, ignorekeys=["context", "element"]))

        for (_id, c) in self._spdxcreationinfo.items():
            cser = {"@id": _id}
            cser.update(c.serializer())
            chunk["@graph"].append(cser)

        chunk["@graph"].append(root)
        chunk["@graph"] = chunk["@graph"] + body

        return chunk

    def to_json(self, f, *, sort_keys=False, indent=None, separators=None):
        class Encoder(json.JSONEncoder):
            def __init__(self, rootElement=None, **kwargs):
                self.rootElement = rootElement
                super(Encoder, self).__init__(**kwargs)

            def default(self, o):
                if isinstance(o, SPDX3SpdxDocument):
                    return o.serializer(self.rootElement)
                elif isinstance(o, SPDXObject):
                    root = o.serializer(self.rootElement)
                    return root

                return super().default(o)

        sha1 = hashlib.sha1()
        for chunk in Encoder(
            rootElement=self,
            sort_keys=sort_keys,
            indent=indent,
            separators=separators,
        ).iterencode(self):
            chunk = chunk.encode("utf-8")
            f.write(chunk)
            sha1.update(chunk)

        return sha1.hexdigest()

    @classmethod
    def from_json(cls, f, attributes=[]):
        """
        Look into a json file. This will return a dictionnary that represents
        the SpdxDocument, and is attributes is specified, a list of
        representation of thos attributes.
        """

        class Decoder(json.JSONDecoder):
            def __init__(self, *args, **kwargs):
                super().__init__(object_hook=self.object_hook, *args, **kwargs)

            def object_hook(self, d):
                if '@graph' in d.keys():
                    spdxDocument = None
                    attr = {a: [] for a in attributes}
                    for p in d['@graph']:
                        if p is not None:
                            if p['type'] == 'SpdxDocument':
                                spdxDocument = p
                            elif p['type'] in attributes:
                                attr[p['type']].append(p)
                    return (spdxDocument, attr)
                else:
                    return d

        return json.load(f, cls=Decoder)

#
# Profile: Software - Datatypes
#
SPDX3SoftwarePurpose = [
    "application",
    "archive",
    "bom",
    "configuration",
    "container",
    "data",
    "device",
    "documentation",
    "executable",
    "file",
    "firmware",
    "framework",
    "install",
    "library",
    "module",
    "operatingSystem",
    "patch",
    "source",
    "other"
]

class SPDX3SoftwareArtifact(SPDX3Artifact):
    primaryPurpose = _String()
    additionalPurpose = _StringList()

class SPDX3Package(SPDX3SoftwareArtifact):
    packageVersion = _String()
    homePage = _String()
    downloadLocation = _String()

class SPDX3File(SPDX3SoftwareArtifact):
    pass

#
# OpenEmbedded base class
#
class SPDX3Graph(SPDXObject):
    # TODO: rework: graph should only have a list of objects and more
    # intelligence in to_json
    package = _Object(SPDX3Package)
    creationInfo = _Object(SPDX3CreationInfo)
    doc = _Object(SPDX3SpdxDocument)
    tool = _Object(SPDX3Tool)
    organization = _Object(SPDX3Organization)
    person = _Object(SPDX3Person)

    def __init__(self, **d):
        super().__init__(**d)


    def to_json(self, f, *, sort_keys=False, indent=None, separators=None):
        class Encoder(json.JSONEncoder):
            def default(self, o):
                if isinstance(o, SPDXObject):
                    return o.serializer()

                return super().default(o)

        sha1 = hashlib.sha1()
        for chunk in Encoder(
            sort_keys=sort_keys,
            indent=indent,
            separators=separators,
        ).iterencode(self):
            chunk = chunk.encode("utf-8")
            f.write(chunk)
            sha1.update(chunk)

        return sha1.hexdigest()

