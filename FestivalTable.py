def lunar_festival(day):
    festival_table = {'1-1': ' 春节',
                      '1-15': ' 元宵节',
                      '2-2': ' 龙抬头|社日',
                      '3-3': ' 上巳节',
                      '5-5': ' 端午节',
                      '7-7': ' 七夕节',
                      '7-15': ' 中元节',
                      '8-15': ' 中秋节',
                      '9-9': ' 重阳节',
                      '12-8': ' 腊八节',
                      '12-23': ' 北方小年',
                      '12-24': ' 南方小年',
                      '12-30': ' 除夕'}
    if day in festival_table:
        return festival_table[day]+' |'
    else:
        return ''


def solar_festival(day):
    festival_table = {'2-14': ' 情人节',
                      '3-8': ' 妇女节',
                      '3-12': ' 植树节',
                      '4-1': ' 愚人节',
                      '5-1': ' 劳动节',
                      '5-4': ' 青年节',
                      '6-1': ' 儿童节',
                      '8-1': ' 建军节',
                      '9-10': ' 教师节',
                      '10-1': ' 教师节',
                      '11-1': ' 万圣节',
                      '12-24': ' 平安夜',
                      '12-25': ' 圣诞节',
                      '1-1': ' 元旦',
                      }
    if day in festival_table:
        return festival_table[day]+' |'
    else:
        return ''


def solar_terms(year, day):
    if year % 4 == 0 or year % 4 == 1:
        festival_table = {
            '4-4': ' 清明',
            '6-5': ' 芒种',
            '6-21': ' 夏至',
            '7-22': ' 大暑',
            '10-8': ' 寒露',
            '11-22': ' 小雪',
            '12-7': ' 大雪',
            '12-21': ' 冬至',
            '1-5': ' 小寒',
            '1-20': ' 大寒',
        }
    elif year % 4 == 2 or year % 4 == 3:
        festival_table = {
            '4-5': ' 清明',
            '6-6': ' 芒种',
            '6-21': ' 夏至',
            '7-23': ' 大暑',
            '10-24': ' 霜降',
            '11-22': ' 小雪',
            '12-7': ' 大雪',
            '12-22': ' 冬至',
            '1-6': ' 小寒',
            '1-20': ' 大寒',
        }
    if year % 4 == 1:

        festival_table.update({'2-3': ' 立春'})
    else:
        festival_table.update({'2-4': ' 立春'})

    if year % 4 == 0 or year % 4 == 3:
        festival_table.update({'2-19': ' 雨水'})
    else:
        festival_table.update({'2-18': ' 雨水'})

    if year % 4 == 3:
        festival_table.update(
            {'3-6': ' 惊蛰', '3-21': ' 春分', '5-6': ' 立夏', '8-8': ' 立秋', '9-8': ' 白露', '10-24': ' 霜降',
             '11-8': '立冬'})
    else:
        festival_table.update(
            {'3-5': ' 惊蛰', '3-20': ' 春分', '5-5': ' 立夏', '8-7': ' 立秋', '9-7': ' 白露', '10-23': ' 霜降',
             '11-7': ' 立冬'})

    if year % 4 == 0:
        festival_table.update(
            {'4-19': ' 谷雨', '5-20': ' 小满', '7-6': ' 小暑', '8-22': ' 处暑', '9-22': ' 秋分', '1-6': ' 小寒'})
    else:
        festival_table.update(
            {'4-20': ' 谷雨', '5-21': ' 小满', '7-7': ' 小暑', '8-23': ' 处暑', '9-23': ' 秋分', '1-5': ' 小寒'})
    if day in festival_table:
        return festival_table[day]+' |'
    else:
        return ''
