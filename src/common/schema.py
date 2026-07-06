#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict
from core.config import settings
class SchemaBase(BaseModel):
    """Base schema configuration"""

    model_config = ConfigDict(
        use_enum_values=True,
        json_encoders={datetime: lambda x: x.strftime(settings.DATETIME_FORMAT)},
    )