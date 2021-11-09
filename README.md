# KoPL: 面向知识的推理问答编程语言 

[安装](#安装) | [快速开始](#快速开始) | [文档](#文档) | [网站](#网站)

KoPL全称 Knowledge oriented Programing Language, 是一个为复杂推理问答而设计的编程语言。我们可以将自然语言问题表示为由基本函数组合而成的KoPL程序，程序运行的结果就是问题的答案。目前，KoPL的27个基本函数覆盖对多种知识元素（如概念、实体、关系、属性、修饰符等）的操作，并支持多种问题类型（如计数、事实验证、比较等）的查询。KoPL提供透明的复杂问题推理过程，易于理解和使用。KoPL面向知识库、文本等不同形式的知识资源，可扩展性强。

下面的代码演示了如何使用Python代码，实现对一个自然语言问题的推理问答。

```python
from kopl.kopl import KoPLEngine
from kopl.test.test_example import example_kb

engine = KoPLEngine(example_kb) # 创建可以在example_kb这个知识库上进行操作的engine示例

# 查询问题：Who is taller, LeBron James Jr. or his father?
ans = engine.SelectBetween( # 在两个实体中，查询'height'更大的实体
  engine.Find('LeBron James Jr.'), # 找到实体'LeBron James Jr'
  engine.Relate( # 找到与'LeBron James Jr'的'father
    engine.Find('LeBron James Jr.'), # 找到实体'LeBron James Jr'
    'father', # 关系标签
    'forward' # ’forward‘代表'LeBron James Jr'为头实体
  ),
  'height', # 属性标签
  'greater' # 查询属性值更大的实体
)

print(ans) # ans是实体名字列表

```

在这个示例里，我们查询LeBron James Jr.和他的父亲谁更高，KoPL程序给出了正确的答案: LeBron James！

# 安装

KoPL支持Linux (e.g., Ubuntu/CentOS)，macOS，Windows。

其依赖为：

* python >= 3.6

* tqdm >= 4.62


KoPL提供pip安装, 下面将展示Ubuntu的安装命令:

```bash
  $ pip install KoPL tqdm
```

运行下面的代码

```python
import kopl

from kopl.test.test_example import *

run_test()
```
如果测试运行成功，恭喜您已经安装成功。

# 快速开始
您可以准备自己的知识库，使用KoPL实现推理问答。知识库的格式请参考 [知识库](https://kopl.xlore.cn/doc/4_helloworld.html#id1)。
更多使用KoPL程序进行的简单问答请参考 [简单问答](https://kopl.xlore.cn/doc/5_example.html#id2)，复杂问答请参考 [复杂问答](https://kopl.xlore.cn/doc/5_example.html#id8)。

您也可以使用我们为您提供的[查询服务](https://kopl.xlore.cn/queryService)，快速开启KoPL之旅。

# 文档
我们为您提供了KoPL[文档](https://kopl.xlore.cn/doc/index.html)，详细介绍了KoPL面向的知识元素，KoPL的基本函数，KoPL引擎的API。

# 网站
https://kopl.xlore.cn
