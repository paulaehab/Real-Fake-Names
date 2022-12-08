from fastapi import APIRouter
from models import get_name
from typing import  Text



userRoutes = APIRouter()



@userRoutes.get('/getName')
def getName(name:str):
    text=name.split("*")
    return get_name(text)

        

