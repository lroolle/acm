"+++
title = "0001. Two Sum 就这？ "
author = ["lun-1"]
date = 2020-09-22T15:25:10+08:00
tags = ["Leetcode", "Algorithms", "Python"]
categories = ["leetcode"]
draft = false
+++

# 就这？

> [0001. Two Sum](https://leetcode-cn.com/problems/two-sum/)
> [就这？](https://leetcode-cn.com/problems/two-sum/solution/jiu-zhe-by-lun-1/) by [lun-1](https://leetcode-cn.com/u/lun-1/)

### 解题思路
过一遍，如果存在目标值就返回，不存在就存到字典里

### 代码

```python
class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        target_dict = {}
        for i, num in enumerate(nums):
            target_num = target - num
            if target_num in target_dict:
                return [target_dict[target_num], i]
            else:
                target_dict[num] = i
```