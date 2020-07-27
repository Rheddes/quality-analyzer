"""
This module contains all the classes related to a product, such as
Module, File, Method.
"""

import logging
import json
from typing import List, Set, Dict, Tuple, Optional
import lizard

logger = logging.getLogger(__name__)


class Package:
    """
    This class defines the metadata of a package,
    extracted from FASTEN call graph Json file.
    """

    def __init__(self, forge, product, version, path):
        self.forge = forge
        self.product = product
        self.version = version
        self.path = path
        self._file_list = []
        self._func_list = []  # List[Function] extracted from lizard with metrics
        self._method_list = []  # List[Methods] extracted from cg
        # aggregated metric
        self._method_count = None
        self._nloc = None
        self._complexity = None
        self._token_count = None

    def nloc(self) -> Optional[int]:
        self._calculate_metrics()
        return self._nloc

    def method_count(self) -> Optional[int]:
        self._calculate_metrics()
        return self._method_count

    def complexity(self) -> Optional:
        self._calculate_metrics()
        return self._complexity

    def _calculate_metrics(self):
        paths = [self.path]
        exc_patterns = ["*/test/*"]
        lans = ["java"]
        self._nloc = 0
        self._method_count = 0
        self._complexity = 0
        self._token_count = 0
        analyser = lizard.analyze(paths, exc_patterns, 1, None, lans)
        for f in analyser:
            self._file_list.append(File(f))
            for fun in f.function_list:
                self._func_list.append(Function(fun))
            self._nloc = self._nloc + f.nloc
            self._method_count = self._method_count + len(f.function_list)
            self._complexity = -1
            self._token_count = self._token_count + f.token_count
        return

    def files(self):
        return self._file_list

    def functions(self):
        return self._func_list

    def metrics(self):
        return {
            "nloc": self.nloc(),
            "method_count": self.method_count(),
            "complexity": self.complexity(),
            "file_list": [f.metrics() for f in self.files()],
        }


class File:
    def __init__(self, fileinfo):
        """
        Initialize a function object. This is extracted from Lizard
        """
        self.filename = fileinfo.filename
        self.nloc = fileinfo.nloc
        self.token_count = fileinfo.token_count
        self.function_list = [Function(x) for x in fileinfo.function_list]

    def metrics(self):
        return {
            "filename": self.filename,
            "nloc": self.nloc,
            "function_list": [fun.metrics() for fun in self.function_list]
        }


class Dependency:
    """
    This class defines the (direct?) dependencies of a package,
    extracted from FASTEN call graph Json file.
    """

    def __int__(self, cg):
        self._dep_list = []  # type: List[Package]


class Function:
    """
    This class represents a function in a package. Contains various information,
    extracted through Lizard.
    """

    def __init__(self, func):
        """
        Initialize a function object. This is calculated using Lizard
        """
        self.name = func.name
        self.long_name = func.long_name
        self.filename = func.filename
        self.nloc = func.nloc
        self.complexity = func.cyclomatic_complexity
        self.token_count = func.token_count
        self.parameters = func.parameters
        self.start_line = func.start_line
        self.end_line = func.end_line
        self.fan_in = func.fan_in
        self.fan_out = func.fan_out
        self.general_fan_out = func.general_fan_out
        self.length = func.length
        self.top_nesting_level = func.top_nesting_level

    def metrics(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

    def __eq__(self, other):
        return self.name == other.name and self.parameters == other.parameters

    def __hash__(self):
        # parameters are used in hashing in order to
        # prevent collisions when overloading method names
        return hash(('name', self.name,
                     'long_name', self.long_name,
                     'params', (x for x in self.parameters)))





