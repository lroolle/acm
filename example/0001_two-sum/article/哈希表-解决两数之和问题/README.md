"+++
title = "0001. Two Sum 哈希表----解决两数之和问题 "
author = ["Echo__wwW"]
date = 2020-09-20T13:11:27+08:00
tags = ["Leetcode", "Algorithms", "Java", "HashTable"]
categories = ["leetcode"]
draft = false
+++

# 哈希表----解决两数之和问题

> [0001. Two Sum](https://leetcode-cn.com/problems/two-sum/)
> [哈希表----解决两数之和问题](https://leetcode-cn.com/problems/two-sum/solution/ha-xi-biao-by-echo__www/) by [Echo__wwW](https://leetcode-cn.com/u/echo__www/)

### 解题思路
使用哈希表将暴力算法O(n^2)的时间复杂度降低到O(n),但哈希表预加载需要消耗一定的时间，所以不是很推荐。
因为哈希表查找的时间复杂度是O(1),所以可以有效地降低时间复杂度。
空间时间两者通常不可兼得，但在硬件足够强大的现在，通常使用空间换时间，以寻求时间复杂度的降低。
**HashMap中常见的操作**：
创建 -Map<对象,对象> map=new HashMap<对象,对象>();map里面是键值对key:value
注意创建时尖括号里是对象不是基本数据类型,Integer（√）  int（×）
增 — map.put(key, value);删 — map.remove(key);改 — map.put(key, value);
查 —boolean map.containsKey(key);boolean map.containsValue(value);
### 代码
**```java
class Solution {
    public int[] twoSum(int[] nums, int target) {
        Map<Integer,Integer> map=new HashMap<>();
        for(int i=0;i<nums.length;i++)
        {
            map.put(nums[i],i);
        }
        for(int i=0;i<nums.length;i++)
        {
            int ans=target-nums[i];
            if(map.containsKey(ans)&&map.get(ans)!=i)//判断map里是否有ans这个键\ans键对应的值是否已经被用过
                return new int[]{i,map.get(ans)};  
        }
        throw new IllegalArgumentException("not found!");//如果找不到就抛出异常
    }
}
```**