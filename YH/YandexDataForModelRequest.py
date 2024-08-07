import json
from pydantic import BaseModel
from DataModelForRequest import Root


class YandexDataForModelRequest(BaseModel):
    url: dict = None
    cookies: str = None
    headers: dict = None
    data: Root = None
