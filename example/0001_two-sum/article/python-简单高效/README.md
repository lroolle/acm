"+++
title = "0001. Two Sum python 简单高效 "
author = ["gua-niu-uk"]
date = 2020-09-18T07:50:36+08:00
tags = ["Leetcode", "Algorithms", "Python3"]
categories = ["leetcode"]
draft = false
+++

# python 简单高效

> [0001. Two Sum](https://leetcode-cn.com/problems/two-sum/)
> [python 简单高效](https://leetcode-cn.com/problems/two-sum/solution/python-jian-dan-gao-xiao-by-gua-niu-uk/) by [gua-niu-uk](https://leetcode-cn.com/u/gua-niu-uk/)

```
nums = [2,7,11,10]
target = 9
temp = []
def sum_two_nums(goal):
    for item in range(len(nums)-1):
        for i in range(item + 1, len(nums)-item):
            if nums[item] + nums[i] == goal:
                temp.append(item)
                temp.append(i)
    return temp
result = sum_two_nums(target)
print(result)
```
