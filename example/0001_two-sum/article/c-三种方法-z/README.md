"+++
title = "0001. Two Sum c++ 三种方法 -z "
author = ["zrita"]
date = 2020-02-10T06:45:51+08:00
tags = ["Leetcode", "Algorithms", "C++"]
categories = ["leetcode"]
draft = false
+++

# c++ 三种方法 -z

> [0001. Two Sum](https://leetcode-cn.com/problems/two-sum/)
> [c++ 三种方法 -z](https://leetcode-cn.com/problems/two-sum/solution/c-san-chong-fang-fa-jian-dan-yi-dong-ji-bai-100-z-/) by [zrita](https://leetcode-cn.com/u/zrita/)

ps:对于存在重复元素的情况，用一遍哈希和两遍哈希确实会得到不同的结果，但是都是符合题目要求的。 题目描述确实有点含糊，但是这个题目的本意是让我们练习哈希表，题目说到You may assume that each input would have exactly one solution，即您可以假设每个输入都只有一个解决方案。
### 两遍哈希
```cpp
class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        unordered_map<int,int> m;
        for(int i = 0; i<nums.size(); i++)
            m[nums[i]] = i;         //向map中添加元素        
        for(int i = 0; i<nums.size(); i++)
        {
            if(m.find(target-nums[i]) != m.end() && m[target-nums[i]] != i)  //如果m中存在对应的键值，且不为i
                return {i, m[target-nums[i]]};
        }
        return {};
    }
};
```
### 一遍哈希
```cpp
class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        unordered_map<int,int> m;        
        for(int i = 0; i < nums.size(); i++)
        {
            if(m.find(target-nums[i]) != m.end())     return {m[target-nums[i]], i};        
                                //  m[target-nums[i]]为已经加入map的元素的索引，所以小于本轮循环中的i，放在前面
            m[nums[i]] = i;       //向map中添加元素
        }
        return {};
    }
};
```

### 暴力解法
```cpp
class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        int len = nums.size();

        for(int i = 0; i < len-1; i++)
        for(int j = i + 1; j < len; j++)
        {
            if(nums[i] + nums[j] == target)
            return {i,j};
        }
        
       return {};
    }
};
```