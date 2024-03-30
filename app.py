import requests, re, time, json
from rich import print
from bs4 import BeautifulSoup

user_url = "https://bizzdo.se/sok/avancerad?q=%7B%22filter%22%3A%5B%7B%22companyTrade%22%3A%7B%22type%22%3A%22enum%22%2C%22values%22%3A%5B68310%5D%2C%22includeNoValue%22%3Afalse%7D%7D%5D%7D"
keyword = re.search(r'values%22%3A%5B(.*?)%', user_url).group(1)
print(keyword)

def get_total_number_of_results(keyword):
    api_request_url = "https://bizzdo.se/api/v1/advancedsearch/results"
    payload = f"""{{
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

    total_number_of_results = None
    
    metadata = response.json().get('metadata', {})
    if metadata:
        total_number_of_results = metadata.get('totalCount')
    return total_number_of_results

print(f"Total: {get_total_number_of_results(keyword)}")

def get_n_results(keyword, max_retries=3, delay=1):
    api_request_url = f"https://bizzdo.se/api/v1/advancedsearch/results?page=0&pageSize=20"
    payload = f"""{{
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
    'accept': 'application/json, text/plain, */*',
    'content-type': 'application/json',
    'cookie': 'cookieSettings={%22all%22:true}; _gcl_au=1.1.488212520.1711796805; _ga=GA1.1.2080007861.1711796805; __hstc=125493397.c3c6e74923e083f5e4b6072c48045e25.1711796805756.1711796805756.1711796805756.1; hubspotutk=c3c6e74923e083f5e4b6072c48045e25; __hssrc=1; messagesUtk=0f71833bc19648d7ad1e4af0e34b7088; selectedUserAccount-331F56AF-431F-4B60-AB8D-1D6BFCA5C5E5=331F56AF-431F-4B60-AB8D-1D6BFCA5C5E5; _ga_PN6WGYW5L4=GS1.1.1711796804.1.1.1711800147.0.0.679970764; __hssc=125493397.12.1711796805756; __hssc=125493397.11.1711796805756; __hssrc=1; __hstc=125493397.c3c6e74923e083f5e4b6072c48045e25.1711796805756.1711796805756.1711796805756.1; _ga=GA1.1.2080007861.1711796805; _ga_PN6WGYW5L4=GS1.1.1711796804.1.1.1711800045.0.0.679970764; _gcl_au=1.1.488212520.1711796805; cookieSettings={%22all%22:true}; hubspotutk=c3c6e74923e083f5e4b6072c48045e25; messagesUtk=0f71833bc19648d7ad1e4af0e34b7088; selectedUserAccount-331F56AF-431F-4B60-AB8D-1D6BFCA5C5E5=331F56AF-431F-4B60-AB8D-1D6BFCA5C5E5',
    'session-id': 'E498D44F-9B86-4645-9CD6-CF049DBE9781',
    'z-usage': 'E9100EEA-95E7-4AB7-81FF-169713A8F093'
    }

    # response = requests.request("POST", api_request_url, headers=headers, data=payload)

    # print(response.text)
    results = None
    for attempt in range(max_retries):
        try:
            response = requests.request("POST", api_request_url, headers=headers, data=payload)
            if response.status_code == 200:
                results = response.json().get('rows', [])
                return results
            else:
                    print(f"Received status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
        
        time.sleep(delay)

# results = get_n_results(keyword)
# print(type(results))
# print(len(results))
    
url = "https://bizzdo.se/foretag/5567405666/Catella-Corporate-Finance-Malm%C3%B6-AB"
response = requests.get(url)
html_content = response.text
print(html_content)
soup = BeautifulSoup(html_content, 'html.parser')
span_elements = soup.find_all('span', class_='CardBody__figure')

print(span_elements)