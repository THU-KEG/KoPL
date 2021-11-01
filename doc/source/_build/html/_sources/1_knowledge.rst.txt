======================
KoPL面向的知识元素
======================

.. image:: knowledge_element.jpg
  :width: 600
  :alt: Alternative text

使用KoPL的前提是要有一个合适的目标知识库，该知识库中应该含有如下元素：

    - 实体（Entity）
    - 概念（Concept）
    - 关系（Relation）
    - 属性（Attribute）
    - 关系型知识（Relational Knowledge）
    - 属性型知识（LiteralKnowledge）
    - 修饰型知识（Qualifier Knowledge）

实体
-----------------

.. glossary::

    知识库中最基本的元素，用来表示一个独一无二的事物。

.. admonition:: 例子 
    
    勒布朗·詹姆斯（Lebron James）和克利夫兰骑士队（Cleveland Cavaliers）都是实体。

概念
-----------------

.. glossary::

    一组具有相同特征的实体组成的集合。

.. admonition:: 例子 
    
    篮球队（Basketball Team）便是一个概念。

关系
-----------------

.. glossary::

    表示两个实体之间的关系。特殊地，实体通过 instance of 关系链接到相应的概念上，概念之间通过 subclass of 关系来组织成层次结构。

.. admonition:: 例子 
    
    父亲（father）和出生地（place of birth）都是关系。

属性
-----------------

.. glossary::

    表示实体的属性信息。又由属性键和属性值两部分组成，属性值有字符串、数字、日期和年份4种类型。其中数值类型的属性值又包含单位，如“206厘米”中的“厘米”。

.. admonition:: 例子 
    
    身高（height）是一个属性，206厘米是对应的属性值。

关系型知识
-----------------

.. glossary::

    用于表示两个实体间关系的三元组， 由（实体，关系，实体）组成。

.. admonition:: 例子 
    
    （勒布朗·詹姆斯，出生地，阿克伦）是一个关系型知识。

属性型知识
-----------------

.. glossary::

    用于表示一个实体属性信息的三元组，由（实体，属性键，属性值）组成。

.. admonition:: 例子 
    
    （勒布朗·詹姆斯，身高，206厘米）是一个属性型知识。

修饰型知识
-----------------

.. glossary::

    用于对一个关系型或属性型的三元组进行进一步的修饰，包含一个修饰键和一个修饰值。由(三元组，修饰键，修饰值)组成。

.. admonition:: 例子 
    
    （（勒布朗·詹姆斯，被选球队，克利夫兰骑士队），选择时间，2003年）是一个修饰型知识。