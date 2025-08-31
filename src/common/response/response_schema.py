#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any, Generic, TypeVar

from fastapi import Response
from pydantic import BaseModel, Field

from common.response.response_code import CustomResponse, CustomResponseCode
from utils.serializers import MsgSpecJSONResponse

SchemaT = TypeVar('SchemaT')


class ResponseModel(BaseModel):
    """
    Generic unified response model without enforcing a data schema.

        @router.get('/test', response_model=ResponseModel)
        def test():
            return ResponseModel(data={'test': 'test'})


        @router.get('/test')
        def test() -> ResponseModel:
            return ResponseModel(data={'test': 'test'})


        @router.get('/test')
        def test() -> ResponseModel:
            res = CustomResponseCode.HTTP_200
            return ResponseModel(code=res.code, msg=res.msg, data={'test': 'test'})
    """

    code: int = Field(CustomResponseCode.HTTP_200.code, description='Response status code')
    msg: str = Field(CustomResponseCode.HTTP_200.msg, description='Response message')
    data: Any | None = Field(None, description='Response payload')


class ResponseSchemaModel(ResponseModel, Generic[SchemaT]):
    """
    Unified response model that enforces a Pydantic schema for the data field.
    Examples::

        @router.get('/test', response_model=ResponseSchemaModel[GetApiDetail])
        def test():
            return ResponseSchemaModel[GetApiDetail](data=GetApiDetail(...))


        @router.get('/test')
        def test() -> ResponseSchemaModel[GetApiDetail]:
            return ResponseSchemaModel[GetApiDetail](data=GetApiDetail(...))


        @router.get('/test')
        def test() -> ResponseSchemaModel[GetApiDetail]:
            res = CustomResponseCode.HTTP_200
            return ResponseSchemaModel[GetApiDetail](code=res.code, msg=res.msg, data=GetApiDetail(...))
    """

    data: SchemaT


class ResponseBase:
    """Provides helper methods to generate standardized responses."""

    @staticmethod
    def __response(
        *,
        res: CustomResponseCode | CustomResponse,
        data: Any | None,
    ) -> ResponseModel | ResponseSchemaModel:
        """
        Internal method to build the response model.

        :param res: A tuple or CustomResponse instance with code and message
        :param data: The payload to return
        """
        return ResponseModel(code=res.code, msg=res.msg, data=data)

    def success(
        self,
        *,
        res: CustomResponseCode | CustomResponse  = CustomResponseCode.HTTP_200,
        data: Any | None = None,

    ) -> ResponseModel | ResponseSchemaModel:
        """
        Build a successful response.

        :param res: Custom response code and message (default: HTTP 200 OK)
        :param data: Payload to include in the response
        """
        return self.__response(res=res, data=data)

    def fail(
        self,
        *,
        res: CustomResponseCode | CustomResponse = CustomResponseCode.HTTP_400,
        data: Any = None,
    ) -> ResponseModel | ResponseSchemaModel:
        """
        Build a failure response.

        :param res: Custom response code and message (default: HTTP 400 Bad Request)
        :param data: Optional payload (e.g. error details)
        """
        return self.__response(res=res, data=data)

    @staticmethod
    def fast_success(
        *,
        res: CustomResponseCode | CustomResponse = CustomResponseCode.HTTP_200,
        data: Any | None = None,
    ) -> Response:
        """
        Fast JSON response for high-performance scenarios. Skips Pydantic validation.

        .. warning::
            Do not use this with `response_model` or return-type hints, as it bypasses validation.

        :param res: Custom response code and message
        :param data: Payload to include
        :return: A JSON response with code, message, and data
        """
        return MsgSpecJSONResponse({'code': res.code, 'msg': res.msg, 'data': data})


response_base: ResponseBase = ResponseBase()