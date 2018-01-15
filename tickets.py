#coding=utf-8

"""命令行火车票查看器
Usage:
    tickets.py tickets [-gdtkz] <from> <to> <date>

Options:
    -h --help   显示帮助菜单
    -g          高铁
    -d          动车
    -t          特快
    -k          快速
    -z          直达

Example:
   tickets -dg 上海 江山  2018-02-15
"""

from docopt import docopt
import stations,requests
from prettytable import PrettyTable

class Tickets(object):

    def printTrainInfo(self):
        arguments = docopt(__doc__)
        from_station = stations.getCode(arguments['<from>'])
        to_station = stations.getCode(arguments['<to>'])
        date = arguments['<date>']
        url = "https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT".format(date,from_station,to_station)
        r = requests.get(url)
        allresults = r.json()
        allTickets = allresults['data']['result']
        rows = self.parse_train(allTickets)
        self.printtable(rows)

    def parse_train(self, allTickets):
        rows = []
        for ticket in allTickets:
            trainlist = ticket.split('|')
            # print(trainlist)
            trainrow = []
            trainlist[6] = stations.getCityName(trainlist[6])
            trainlist[7] = stations.getCityName(trainlist[7])
            # print(trainlist[7])
            trainrow.append(trainlist[3])
            trainrow.append(trainlist[6])
            trainrow.append(trainlist[7])
            trainrow.extend(trainlist[8:11])
            trainrow.extend(trainlist[32:21:-1])
            row = []
            for x in trainrow:
                x = x or "--"
                row.append(x)
            rows.append(row)
        return rows

    def printtable(self, rows):

        info = "车次 出发站 到达站 出发时间 到达时间 历时 商务座 特等座 一等座 二等座 高级 软卧 动卧 硬卧 软座 硬座 无座"
        info = info.split(" ")
        x = PrettyTable(info)
        for row in rows:
            x.add_row(row)
        print(x.get_string())

if __name__ == '__main__':
    Tickets().printTrainInfo()




















