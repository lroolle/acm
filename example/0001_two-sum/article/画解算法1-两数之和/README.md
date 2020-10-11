"+++
title = "0001. Two Sum 画解算法：1. 两数之和 "
author = ["guanpengchn"]
date = 2019-06-01T03:46:35+08:00
tags = ["Leetcode", "Algorithms", "HashTable", "Java"]
categories = ["leetcode"]
draft = false
+++

# 画解算法：1. 两数之和

> [0001. Two Sum](https://leetcode-cn.com/problems/two-sum/)
> [画解算法：1. 两数之和](https://leetcode-cn.com/problems/two-sum/solution/jie-suan-fa-1-liang-shu-zhi-he-by-guanpengchn/) by [guanpengchn](https://leetcode-cn.com/u/guanpengchn/)

### 思路

- 标签：哈希映射
- 这道题本身如果通过暴力遍历的话也是很容易解决的，时间复杂度在 $O(n2)$
- 由于哈希查找的时间复杂度为 $O(1)$，所以可以利用哈希容器 map 降低时间复杂度
- 遍历数组 nums，i 为当前下标，每个值都判断map中是否存在 `target-nums[i]` 的 key 值
- 如果存在则找到了两个值，如果不存在则将当前的 `(nums[i],i)` 存入 map 中，继续遍历直到找到为止
- 如果最终都没有结果则抛出异常
- 时间复杂度：$$
### 代码

```Java
class Solution {
    public int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> map = new HashMap<>();
        for(int i = 0; i< nums.length; i++) {
            if(map.containsKey(target - nums[i])) {
                return new int[] {map.get(target-nums[i]),i};
            }
            map.put(nums[i], i);
        }
        throw new IllegalArgumentException("No two sum solution");
    }
}
```

### 画解

<![Messages Image(1369442164).png](https://pic.leetcode-cn.com/146e209493728cd7b9fd6095c5947300732799db9b28b2f8e497525ea7b31d58-Messages%20Image\(1369442164\).png),![Messages Image(3072076888).png](https://pic.leetcode-cn.com/d54dcd98bf9b8f5f5575893a9c253dda04cb177436322a9b41ce89290deb651d-Messages%20Image\(3072076888\).png),![Messages Image(645062534).png](https://pic.leetcode-cn.com/c486f3ff7e4b810dd228acad621aa76899eb39b053723d663fc0359dc1d85fac-Messages%20Image\(645062534\).png),![Messages Image(2668429756).png](https://pic.leetcode-cn.com/89121495efbd8b51444cf5a4a1326073e1bd801cd7070a4d82a6897d3c86ba9f-Messages%20Image\(2668429756\).png),![Messages Image(983425875).png](https://pic.leetcode-cn.com/9611f15b036508c66ca99fe3cd3e4f47886f72880ed406e58ad51f008f91e9d8-Messages%20Image\(983425875\).png)>

想看大鹏画解更多高频面试题，欢迎阅读大鹏的 LeetBook：[《画解剑指 Offer 》](https://leetcode-cn.com/leetbook/detail/illustrate-lcof/)，O(∩_∩)O