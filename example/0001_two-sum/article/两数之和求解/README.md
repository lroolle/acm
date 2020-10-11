"+++
title = "0001. Two Sum 两数之和求解 "
author = ["HerrLu"]
date = 2020-09-12T21:19:28+08:00
tags = ["Leetcode", "Algorithms", "Python3", "Python"]
categories = ["leetcode"]
draft = false
+++

# 两数之和求解

> [0001. Two Sum](https://leetcode-cn.com/problems/two-sum/)
> [两数之和求解](https://leetcode-cn.com/problems/two-sum/solution/liang-shu-zhi-he-qiu-jie-by-herrlu/) by [HerrLu](https://leetcode-cn.com/u/herrlu/)

### 解题思路
来自菜鸟先生的第一题：
两数之和用最简单的遍历来求
要注意第一个for循环的i从0开始，第二个for循环要从i+1开始
这样可以避免重复比较
(有没有小伙伴和我一起从头开始刷题!!!!)
### 代码

```python3
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        for i in range(len(nums)):
            for j in range(i+1,len(nums)):
                if nums[i] + nums[j] == target:
                    return [i,j]
 