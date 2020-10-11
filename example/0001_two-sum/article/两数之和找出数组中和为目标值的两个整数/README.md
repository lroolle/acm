"+++
title = "0001. Two Sum 两数之和：找出数组中和为目标值的两个整数 "
author = ["jue-qiang-zha-zha"]
date = 2020-09-15T03:09:37+08:00
tags = ["Leetcode", "Algorithms", "Python3", "Python"]
categories = ["leetcode"]
draft = false
+++

# 两数之和：找出数组中和为目标值的两个整数

> [0001. Two Sum](https://leetcode-cn.com/problems/two-sum/)
> [两数之和：找出数组中和为目标值的两个整数](https://leetcode-cn.com/problems/two-sum/solution/liang-shu-zhi-he-zhao-chu-shu-zu-zhong-he-wei-mu-b/) by [jue-qiang-zha-zha](https://leetcode-cn.com/u/jue-qiang-zha-zha/)

### 解题思路
1. 建立哈希表（字典），存储数组各元素及其对应的下标。{hashmap[num]:i, ...}
2. 遍历数组。设当前元素坐标为i，值为num，用字典的get方法返回（target-num）的坐标j。如果坐标j不为None且与i不同，则返回两个数的坐标位置。

### 代码

```python3
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        hashmap = {}
        for i, num in enumerate(nums):
            hashmap[num] = i
        for i, num in enumerate(nums):
            j = hashmap.get(target-num)
            if j != None and j != i:
                return [i,j]
```