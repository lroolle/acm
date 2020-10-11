"+++
title = "0001. Two Sum C# "
author = ["licodecheng-die-yi"]
date = 2020-09-25T14:36:43+08:00
tags = ["Leetcode", "Algorithms", ]
categories = ["leetcode"]
draft = false
+++

# C#

> [0001. Two Sum](https://leetcode-cn.com/problems/two-sum/)
> [C#](https://leetcode-cn.com/problems/two-sum/solution/c-by-licodecheng-die-yi/) by [licodecheng-die-yi](https://leetcode-cn.com/u/licodecheng-die-yi/)

static void Main(string[] args)
        {
            int[] nums = new int[] { 7, 15, 2, 11 };
            int target = 9;
            for (int i = 0; i < nums.Length-1; i++)
            {
                for (int j = i+1; j < nums.Length; j++)
                {
                    if (nums[i]+nums[j] == target)
                    {
                        Console.WriteLine($"下标为：{i}和{j}");
                    }
                }
            }
        }