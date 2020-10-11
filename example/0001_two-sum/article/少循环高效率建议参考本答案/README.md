"+++
title = "0001. Two Sum 【少循环，高效率】建议参考本答案 "
author = ["ke-yan-xiao-bai-10"]
date = 2020-09-15T03:36:11+08:00
tags = ["Leetcode", "Algorithms", "Python", "Python3"]
categories = ["leetcode"]
draft = false
+++

# 【少循环，高效率】建议参考本答案

> [0001. Two Sum](https://leetcode-cn.com/problems/two-sum/)
> [【少循环，高效率】建议参考本答案](https://leetcode-cn.com/problems/two-sum/solution/shao-xun-huan-gao-xiao-lu-jian-yi-can-kao-ben-da-a/) by [ke-yan-xiao-bai-10](https://leetcode-cn.com/u/ke-yan-xiao-bai-10/)

### 解题思路
+ 为了防止在pop()之后无法找到第一个元素的索引，此处使用浅拷贝
+ 第一个元素的索引在原数组中查找
+ 第二个元素的索引使用计数法进行标记

### 代码

```python3
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        num = nums.copy()
        n = 0
        while len(num):
            i = num.pop(0)
            n += 1
            if target-i in num:
                return [nums.index(i),num.index(target-i)+n]
```