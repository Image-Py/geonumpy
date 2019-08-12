import geonumpy.download as gdl

def modis_test():
    imgs = gdl.modis_search(['MOD09Q1', 'MOD11A2'],
                            level=6,
                            areas=['h25v05', 'h27v05', 'h28v05'],
                            terms=[(2019, (0,30))])

    gdl.download(imgs, './download/')

def landsat_test():
    blocks = [(123,43), (119,37), (122,37)]
    # 等级（7，8），行列号，起始，结束日期，月份限定，陆地云量，传感器云量，页数
    records = gdl.landsat_search(7, blocks, '06/30/2018', '07/30/2019', None, 10, 10, 1)
    for i in records: print(i) # 打印
