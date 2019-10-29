from heapq import nsmallest
from collections import deque


def quick_sort(_list):
    if len(_list) < 2:
        return _list
    pivot_index = 0
    pivot = _list(pivot_index)
    left_list = [i for i in _list[:pivot_index] if i < pivot]
    right_list = [i for i in _list[pivot_index:] if i > pivot]

    return quick_sort(left_list) + [pivot] + quick_sort(right_list)


def select_sort(seq):
    n = len(seq)
    for i in range(n - 1):
        min_idx = i
    for j in range(i + 1, n):
        if seq[j] < seq[min_idx]:
            min_idx = j
    if min_idx != i:
        seq[i], seq[min_idx] = seq[min_idx], seq[i]


def insertion_sort(_list):
    n = len(_list)
    for i in range(1, n):
        value = _list[i]
        pos = i
        while pos > 0 and value < _list[pos - 1]:
            _list[pos] = _list[pos - 1]
            pos -= 1
        _list[pos] = value
        print(1)


def merge_sorted_list(_list1, _list2):  # 合并有序列表
    len_a, len_b = len(_list1), len(_list2)
    a = b = 0
    sort = []
    while len_a > a and len_b > b:
        if _list1[a] > _list2[b]:
            sort.append(_list2[b])
            b += 1
        else:
            sort.append(_list1[a])
            a += 1
    if len_a > a:
        sort.append(_list1[a:])
    if len_b > b:
        sort.append(_list2[b:])
    return sort


def merge_sort(list1):
    if len(list1) < 2:
        return list1
    else:
        mid = int(len(list1) / 2)
        left = merge_sort(list1[:mid])
        right = merge_sort(list1[mid:])
        return merge_sorted_list(left, right)


def heap_sort(_list):
    return nsmallest(len(_list), _list)


class Stack:
    def __init__(self):
        self.s = deque()

    def peek(self):
        p = self.pop()
        self.push(p)
        return p

    def push(self, el):
        self.s.append(el)

    def pop(self):
        return self.pop()


class Queue:
    def __init__(self):
        self.s = deque()

    def push(self, el):
        self.s.append(el)

    def pop(self):
        return self.popleft()


def binary_search(_list, num):
    mid = len(_list) // 2
    if len(_list) < 1:
        return False
    if num > _list[mid]:
        binary_search(_list[mid:], num)
    elif num < _list[mid]:
        binary_search(_list[:mid], num)
    else:
        return _list.index(num)
