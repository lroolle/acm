"+++
title = "0001. Two Sum Reduce + 哈希表（1行代码，超96%） "
author = ["mantoufan"]
date = 2020-10-03T04:06:19+08:00
tags = ["Leetcode", "Algorithms", "JavaScript", "HashTable"]
categories = ["leetcode"]
draft = false
+++

# Reduce + 哈希表（1行代码，超96%）

> [0001. Two Sum](https://leetcode-cn.com/problems/two-sum/)
> [Reduce + 哈希表（1行代码，超96%）](https://leetcode-cn.com/problems/two-sum/solution/reduce1xing-dai-ma-chao-96-by-mantoufan/) by [mantoufan](https://leetcode-cn.com/u/mantoufan/)

### 解题思路
- `p`：最后一位下标 以及 和为`target`的所需`值`下标
- `reduce`：
    - `p[v]`找到，`ar.splice(1)`，提前终止`reduce`循环，返回 [`p`存的下标, 当前下标]
    - `p[v]`未找到
        - 最后一位，返回`[]`
        - 不是最后一位，存下标，`p[target - v] = i`

### 代码

```javascript
var twoSum = function(nums, target) {
    return nums.reduce((p, v, i, ar) => p[v] !== undefined && ar.splice(1) && [p[v], i] || (i === p['l'] ? [] : p[target - v] = i, p), {l: nums.length - 1})
};
```

### 结果
![QQ拼音截图20201003114911.png](https://pic.leetcode-cn.com/1601697572-JGbWeA-QQ%E6%8B%BC%E9%9F%B3%E6%88%AA%E5%9B%BE20201003114911.png)
