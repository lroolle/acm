"+++
title = "0001. Two Sum 两数之和，最简单方法 "
author = ["qing-shu-k"]
date = 2020-09-14T13:58:23+08:00
tags = ["Leetcode", "Algorithms", "Java"]
categories = ["leetcode"]
draft = false
+++

# 两数之和，最简单方法

> [0001. Two Sum](https://leetcode-cn.com/problems/two-sum/)
> [两数之和，最简单方法](https://leetcode-cn.com/problems/two-sum/solution/liang-shu-zhi-he-zui-jian-dan-fang-fa-by-qing-shu-/) by [qing-shu-k](https://leetcode-cn.com/u/qing-shu-k/)

### 解题思路
此处撰写解题思路

### 代码

```java
class Solution {
    public int[] twoSum(int[] nums, int target) {
          int[] jieguo=new int[2];//定义一个空白的，含有2个位置的数组
          for(int i=0;i<nums.length;i++){
              for(int j=i+1;j<nums.length;j++){
                  if(nums[j]==target-nums[i]){
                     jieguo[0]=i;
                     jieguo[1]=j;
                     return jieguo;
                  }
              }            
          }
          return jieguo;
    }
}
```