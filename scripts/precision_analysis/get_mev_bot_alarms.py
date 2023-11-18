import requests
import json
import random

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


ALERT_IDS = ["MEV-ARBITRAGE-BOT-IDENTIFIED", "MEV-SANDWICH-BOT-IDENTIFIED", "MEV-LIQUIDATION-BOT-IDENTIFIED"]
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
START_DATE = "2023-11-10"
END_DATE = "2023-11-15"
ALERT_COUNT_LIMIT = 100

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


query = """
query exampleQuery($input: AlertsInput) {
  alerts(input: $input) {
    alerts {
      hash
      chainId
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
for alert_id in ALERT_IDS:
  all_alerts = []
  sample = []
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

    while next_page_exists and len(per_chain_alerts) < ALERT_COUNT_LIMIT:
        # query Forta API
        payload = dict(query=query, variables=query_variables)
        response = requests.request("POST", forta_api, json=payload, headers=headers)

        # collect alerts
        data = response.json()['data']['alerts']
        alerts = data['alerts']
        for a in alerts:
          per_chain_alerts.append(f"{a['hash']},{ci}")

        # get next page of alerts if it exists
        next_page_exists = data['pageInfo']['hasNextPage']
        # endCursor contains alert Id and block number.
        # This is needed to get the next page of alerts.
        end_cursor = data['pageInfo']['endCursor']
        query_variables['input']['after'] = end_cursor
    all_alerts += per_chain_alerts
    sample += random.sample(per_chain_alerts, 4)

  with open(f"{alert_id}_candidates.txt", 'w') as archivo:
      json.dump(all_alerts, archivo)


  with open(f"{alert_id}_sample.txt", 'w') as archivo:
    json.dump(sample, archivo)

  print(f"---{alert_id}---")
  for s in sample:
    print(s)
