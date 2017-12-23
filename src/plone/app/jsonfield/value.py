# _*_ coding: utf-8 _*_
from .interfaces import IJSONValue
from collections import defaultdict
from plone import api
from plone.app.jsonfield.compat import _
from plone.app.jsonfield.compat import json
from zope.interface import implementer
from zope.interface import Invalid
from zope.schema import NO_VALUE
from zope.schema.interfaces import WrongType

import jsonpatch
import jsonschema
import six
import sys


__author__ = 'Md Nazrul Islam<email2nazrul@gmail.com>'


@implementer(IJSONValue)
class JSONValue(defaultdict):
    """"""
    def patch(self, patch_data):
        """:@links: https://python-json-patch.readthedocs.io/en/latest/tutorial.html#creating-a-patch"""
        if not isinstance(patch_data, (list, tuple)):
            raise WrongType('patch value must be list or tuple type! but got `{0}` type.'.format(type(patch_data)))

        try:
            patcher = jsonpatch.JsonPatch(patch_data)
            patcher.apply(self)
        except jsonpatch.JsonPatchException as e:
            six.reraise(Invalid, Invalid(str(e)), sys.exc_info()[2])

    def stringify(self, prettify=False):
        """ """
        params = {}
        params['encoding'] = 'utf-8'
        if prettify:
            # will make little bit slow, so apply only if needed
            params['indent'] = 4

        return 0 < len(self) and \
            json.dumps(self, **params) or \
            ''

    def _validate_object(self, obj, schema=None):
        """ """
        if obj in (None, NO_VALUE):
            return

        if schema:
            try:
                jsonschema.validate(obj, schema)
            except (
                    jsonschema.ErrorTree,
                    jsonschema.ValidationError,
                    jsonschema.SchemaError,
                    jsonschema.FormatError,
                    jsonschema.RefResolutionError
                    ) as exc:
                six.reraise(Invalid, Invalid(str(exc)), sys.exc_info()[2])
        else:
            try:
                json.dumps(obj)
            except ValueError as exc:
                msg = _('Only dict or list type value is allowed, value must be json serialable!')
                if api.debug_mode():
                    msg += _('Original exception: {0!s}').format(exc)

                six.reraise(WrongType, Invalid(msg), sys.exc_info()[2])

    def __init__(self, obj=None, schema=None, encoding='utf-8'):
        """ """
        # Let's validate before value assignment!
        self._validate_object(obj, schema=schema)
        self.encoding = encoding

        super(JSONValue, self).__init__(dict, obj)
