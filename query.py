import json
from datetime import datetime
from prettyconf import config
import requests


all_live_environment = [
    "0ae0c857-0dae-4300-be6e-e492f67bbb35",
    "79522e92-6acf-4cbd-ac00-7c59a76abc05",
    "d7c06d65-c316-4803-a98c-ac789c3e0aef",
    "4a6fcade-8d8d-45ad-ab38-2060e34ab3c4",
    "fb4fb0a9-ed27-40e3-a1df-e356ea17137d",
    "f86adbbf-7fca-4289-b997-b2d2dd62eab5",
    "92b76418-0464-4ac3-8e19-313e90a9cd04",
    "17c8778d-36a0-45bd-9566-dcf135682273",
    "61e19c12-d2f8-40e9-8225-5bc225e42642",
    "f9331205-b5cd-4585-95c8-b0abf56df598",
    "e33e86cf-2662-494d-b730-4a0570f71d81",
    "eec6a504-13a5-4e74-a322-573807ed979d",
    "002ea0a8-0ec0-449f-b27a-1097f341a4a6",
    "a21c369d-4e83-4d3f-8131-dbd1bc517be3",
    "0ab6666a-7505-47ff-b89e-911147f4f9e4",
    "db490c08-4dfa-4410-bcf4-f02b29068429",
    "76a34e2d-fdb7-4e6f-bb2b-30a2f5f5a1bb",
    "fcf13173-ed81-3fa7-83d8-6d03581d744f",
    "38afabb8-1399-4d24-b1b8-138c8feb3190",
    "f61765e6-b3a8-4242-8b96-1126cc84bcb9",
    "8cd8a3c1-c435-4e9c-9dcc-8df3377c7b35",
    "f975c409-f4dd-47db-be4b-096949df578a",
    "733ba343-1761-4087-8d5a-5dae16246007",
    "90fd6bdc-1261-4703-a32c-b06aff40d32f",
    "e74e3359-96b8-45eb-aaf9-4060668e598f",
]

all_test_environment = [
    "b98480aa-ea85-431c-a6cf-3f07f7476516",
    "c518d0cd-40a7-4f43-a65e-71891b157e66",
    "a0b9b560-2eb3-4560-ba26-3ee91894032e",
    "9c288471-e451-4081-a135-34d90a022599",
    "e3a40925-1a4a-4e41-ad62-b22cf178f8c1",
    "40ec235e-f1e2-46f2-b0c5-a301b21fb469",
    "2d7cb764-787d-4037-bc99-2276b18c32c0",
    "a1e01969-37a8-4cad-8fd7-9399ba29c032",
    "38485a9b-0a6d-4720-9c64-bcdcc7263432",
    "ee299cbd-de1e-4a23-b7d3-d23820a75269",
    "6c4598c1-5cf8-4f5e-ad34-986e362cd6f1",
    "a697775a-acf7-4f09-b31b-304766e3a3dc",
    "73ed02f6-97b9-41f6-9855-3e3958cf0a74",
    "dda7531b-21a0-48f5-94bd-29700264dd6f",
    "a22898fd-5ffd-4bae-8486-e4fd471104db"]


def get_timestamp(dt):
    dt_obj = datetime.strptime(dt, '%d/%m/%Y %H:%M:%S,%f')
    millisec = int(dt_obj.timestamp() * 1000)
    return millisec


def post_query(statement=None, from_time=None, to_time=None):
    body = {"logs": all_test_environment + all_live_environment,
            "leql": {"during": {"from": ft, "to": tt}, "statement": statement}}
    uri = 'https://rest.logentries.com/query/logs/'
    headers = {'x-api-key': config('LOGENTRIES_API_KEY')}

    response = requests.post(uri, json=body, headers=headers)

    while response.status_code >= 200:
        if 'links' in response.json():
            continue_url = response.json()['links'][0]['href']
            response = requests.get(continue_url, headers={'x-api-key': config('LOGENTRIES_API_KEY')})
        else:
            print(json.dumps(response.json(), indent=4, separators={':', ';'}))
            break


if __name__ == '__main__':
    query = "where(statusCode=400) groupby(name) calculate(count)"
    from_time = get_timestamp("08/02/2018 09:00:00,00")
    to_time = get_timestamp("08/02/2018 09:30:00,00")
    post_query(query, from_time, to_time)
