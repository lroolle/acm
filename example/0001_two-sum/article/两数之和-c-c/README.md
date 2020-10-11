"+++
title = "0001. Two Sum 两数之和 C / C++ "
author = ["chenlele"]
date = 2019-05-10T02:52:50+08:00
tags = ["Leetcode", "Algorithms", "C++"]
categories = ["leetcode"]
draft = false
+++

# 两数之和 C / C++

> [0001. Two Sum](https://leetcode-cn.com/problems/two-sum/)
> [两数之和 C / C++](https://leetcode-cn.com/problems/two-sum/solution/liang-shu-zhi-he-by-gpe3dbjds1/) by [chenlele](https://leetcode-cn.com/u/chenlele/)

#### 解题思路：
题目：给定一个整数数组 `nums` 和一个目标值 `target`，请你在该数组中找出和为目标值的那 两个 **整数**，并返回他们的数组下标。

你可以假设每种输入只会对应一个答案。但是，你不能重复利用这个数组中同样的元素。

示例:
给定 nums = [2, 7, 11, 15], target = 9
因为 nums[0] + nums[1] = 2 + 7 = 9
所以返回 [0, 1]
####  暴力法：

```C++
class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        int i,j;
        for(i=0;i<nums.size()-1;i++)
        {
            for(j=i+1;j<nums.size();j++)
            {
                if(nums[i]+nums[j]==target)
                {
                   return {i,j};
                }
            }
        }
        return {i,j};
    };
};
```
注： `nums.size()` 获取向量元素个数；
<br>

```C
int* twoSum(int* nums, int numsSize, int target) {
    int i,j;
    int *result=NULL;
    for(i=0;i<numsSize-1;i++)
    {
        for(j=i+1;j<numsSize;j++)
        {
            if(nums[i]+nums[j]==target)
            {
                 result=(int*)malloc(sizeof(int)*2);
                 result[0]=i;
                 result[1]=j;
                 return result;
            }
        }
    }
    return result;
}
```
注：malloc 是 c 语言中的动态分配内存，`result=(int*)malloc(sizeof(int)*2)`； malloc 函数返回的是 `void\*` 型，所以要强制类型转换成 `int`，在前面加上 `(int *)`，才能给整型赋值，后面 `(sizeof(int)*2)` 的意思是分配两个 `int` 大小的空间；

**总结：该方法简单但是时间复杂度为 $O(n^2^)$。空间复杂度为 $O(1)$;运行速度慢且内存空间消耗大**
<br>
####  两遍哈希表：

```C++
class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        map<int,int> a;//建立hash表存放数组元素
        vector<int> b(2,-1);//存放结果
        for(int i=0;i<nums.size();i++)
            a.insert(map<int,int>::value_type(nums[i],i));
        for(int i=0;i<nums.size();i++)
        {
            if(a.count(target-nums[i])>0&&(a[target-nums[i]]!=i))
            //判断是否找到目标元素且目标元素不能是本身
            {
                b[0]=i;
                b[1]=a[target-nums[i]];
                break;
            }
        }
        return b;
    };
};
```
注：该方法用 map 实现，map 是 STL 的一个关联容器，它提供一对一（其中第一个可以称为关键字，每个关键字只能在 map 中出现一次，第二个可能称为该关键字的值）的数据处理能力
<br>

####  一编哈希表
改进：在进行迭代并将元素插入到表中的同时，我们还会回过头来检查表中是否已经存在当前元素所对应的目标元素。如果它存在，那我们已经找到了对应解，并立即将其返回。

```C++
class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        map<int,int> a;//提供一对一的hash
        vector<int> b(2,-1);//用来承载结果，初始化一个大小为2，值为-1的容器b
        for(int i=0;i<nums.size();i++)
        {
            if(a.count(target-nums[i])>0)
            {
                b[0]=a[target-nums[i]];
                b[1]=i;
                break;
            }
            a[nums[i]]=i;//反过来放入map中，用来获取结果下标
        }
        return b;
    };
};
```
**觉得本文对你有帮助，点个赞噢谢谢**
