I wrote several calculators (as you've seen in this repo), in order to get deeper understanding of parsing techniques such as LL, LR and recursive descent.  
  
The parsers themselves are written by C++, and the algorithms of building parse tables and deriving LR items are written in Python, since I want calculators to be fast and the said algorithms appear like pseudocode.  
  
In folder "tables" there are algorithms of building LL(1) table and LR table and other algorithms related to them, like algorithms of finding FIRST set and of eliminating left recursions. I tried my best to make critial parts appear like pseudocode described in textbooks such as *the Dragon Book* and *EAC2*.  
  
In folder "descent" a simple recursive-descent parser is made. It is based on the corresponding part of the front end described in appendix A of *the Dragon Book*, through lots of simplifications are made. The simple lexical analyser in folder "utilities" is based on the front end too.  
  
LL1 folder contains an LL(1)-based calculator, and I've fixed the bugs in it.
  
In folder "LRx" there are two parsers using LR(1) and SLR, respectively. The class "Parser" are all the same in the two parsers, the only difference is their action table and goto table.  
  
In folder "generated" there is a calculator implemented using lex and yacc. Just type "make gcalc" to build it.  
  
I will still create commits in this repository in the next few weeks, so if you have cloned it, you can "git fetch" now and then to see my recent progress.
***
这个仓库里是若干四则运算语法的解析器（或者说，“计算器”，因为它们真的会生成相应的 AST，还能把值算出来）。这些解析器有 LL(1) 的，有递归向下的，还会有 SLR 和 LALR 的。  

解析器本身是用 C++ 写的，但是搭解析表和推 LR 项之类的算法是用 Python 写的。因为我想计算器能跑得快些，还想让那些建表的算法关键部分尽可能接近伪代码。
  
“tables”里就是建表的算法，外加支持它们算法，比方说找 FIRST 集、FOLLOW 集的，去左递归的。我尽量把关键部分写得接近龙书和橡书里的伪代码。
  
“descent”文件夹里是一个简单的递归下降解析器——照着龙书的附录 A 抄的。文件夹“utilities”中的简单词法分析器也是照着它抄的。
  
LL1 文件夹中是一个 LL(1) 的计算器。最开始这里有一 bug 我没发现，后来改了。现在这个计算器可以产生正确的结果了。  
  
LRx 文件夹里有 SLR 和 LR(1) 的计算器。Parser 类都是一样的，只不过链接的时候用到的 action 表和 goto 表不一样。  
  
generated 文件夹里是给 lex 和 yacc 用的语法文件。也可以用它们生成完整的计算器。  
  
这个项目还没结束（还差 LALR），所以如果你已经克隆了它，你可以不时地“git fetch”来查看我最近的进展。
