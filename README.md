我写了几个计算器（正如你在这个 repo 中看到的那样），以便更深入地了解解析技术，如 LL、LR 和递归下降。
解析器本身是用 C++ 编写的，构建解析表和归纳 LR 项的算法是用 Python 编写的，因为我希望计算器速度快，并且上述算法看起来像伪代码。
  
在文件夹“tables”中有构建 LL(1) 表和 LR 表的算法以及与它们相关的其他算法，例如查找 FIRST 集和消除左递归的算法。我尽力使关键部分看起来像 *Dragon Book* 和 *EAC2* 等教科书中描述的伪代码。
  
“descent”文件夹里是一个简单的递归下降解析器。它基于龙书附录 A 中描述的前端的相应部分制作——虽然做了很多简化。文件夹“utilities”中的简单词法分析器也是基于它的。
  
LL1 文件夹中是一个 LL(1) 的计算器。现在这个计算器可以产生正确的结果了。  

在接下来的几周内，我仍然会在这个存储库中创建提交，所以如果你已经克隆了它，你可以不时地“git fetch”来查看我最近的进展。
***
I wrote several calculators (as you've seen in this repo), in order to get deeper understanding of parsing techniques such as LL, LR and recursive descent.  
The parsers themselves are written by C++, and the algorithms of building parse tables and inducing LR items are written in Python, since I want calculators to be fast and the said algorithms appear like persudocode.  
  
In folder "tables" there are algorithms of building LL(1) table and LR table and other algorithms related to them, like algorithms of finding first set and of eliminating left recursions. I tried my best to make critial parts appear like persudocode described in textbooks such as *Dragon Book* and *EAC2*.  
  
In folder "descent" a simple recursive-descent parser is made. It is based on the corresponding part of the front end described in appendix A of *Dragon Book*, with lots of simplifications made. The simple lexical analyser in folder "utilities" is based on the front end too.  
  
LL1 folder contains a LL(1)-based calculator, and I've fixed the bugs in it.
  
I will still create commits in this repository in the next few weeks so if you have cloned it you can "git fetch" now and then to see my recent progress.
