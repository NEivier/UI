def get_city_code(city_pinyin):
    city_codes = {'beijing': '010100',  # 北京
                  'shanghai': '020100',  # 上海
                  'guangzhou': '280101',  # 广州
                  'shenzhen': '280601',  # 深圳
                  'chengdu': '270101',  # 成都
                  'hangzhou': '210101',  # 杭州
                  'wuhan': '200101',  # 武汉
                  'xian': '110101',  # 西安
                  'nanjing': '190101',  # 南京
                  'chongqing': '040100',  # 重庆
                  'tianjin': '030100',  # 天津
                  'changsha': '250101',  # 长沙
                  'fuzhou': '230101',  # 福州
                  'nanning': '300101',  # 南宁
                  'lanzhou': '160101',  # 兰州
                  'xining': '150101',  # 西宁
                  'shenyang': '070101',  # 沈阳
                  'dalian': '070201',  # 大连
                  'qingdao': '120201',  # 青岛
                  'yantai': '120501',  # 烟台
                  'zibo': '120301',  # 淄博
                  'taian': '120801',  # 泰安
                  'xuzhou': '190801',  # 徐州
                  'changzhou': '191101',  # 常州
                  'suzhou': '190401',  # 苏州
                  'shijiazhuang': '090101',  # 石家庄
                  'zhengzhou': '180101',  # 郑州
                  'taiyuan': '100101',  # 太原
                  'wulumuqi': '130101',  # 乌鲁木齐
                  'kunming': '290101',  # 昆明
                  'changchun': '060101',  # 长春
                  'jilin': '060201',  # 吉林
                  'haerbin': '050101',  # 哈尔滨
                  'hefei': '220101',  # 合肥
                  'qiqihaer': '050201',  # 齐齐哈尔
                  'huhehaote': '080101',  # 呼和浩特
                  'mudanjiang': '050301',  # 牡丹江
                  'ningbo': '210401',  # 宁波
                  'wenzhou': '210701',  # 温州
                  'xiamen': '230201',  # 厦门
                  'nanchang': '240101',  # 南昌
                  'langfang': '090601',  # 廊坊
                  'xuancheng': '221401',  # 宣城
                  'hengyang': '250401',  # 衡阳
                  'yueyang': '251001',  # 岳阳
                  'guiyang': '260101',  # 贵阳
                  'kunshan': '190404',  # 昆山
                  'hanzhong': '110701',  # 汉中
                  'yichang': '200901',  # 宜昌
                  'zhenjiang': '190301',  # 镇江
                  'huaian': '190901',  # 淮安
                  'wuhu': '220301',  # 芜湖
                  'baotou': '080201',  # 包头
                  'jinzhou': '070701',  # 锦州
                  'yibin': '271101',  # 宜宾
                  'mianyang': '270401',  # 绵阳
                  'zigong': '270301',  # 自贡
                  'nanchong': '270501',  # 南充
                  'xianggan': '320101',  # 香港
                  'aomen': '330101',  # 澳门
                  'taibei': '340101',  # 台北
                  'taizhong': '340401',  # 台中
                  'tainan': '340203',  # 台南
                  'taidong': '340204',  # 台东
                  'hualian': '340405',  # 花莲
                  'xinzhu': '340103',  # 新竹
                  'sanya': '310201',  # 三亚
                  'haikou': '310101',  # 海口
                  # 待更新
                  'pidu': '270107',  # 郫都
                  }
    city_pinyin = city_pinyin.lower()
    if city_pinyin in city_codes:
        return "101"+city_codes[city_pinyin]
    else:
        return "101010100"   # 默认北京
