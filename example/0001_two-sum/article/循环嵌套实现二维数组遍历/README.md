"+++
title = "0001. Two Sum 循环嵌套实现二维数组遍历 "
author = ["er-shi-di"]
date = 2020-09-17T03:22:24+08:00
tags = ["Leetcode", "Algorithms", "Java"]
categories = ["leetcode"]
draft = false
+++

# 循环嵌套实现二维数组遍历

> [0001. Two Sum](https://leetcode-cn.com/problems/two-sum/)
> [循环嵌套实现二维数组遍历](https://leetcode-cn.com/problems/two-sum/solution/xun-huan-qian-tao-shi-xian-er-wei-shu-zu-bian-li-b/) by [er-shi-di](https://leetcode-cn.com/u/er-shi-di/)

循环嵌套实现二维数组遍历

### 代码

```java
class Solution {
    public int[] twoSum(int[] nums, int target) {
int[] aa={0,0};

        for (int i = 0; i < nums.length; i++) {
            for (int j = 1; j < nums.length; j++) {
                if (nums[i] + nums[j] == target&& i!=j) {
                   aa = new int[] {i, j};
                    System.out.println(aa[0] + "," + aa[1]);
                }
            }

        }
        return aa;

    }
}
```