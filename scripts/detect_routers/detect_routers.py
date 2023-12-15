import requests
import json
import random
import os

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
apy_key = os.getenv("FORTA_GRAPHQL_API_KEY")

ALERT_IDS = ["MEV-SANDWICH-BOT-IDENTIFIED"]
CHAIN_ID= [
    1,
    137,
    56,
    43114,
    42161,
    10,
    250
  ]

forta_api = "https://api.forta.network/graphql"
headers = {"content-type": "application/json", "Authorization": f"Bearer {apy_key}"}

# start and end date needs to be in the format: YYYY-MM-DD
START_DATE = "2023-12-01"
END_DATE = "2023-12-13"
ALERT_COUNT_LIMIT = 800

query = """
query exampleQuery($input: AlertsInput) {
  alerts(input: $input) {
    alerts {
      name
      protocol
      findingType
      chainId
      source {
        transactionHash
        block {
          number
          chainId
          timestamp
          hash
        }
        bot {
          id
        }
      }
      severity
      metadata
      alertId
      addresses
      description
      hash
    }
    pageInfo {
      hasNextPage
      endCursor {
        blockNumber
        alertId
      }
    }
  }
}
"""


# query = """
# query exampleQuery($input: AlertsInput) {
#   alerts(input: $input) {
#     alerts {
#       hash
#       chainId
#     }
#     pageInfo {
#       hasNextPage
#       endCursor {
#         blockNumber
#         alertId
#       }
#     }
#   }
# }
# """
for alert_id in ALERT_IDS:
  for ci in CHAIN_ID:
    query_variables = {
      "input": {
        "alertId": alert_id,
        "chainId": ci,
        "bots": ["0x5bb675492f3accba1d35e7f59f584b6fae11df919f13223f3056a69dc5686b4b"],
        "blockDateRange": {
          "startDate": START_DATE,
          "endDate": END_DATE
        }
      }
    }

    per_chain_alerts = []
    next_page_exists = True
    address_counter = {}
    c = 0
    while next_page_exists and c < ALERT_COUNT_LIMIT:
        # query Forta API
        payload = dict(query=query, variables=query_variables)
        response = requests.request("POST", forta_api, json=payload, headers=headers)

        # collect alerts
        data = response.json()['data']['alerts']
        alerts = data['alerts']
        for a in alerts:
          c += 1
          sandwitcher = a['metadata']['sandwicherAddress']
          if sandwitcher in address_counter:
             address_counter[sandwitcher] = address_counter[sandwitcher] + 1
          else:
             address_counter[sandwitcher] = 1

        # get next page of alerts if it exists
        next_page_exists = data['pageInfo']['hasNextPage']
        # endCursor contains alert Id and block number.
        # This is needed to get the next page of alerts.
        end_cursor = data['pageInfo']['endCursor']
        query_variables['input']['after'] = end_cursor
    sorted_address_counter_desc = sorted(address_counter.items(), key=lambda x: x[1], reverse=True)
    print (f"===={ci}====")
    for i in sorted_address_counter_desc:
        if i[1] > 10:
            print(f"{i[0]},{i[1]}")
