import requests, json, time
from bs4 import BeautifulSoup
client = requests.session()

url_rc = 'https://earthexplorer.usgs.gov/ajax/wrstolatlng?path=%.3d&row=%.3d&type=WRS2&wrsType=Point'
url_set = 'https://earthexplorer.usgs.gov/tabs/save'
url_index = 'https://earthexplorer.usgs.gov/result/index'

data_set_date = '''
    {"tab":1,"destination":2,"coordinates":[
    {"c":"0","a":%.4f,"o":%.4f}],
    "format":"dms","dStart":"%s","dEnd":"%s",
    "searchType":"Std","num":"1000",
    "includeUnknownCC":"1","maxCC":100,"minCC":0,
    "months":%s,"pType":"polygon"}'''

data_set_L8 = '''
    {"tab":3,"destination":4,"criteria":{"12864":{
    "select_20522_5":["%s"],"select_20515_5":["%s"],
    "select_20510_4":[""],"select_20517_4":[""],
    "select_20518_4":[""],"select_20513_3":[""],
    "select_20519_3":[""]}},"selected":"12864"}'''

data_set_L7 = '''
    {"tab":3,"destination":4,"criteria":{"12267":{
    "select_19893_5":["%s"],"select_19883_5":["%s"],
    "select_19890_3":[""],"select_19886_4":[""],
    "select_19892_3":[""],"select_19885_3":[""]}},"selected":"12267"}'''

data_set_L45 = '''
    {"tab":3,"destination":4,"criteria":{"12266":{
    "select_19881_5":["%s"],"select_19874_5":["%s"],
    "select_19880_3":[""],"select_19876_4":[""],
    "select_19877_3":[""],"select_25173_3":[""],
    "select_19875_3":[""]}},"selected":"12266"}'''

def get_latlon_byrc(path, row):
    rst = client.get(url_rc%(path, row))
    return rst.json()['coordinates'][0]

def set_rc_date(coord, start, end, month=None):
    if month is None: month = ['']+list(range(12))
    month = json.dumps(["%s"%i for i in month])
    data = data_set_date%(coord[0], coord[1], start, end, month)
    data = data.replace(' ', '').replace('\n', '')
    rst = client.post(url_set, {'data':data})
    if rst.content != b'1': print('Error:set rc data')

def set_criterial(product, landcloud='', scenecloud=''):
    datastr = {8:data_set_L8, 7:data_set_L7, 45:data_set_L45}[product]
    data = datastr%(landcloud, scenecloud)
    data = data.replace(' ', '').replace('\n', '')
    rst = client.post(url_set, {'data':data})
    if rst.content != b'1': print('Error:set criterial data')

def get_content(product, page):
    cid = {7:12267, 8:12864, 45:12266}[product]
    rst = client.post(url_index, {'collectionId':cid, 'pageNum':page})
    return rst.content.decode('utf-8')

def parse_record(cont):
    soup = BeautifulSoup(cont, 'html.parser')
    records = soup.findAll(attrs={'class':'metadata', 'data-url':True})
    return [i.text for i in records[1::3]]

def search(product, prs, start, end, month=None, lcloud='', scloud='', page=1):
    records = []
    for path, row in prs:
        client.cookies.clear()
        print('searching %.3d %.3d, ...'%(path, row))
        coord = get_latlon_byrc(path, row)
        set_rc_date(coord, start, end, month)
        set_criterial(product, lcloud, scloud)
        for i in range(page):
            cont = get_content(product, i+1)
            rds = parse_record(cont)
            print(len(rds))
            records.extend(rds)
            if len(rds)<10: break
    return records

def to_order(records):
    f = open('order.txt', 'w')
    f.write('\n'.join(records))
    f.close()

# 这里输入需要下载的行列号
blocks = [(123,43), (119,37), (122,37)]

if __name__ == '__main__':
    # 等级（7，8），行列号，起始，结束日期，月份限定，陆地云量，传感器云量，页数
    records = search(7, blocks, '06/30/2018', '07/30/2019', None, 10, 10, 1)
    for i in records: print(i) # 打印
    #to_order(records) # 存储为订单文件

