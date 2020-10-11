"+++
title = "0001. Two Sum 通过for循环来遍历实现 "
author = ["may-c"]
date = 2020-09-01T06:54:56+08:00
tags = ["Leetcode", "Algorithms", "JavaScript"]
categories = ["leetcode"]
draft = false
+++

# 通过for循环来遍历实现

> [0001. Two Sum](https://leetcode-cn.com/problems/two-sum/)
> [通过for循环来遍历实现](https://leetcode-cn.com/problems/two-sum/solution/tong-guo-forxun-huan-lai-bian-li-shi-xian-by-may-c/) by [may-c](https://leetcode-cn.com/u/may-c/)

### 解题思路
此处撰写解题思路
通过两层for循环来依次匹配数据
### 代码

```javascript
/**
 * @param {number[]} nums
 * @param {number} target
 * @return {number[]}
 */
var twoSum = function (nums, target) {
  const _arr = [];
  for (let i = 0; i < nums.length; i++) {
    for (let j = i + 1; j < nums.length; j++) {
      if (nums[i] + nums[j] === target) {
        _arr.push(i, j);
      }
    }
  }
  return _arr;
};
```