#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from datetime import datetime
import pprint as pp

def parse_log_to_list(filename):
  import re

  log_list = list()
  IP = f"([(\d\.)]+)"
  date = f"\[(.*?)\]"
  HTTP_request_type = f'"(.*?) '
  others = f'(.*)'
  log_regex = f"{IP} - - {date} {HTTP_request_type}{others}"

  with open(filename, 'r') as file:
    row = file.read()
    log_tuple = re.findall(log_regex, row)

  for log in log_tuple:
    log_list.append([log[0], datetime.strptime(log[1], "%d/%b/%Y:%H:%M:%S %z"), log[2], log[3:]])

  return log_list

def find_top_10_requesting_IP_within_datetimes(log_list, from_datetime, to_datetime):
  from collections import Counter

  valid_IP_list = [log[0] for log in log_list if
    from_datetime <= log[1] <= to_datetime]

  IP_counter = Counter(valid_IP_list)
  top_10_requesting_IP_list = [IP[0] for IP in IP_counter.most_common(10)]
  return top_10_requesting_IP_list

def find_most_requesting_country(log_list):
  from collections import Counter
  import subprocess as sp
  import json

  IP_counter = Counter([log[0] for log in log_list])
  most_requesting_IP = IP_counter.most_common(1)
  most_requesting_IP, most_requesting_freq = IP_counter.most_common(1)[0]

  cmd = f"curl -s ipinfo.io/{most_requesting_IP}"
  sp_obj = sp.Popen(cmd, stdout=sp.PIPE, shell=True)
  cmd_stdout = sp_obj.communicate()[0].strip()
  most_requesting_country = json.loads(cmd_stdout)['country']

  return most_requesting_IP, most_requesting_country

if __name__ == '__main__':
  from_datetime_str = "2017-06-10 00:00:00 +0800"
  to_datetime_str = "2017-06-19 23:59:59 +0800"

  log_list = parse_log_to_list("/home/ec2-user/devopstest/sre_test_access.log")
  top_10_requesting_IP_list = find_top_10_requesting_IP_within_datetimes(
    log_list,
    datetime.strptime(from_datetime_str, "%Y-%m-%d %H:%M:%S %z"),
    datetime.strptime(to_datetime_str, "%Y-%m-%d %H:%M:%S %z")
  )
  most_requesting_IP, most_requesting_country = find_most_requesting_country(log_list)

  print(f"Total number of HTTP requests: {len(log_list)}")
  print(f"Top 10 requesting hosts (source IPs) from {from_datetime_str} to {to_datetime_str}: {top_10_requesting_IP_list}")
  print(f"Most requesting source IP, country: {most_requesting_IP}, {most_requesting_country}")
