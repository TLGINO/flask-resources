# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2021 CERN.
# Copyright (C) 2020-2021 Northwestern University.
#
# Flask-Resources is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""JSON serializer."""

import json
import warnings

from flask import request
from flask.json import JSONEncoder as JSONEncoderBase
from speaklater import is_lazy_string

from .base import MarshmallowSerializer, SerializerMixin


def flask_request_options():
    """Options to pretty print the JSON."""
    if request and request.args.get("prettyprint"):
        return {
            "indent": 2,
            "sort_keys": True,
        }
    return {}


class JSONEncoder(JSONEncoderBase):
    """JSONEncoder for our custom needs.

    - Knows to force translate lazy translation strings.
    """

    def default(self, obj):
        """Override parent's default."""
        if is_lazy_string(obj):
            return str(obj)
        return super().default(obj)


class JSONSerializer(SerializerMixin):
    """JSON serializer implementation."""

    def __init__(self, encoder=None, options=None):
        """Initialize the JSONSerializer."""
        self._options = options or flask_request_options
        self._encoder = encoder or JSONEncoder

    @property
    def dumps_options(self):
        """Support adding options for the dumps() method."""
        return self._options() if callable(self._options) else self._options

    @property
    def encoder(self):
        """Support overriding the JSONEncoder used for serialization."""
        # We let classes through as-is
        if isinstance(self._encoder, type):
            return self._encoder
        elif callable(self._encoder):
            return self._encoder()
        return self._encoder

    def serialize_object(self, obj):
        """Dump the object into a json string."""
        return json.dumps(obj, cls=self.encoder, **self.dumps_options)

    def serialize_object_list(self, obj_list):
        """Dump the object list into a json string."""
        return json.dumps(obj_list, cls=self.encoder, **self.dumps_options)


class MarshmallowJSONSerializer(MarshmallowSerializer):
    """JSON serializing using Marshmallow to transform output."""

    warnings.warn(
        (
            "MarshmallowJSONSerializer is going to be deprecated"
            " use MarshmallowSerializer instead."
        ),
        DeprecationWarning,
    )

    def __init__(self, schema_cls, many_schema_cls=None, **options):
        """Initialize the serializer."""
        super().__init__(
            format_serializer_cls=JSONSerializer,
            object_schema_cls=schema_cls,
            list_schema_cls=many_schema_cls,
            **options
        )

    def dump_one(self, obj):
        """Dump the object with extra information."""
        warnings.warn(
            (
                "MarshmallowJSONSerializer.dump_one is going to be deprecated"
                "use MarshmallowSerializer.dump_obj instead."
            ),
            DeprecationWarning,
        )
        return super().dump_obj(obj)

    def dump_many(self, obj_list):
        """Dump the list of objects with extra information."""
        warnings.warn(
            (
                "MarshmallowJSONSerializer.dump_one is going to be deprecated"
                "use MarshmallowSerializer.dump_list instead."
            ),
            DeprecationWarning,
        )
        return super().dump_list(obj_list)
