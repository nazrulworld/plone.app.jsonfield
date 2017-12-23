# _*_ coding:utf-8 _*_
from plone import api
from plone.app.jsonfield.compat import _
from plone.app.jsonfield.compat import json
from plone.app.jsonfield.helpers import parse_json_str
from plone.app.jsonfield.interfaces import IJSON
from plone.app.jsonfield.interfaces import IJSONValue
from plone.app.jsonfield.value import JSONValue
from zope.interface import implementer
from zope.interface import Invalid
from zope.schema import NO_VALUE
from zope.schema import Object
from zope.schema.interfaces import IFromUnicode
from zope.schema.interfaces import WrongType

import six
import sys


__author__ = 'Md Nazrul Islam<nazrul@zitelab.dk>'


@implementer(IJSON, IFromUnicode)
class JSON(Object):
    """JSON field"""
    _type = JSONValue

    def __init__(self, schema=None, **kw):
        """
        :param: schema: JSON Schema http://json-schema.org/
        """
        self.schema = schema
        self.init_validate()

        if 'default' in kw:
            default = kw['default']
            if isinstance(default, six.string_types):
                kw['default'] = self.fromUnicode(default)
            elif isinstance(default, dict):
                kw['default'] = self.from_iterable(default)
            elif default is None:
                kw['default'] = self.from_none()

        super(JSON, self).__init__(schema=IJSONValue, **kw)

    def fromUnicode(self, str_val):
        """ """
        json_dict = parse_json_str(str_val)

        return self.from_iterable(json_dict)

    def from_iterable(self, iter_value):
        """ """
        value = JSONValue(iter_value, schema=self.schema, encoding='utf-8')

        self.validate(value)

        return value

    def from_none(self):
        """" """
        return JSONValue(NO_VALUE)

    def init_validate(self):
        """ """
        if self.schema is None:
            # No validation is required.
            return

        try:
            json.dumps(self.schema)
            if not isinstance(self.schema, dict):
                raise WrongType(
                    'Schema value must be dict type! but got `{0!s}` type'.format(type(self.schema)))

        except ValueError as exc:
            msg = _('Invalid schema data type! dict data type is expected.')
            if api.env.debug_mode():
                msg += _('Original Exception: {0!s}').format(exc)
            six.reraise(Invalid, Invalid(msg), sys.exc_info()[2])
