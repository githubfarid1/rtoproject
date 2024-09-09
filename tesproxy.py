import requests
cookies = {
    'ASP.NET_SessionId': 'g5dtvcqhwu3o4inpyljxwafh',
    '__utma': '185625580.1980569484.1724803747.1724803747.1724803747.1',
    '__utmc': '185625580',
    '__utmz': '185625580.1724803747.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    'ifShowHistory': 'false',
    '_ga': 'GA1.1.1812385217.1724803747',
    'TgaSearchOption': 'Rto',
    'Search_Index_gridRtoSearchResults': '100',
    '.ASPXANONYMOUS': 'sntAZy4sGa0wA4GDMfj8bLLkdG73yUKpNnmnhid2RybMkrgSiedit359aWVAkkb0FKTl5lrFyyyyWtaTSHsT_RzZRdQHm6qHCsKbjeNzCjyK4FVScEHWe8mov1zm7WXW_GbBW9NcU-CHQv2ovzf99A2',
    '_ga_87JLQNND29': 'GS1.1.1724810369.2.1.1724811946.0.0.0',
}

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,id;q=0.8',
    # 'content-length': '0',
    'content-type': 'application/x-www-form-urlencoded',
    # 'cookie': 'ASP.NET_SessionId=g5dtvcqhwu3o4inpyljxwafh; __utma=185625580.1980569484.1724803747.1724803747.1724803747.1; __utmc=185625580; __utmz=185625580.1724803747.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); ifShowHistory=false; _ga=GA1.1.1812385217.1724803747; TgaSearchOption=Rto; Search_Index_gridRtoSearchResults=100; .ASPXANONYMOUS=sntAZy4sGa0wA4GDMfj8bLLkdG73yUKpNnmnhid2RybMkrgSiedit359aWVAkkb0FKTl5lrFyyyyWtaTSHsT_RzZRdQHm6qHCsKbjeNzCjyK4FVScEHWe8mov1zm7WXW_GbBW9NcU-CHQv2ovzf99A2; _ga_87JLQNND29=GS1.1.1724810369.2.1.1724811946.0.0.0',
    'origin': 'https://training.gov.au',
    'priority': 'u=1, i',
    'referer': 'https://training.gov.au/Search?searchTitleOrCode=&SearchType=Rto&searchTgaSubmit=Search',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0',
    'x-requested-with': 'XMLHttpRequest',
}

params = {
    'searchTitleOrCode': '',
    'SearchType': 'Rto',
    'searchTgaSubmit': 'Search',
}

username = 'sp90lzhoej'
password = '2vQ_jk6cpTF98ujLyj'
proxy = f"http://{username}:{password}@gate.smartproxy.com:10016"
proxy = "http://sp90lzhoej:2vQ_jk6cpTF98ujLyj@gate.smartproxy.com:7000"
proxies = {
    'http': proxy,
    'https': proxy
}
proxies = {
  "http": "http://scrapeops:c58f3885-5149-4c03-8a3a-1b2d3ffba3c6@residential-proxy.scrapeops.io:8181",
  "https": "http://scrapeops:c58f3885-5149-4c03-8a3a-1b2d3ffba3c6@residential-proxy.scrapeops.io:8181"
}
response = requests.get(
    'https://training.gov.au/Search/AjaxOrganisationSearchFiltersCount',
    # params=params,
    # cookies=cookies,
    # headers=headers
    proxies=proxies
)
print(response.text)