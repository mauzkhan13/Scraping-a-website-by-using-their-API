import pandas as pd
import requests
import sys, os
import os
import time
import random

application_path = os.path.dirname(sys.executable)

list1 = []
l_eng = []
kindred = []
kindred_factor = []

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9,de;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json;charset=UTF-8',
    'Origin': 'https://tmsearch.ipthailand.go.th',
    'Pragma': 'no-cache',
    'Referer': 'https://tmsearch.ipthailand.go.th/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

json_data = {
    'filter': '',
    'nowPage': 1,
    'perPage':20,
    'sortProduct': 'order by 1 asc',
}

response = requests.post('https://tmsearch.ipthailand.go.th/api/v2/product', headers=headers, json=json_data)

result_json = response.json()

result_items = result_json['data']

start_time = time.time()

total_items = len(result_items)
for i, result in enumerate(result_items):
    progress = (i + 1) / total_items * 100
    sys.stdout.write('\r')
    sys.stdout.write("[%-100s] %.2f%%" % ('='*int(progress), progress))
    sys.stdout.flush()

    list1.append(result['list_name'])
    l_eng.append(result['list_eng'])
    kindred.append(result['cate_ID'])

    kindred_f = result.get('eu')
    kindred_fa = result.get('madrid')

    if kindred_f == 'Y' and kindred_fa == 'Y':
        kindred_factor.append('NCL,MGS')
    elif kindred_f == 'Y':
        kindred_factor.append('NCL')
    elif kindred_fa == 'Y':
        kindred_factor.append('MGS')
    else:
        kindred_factor.append('N/A')

    # delay_time = random.uniform(0.5 , 1)
    # time.sleep(delay_time)
# Print 100% progress after the loop completes
sys.stdout.write('\r')
sys.stdout.write("[%-100s] %.2f%%\n" % ('='*100, 100.0))
sys.stdout.flush()

end_time = time.time()
time_taken = end_time - start_time
print(f"Time taken: {time_taken:.2f} seconds")

 
df = pd.DataFrame({'รายการ': list1 , 'รายการภาษาอังกฤษ' : l_eng,  'จำพวก': kindred, 'จำพวก Factor (MGS or NCL or N/A)': kindred_factor} )
print(df)
# df.to_excel("output20.xlsx", index=False)
