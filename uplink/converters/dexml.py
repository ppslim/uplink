"""
This module defines a converter that uses :py:mod:`dexml` Models
to deserialize and serialize values.
"""

# Standard library imports
import inspect

# Local imports
from uplink.converters import interfaces

# Import and monkeypatch minidom for safety
from xml.dom import minidom
from defusedxml.minidom import parse as defused_parse, parseString as defused_parseString
minidom.parse, minidom.parseString = defused_parse, defused_parseString

class DexmlConverter(interfaces.ConverterFactory):
    """
    A converter that serializes and deserializes values using
    :py:mod:`dexml` schemas.
    To deserialize XML responses into dexml model objects with this
    converter, define a :py:class:`dexml.Model` subclass and set
    it as the return annotation of a consumer method:
    .. code-block:: python
        @get("/users")
        def get_users(self, username) -> DexmlCustomModel():
            '''Fetch a single user'''
    Also, when instantiating a consumer, be sure to set this class as
    a converter for the instance:
    .. code-block:: python
        github = GitHub(BASE_URL, converter=DexmlConverter())
    Note:
        This converter is an optional feature and requires the :py:mod:`dexml`
        and :py:mod:`defusedxml` packages. For example, here's how to install
        this feature using pip::
            $ pip install uplink[dexml]
    """
    
