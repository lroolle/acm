"+++
title = "0001. Two Sum python小白的正常解法，第一道力扣通过的题目，加油，嘎嘎~ "
author = ["sad-payneh7q"]
date = 2020-09-17T14:48:42+08:00
tags = ["Leetcode", "Algorithms", "Python"]
categories = ["leetcode"]
draft = false
+++

# python小白的正常解法，第一道力扣通过的题目，加油，嘎嘎~

> [0001. Two Sum](https://leetcode-cn.com/problems/two-sum/)
> [python小白的正常解法，第一道力扣通过的题目，加油，嘎嘎~](https://leetcode-cn.com/problems/two-sum/solution/pythonxiao-bai-de-zheng-chang-jie-fa-di-yi-dao-li-/) by [sad-payneh7q](https://leetcode-cn.com/u/sad-payneh7q/)

### 解题思路
按照正常思考方式解法

### 代码

```python3
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        res = []    #用于保存结果
        lg = len(nums)  #取列表长度
        for i in range(0,lg-1): #外层循环
            for j in range(i+1,lg): #内层循环
                if(nums[i]+nums[j])==target:
                    res.append(i)
                    res.append(j)
                    return res

```