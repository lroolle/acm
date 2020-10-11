"+++
title = "0001. Two Sum 利用哈希表求两数之和详细题解 "
author = ["1234-52"]
date = 2020-09-22T14:04:33+08:00
tags = ["Leetcode", "Algorithms", "Java"]
categories = ["leetcode"]
draft = false
+++

# 利用哈希表求两数之和详细题解

> [0001. Two Sum](https://leetcode-cn.com/problems/two-sum/)
> [利用哈希表求两数之和详细题解](https://leetcode-cn.com/problems/two-sum/solution/li-yong-ha-xi-biao-qiu-liang-shu-zhi-he-xiang-xi-t/) by [1234-52](https://leetcode-cn.com/u/1234-52/)

一.解题思路：
1. 判空
2. 新建一个哈希表，长度同nums数组
3. 遍历数组：判断哈希表中是否存在当前元素的key值
    1). 如果不存在，则将target减去当前元素得到一个减数，如果哈希表中不存在该减数的key值，则以该减数作为key，以当前元素下标作为value存入哈希表
    2). 如果存在，则直接返回当前元素作为key对应的value（之前存的下标），以及当前元素的下标
4. 没有符合条件的结果则返回null

二.时间复杂度：o(n)
三.空间复杂度：o(n)
四.执行用时: 2 ms,超过来100%的java提交记录
五.内存消耗: 38.7 MB,超过了96%的java提交记录
六.java代码：
```
class Solution {
    public int[] twoSum(int[] nums, int target) {
        if (nums == null || nums.length == 0) {
            return null;
        }

        Map<Integer, Integer> subtractMap = new HashMap<>(nums.length);
        Integer subtract;
        for (int i = 0; i < nums.length; i ++) {
            if (subtractMap.containsKey(nums[i])) {
                return new int[]{subtractMap.get(nums[i]), i};
            }
            subtract = target - nums[i];
            if (!subtractMap.containsKey(subtract)) {
                subtractMap.put(subtract, i);
            }
        }
        return null;
    }
}
```
