# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2021 CERN.
# Copyright (C) 2020-2021 Northwestern University.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Serializers."""

from .base import MarshmallowSerializer, SerializerMixin
from .json import JSONSerializer, MarshmallowJSONSerializer
from .xml import XMLSerializer

__all__ = (
    "JSONSerializer",
    "MarshmallowSerializer",
    "MarshmallowJSONSerializer",
    "SerializerMixin",
    "XMLSerializer",
)
