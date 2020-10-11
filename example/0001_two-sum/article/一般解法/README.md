"+++
title = "0001. Two Sum 一般解法 "
author = ["nuan-xin-shao-nian-nan-ou-ba"]
date = 2020-09-22T02:35:10+08:00
tags = ["Leetcode", "Algorithms", "Java"]
categories = ["leetcode"]
draft = false
+++

# 一般解法

> [0001. Two Sum](https://leetcode-cn.com/problems/two-sum/)
> [一般解法](https://leetcode-cn.com/problems/two-sum/solution/yi-ban-jie-fa-by-nuan-xin-shao-nian-nan-ou-ba/) by [nuan-xin-shao-nian-nan-ou-ba](https://leetcode-cn.com/u/nuan-xin-shao-nian-nan-ou-ba/)

### 解题思路
此处撰写解题思路
首先定义两个变量first second分别保存先后两个答案的下标，定义变量text记录差值。
从数组第一个元素开始记录（将其下标保存在first），与目标值求差，在二层循环中寻找是否有解，找到后将其下标保存在second，跳出循环，如果此时循环变量j等于数组长度nums.length则说明没找到解，重新开始外层循环。如果不等于则说明找到解后跳出了二层循环，此时再次使用break跳出一层循环。创建一个大小为2的数组保存结果返回。
### 代码

```java
class Solution {
    public int[] twoSum(int[] nums, int target) {
        int first=0,second=0,text=0,i,j;
       for(i=0;i<nums.length;i++){
             first=i;
             text=target-nums[i];
             for(j=i+1;j<nums.length;j++){
                 if(nums[j]==text){
                     second=j;
                     break;
                 }
             }
             if(j==nums.length){
                 continue;
             }
             else{
                 break;
             }
         }
       int [] arr=new int[2];
       arr[0]=first;
       arr[1]=second;
       return arr;
    }
}
```