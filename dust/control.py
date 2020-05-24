#！/usr/bin/env python
#! -*-coding:utf-8 -*-
#!@Author : zhuxx
#!@time : 2020/05/18 20:26

import psutil
import time
import platform

cpu_percent_dict = {}
net_io_dict = {'net_io_time':[], 'net_io_sent': [], 'net_io_recv': [], 'pre_sent': 0, 'pre_recv': 0, 'len': -1}
disk_dict = {'disk_time':[], 'write_bytes': [], 'read_bytes': [], 'pre_write_bytes': 0, 'pre_read_bytes': 0, 'len': -1}


def cpu():
    now = time.strftime('%H:%M:%S', time.localtime(time.time()))
    cpu_percent = psutil.cpu_percent() 
    cpu_percent_dict[now] = cpu_percent
    if len(cpu_percent_dict.keys()) == 11:
        cpu_percent_dict.pop(list(cpu_percent_dict.keys())[0])

def memory():
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()
    if platform.system() == 'Windows':
        return memory.total, memory.total - (
                memory.free), memory.free , swap.total, swap.used, swap.free, memory.percent
    else:
        return memory.total, memory.total - (memory.free + memory.inactive), memory.free + memory.inactive, swap.total, swap.used, swap.free, memory.percent

def net_io():
    now = time.strftime('%H:%M:%S', time.localtime(time.time()))
    count = psutil.net_io_counters()
    g_sent = count.bytes_sent
    g_recv = count.bytes_recv

    if net_io_dict['len'] == -1:
        net_io_dict['pre_sent'] = g_sent
        net_io_dict['pre_recv'] = g_recv
        net_io_dict['len'] = 0
        return

    net_io_dict['net_io_sent'].append(g_sent - net_io_dict['pre_sent'])
    net_io_dict['net_io_recv'].append(g_recv - net_io_dict['pre_recv'])
    net_io_dict['net_io_time'].append(now)
    net_io_dict['len'] = net_io_dict['len'] + 1

    net_io_dict['pre_sent'] = g_sent
    net_io_dict['pre_recv'] = g_recv

    if net_io_dict['len'] == 11:
        net_io_dict['net_io_sent'].pop(0)
        net_io_dict['net_io_recv'].pop(0)
        net_io_dict['net_io_time'].pop(0)
        net_io_dict['len'] = net_io_dict['len'] - 1

def disk():
    disk_usage = psutil.disk_usage('/')
    disk_used = 0
    partitions = psutil.disk_partitions()
    for partition in partitions:
        if partition[3] != 'removable':
            partition_disk_usage = psutil.disk_usage(partition[1])
            disk_used = partition_disk_usage.used + disk_used

    now = time.strftime('%H:%M:%S', time.localtime(time.time()))
    count = psutil.disk_io_counters()
    read_bytes = count.read_bytes
    write_bytes = count.write_bytes

    if disk_dict['len'] == -1:
        disk_dict['pre_write_bytes'] = write_bytes
        disk_dict['pre_read_bytes'] = read_bytes
        disk_dict['len'] = 0
        return disk_usage.total, disk_used, disk_usage.free

    disk_dict['write_bytes'].append((write_bytes - disk_dict['pre_write_bytes'])/1024)
    disk_dict['read_bytes'].append((read_bytes - disk_dict['pre_read_bytes'])/ 1024)
    disk_dict['disk_time'].append(now)
    disk_dict['len'] = disk_dict['len'] + 1

    disk_dict['pre_write_bytes'] = write_bytes
    disk_dict['pre_read_bytes'] = read_bytes

    if disk_dict['len'] == 51:
        disk_dict['write_bytes'].pop(0)
        disk_dict['read_bytes'].pop(0)
        disk_dict['disk_time'].pop(0)
        disk_dict['len'] = disk_dict['len'] - 1

    return disk_usage.total, disk_used, disk_usage.free