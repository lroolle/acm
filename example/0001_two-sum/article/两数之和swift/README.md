"+++
title = "0001. Two Sum 两数之和Swift "
author = ["da-dong-14"]
date = 2020-10-01T16:20:08+08:00
tags = ["Leetcode", "Algorithms", "Swift"]
categories = ["leetcode"]
draft = false
+++

# 两数之和Swift

> [0001. Two Sum](https://leetcode-cn.com/problems/two-sum/)
> [两数之和Swift](https://leetcode-cn.com/problems/two-sum/solution/liang-shu-zhi-he-swift-by-da-dong-14/) by [da-dong-14](https://leetcode-cn.com/u/da-dong-14/)
```Swift
class Solution {
    func twoSum(_ nums: [Int], _ target: Int) -> [Int] {
        var dic:[Int:Int] = [:]
        for i in 0..<nums.count {
            var a = nums[i]
            // 从字典中查找，找到了直接返回
            if let bIndex = dic[target - a] {                
                return [bIndex,i]
            } else {
                // 存储到字典中【值：下标】
                dic[a] = i
            }
        }
        // 没找到返回默认值
        return []
    }
}
```

![20201002001556.jpg](https://pic.leetcode-cn.com/1601569152-ZLGPvp-20201002001556.jpg)

