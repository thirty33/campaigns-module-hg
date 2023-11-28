from fastapi.security import HTTPBearer
from pydantic import BaseModel, Field, validator
from typing import Any, Coroutine, Optional, List
from lambdas.transaction.helpers.jwt.jwt_manager import create_token, validate_token
from fastapi import FastAPI, Body, HTTPException, Path, Query, Depends, Request
import re
from datetime import datetime

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != 'admin@gmail.com':
            raise HTTPException(status_code=403, detail='Invalid Credentials')


class User(BaseModel):
    email: str
    password: str


class Movie(BaseModel):
    id: Optional[int]
    # title: str = Field(default="Movie title",min_length=5,max_length=15)
    title: str = Field(min_length=5, max_length=15)
    # overview: str = Field(default="Movie description",min_length=15,max_length=50)
    overview: str = Field(min_length=15, max_length=50)
    # year: int = Field(default=2022, le=2022)
    year: int = Field(le=2022)
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_length=1, max_length=15)

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Movie title",
                "overview": "Movie description",
                "year": 2022,
                "rating": 9.8,
                "category": "Acción"
            }
        }

class Transaction(BaseModel):
    Title: Optional[str] = Field(min_length=5, max_length=15)
    Category: Optional[str] = Field(min_length=1, max_length=10)
    Bank: Optional[str] = Field(min_length=1, max_length=10)
    DateTransaction: Optional[str] = Field(min_length=5, max_length=100)
    Description: Optional[str] = Field(min_length=5, max_length=255)
    nombreApellido: Optional[str]
    email: Optional[str]
    genero: Optional[str]
    numeroTelefonico: Optional[str]
    ciudadOrigen: Optional[str]
    ciudadDestino: Optional[str]
    tipoViaje: Optional[str]
    fechaSalida: datetime
    fechaRegreso: datetime
    recibirCotizacion: Optional[str]

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            Any: lambda v: str(v)
        }
        json_schema_extra = {
            "example": {
                "Title": "quote",
                "Category": "1",
                "Bank": "1",
                "DateTransaction": '2023-01-01 10:30:50',
                "Description": "Description",
                "nombreApellido": "dasd",
                "email": "test@test.com",
                "genero": "masculino",
                "numeroTelefonico": "213123122",
                "ciudadOrigen": "dsads",
                "ciudadDestino": "dasdsa",
                "tipoViaje": "Viaje de ida",
                "fechaSalida": "2023-01-01 10:30:50",
                "fechaRegreso": "2023-02-27 20:30:50",
                "recibirCotizacion": "WhatsApp",
            }
        }
        
class LoginRequest(BaseModel):
    email: str = Field(default="joell@test.co",min_length=5, max_length=20)
    password: str = Field(default="k2m=@[7C!sQX",min_length=4, max_length=100)
    class Config:
        json_schema_extra = {
            "example": {
                "email": "joell@test.co",
                "password": "k2m=@[7C!sQX",
            }
        }

    @validator('email')
    def validate_email(cls, email):
        if not re.match(r'^[\w\.-]+@[\w\.-]+$', email):
            raise ValueError('Invalid email address')
        return email
    
class User(BaseModel):
    email: str = Field(min_length=5, max_length=15)
    uid: str = Field(min_length=4, max_length=255)
    class Config:
        json_schema_extra = {
            "example": {
                "email": "joel@test.co",
                "uid": "111111111111",
            }
        }

class ParamsModel(BaseModel):
    Title: Optional[str] = 'quote'
    Category: Optional[str] = '1'
    Bank: Optional[str] = None
    DateTransaction: Optional[str] = None
    Description: Optional[str] = None
    nombreApellido: Optional[str] = None
    email: Optional[str] = None
    genero: Optional[str] = None
    numeroTelefonico: Optional[str] = None
    ciudadOrigen: Optional[str] = None
    ciudadDestino: Optional[str] = None
    tipoViaje: Optional[str] = None
    fechaSalida: Optional[str] = None
    fechaRegreso: Optional[str] = None
    recibirCotizacion: Optional[str] = None
    page: Optional[str] = '1'
    token: Optional[str] = 'eyJraWQiOiJ0OFdqUTRreW1YTjZpcGRCRmpucWRZemZwQXM2bndWRFZwd3FaT3A2YzMwPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiI4ODcwYWZjMC0xNjE0LTRiOWUtOTU3ZC01MDc3NDk2MjIyZTUiLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtd2VzdC0yLmFtYXpvbmF3cy5jb21cL3VzLXdlc3QtMl9IeVhBc2N4NGkiLCJjbGllbnRfaWQiOiI3NDRwdW90b29jYzh2bnQ0bGQ0aGdpc2drZyIsIm9yaWdpbl9qdGkiOiI1YTZkODFkOS00YTljLTRkOGMtYWQ3OS05NDEyNmMyZWFiYzIiLCJldmVudF9pZCI6IjFlMGQyOGZkLTM1MjMtNGQ5OS04MjY5LWI0MDJiZjk3ZjMxZiIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4iLCJhdXRoX3RpbWUiOjE3MDAzMTY0OTksImV4cCI6MTcwMDMzNDQ5OSwiaWF0IjoxNzAwMzE2NDk5LCJqdGkiOiI4M2JlZGU3MC1lOWNjLTQ0ZDUtODg3NC00OTJiOGE4YzkzMzMiLCJ1c2VybmFtZSI6ImpvZWxsQHRlc3QuY28ifQ.bSDmxwC7cofzlyege4fSto0QWP0vCYsy6nVBCtrLzTQLypYii_FWpbyUUe7wgMDPKTTQue23K49nJyhID3LC92ubNLAMpdIhZFNKIzqgwUGKAVjwH6XZ5K_C7GxGGO4TY0n1YQNHJ_UncTybUAoAArk219JaDfyOicTQEn4WUySy1OqPBw7oauruKLZspbAhtee9NVUUdshzwsEiM0cO0NDUVlTsw1yUghhxfqLIIW2vjxG2tJND-pFcJbokjPMawk5-avpVECaIUW_v_KtO_nLp6vxwjHvuM53ON0OZPGWyTvnuGaeDK8qygdBUoWS1oEO7GzJDh9MebLL9vLz0-A'
    Uid: Optional[str] = ''


