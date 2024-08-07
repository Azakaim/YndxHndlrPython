import json
from environs import Env
from FabricResponder import FabricResponder
from SpintaxGenerator import SpintaxGen
from YandexHandler import YandexHandler

env = Env()
env.read_env()

headers = json.loads(env('HEADERS'))
url = json.loads(env('URL'))
business_id = [78039885, 4006213]
campaignId = [67825273, 2338356]
responses = json.loads(env('RESPONSES'))
fabric_responder = FabricResponder()
spintax = SpintaxGen()

for y in range(2):
    print(business_id[y])
    print(campaignId[y])
    ya = YandexHandler(business_id[y], campaignId[y], headers, url, fabric_responder, spintax, responses)

    count_reviews = ya.exact_quantity_reviews()

    print(count_reviews)
    #
    # if count_reviews == 0:
    #     exit()

    first_count = count_reviews % 50

    part_1 = ya.get_reviews_id(first_count)

    for grade_id in part_1:
        print(ya.send_response(grade_id))
    print("part_1 done")

    count_reviews -= first_count

    for i in range(50, count_reviews + 50, 50):
        part_2 = ya.get_reviews_id(50)
        for grade_id in part_2:
            print(ya.send_response(grade_id))
    print("part_2 done")

