# -*- coding: utf-8 -*-
from plone.app.jsonfield import patch


patch.monkey_patch_fhir_base_model()

__author__ = 'Md Nazrul Islam<email2nazrul@gmail.com>'


# IMPORTS as API

from .field import JSON  # noqa: I001,F401
from .widget import JSONWidget  # noqa: I001,F401
# DONE
