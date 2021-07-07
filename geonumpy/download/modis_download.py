import urllib.request as request
import os, datetime, json

url = 'https://ladsweb.modaps.eosdis.nasa.gov/archive/allData'

def get_lev_pro_year(level, product, year):
    ref = url + '/%s/%s/%s.json'%(level, product, year)
    req = request.Request(ref)
    response = request.urlopen(req)
    return json.loads(response.read().decode('utf-8'))

def get_list(level, product, year, day):
    ref = url + '/%s/%s/%s/%s.json'%(level, product, year, day)
    req = request.Request(ref)
    response = request.urlopen(req)
    return json.loads(response.read().decode('utf-8'))

def get_all(level, product, areas, year, days = (0,365)):
    print('searching... %s level %s %s'%(product, level, year))
    if isinstance(days, list): days = ['%.3d'%i for i in days]
    else:
        buf = [i['name'] for i in get_lev_pro_year(level, product, year)]
        days = [i for i in buf if int(i)>=days[0] and int(i)<=days[1]]
    files = []
    for day in days:
        print('\t%s day ...'%day, end=' ')
        lst = [i['name'] for i in get_list(level, product, year, day)]
        files.extend([(level, product, year, day), i] for i in lst)
        print('done')
    print()
    files = [i for i in files if sum([a in i[1] for a in areas])]
    return files

def download_one(pre, name, des):
    ref = url + '/%s/%s/%s/%s/%s'%(pre+(name,))
    req = request.Request(ref)
    response = request.urlopen(req)
    html = response.read()
    f = open('%s/%s'%(des,name), 'wb')
    f.write(html)
    f.close()

def search(product, level, areas, terms):
    files = []
    for pro in product:
        for year, days in terms:
            files.extend(get_all(level, pro, areas, year, days))
    print('%s new files found!'%len(files))
    return files

def download(files, des):
    succ = 0
    for pre, name in files:
        try:
            print('\t', name, end=' ... ')
            download_one(pre, name, des)
            print('done')
            succ += 1
        except:
            print('failed!')
    print('download completed, succ %s，failed %s'%(succ, len(files)-succ))


    
if __name__ == '__main__':
    files = search(['MOD09Q1', 'MOD11A2'], level=6, areas=['h25v05', 'h27v05', 'h28v05'], terms=[(2019, (0,30))])
    download(files, '')
