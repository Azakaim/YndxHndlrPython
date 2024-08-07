from typing import List
from pydantic import BaseModel


class ParamUserDetailsModel(BaseModel):
    kind: str = None
    businessId: int = None
    gradeId: int = None


class ParamCounterReviewsModel(BaseModel):
    kind: str = None
    businessId: int = None


class ParamsForGetReviewsModel(BaseModel):
    kind: str = None
    businessId: int = None
    dtFrom: float = None
    dtTo: float = None
    brandId: List[object] = None
    limit: int = None
    type: str = None


class ParamsForSendResponsesModel(BaseModel):
    kind: str = None
    businessId: int = None
    gradeFixId: int = None
    gradeId: int = None
    text: str = None


class Root(BaseModel):
    params: List[object] = None
    path: str = None

