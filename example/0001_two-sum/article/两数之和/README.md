"+++
title = "0001. Two Sum 两数之和 "
author = ["feng-95s"]
date = 2020-10-10T18:04:03+08:00
tags = ["Leetcode", "Algorithms", "Java"]
categories = ["leetcode"]
draft = false
+++

# 两数之和

> [0001. Two Sum](https://leetcode-cn.com/problems/two-sum/)
> [两数之和](https://leetcode-cn.com/problems/two-sum/solution/liang-shu-zhi-he-by-feng-95s/) by [feng-95s](https://leetcode-cn.com/u/feng-95s/)

### 解题思路
核心思想：将数组中数据依次存入HashMap中[数据做key，地址做value]，当存到某一位时刚好target-这个key的结果能在之前存入的数据中找到（判断方法用map.containsKey()，它判断map集合中是否存在此key），此时即可将该数对应的value值（即为该数在数组中的地址位置的值）存到保存结果的数组中。
1.结果返回以一个数组形式，首先创建一个数组用于存放结果
2.创建一个HashMap集合，遍历数组依次存入集合中
3.判断key，存在则返回，不存在则存入集合中
4.返回结果

### 代码

```java
class Solution {
    public int[] twoSum(int[] nums, int target) {
      int[] arr = new int[2];     //创建一个存放结果的数组 
        HashMap<Integer,Integer> map = new HashMap<>();     
        for(int i = 0; i < nums.length; i ++){      //遍历
            if(map.containsKey(target - nums[i])){       //判断集合中是否存在啊该key
                return new int[]{map.get(target - nums[i]),i};//返回结果
            }
            map.put(nums[i],i);//集合中无key,则将遍历的数组存入到map集合中
        }
        return arr;     //返回数组
    }
}
```