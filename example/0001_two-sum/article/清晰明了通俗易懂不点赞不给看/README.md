"+++
title = "0001. Two Sum 清晰明了，通俗易懂，不点赞不给看 "
author = ["xmblgt"]
date = 2020-09-19T06:21:53+08:00
tags = ["Leetcode", "Algorithms", "Java", "HashTable"]
categories = ["leetcode"]
draft = false
+++

# 清晰明了，通俗易懂，不点赞不给看

> [0001. Two Sum](https://leetcode-cn.com/problems/two-sum/)
> [清晰明了，通俗易懂，不点赞不给看](https://leetcode-cn.com/problems/two-sum/solution/qian-xian-yi-dong-ha-xi-biao-fu-zhu-yi-ci-bian-li-/) by [xmblgt](https://leetcode-cn.com/u/xmblgt/)

思路：
1. 创建一个存放结果的数组
2. 创建一个哈希表: key存元素，value存元素的索引
3. 遍历，对**每一个元素e**作如下处理：
     - 作差：tmp = target - e;
    - 判断：tmp是否存在map中
        - 若存在 --> 把tmp与e的索引取出，返回res
        - 若不存在 --> 把e以及索引存放在map中
4. 遍历完之后，如果存在也会在遍历中把结果返回，如果不存在就会直接throw异常或者返回空数组res

```java
class Solution {
    public int[] twoSum(int[] nums, int target) {   
        int[] res = new int[2];     //1.创建一个存放结果的数组res 
        HashMap<Integer,Integer> map = new HashMap<>();     //2.创建一个辅助的哈希表
        for(int i = 0; i < nums.length; i ++){      //3.遍历
            int tmp = target - nums[i];     //作差
            if(map.containsKey(tmp)){       //判断
                res[0] = map.get(tmp);
                res[1] = i;
                break;
            }
            map.put(nums[i],i);
        }
        return res;     //返回
    }
}
```

![微信图片_20200919202332.jpg](https://pic.leetcode-cn.com/1600657611-yYNMmJ-%E5%BE%AE%E4%BF%A1%E5%9B%BE%E7%89%87_20200919202332.jpg)

