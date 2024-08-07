import json
import time
import requests

from datetime import datetime
from dateutil.relativedelta import relativedelta
from requests import Response

from DataModelForRequest import Root, ParamCounterReviewsModel, ParamsForGetReviewsModel, ParamsForSendResponsesModel, \
    ParamUserDetailsModel
from Interfaces import IFabricResponder, TypeResponder
from SpintaxGenerator import ISpintaxGen
from YandexDataForModelRequest import YandexDataForModelRequest


class YandexHandler:
    headers: dict
    url: dict
    responses: dict

    def __init__(self, business_id: int, campaign_id: int, headers: dict, url: dict, responder: IFabricResponder,
                 spintax: ISpintaxGen, responses: dict):
        self.business_id = business_id
        self.campaign_id = campaign_id
        self.headers = headers
        self.url = url
        self.responses = responses
        self.pattern_responder = responder.get_responder_instance(TypeResponder.PATTERN)
        self.pattern_responder.responses_5_star = responses.get('star_5')
        self.pattern_responder.responses_4_star = responses.get('star_4')
        self.pattern_responder.responses_4bad_rev = responses.get('bad_reviews')
        self.pattern_responder.spin = spintax
        self.gpt_responder = responder.get_responder_instance(TypeResponder.GPT)

    def _reviews_quantity_data(self) -> str:
        ya_data_reviews_counter = YandexDataForModelRequest()
        ya_data_reviews_counter.headers = self.headers
        ya_data_reviews_counter.url = self.url
        ya_data_reviews_counter.data = Root()
        ya_data_reviews_counter.data.params = []
        ya_data_reviews_counter.data.path = f"/business/{self.business_id}/reviews?campaignId={self.campaign_id}"
        param_counter = ParamCounterReviewsModel()
        param_counter.kind = "BUSINESS"
        param_counter.businessId = self.business_id
        ya_data_reviews_counter.data.params.append(param_counter)
        request = requests.post(ya_data_reviews_counter.url["resolveNeedReactionCounter"],
                                data=json.dumps(ya_data_reviews_counter.data.dict()),
                                headers=ya_data_reviews_counter.headers)
        return request.text

    def exact_quantity_reviews(self) -> int:
        request_text = self._reviews_quantity_data()
        try:
            quantity = json.loads(request_text)['results'][0]['data']['count']
        except KeyError as e:
            quantity = 0
        return quantity

    def _get_reviews_info(self, **kwargs) -> str:
        ya_data_for_reviews = YandexDataForModelRequest()
        ya_data_for_reviews.headers = self.headers
        ya_data_for_reviews.url = self.url
        ya_data_for_reviews.data = Root()
        ya_data_for_reviews.data.params = []
        ya_data_for_reviews.data.path = f"/business/{self.business_id}/reviews?campaignId={self.campaign_id}"
        param = ParamsForGetReviewsModel()
        param.kind = "BUSINESS"
        param.businessId = self.business_id
        param.dtFrom = self._date_stamp(3)
        param.dtTo = self._date_stamp()
        param.brandId = []
        param.limit = kwargs.get('limit_reviews')
        param.type = "NEED_REACTION"
        ya_data_for_reviews.data.params.append(param)
        request = requests.post(ya_data_for_reviews.url["resolveReviews"], data=json.dumps
                                (ya_data_for_reviews.data.model_dump()),
                                headers=ya_data_for_reviews.headers)
        return request.text

    def get_reviews_id(self, limit_reviews: int) -> list[int]:
        result = self._get_reviews_info(limit_reviews=limit_reviews)
        try:
            reviews_id = json.loads(result)['results'][0]['data']['grades']['data']['result']
        except KeyError as e:
            print("KeyError: ", e)
            reviews_id = []
        return reviews_id

    def send_response(self, grade_id: int):
        ya_data_response = YandexDataForModelRequest()
        ya_data_response.headers = self.headers
        ya_data_response.url = self.url
        ya_data_response.data = Root()
        ya_data_response.data.params = []
        ya_data_response.data.path = f"/business/{self.business_id}/reviews?campaignId={self.campaign_id}"
        param_response = ParamsForSendResponsesModel()
        param_response.kind = "BUSINESS"
        param_response.businessId = self.business_id
        param_response.gradeFixId = grade_id
        param_response.gradeId = grade_id

        request_text = self._get_user_details(grade_id=grade_id)

        name_client = self._get_user_name(request_text)
        grade = self._get_grade_reviews(request_text)
        request = Response()
        if grade > 2:
            param_response.text = self.pattern_responder.response(name_client=name_client, grade=grade)
            ya_data_response.data.params.append(param_response)
            request = requests.post(ya_data_response.url["resolvePostComment"],
                                    data=json.dumps(ya_data_response.data.dict()),
                                    headers=ya_data_response.headers)
        return request.text

    def _get_user_details(self, **kwargs):
        ya_data_user_details = YandexDataForModelRequest()
        ya_data_user_details.headers = self.headers
        ya_data_user_details.url = self.url
        ya_data_user_details.data = Root()
        ya_data_user_details.data.params = []
        ya_data_user_details.data.path = (f"/business/{self.business_id}/reviews?campaignId={self.campaign_id}"
                                          f"&tab=WAITING_FOR_REACTION&cabinetType=BUSINESS")
        param_user_details = ParamUserDetailsModel()
        param_user_details.kind = "BUSINESS"
        param_user_details.businessId = self.business_id
        param_user_details.gradeId = kwargs.get('grade_id')
        ya_data_user_details.data.params.append(param_user_details)
        request = requests.post(ya_data_user_details.url["resolveReviewDetails"],
                                data=json.dumps(ya_data_user_details.data.dict()),
                                headers=ya_data_user_details.headers)
        try:
            result = json.loads(request.text)['results'][0]['data']
        except KeyError as e:
            result = {}
        return result

    def _get_user_name(self, request_text: dict) -> str:
        try:
            data = request_text['thread']['authors']
            user_name = {'author_name': info['publicName'] if 'publicName' in info else "" for autor_name, info in
                         data.items()}
        except KeyError as e:
            user_name = {'author_name': "ERORR"}
        return user_name['author_name']

    def _get_grade_reviews(self, request_text: dict) -> int:
        try:
            grade = request_text['grade']['averageGrade']
        except KeyError as e:
            grade = 0
        return grade

    def _get_comment_reviews(self, request_text: dict) -> str:
        try:
            comment = request_text['grade']['comment']
        except KeyError as e:
            comment = ""
        return comment

    def _date_stamp(self, date_from: int = 0) -> float:
        now = datetime.now() - relativedelta(months=date_from)
        timestamp = time.mktime(now.timetuple()) * 1000
        return timestamp
