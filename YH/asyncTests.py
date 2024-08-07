import time
import asyncio
import aiohttp
import json

from datetime import datetime
from pprint import pprint
from dateutil.relativedelta import relativedelta
from environs import Env
from pydantic import BaseModel
from FabricResponder import FabricResponder
from SpintaxGenerator import SpintaxGen


class ParamForGetReviewsDetail(BaseModel):
    kind: str = None
    businessId: int = None
    gradeId: int = None


class ParamForGetReviewsProducts(BaseModel):
    kind: str = None
    businessId: int = None
    dtFrom: int = None
    dtTo: int = None
    brandId: list[object] = None
    pageToken: str = None
    limit: int = None
    type: str = None


class ParamCommentModel(BaseModel):
    platformType: str = None
    campaignId: int = None
    activeTab: str = None
    id: int = None
    shopId: int = None
    page: int = None
    pageSize: int = None
    sortBy: str = None
    sortOrder: str = None
    gradeValue: str = None
    lastComment: str = None
    withClones: str = None
    inShopRegion: str = None
    regionId: str = None
    gradeId: str = None
    reviewsDateFrom: str = None
    reviewsDateTo: str = None
    dateFrom: str = None
    dateTo: str = None
    userId: int = None


class Root(BaseModel):
    params: list[object] = None
    path: str = None


class YandexCommentParam(BaseModel):
    url: dict = None
    headers: dict = None
    data: Root = None


class UserModelUid(BaseModel):
    comment_id: int = None
    uid: int = None
    name: str = None
    comment: str = None
    averageGrade: int = None


def _date_stamp(date_from: int = 0) -> float:
    now = datetime.now() - relativedelta(months=date_from)
    timestamp = time.mktime(now.timetuple()) * 1000
    return timestamp


async def _get_details_review(comment_id: id, business_id: int, headers: dict, url: dict) -> str:
    data_for_review = YandexCommentParam()
    data_for_review.headers = headers
    data_for_review.url = url
    data_for_review.data = Root()
    data_for_review.data.path = "/business/4006213/reviews?campaignId=25705548&tab=ALL&cabinetType=BUSINESS&dtFrom=2024-02-21&dtTo=2024-05-21"
    param = ParamForGetReviewsDetail()
    param.kind = "BUSINESS"
    param.businessId = business_id
    param.gradeId = comment_id
    data_for_review.data.params = []
    data_for_review.data.params.append(param)
    #https://partner.market.yandex.ru/api/resolve/?r=businessReviews/resolveReviewDetails:resolveReviewDetails
    # print(data_for_review.url["resolveReviewDetails"])
    # print(json.dumps(data_for_review.data.dict()))
    async with asyncio.Semaphore(1000):
        async with aiohttp.ClientSession() as session:
            async with session.post(data_for_review.url["resolveReviewDetails"],
                                    json=data_for_review.data.dict(),
                                    headers=data_for_review.headers) as response:
                return await response.text()


async def get_comments_products(business_id: int, headers: dict,
                                url: dict, count_reviews: int, page: int = None) -> str:
    ya_data_products = YandexCommentParam()
    ya_data_products.headers = headers
    ya_data_products.url = url
    ya_data_products.data = Root()
    ya_data_products.data.params = []
    ya_data_products.data.path = ""
    param_products = ParamForGetReviewsProducts()
    param_products.kind = "BUSINESS"
    param_products.businessId = business_id
    param_products.dtFrom = int(_date_stamp(3))
    param_products.dtTo = int(_date_stamp())
    param_products.brandId = []
    param_products.limit = count_reviews
    param_products.type = "ALL"
    param_products.pageToken = str(page) if page is not None else None
    ya_data_products.data.params.append(param_products)
    # print(ya_data_products.url["resolveReviews"])
    # print(ya_data_products.data.dict())
    async with aiohttp.ClientSession() as session:
        async with session.post(ya_data_products.url["resolveReviews"],
                                json=ya_data_products.data.dict(),
                                headers=ya_data_products.headers) as response:
            return await response.text()


async def fetch(business_id: int, headers: dict, url: dict) -> list[str]:
    count = 0
    comments_id = []
    coroutines = []
    _next_page_token = None
    while True:
        if _next_page_token:
            coroutines.append(get_comments_products(business_id, headers, url, 20, _next_page_token))
        else:
            coroutines.append(get_comments_products(business_id, headers, url, 20))
        print(data)
        _data = json.loads(data)
        _next_page_token = _data['results'][0]['data']["grades"].get('nextPageToken', None)
        comments_id.extend(_data['results'][0]['data']['grades']['data'].get('result', []))
        if not _next_page_token:
            break
        count += 1
    return comments_id


async def _get_result_from_info_comments(data: str):
    _data = json.loads(data)
    _next_page_token = _data['results'][0]['data']["grades"].get('nextPageToken', None)
    comments_id = _data['results'][0]['data']['grades']['data'].get('result', [])
    return _next_page_token, comments_id


async def main():
    list_comments_id = await fetch(_business_id, _headers, _url)
    print(list_comments_id)
    print(list_comments_id.__len__())
    print("i'm done")
    for item in list_comments_id:
        user_model = []
        data = json.loads(await _get_details_review(item, _business_id, _headers, _url))
        # print(data)
        need_reaction = data['results'][0]['data']['extraInfo']['needReaction']
        users = data['results'][0]['data']['thread']['authors']
        if need_reaction:
            _grade = data['results'][0]['data']['grade']
            _uid = _grade['user'].get('uid')
            _averageGrade = _grade.get('averageGrade', 0)
            _comment = _grade.get('comment', '')
            _name = users[str(_uid)].get('publicName', '')
            user_model.append(UserModelUid(uid=_uid,
                                           averageGrade=_averageGrade,
                                           comment=_comment,
                                           comment_id=item,
                                           name=_name))
        else:
            print('No need reaction')
        pprint(user_model)


if __name__ == '__main__':
    env = Env()
    env.read_env()

    _headers = json.loads(env('HEADERS'))
    _url = json.loads(env('URL'))
    user_id = 1017728281
    _business_id = 4006213
    campaign_id1 = 2338356
    campaign_id2 = 25705548
    cabinet_id = [10791548, 4006217]
    responses = json.loads(env('RESPONSES'))
    fabric_responder = FabricResponder()
    spintax = SpintaxGen()
    list_data_rev = []

    asyncio.run(main())
