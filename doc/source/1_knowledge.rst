==============================
Knowledge Elements
==============================

.. image:: knowledge_element.jpg
  :width: 600
  :alt: Alternative text

A prepared knowledge base is the pre-requisite to execute KoPL. Such knowledge base should have the following knowledge elements:

    - Entity
    - Concept
    - Relation
    - Attribute
    - Relational Knowledge
    - Literal Knowledge
    - Qualifier Knowledge
    
Entity
-----------------

.. glossary::

    Entities are the most basic elements in the knowledge, which are used to represent each unique object in the real world.

.. admonition:: Example
    
    - *LeBron James*, the basketball player, is an entity.
    - *Cleveland Cavaliers*, the basketball team, is also an entity.

Concept
-----------------

.. glossary::

    Concepts are sets of entities with common characteristic.

.. admonition:: Example
    
    - *Basketball Team* is a concept.

Relation
-----------------

.. glossary::

    Relation represent the relationship between entities. In particular, entities are connected to its corresponding concepts via *InstanceOf* relation, while concepts are connected with *SubclassOf* relation to construct the hierarchy.

.. admonition:: Example
    
    - *Father* is a relation
    - *Place of Birth* is also a relation

Attribute
-----------------

.. glossary::

    表示实体的属性信息。又由属性键和属性值两部分组成，属性值有字符串、数字、日期和年份4种类型。其中数值类型的属性值又包含单位，如“206厘米”中的“厘米”。

.. admonition:: Example
    
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