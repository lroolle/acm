"+++
title = "0001. Two Sum 执行用时：0 ms, 在所有 Java 提交中击败了100.00% 的用户 内存消耗：39.7 MB, 在所有 Java 提交中击败了90.83% 的用户 "
author = ["fei-193"]
date = 2020-09-11T08:23:31+08:00
tags = ["Leetcode", "Algorithms", "Java", "BitManipulation", "Array"]
categories = ["leetcode"]
draft = false
+++

# 执行用时：0 ms, 在所有 Java 提交中击败了100.00% 的用户 内存消耗：39.7 MB, 在所有 Java 提交中击败了90.83% 的用户

> [0001. Two Sum](https://leetcode-cn.com/problems/two-sum/)
> [执行用时：0 ms, 在所有 Java 提交中击败了100.00% 的用户 内存消耗：39.7 MB, 在所有 Java 提交中击败了90.83% 的用户](https://leetcode-cn.com/problems/two-sum/solution/zhi-xing-yong-shi-0-ms-zai-suo-you-java-ti-jia-452/) by [fei-193](https://leetcode-cn.com/u/fei-193/)

**解题思路：**
假设a+b=target，则b=target-a，定义一个int数组res，令bitNum=2047(二进制为11111111111),遍历数组nums，将数组res下标为a&bitNum的值存为i+1，如果res[b&bitNum]的值不为0，则找到目标值。
```
**代码**
class Solution {
    public int[] twoSum(int[] nums, int target){
        int volume = 2<<10; //2048
        int bitNum = volume-1; //11111111111
        int[] res = new int[volume];
        for(int i=0;i<nums.length;i++){
            int c = (target-nums[i])&bitNum;
            if(res[c]!=0){
                return new int[]{res[c]-1,i};
            }
            res[nums[i]&bitNum] = i+1;
        }
        throw new IllegalArgumentException("No two sum solution");
    }
}
```