import requests
import pandas as pd
from progressbar import ProgressBar


# execute api request
def execute_api_request(url, params):
    request_url = domain_url + url
    return requests.get(request_url, params=params)


# before id
before_id = 0
# bit data size
count = 500
# loop counter
loop_count = 0
# loop size
count_limit = 20
# request url
domain_url = "https://api.bitflyer.jp"
execution_history_url = '/v1/getexecutions'
# column array
keys = ["id",
        "side",
        "price",
        "size",
        "exec_date",
        "buy_child_order_acceptance_id",
        "sell_child_order_acceptance_id"]

# params
execution_history_params = {'count': count,
                            'before': before_id}
# init ProgressBar
p = ProgressBar(loop_count, count_limit)

# init DataFrame
df = pd.DataFrame(columns=keys)

while loop_count < count_limit:
    # request execution history
    response = execute_api_request(execution_history_url, execution_history_params)
    for index, bitData in enumerate(response.json()):
        for key in keys:
            print(end='')
        else:
            before_id = bitData["id"]

    # show execution progress
    p.update(loop_count)

    tmpDf = pd.read_json(response.text)
    df = pd.concat([df, tmpDf])

    loop_count += 1

df.to_csv("bit_data.csv", index=False)
