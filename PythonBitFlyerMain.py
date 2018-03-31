import requests
import pandas as pd


def show_degree_of_progress():
    print(str(loopCount + 1) + " / " + str(countLimit))
    print(("■" * loopCount) + ("□" * (countLimit - loopCount - 1)))


# before id
before_id = 0
# bit data size
count = 500
# loop counter
loopCount = 0
# loop size
countLimit = 20
# request url
domainUrl = "https://api.bitflyer.jp"
executionHistoryUrl = '/v1/getexecutions'
# column array
keys = ["id",
        "side",
        "price",
        "size",
        "exec_date",
        "buy_child_order_acceptance_id",
        "sell_child_order_acceptance_id"]

# init DataFrame
df = pd.DataFrame(columns=keys)

while loopCount < countLimit:
    # request execution history
    requestUrl = domainUrl + executionHistoryUrl
    response = requests.get(requestUrl, params={'count': count,
                                                'before': before_id})
    for index, bitData in enumerate(response.json()):
        for key in keys:
            print(end='')
        else:
            before_id = bitData["id"]

    show_degree_of_progress()

    tmpDf = pd.read_json(response.text)
    df = pd.concat([df, tmpDf])

    loopCount += 1

df.to_csv("bit_data.csv", index=False)