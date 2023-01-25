#! /usr/bin/env python3


# CacheNodes construct a tree of possible values for each variable. Each nodes
# has a dictionary of override children where the key is the name of the
# override, and value is the CacheNode for that child.
#
# Nodes may or may not have a value associated with them
class CacheNode(object):
    def __init__(self, value=None):
        self.value = value
        self.overrides = {}

    def get_value(self, overrides=""):
        """
        Get node value

        :returns: The value of the node, applying any overrides
        """
        if not overrides:
            return self.value

        # Calculate the priority of each override; higher numbers mean a higher
        # priority. This will be used to both efficiently determine if an override
        # exists, and also determine which override should be used if multiple
        # match.
        override_priority = {
            value: idx for idx, value in enumerate(overrides.split(":"))
        }

        # Recursively check overrides
        child_value = self._get_override_value(override_priority)
        if child_value is not None:
            return child_value

        return self.value

    def _get_override_value(self, override_priority):
        # Generate a list of child overrides that are in the overrides list,
        # and sorted from highest priority to lowest
        sorted_overrides = sorted(
            (o for o in self.overrides if o in override_priority),
            key=lambda k: override_priority[k],
            reverse=True,
        )

        # Since the list of override children is sorted from highest priority
        # to lowest, the first one found is the highest priority and should be
        # returned
        for name in sorted_overrides:
            child_value = self.overrides[name]._get_override_value(override_priority)
            if child_value is not None:
                return child_value

        return self.value

    def walk(self, path, fn):
        fn(self, path)
        for name, node in self.overrides.items():
            node.walk(path + [name], fn)


class Cache(object):
    def __init__(self):
        self.root = CacheNode()

    def _get_node(self, varname):
        node = self.root
        for v in varname.split(":"):
            if not v in node.overrides:
                return None
            node = node.overrides[v]
        return node

    def _make_path(self, path):
        node = self.root

        for v in path:
            if v not in node.overrides:
                node.overrides[v] = CacheNode()
            node = node.overrides[v]

        return node

    def set(self, varname, value):
        """
        Set (or delete) a variable

        Sets the variable to the specified value. If value is `None`, this is
        equivalent to delete()
        """
        if value is None:
            self.delete(varname)
            return

        node = self._make_path(varname.split(":"))
        node.value = value

    def get(self, varname, overrides=""):
        """
        Get the value of a variable

        :returns: The value of the variable
        """

        # Get the starting node based on the request variable name
        node = self._get_node(varname)
        if node is None:
            return None

        return node.get_value(overrides)

    def _remove_node(self, varname, recursive=False):
        # If the deleted node is a leaf (has no children) and now has no value
        # (due to being deleted), it is removed from the tree. This continues
        # recursively up to the parent nodes, which are also removed if they
        # now have no children and also has no value. This ensures that the
        # cache tree maintains the minimum set of nodes; it also means that
        # every leaf node of the tree must have a non-None value
        def _remove_helper(node, name):
            if not name:
                # Remove this node if it has no child overrides, or this is a
                # recursive deletion
                return node, not node.overrides or recursive

            if not name[0] in node.overrides:
                return None, False

            del_node, needs_delete = _remove_helper(node.overrides[name[0]], name[1:])
            if needs_delete:
                del node.overrides[name[0]]

            # Remove this node if it has no value, and has no child
            # overrides (e.g. is now a leaf node)
            return del_node, node.value is None and not node.overrides

        n, _ = _remove_helper(self.root, varname.split(":"))
        return n

    def unset(self, varname):
        """
        Deletes the value for a variable in the cache

        Note that this doesn't affect any of the overrides which may apply to the variable

        :returns: The value the deleted variable had before it was removed
        """
        del_node = self._remove_node(varname)
        if del_node is not None:
            # Capture the value of the deleted node to be returned, then set
            # the node value to None. The node may or may not have been removed
            # from the tree; if not, setting the value to None is the actual
            # "deletion" of the node.
            value = del_node.value
            del_node.value = None
            return value

        return None

    def remove(self, varname):
        """
        Remove a value and all of its overrides from the cache
        """
        self._remove_node(varname, True)

    def rename(self, oldname, newname):
        """
        Rename a variable

        Renames a variable from one name to another. This doesn't move any of
        the child overrides of the renamed node
        """
        value = self.unset(oldname)
        # TODO: What to do if value is None? This will delete newname in that
        # case
        self.set(newname, value)

    def move(self, oldname, newname):
        """
        Move a variable in the cache

        Moves a variable and all of its overrides to another location in the cache
        """
        # Remove the node from its old location
        node = self._remove_node(oldname, True)

        if node is None or (node.value is None and not node.overrides):
            # Delete the target tree (TODO: Is this correct?)
            self._remove_node(newname, True)
            return

        # Insert the node at the new location
        newname = newname.split(":")
        parent = self._make_path(newname[:-1])
        parent.overrides[newname[-1]] = node

    def walk(self, fn):
        """
        Walk tree

        Walks the entire tree, calling `fn` for each node
        """
        # Don't call root.walk, because we don't really want to call the
        # callback on it
        for name, node in self.root.overrides.items():
            node.walk([name], fn)


def parse(code):
    cache = Cache()

    for l in code.splitlines():
        l = l.strip()
        if not l:
            continue

        if l.startswith("#"):
            continue

        var, value = l.split("=", maxsplit=1)
        var = var.strip()
        value = value.strip()

        cache.set(var, value)

    return cache


def main():
    import textwrap

    cache = parse(
        textwrap.dedent(
            """\
            VAR = 0
            VAR:b = 1
            VAR:a:b = 5
            VAR:a:c = 4
            VAR:b:d = 3
            VAR:b:a = 2
            VAR:f = 6
            """
        )
    )

    def print_node(node, prefix):
        name = ":".join(prefix)
        if node.value is not None:
            print(f"{name} = {node.value}")
        else:
            print(f"{name} is undefined")

    cache.walk(print_node)

    def e(varname, overrides=""):
        value = cache.get(varname, overrides)
        print(f"{varname} ({overrides}) = {value}")
        return value

    # Test cases
    assert e("VAR") == "0"
    assert e("VAR:b") == "1"
    assert e("VAR:a") is None
    assert e("VAR:c") is None
    assert e("VAR:d") is None

    # No override defined for "A"
    assert e("VAR", "a") == "0"
    assert e("VAR", "b") == "1"

    # No directly assigned value for VAR:C; defaults to VAR
    assert e("VAR", "c") == "0"

    # C is higher priority, but has no value defined, so B is used
    assert e("VAR", "b:c") == "1"

    assert e("VAR", "b:f") == "6"
    assert e("VAR", "f:b") == "1"

    # Priority crisscross from; NOTE THIS DIFFERS FROM CURRENT BITBAKE BEHAVIOR
    assert e("VAR", "b:a") == "5"
    assert e("VAR", "a:b") == "2"

    cache.unset("VAR:b")
    assert e("VAR", "b") == "0"
    assert e("VAR", "b:d") == "3"

    cache.rename("VAR:f", "VAR:g")
    assert e("VAR", "f") == "0"
    assert e("VAR", "g") == "6"

    cache.unset("VAR:a:b")
    cache.unset("VAR:a:c")
    cache.walk(print_node)
    assert e("VAR:a") is None

    cache.move("VAR:b", "VAR:h")
    cache.walk(print_node)
    assert e("VAR:b") is None
    assert e("VAR", "h") == "0"
    assert e("VAR", "h:d") == "3"


if __name__ == "__main__":
    import sys

    sys.exit(main())
