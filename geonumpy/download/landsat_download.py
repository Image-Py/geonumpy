import requests, json, re
from bs4 import BeautifulSoup
client = requests.session()

url_index = 'https://espa.cr.usgs.gov/index/'
url_login = 'https://ers.cr.usgs.gov/login/'
url_order = 'https://espa.cr.usgs.gov/ordering/status/'
url_download = 'https://espa.cr.usgs.gov/ordering/order-status/'

def login(username, pwd):
    rst = client.get(url_login)
    cont = rst.content.decode('utf-8')
    loc = cont.index('==')
    token = cont[loc-6:loc+2]
    data = {'username':username,'password':pwd,'csrf_token':token}
    rst = client.post(url_login, data)
    if rst.status_code!=502: print('Error:login')
    
def list_order():
    rst = client.get(url_order)
    cont = rst.content.decode('utf-8')
    p = re.compile('>espa-kongwp@radi.ac.cn-\d+-\d+-\d+<')
    return [i[1:-1] for i in p.findall(cont)]

def list_file(orderid):
    rst = client.get(url_download+orderid)
    cont = rst.content.decode('utf-8')
    patten = re.compile('https://edclpdsftp.*tar.gz')
    return patten.findall(cont)

def download(files):
    for imgurl in files:
        print('downloading', imgurl.split('/')[-1], '...', end='')
        try:
            rst = client.get(imgurl)
            f = open('download/'+imgurl.split('/')[-1], 'wb')
            f.write(rst.content)
            f.close()
            print('ok')
        except: print('failed!')
    print('completed!')
    
if __name__ == '__main__':
    login('weiping_RADI', '123ca#456') # 登录
    orders = list_order() # 列举订单
    files = list_file(orders[0]) # 列举某个订单中的文件
    download(files) # 下载文件
