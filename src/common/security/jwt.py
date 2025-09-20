#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import timedelta
from typing import Any
from uuid import uuid4

from fastapi import Depends, Request
from fastapi.security import HTTPBearer
from fastapi.security.utils import get_authorization_scheme_param
from jose import ExpiredSignatureError,JWTError,jwt
from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher
from common.dataclasses import AccessToken, NewToken, RefreshToken, TokenPayload
from common.exception.errors import TokenError
from core.config import settings
# from backend.database.redis import redis_client
from utils.timezone import timezone

# JWT authorizes dependency injection
DependsJwtAuth = Depends(HTTPBearer())

password_hash = PasswordHash((BcryptHasher(),))

def get_hash_password(password: str, salt: bytes | None) -> str:
    """
    Encrypt password using hashing algorithm

    :param password: Password
    :param salt: Salt value
    :return: Hashed password
    """
    return password_hash.hash(password, salt=salt)


def password_verify(plain_password: str, hashed_password: str) -> bool:
    """
    Password verification

    :param plain_password: Password to verify
    :param hashed_password: Hashed password
    :return: Verification result
    """
    return password_hash.verify(plain_password, hashed_password)


def jwt_encode(payload: dict[str, Any]) -> str:
    """
    Generate JWT token
    :param payload: Token payload
    :return: JWT token string
    """
    return jwt.encode(
        payload,
        settings.TOKEN_SECRET_KEY,
        settings.TOKEN_ALGORITHM,
    )


def jwt_decode(token: str) -> TokenPayload:
    """
    Decode JWT token
    :param token: JWT token string
    :return: Decoded token payload
    """
   
    try:
        payload = jwt.decode(token, settings.TOKEN_SECRET_KEY, algorithms=settings.TOKEN_ALGORITHM)
        session_uuid = payload.get('session_uuid') or 'debug'
        user_id = payload.get('sub')
        expire_time = payload.get('exp')

       
        if not user_id:
           
            raise TokenError(msg='Token invalid')
    except ExpiredSignatureError:
        raise TokenError(msg='Token expired')
    except (JWTError, Exception):
        raise TokenError(msg='Token invalid')
    return TokenPayload(id=int(user_id), session_uuid=session_uuid, expire_time=expire_time)


async def create_access_token(user_id: str) -> AccessToken:
    """
    Generate encrypted access token

    :param user_id: User ID
    :return: Access token object
    """
    expire = timezone.now() + timedelta(seconds=settings.TOKEN_EXPIRE_SECONDS)
    session_uuid = str(uuid4())
    access_token = jwt_encode({
        'session_uuid': session_uuid,
        'exp': expire,
        'sub': user_id,
    })

    return AccessToken(access_token=access_token, access_token_expire_time=expire, session_uuid=session_uuid)


async def create_refresh_token(user_id: str) -> RefreshToken:
    """
    Generate encrypted refresh token (only for creating new tokens)

    :param user_id: User ID
    :return: Refresh token object
    """
    expire = timezone.now() + timedelta(seconds=settings.TOKEN_REFRESH_EXPIRE_SECONDS)
    refresh_token = jwt_encode({'exp': expire, 'sub': user_id})

 
    return RefreshToken(refresh_token=refresh_token, refresh_token_expire_time=expire)


async def create_new_token(user_id: str, refresh_token: str, multi_login: bool, **kwargs) -> NewToken:
    """
    Generate new access token using refresh token
    :param user_id: User ID
    :return: New token object
    """

    new_access_token = await create_access_token(user_id)
    return NewToken(
        new_access_token=new_access_token.access_token,
        new_access_token_expire_time=new_access_token.access_token_expire_time,
        session_uuid=new_access_token.session_uuid,
    )




def get_token(request: Request) -> str:
    """
    Extract token from request headers

    :param request: FastAPI request object
    :return: Token string
    """
    authorization = request.headers.get('Authorization')
    scheme, token = get_authorization_scheme_param(authorization)
    if not authorization or scheme.lower() != 'bearer':
        raise TokenError(msg='Token invalid')
    return token


