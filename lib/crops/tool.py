from json import JSONEncoder, JSONDecoder


class Tool(JSONEncoder):
    """
    Describes a tool in a toolchain, e.g. gcc or clang.
    """

    def __init__(self, uid, name, command, *args, **kwargs):
        self.uid = uid
        self.name = name
        self.command = command
        self.args = args
        self.kwargs = kwargs
        JSONEncoder.__init__(self, Tool)

    def default(self, obj):
        """
        Converts a Tool python object into objects
        that can be decoded using the ToolJSONDecoder
        """
        if isinstance(obj, Tool):
            return {
                '__type__': 'Tool',
                'uid': obj.uid,
                'name': obj.name,
                'command': obj.command,
                'args': obj.args
            }
        raise TypeError( repr(obj) + " is not an instance of Tool")


class ToolJSONDecoder(JSONDecoder):
    """
    Converts a json string, where a Tool python object was
    converted into objects compatible with ToolJSONEncoder, back
    into a python object.
    """

    def __init__(self, *args, **kwargs):
        JSONDecoder.__init__(self, object_hook=self.dict_to_object, *args, **kwargs)

    @staticmethod
    def dict_to_object(self, d):
        if '__type__' not in d:
            return d

        thistype = d.pop('__type__')
        if thistype == 'Tool':
            return Tool(**d)
        else:
            # Unhandled, so put it back together
            # TODO: throw NotSupportedException ?
            d['__type__'] = thistype
            return d
