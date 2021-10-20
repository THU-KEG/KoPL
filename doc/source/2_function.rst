===========
KoPL的元函数
===========

用 KoPL 编程可以看作对元函数进行组合操作。
元函数有两种:

    - 操作函数（Operation Functions）
    - 查询函数（Query Functions）

KoPL 通过对这些元函数的组合实现查询操作。
本教程将详细介绍这些元函数各自的 **功能** 和 **参数** 格式。

.. note::  
    我们定义函数参数的格式为:
        (函数输入) :math:`\times` (文本输入) :math:`\mapsto` (输出)

    函数输入是之前的 function 的输出
    
    文本输入是由问题推断得到的

.. .. topic:: Your Topic Title

..     Subsequent indented lines comprise
..     the body of the topic, and are
..     interpreted as body elements.

.. .. admonition:: Test

..     Description of the limitations ...

.. .. raw:: html

..     <b>text</b>

操作函数
-----------------

.. glossary::

    FindAll: (`Null`) :math:`\times` (`Null`) :math:`\mapsto` (`Entities`)

        - 描述
            返回知识库中的所有实体
        - 函数输入
            `Null`: 空

        - 文本输入
            `Null`: 空

        - 输出
            `Entities`: 实体集合

        - 示例
            .. code-block:: python

                FindAll()

                
            
    Find: (`Null`) :math:`\times` (`Name`) :math:`\mapsto` (`Entities`) 

        - 描述
            返回知识库中所有名字为 `Name` 的实体集合
        - 函数输入
            `Null`: 空

        - 文本输入
            `Name`: 实体名称

        - 输出
            `Entities`: 所有名称为 `Name` 的实体的集合

        - 示例
            .. code-block:: python

                Find(Kobe Bryant)
            
    FilterConcept: (`Entities`) :math:`\times` (`Name`) :math:`\mapsto` (`Entities`)

        - 描述
            筛选出实体，要求属于给定的概念
        - 函数输入
            `Entities`: 筛选的实体集合
        - 文本输入
            `Name`: 概念名称
        - 输出
            `Entities`: 满足筛选条件的实体集合
        - 示例
            .. code-block:: python

                FilterConcept(athlete)
            
    FilterStr: (`Entities`) :math:`\times` (`Key`, `Value`) :math:`\mapsto` (`Entities`, `Facts`)

        - 描述
            筛选出实体和对应的事实，要求选出的 **实体** 具有 **字符串** 属性，且该属性的属性值等于给定的属性值

        - 函数输入
            `Entities`: 筛选的实体集合

        - 文本输入
            `Key`: 筛选的目标属性
            `Value`: 筛选的目标属性的属性值

        - 输出
            `Entities`: 满足筛选条件的实体集合
            `Facts`: 满足筛选条件的事实

        - 示例
            .. code-block:: python

                FilterStr(gender, male)

    FilterNum: (`Entities`) :math:`\times` (`Key`, `Value`, `Op`) :math:`\mapsto` (`Entities`, `Facts`)
        
        - 描述
            筛选出实体和对应的事实，要求选出的 **实体** 具有 **数值** 属性，且该属性的属性值满足和给定的属性值的某种关系

        - 函数输入
            `Entities`: 筛选的实体集合

        - 文本输入
            `Key`: 筛选的目标属性
            `Value`: 筛选的目标属性用于比较的属性值
            `Op`: 比较方法

        - 输出
            `Entities`: 满足筛选条件的实体集合
            `Facts`: 满足筛选条件的事实

        - 示例
            .. code-block:: python

                FilterNum(height, 200 centimetres, >)

    FilterYear: (`Entities`) :math:`\times` (`Key`, `Value`, `Op`) :math:`\mapsto` (`Entities`, `Facts`)
        
        - 描述
            筛选出实体和对应的事实，要求选出的 **实体** 具有 **年份** 属性，且该属性的属性值满足和给定的属性值的某种关系

        - 函数输入
            `Entities`: 筛选的实体集合

        - 文本输入
            `Key`: 筛选的目标属性
            `Value`: 筛选的目标属性用于比较的属性值
            `Op`: 比较方法

        - 输出
            `Entities`: 满足筛选条件的实体集合
            `Facts`: 满足筛选条件的事实

        - 示例
            .. code-block:: python

                FilterYear(birthday, 1980, =)

    FilterDate: (`Entities`) :math:`\times` (`Key`, `Value`, `Op`) :math:`\mapsto` (`Entities`, `Facts`)
        
        - 描述
            筛选出实体和对应的事实，要求选出的 **实体** 具有 **日期** 属性，且该属性的属性值满足和给定的属性值的某种关系

        - 函数输入
            `Entities`: 筛选的实体集合

        - 文本输入
            `Key`: 筛选的目标属性
            `Value`: 筛选的目标属性用于比较的属性值
            `Op`: 比较方法

        - 输出
            `Entities`: 满足筛选条件的实体集合
            `Facts`: 满足筛选条件的事实

        - 示例
            .. code-block:: python

                FilterDate(birthday, 1980-06-01, <)

    QFilterStr: (`Entities`, `Facts`) :math:`\times` (`QKey`, `QValue`) :math:`\mapsto` (`Entities`, `Facts`)
        
        - 描述
            筛选出实体和对应的事实，要求对应的 **事实** 具有 **字符** 类型的限定条件，且该限定条件符合给定的值

        - 函数输入
            `Entities`: 筛选的实体集合
            `Facts`: 筛选的事实集合

        - 文本输入
            `QKey`: 筛选的目标限定词
            `QValue`: 筛选的限定词满足的值

        - 输出
            `Entities`: 满足筛选条件的实体集合
            `Facts`: 满足筛选条件的事实
            
        - 示例
            .. code-block:: python

                QFilterStr(language, English)

    QFilterNum: (`Entities`, `Facts`) :math:`\times` (`QKey`, `QValue`, `Op`) :math:`\mapsto` (`Entities`, `Facts`)
        
        - 描述
            筛选出实体和对应的事实，要求对应的 **事实** 具有 **数值** 类型的限定条件，且该限定条件和给定的值之间存在某种指定的关系

        - 函数输入
            `Entities`: 筛选的实体集合
            `Facts`: 筛选的事实集合

        - 文本输入
            `QKey`: 筛选的目标限定词
            `QValue`: 给定的值用来和限定条件比较
            `Op`: 用来比较的方法

        - 输出
            `Entities`: 满足筛选条件的实体集合
            `Facts`: 满足筛选条件的事实

        - 示例
            .. code-block:: python

                QFilterNum(bonus, 20000 dollars, >)

    QFilterYear: (`Entities`, `Facts`) :math:`\times` (`QKey`, `QValue`, `Op`) :math:`\mapsto` (`Entities`, `Facts`)
        
        - 描述
            筛选出实体和对应的事实，要求对应的 **事实** 具有 **年份** 类型的限定条件，且该限定条件和给定的值之间存在某种指定的关系

        - 函数输入
            `Entities`: 筛选的实体集合
            `Facts`: 筛选的事实集合
            
        - 文本输入
            `QKey`: 筛选的目标限定词
            `QValue`: 给定的值用来和限定条件比较
            `Op`: 用来比较的方法
            
        - 输出
            `Entities`: 满足筛选条件的实体集合
            `Facts`: 满足筛选条件的事实
            
        - 示例
            .. code-block:: python

                QFilterYear(start time, 1980, =)

    QFilterDate: (`Entities`, `Facts`) :math:`\times` (`QKey`, `QValue`, `Op`) :math:`\mapsto` (`Entities`, `Facts`)
        - 描述
            筛选出实体和对应的事实，要求对应的 **事实** 具有 **日期** 类型的限定条件，且该限定条件和给定的值之间存在某种指定的关系

        - 函数输入
            `Entities`: 筛选的实体集合
            `Facts`: 筛选的事实集合
            
        - 文本输入
            `QKey`: 筛选的目标限定词
            `QValue`: 给定的值用来和限定条件比较
            `Op`: 用来比较的方法
            
        - 输出
            `Entities`: 满足筛选条件的实体集合
            `Facts`: 满足筛选条件的事实
            
        - 示例
            .. code-block:: python

                QFilterDate(start time 1980-06-01, <)

    Relate: (`Entities`) :math:`\times` (`Rel`, `Dir`) :math:`\mapsto` (`Entities`, `Facts`)
        
        - 描述
            筛选出实体，要求实体和给定的实体之间具有某种关系

        - 函数输入
            `Entities`: 筛选的实体集合

        - 文本输入
            `Rel`: 表示关系
            `Dir`: 目标实体

        - 输出
            `Entities`: 满足筛选条件的实体集合
            `Facts`: 满足筛选条件的事实

        - 示例
            .. code-block:: python

                Relate(capital, forward)

    And: (`Entities`, `Entities`) :math:`\times` (`Null`) :math:`\mapsto` (`Entities`)
        
        - 描述
            计算两个实体集合的 **交集**

        - 函数输入
            `Entities`: 实体的集合

        - 文本输入
            `Null`

        - 输出
            `Entities`: 实体交集
            
    Or: (`Entities`, `Entities`) :math:`\times` (`Null`) :math:`\mapsto` (`Entities`)
        
        - 描述
            计算两个实体集合的 **并集**

        - 函数输入
            `Entities`: 实体的集合

        - 文本输入
            `Null`

        - 输出
            `Entities`: 实体交集
            

查询函数
-----------------


.. glossary::

    QueryName: (`Entity`) :math:`\times` (`Null`) :math:`\mapsto` (`string`)

        - 描述
            查询实体的名称

        - 函数输入
            `Entity`: 待查询的实体

        - 文本输入
            `Null`

        - 输出
            `string`: 实体名称
                
            
    Count: (`Entities`) :math:`\times` (`Null`) :math:`\mapsto` (`number`) 

        - 描述
            计算实体的数量

        - 函数输入
            `Entities`: 待统计的实体集合

        - 文本输入
            `Null`

        - 输出
            `number`: 集合中的实体数量

                
    QueryAttr: (`Entity`) :math:`\times` (`Key`) :math:`\mapsto` (`Value`) 

        - 描述
            查询实体的属性的值

        - 函数输入
            `Entity`: 待查询的实体

        - 文本输入
            `Key`: 待查询的属性

        - 输出
            `Value`: 查询结果

        - 示例
            .. code-block:: python

                QueryAttr(height)

    QueryAttrUnderCondition: (`Entity`) :math:`\times` (`Key`, `QKey`, `QValue`) :math:`\mapsto` (`Value`) 

        - 描述
            查询实体的属性的值，要求这条事实类型的知识满足给定的限定条件

        - 函数输入
            `Entity`: 待查询的实体

        - 文本输入
            `Key`: 待查询的属性
            `QKey`: 待查询的属性要求满足的限定词
            `QValue`: 限定条件要求的值

        - 输出
            `Value`: 查询出的属性值

        - 示例
            .. code-block:: python

                QueryAttrUnderCondition(population, point in time, 2016)


    QueryRelation: (`Entity`, `Entity`) :math:`\times` (`Null`) :math:`\mapsto` (`Rel`) 

        - 描述
            查询两个实体之间的关系

        - 函数输入
            `Entity`: 待查询的属性

        - 文本输入
            `Null`

        - 输出
            `Rel`: 查询的两个实体的关系

        - 示例
            .. code-block:: python

                QueryRelation(Kobe Bryant, America)


    SelectBetween: (`Entity`, `Entity`) :math:`\times` (`Key`, `Op`) :math:`\mapsto` (`string`) 

        - 描述
            对于两个实体，给出它们在某个属性上谁大谁小

        - 函数输入
            `Entity`: 待比较的两个实体

        - 文本输入
            `Key`: 比较的属性
            `Op`: 比较操作的条件

        - 输出
            `string`: 比较结果

        - 示例
            .. code-block:: python

                SelectBetween(height, greater)

    SelectAmong: (`Entities`) :math:`\times` (`Key`, `Op`) :math:`\mapsto` (`string`) 

        - 描述
            对一个实体集合，给出这个集合中某个属性值最大或者最小的那个实体

        - 函数输入
            `Entities`: 待比较的实体集合

        - 文本输入
            `Key`: 比较的属性
            `Op`: 比较操作的条件

        - 输出
            `string`: 比较结果

        - 示例
            .. code-block:: python

                SelectAmong(height, largest)

    VerifyStr: (`Value`) :math:`\times` (`Value`) :math:`\mapsto` (`boolean`) 

        - 描述
            判断输入的 **字符串** 是否和给定的值相同

        - 函数输入
            `Value`: 待比较的字符串

        - 文本输入
            `Value`: 给定的字符串的值

        - 输出
            `boolean`: 是否相同

        - 示例
            .. code-block:: python

                VerifyStr(male)

    VerifyNum: (`Value`) :math:`\times` (`Value`, `Op`) :math:`\mapsto` (`boolean`) 

        - 描述
            判断输入的 **数值** 是否和给定的值具有某种关系

        - 函数输入
            `Value`: 待比较的数值

        - 文本输入
            `Value`: 给定的数值
            `Op`: 比较操作

        - 输出
            `boolean`: 是否具有给定的关系

        - 示例
            .. code-block:: python

                VerifyNum(20000 dollars, >)

    VerifyYear: (`Value`) :math:`\times` (`Value`, `Op`) :math:`\mapsto` (`boolean`) 

        - 描述
            判断输入的 **年份** 是否和给定的年份具有某种关系

        - 函数输入
            `Value`: 待比较的年份

        - 文本输入
            `Value`: 给定的年份
            `Op`: 比较操作

        - 输出
            `boolean`: 是否具有该给定的关系

        - 示例
            .. code-block:: python

                VerifyYear(1980, >)

    VerifyDate: (`Value`) :math:`\times` (`Value`, `Op`) :math:`\mapsto` (`boolean`) 

        - 描述
            判断输入的 **日期** 是否和给定的日期具有某种关系

        - 函数输入
            `Value`: 待比较的日期

        - 文本输入
            `Value`: 给定的日期
            `Op`: 比较操作

        - 输出
            `boolean`: 是否具有该给定的关系

        - 示例
            .. code-block:: python

                VerifyYear(1980-06-01, >)

    QueryAttrQualifier: (`Entity`) :math:`\times` (`Key`, `Value`, `QKey`) :math:`\mapsto` (`QValue`) 

        - 描述
            查询给定的 **属性** 类型事实的限定条件的值

        - 函数输入
            `Entity`: 待查询的事实的参与实体

        - 文本输入
            `Key`: 待查询的事实的属性
            `Value`: 待查询的事实的属性值
            `QKey`: 待查询的限定条件

        - 输出
            `QValue`: 查询到的限定条件的值

        - 示例
            .. code-block:: python

                QueryAttrQualifier(population, 23,390,000, point in time)

    QueryRelationQualifier: (`Entity`, `Entity`) :math:`\times` (`Rel`, `QKey`) :math:`\mapsto` (`QValue`) 

        - 描述
            查询给定的 **关系** 类型事实的限定条件的值

        - 函数输入
            `Entity`: 两个 `Entity` 分别为关系的头实体和尾实体

        - 文本输入
            `Rel`: 实体的关系
            `QKey`: 待查询的限定条件

        - 输出
            `QValue`: 限定条件的值

        - 示例
            .. code-block:: python

                QueryRelationQualifier(spouse, start time)
