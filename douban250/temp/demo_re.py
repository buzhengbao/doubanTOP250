import re

# re.find_all(正则表达式，目标字符串)
#
str1 = 'abcdlkasdjfslkdjcdcdcdccdcddfKcddJKJkjKJKJMn'
#
# pattern = 'cd*'
# pattern = '[a-z]'  # 匹配单个小写字母
# print(re.findall(pattern, str1))
# pattern = '[A-Z]'  # 匹配单个大写字母
# pattern = '[a-z]+'
# print(re.findall(pattern, str1))
#
# # re.sub(正则表达式1， 正则表达式2， 目标字符串)
pattern1 = 'cd*'
pattern2 = 'U'
print(re.sub(pattern1, pattern2, str1))
str2 = '<h2>二级标题</h2><h1 class="pp1">一级标题a</h1>    123123    <h2>二级标题</h2>'
# # .所有字符 除了\n
# pattern = '<h1.*</h1>'
# pattern = '<h1.*>(.*)</h1>'
# print(re.findall(pattern,str2))
# str2 = '<h1 class="pp1">一级标题a</h1>'
# .+ 和 .+?
# pattern = '<.+>'
# print(re.findall(pattern, str2))
pattern = '<.+?>'
# print(re.findall(pattern, str2))
# pattern = '<(.+?)>'
# pattern = '<h2>二级标题</h2><h1 class="pp1">一级标题a</h1>(.+)<h2>二级标题</h2>'
print(re.findall(pattern, str2))