"+++
title = "0001. Two Sum 哈希表法 "
author = ["lanshiqin"]
date = 2020-10-04T11:08:44+08:00
tags = ["Leetcode", "Algorithms", "Java"]
categories = ["leetcode"]
draft = false
+++

# 哈希表法

> [0001. Two Sum](https://leetcode-cn.com/problems/two-sum/)
> [哈希表法](https://leetcode-cn.com/problems/two-sum/solution/ha-xi-biao-fa-by-lanshiqin-2/) by [lanshiqin](https://leetcode-cn.com/u/lanshiqin/)

### 解题思路
1. 定义一个哈希表，用来存储循环的每个元素，nums数组值作为key，nums数组下标作为value。
2. 每次循环判时，断哈希表中是否有key等于 target - nums[i],如果有就返回下标。没有则继续保存key value。

### 代码

```java
class Solution {
    public int[] twoSum(int[] nums, int target) {
        Map<Integer,Integer> map = new HashMap<>(nums.length);
        for(int i=0; i< nums.length; i++){
            int x = nums[i];
            int key = target - x;
            if (!map.containsKey(key)){
                map.put(x,i);
                continue;
            }
            return new int[]{map.get(key),i};
        }
        return new int[0];
    }
}
```