"+++
title = "0001. Two Sum LeetCode第一题，我来闲扯一下 "
author = ["xiao_ben_zhu"]
date = 2020-06-23T20:46:26+08:00
tags = ["Leetcode", "Algorithms", "JavaScript", "HashTable"]
categories = ["leetcode"]
draft = false
+++

# LeetCode第一题，我来闲扯一下

> [0001. Two Sum](https://leetcode-cn.com/problems/two-sum/)
> [LeetCode第一题，我来闲扯一下](https://leetcode-cn.com/problems/two-sum/solution/qing-xi-de-bian-liang-ming-ming-bang-zhu-ji-yi-bu-/) by [xiao_ben_zhu](https://leetcode-cn.com/u/xiao_ben_zhu/)

#### 思路
- 用 hashMap 存一下遍历过的元素和对应的索引。
- 每访问一个元素，查看一下 hashMap 中是否存在满足要求的目标数字。
- 所有事情在一次遍历中完成，因为用了空间换取时间。


#### 代码
```javascript
const twoSum = (nums, target) => {
  const prevNums = {};       // 存储出现过的数字，和对应的索引               

  for (let i = 0; i < nums.length; i++) { // 遍历元素   
    const curNum = nums[i];               // 当前元素   
    const targetNum = target - curNum;    // 满足要求的目标元素   
    const targetNumIndex = prevNums[targetNum]; // 在prevNums中获取目标元素的索引
    if (targetNumIndex !== undefined) { // 如果存在，直接返回 [目标元素的索引,当前索引]
      return [targetNumIndex, i];
    } else {                   // 如果不存在，说明之前没出现过目标元素
      prevNums[curNum] = i;    // 存入当前的元素和对应的索引
    }
  }
}
```
#### 通过情况：
![image.png](https://pic.leetcode-cn.com/1599979335-cIgiAM-image.png)

#### 一点点感想
写好变量命名蛮重要。有时候多写一两行没关系，反而带来更好的可读性，不需要一味追求简洁。

据说我们90%的时间是在看代码，10%时间在写代码，代码的可读性直接决定了你和你同事每天的心情。写代码就像写句子，读起来轻松的代码，自己理解和记忆也方便，下次再看的时候，也不会出现“我当时写的是啥，我怎么看不懂”的情况，而且再敲一遍也不容易出bug。
#### 如果有帮助，点个赞鼓励我继续写下去，写写画画了一百多篇题解（图解），纯分享没有广告成分。
