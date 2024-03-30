import requests, re
from rich import print

user_url = "https://bizzdo.se/sok/avancerad?q=%7B%22filter%22%3A%5B%7B%22companyTrade%22%3A%7B%22type%22%3A%22enum%22%2C%22values%22%3A%5B68310%5D%2C%22includeNoValue%22%3Afalse%7D%7D%5D%7D"
keyword = re.search(r'values%22%3A%5B(.*?)%', user_url).group(1)
print(keyword)

api_request_url = "https://bizzdo.se/api/v1/advancedsearch/results"
first_payload = payload = f"""{{
    "filter": [
        {{
            "companyTrade": {{
                "type": "enum",
                "values": [{keyword}],
                "includeNoValue": false
            }}
        }}
    ],
    "select": ["name"],
    "sort": [
        {{
            "companyTurnover": "desc"
        }}
    ]
}}"""

headers = {
  'session-id': 'DCC16207-D851-4831-834B-3BF3DF558514',
  'z-usage': 'E9100EEA-95E7-4AB7-81FF-169713A8F093',
  'Content-Type': 'text/plain'
}

response = requests.request("POST", api_request_url, headers=headers, data=payload)


def get_total_number_of_results(response_json):
    total_number_of_results = None
    
    metadata = response_json.get('metadata', {})
    if metadata:
        total_number_of_results = metadata.get('totalCount')
    return total_number_of_results

print(f"Total: {get_total_number_of_results(response.json())}")
    
    
