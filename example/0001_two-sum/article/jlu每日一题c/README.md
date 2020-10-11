"+++
title = "0001. Two Sum [JLU每日一题]C++  "
author = ["HdlugJqzc5"]
date = 2020-10-03T01:31:48+08:00
tags = ["Leetcode", "Algorithms", "cpp"]
categories = ["leetcode"]
draft = false
+++

# [JLU每日一题]C++ 

> [0001. Two Sum](https://leetcode-cn.com/problems/two-sum/)
> [[JLU每日一题]C++ ](https://leetcode-cn.com/problems/two-sum/solution/jlumei-ri-yi-ti-c-by-hdlugjqzc5/) by [HdlugJqzc5](https://leetcode-cn.com/u/HdlugJqzc5/)

# 解题思路
技巧:通过哈希表确定元素是否存在,一次遍历
# 代码
```
    vector<int> twoSum(vector<int>& nums, int target) {
        map<int, int> nMap;
        vector<int> ans;
        int length = nums.size();
        for (int i = 0; i < length; ++i) {
            if (nMap.count(target - nums[i])) {
                ans.push_back(nMap[target - nums[i]]);
                ans.push_back(i);
                return ans;
            }
            nMap[nums[i]] = i;
        }
        return ans;
    }
```
