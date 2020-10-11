"+++
title = "0001. Two Sum 【Java】简单易懂的 “补数思想” "
author = ["leetcoder-youzg"]
date = 2020-10-03T01:48:46+08:00
tags = ["Leetcode", "Algorithms", "Java", "HashTable"]
categories = ["leetcode"]
draft = false
+++

# 【Java】简单易懂的 “补数思想”

> [0001. Two Sum](https://leetcode-cn.com/problems/two-sum/)
> [【Java】简单易懂的 “补数思想”](https://leetcode-cn.com/problems/two-sum/solution/java-jian-dan-yi-dong-de-bu-shu-si-xiang-by-leetco/) by [leetcoder-youzg](https://leetcode-cn.com/u/leetcoder-youzg/)

### 解题思路
> 遍历一轮 nums数组，以 补数 为键，下标 为值，填充map
> 并在map中寻找是否有这个补数 的键，其值即为 nums数组中的下标

### 运行结果
![image.png](https://pic.leetcode-cn.com/1601689545-MUgkkv-image.png)

### 代码

```java
class Solution {
    public int[] twoSum(int[] nums, int target) {
        HashMap<Integer, Integer> map = new HashMap<>();    // 以 补数 为键，下标 为值
        int[] res = new int[2];

        for(int i=0; i < nums.length; i++) {
            int other = target - nums[i];

            if(map.get(other) !=null) {
                res[0] = i;
                res[1] = map.get(other);
                return res;
            }
            map.put(nums[i], i);
        }
        return res;
    }
}
```
打卡第74天，加油！！！