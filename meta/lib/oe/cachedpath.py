#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: GPL-2.0-only
#
# Based on standard python library functions but avoid
# repeated stat calls. Its assumed the files will not change from under us
# so we can cache stat calls.
#

import os
import errno
import stat as statmod

class CachedPath(object):
    def __init__(self):
        self.statcache = {}
        self.lstatcache = {}
        self.normpathcache = {}
        return

    def updatecache(self, x):
        x = self.normpath(x)
        if x in self.statcache:
            del self.statcache[x]
        if x in self.lstatcache:
            del self.lstatcache[x]

    def normpath(self, path):
        if path in self.normpathcache:
            return self.normpathcache[path]
        newpath = os.path.normpath(path)
        self.normpathcache[path] = newpath
        return newpath

    def _callstat(self, path):
        if path in self.statcache:
            return self.statcache[path]
        try:
            st = os.stat(path)
            self.statcache[path] = st
            return st
        except os.error:
            self.statcache[path] = False
            return False

    # We might as well call lstat and then only 
    # call stat as well in the symbolic link case
    # since this turns out to be much more optimal
    # in real world usage of this cache
    def callstat(self, path):
        path = self.normpath(path)
        self.calllstat(path)
        return self.statcache[path]

    def calllstat(self, path):
        path = self.normpath(path)
        if path in self.lstatcache:
            return self.lstatcache[path]
        #bb.error("LStatpath:" + path)
        try:
            lst = os.lstat(path)
            self.lstatcache[path] = lst
            if not statmod.S_ISLNK(lst.st_mode):
                self.statcache[path] = lst
            else:
                self._callstat(path)
            return lst
        except (os.error, AttributeError):
            self.lstatcache[path] = False
            self.statcache[path] = False
            return False

    # This follows symbolic links, so both islink() and isdir() can be true
    # for the same path ono systems that support symlinks
    def isfile(self, path):
        """Test whether a path is a regular file"""
        st = self.callstat(path)
        if not st:
            return False
        return statmod.S_ISREG(st.st_mode)

    # Is a path a directory?
    # This follows symbolic links, so both islink() and isdir()
    # can be true for the same path on systems that support symlinks
    def isdir(self, s):
        """Return true if the pathname refers to an existing directory."""
        st = self.callstat(s)
        if not st:
            return False
        return statmod.S_ISDIR(st.st_mode)

    def islink(self, path):
        """Test whether a path is a symbolic link"""
        st = self.calllstat(path)
        if not st:
            return False
        return statmod.S_ISLNK(st.st_mode)

    # Does a path exist?
    # This is false for dangling symbolic links on systems that support them.
    def exists(self, path):
        """Test whether a path exists.  Returns False for broken symbolic links"""
        if self.callstat(path):
            return True
        return False

    def lexists(self, path):
        """Test whether a path exists.  Returns True for broken symbolic links"""
        if self.calllstat(path):
            return True
        return False

    # WARNING - this is not currently a drop in replacement since they return False
    # rather than raise exceptions.
    def stat(self, path):
        return self.callstat(path)

    # WARNING - this is not currently a drop in replacement since they return False
    # rather than raise exceptions.
    def lstat(self, path):
        return self.calllstat(path)

    def walk(self, top, topdown=True, onerror=None, followlinks=False):
        # Matches os.walk, not os.path.walk()
        stack = [top]
        islink, join = self.islink, os.path.join
        while stack:
            top = stack.pop()
            if isinstance(top, tuple):
                yield top
                continue

            dirs = []
            nondirs = []
            walk_dirs = []

            # We may not have read permission for top, in which case we can't
            # get a list of the files the directory contains.
            # We suppress the exception here, rather than blow up for a
            # minor reason when (say) a thousand readable directories are still
            # left to visit.
            try:
                scandir_it = os.scandir(top)
            except OSError as error:
                if onerror is not None:
                    onerror(error)
                continue

            cont = False
            with scandir_it:
                while True:
                    try:
                        try:
                            entry = next(scandir_it)
                        except StopIteration:
                            break
                    except OSError as error:
                        if onerror is not None:
                            onerror(error)
                        cont = True
                        break

                    try:
                        if followlinks:
                            is_dir = entry.is_dir(follow_symlinks=False) and not entry.is_junction()
                        else:
                            is_dir = entry.is_dir()
                    except OSError:
                        # If is_dir() raises an OSError, consider the entry not to
                        # be a directory, same behaviour as os.path.isdir().
                        is_dir = False

                    if is_dir:
                        dirs.append(entry.name)
                    else:
                        nondirs.append(entry.name)

                    if not topdown and is_dir:
                        # Bottom-up: traverse into sub-directory, but exclude
                        # symlinks to directories if followlinks is False
                        if followlinks:
                            walk_into = True
                        else:
                            try:
                                is_symlink = entry.is_symlink()
                            except OSError:
                                # If is_symlink() raises an OSError, consider the
                                # entry not to be a symbolic link, same behaviour
                                # as os.path.islink().
                                is_symlink = False
                            walk_into = not is_symlink

                        if walk_into:
                            walk_dirs.append(entry.path)
            if cont:
                continue

            if topdown:
                # Yield before sub-directory traversal if going top down
                yield top, dirs, nondirs
                # Traverse into sub-directories
                for dirname in reversed(dirs):
                    new_path = join(top, dirname)
                    # bpo-23605: os.path.islink() is used instead of caching
                    # entry.is_symlink() result during the loop on os.scandir() because
                    # the caller can replace the directory entry during the "yield"
                    # above.
                    if followlinks or not islink(new_path):
                        stack.append(new_path)
            else:
                # Yield after sub-directory traversal if going bottom up
                stack.append((top, dirs, nondirs))
                # Traverse into sub-directories
                for new_path in reversed(walk_dirs):
                    stack.append(new_path)


    ## realpath() related functions
    def __is_path_below(self, file, root):
        return (file + os.path.sep).startswith(root)

    def __realpath_rel(self, start, rel_path, root, loop_cnt, assume_dir):
        """Calculates real path of symlink 'start' + 'rel_path' below
        'root'; no part of 'start' below 'root' must contain symlinks. """
        have_dir = True

        for d in rel_path.split(os.path.sep):
            if not have_dir and not assume_dir:
                raise OSError(errno.ENOENT, "no such directory %s" % start)

            if d == os.path.pardir: # '..'
                if len(start) >= len(root):
                    # do not follow '..' before root
                    start = os.path.dirname(start)
                else:
                    # emit warning?
                    pass
            else:
                (start, have_dir) = self.__realpath(os.path.join(start, d),
                                                    root, loop_cnt, assume_dir)

            assert(self.__is_path_below(start, root))

        return start

    def __realpath(self, file, root, loop_cnt, assume_dir):
        while self.islink(file) and len(file) >= len(root):
            if loop_cnt == 0:
                raise OSError(errno.ELOOP, file)

            loop_cnt -= 1
            target = os.path.normpath(os.readlink(file))
    
            if not os.path.isabs(target):
                tdir = os.path.dirname(file)
                assert(self.__is_path_below(tdir, root))
            else:
                tdir = root

            file = self.__realpath_rel(tdir, target, root, loop_cnt, assume_dir)

        try:
            is_dir = self.isdir(file)
        except:
            is_dir = False

        return (file, is_dir)

    def realpath(self, file, root, use_physdir = True, loop_cnt = 100, assume_dir = False):
        """ Returns the canonical path of 'file' with assuming a
        toplevel 'root' directory. When 'use_physdir' is set, all
        preceding path components of 'file' will be resolved first;
        this flag should be set unless it is guaranteed that there is
        no symlink in the path. When 'assume_dir' is not set, missing
        path components will raise an ENOENT error"""

        root = os.path.normpath(root)
        file = os.path.normpath(file)

        if not root.endswith(os.path.sep):
            # letting root end with '/' makes some things easier
            root = root + os.path.sep

        if not self.__is_path_below(file, root):
            raise OSError(errno.EINVAL, "file '%s' is not below root" % file)

        try:
            if use_physdir:
                file = self.__realpath_rel(root, file[(len(root) - 1):], root, loop_cnt, assume_dir)
            else:
                file = self.__realpath(file, root, loop_cnt, assume_dir)[0]
        except OSError as e:
            if e.errno == errno.ELOOP:
                # make ELOOP more readable; without catching it, there will
                # be printed a backtrace with 100s of OSError exceptions
                # else
                raise OSError(errno.ELOOP,
                              "too much recursions while resolving '%s'; loop in '%s'" %
                              (file, e.strerror))

            raise

        return file
