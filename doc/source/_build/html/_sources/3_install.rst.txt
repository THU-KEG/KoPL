安装
============

KoPL支持Linux (e.g., Ubuntu/CentOS)，macOS，Windows。

其中Linux和macOS的依赖为：

::

  python >= 3.6

  tqdm >= 4.62

Windows对环境的要求为：

::

  Python >= 3.6

  tqdm >= 4.62

  x86_64处理器

  Windows10及以上


KoPL提供pip安装, 下面将展示Ubuntu的安装命令:

::

  $ sudo apt install python3.7-dev

  $ python3.7 -m pip install KoPL

运行下面的代码

::

  import kopl
  from kopl.test.test_example import *
  run_test()

如果测试运行通过，恭喜您已经安装成功。
