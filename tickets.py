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
            # trainrow.extend(trainlist[3:6])
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










# class TrainCollection:
#     header = '车次 车站 时间 历时 一等 二等 软卧 硬卧 硬座 无座'.split()
#     def __init__(self,availabal_trains,options):
#         self.available_trains = availabal_trains
#         self.options = options
#
#     def __get__duration(self, raw_train):
#         duration = raw_train.get('lishi').replace(':','小时')+'分'
#         if duration.startswith('00'):
#             return duration[4:]
#         if duration.startswith('0'):
#             return duration[1:]
#         return duration
#     @property
#     def trains(self):
#         for raw_train in self.available_trains:
#             train_no = raw_train['station_train_code']
#             initial = train_no[0].lower()
#             if not self.options or initial in self.options:
#                 train = [
#                     train_no,
#                     '\n'.join([Fore.GREEN + raw_train['from_station_name'] + Fore.RESET,
#                                Fore.RED + raw_train['to_station_name'] + Fore.RESET]),
#                     '\n'.join([Fore.GREEN + raw_train['start_time'] + Fore.RESET,
#                                Fore.RED + raw_train['arrive_time'] + Fore.RESET]),
#                     self.__get__duration(raw_train),
#                     raw_train['zy_num'],
#                     raw_train['ze_num'],
#                     raw_train['rw_num'],
#                     raw_train['yw_num'],
#                     raw_train['yz_num'],
#                     raw_train['wz_num'],
#                 ]
#                 yield train
#     def pretty_print(self):
#         pt = PrettyTable()
#         pt._set_field_names(self.header)
#         for train in self.trains:
#             pt.add_row(train)
#         print(pt)
#
#
# def cli():
#     arguments = docopt(__doc__)
#     from_station = stations.get(arguments['<from>'])
#     to_station = stations.get(arguments['<to>'])
#     date = arguments['<date>']
#     url = "https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT".format(date,from_station,to_station)
#
#     options = ''.join([
#         key for key,value in arguments.items() if value is True
#     ])
#     r = requests.get(url,verify=False)
#     available_trains = r.json()
#     # ['data']['datas']
#     TrainCollection(available_trains,options).pretty_print()
#     # print(r.json())
#
# if __name__ == '__main__':
#     cli()









