'''
1，将食材列表转秩后写入fooddict.txt
2，将记录内容写入foodtest.txt
3，Ctrl+B运行程序
4，检查“没有找到”的部分，是不是应该列入食材列表，如果是goto第一步，如果不是可以加入forbid列表
5，从foodresult.txt中复制结果到GoogleSheet的食材列表
'''
# 不必报错的词汇
forbid = ['羹','ml', 'ml左右', '猪','番茄面', '泥', '干重', '不喜欢吃', '吐了一点', '皮', '卷', '片', '去', '参加联合敬拜', '左右', '饼', '瓣', '约', '呕吐', '糕', '糊', '上午', '下午', '松', '软', '丸', '一丁点', '汤',
          '丁', '煎', '用的', '牌的油菜花油', '葵花籽油', '可能有鸡蛋', '粥', "一共", "晚上", "中午", "早上", "水", "没吃", "若干", "一点", "条", "酵母", "带蛋清", "炒", "水煮蛋打碎", "嘴边出现荨麻疹", "一点蛋清", ""]
errorlist = []
fooddata = open("foodtest.txt", "r", -1, 'utf-8')
data = fooddata.readlines()  # read everything in data
# print (len(data[0])

datelist = []
dateindex = []
for lines in data:
    if len(lines) >= 11 and lines[6] == '2' and lines[7] == '0':
        datelist.append(lines)
        # find Date text for A columm
        dateindex.append(data.index(lines))
        # find Position of the Date for later use
dateindex.append(len(data))
n = 0
for date in datelist:
    date = list(str(date))
    date = date[:-1]
    date = str("".join(date))
    datelist[n] = date
    n += 1

#print (dateindex)
fooddata.close()

foodresult = open("foodresult.txt", "w", -1, "utf-8")
foodresult.write('')
foodresult.close()

fooddict = open("fooddict.txt", "r", -1, "utf-8")
fdict = fooddict.readlines()
# now clean the fdict and remove /n from it
n = 0
for food in fdict:
    food = list(str(food))
    food = food[:-1]
    food = str("".join(food))
    fdict[n] = food
    n += 1

fooddict.close()

# A list of ord(letter)
letterlist = [97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122,
              65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 220, 252, 246, 214, 228, 196, 223]

# Delete words that neither CHN nor ENG nor DE


def delete_non_chn(word):
    if (ord(word) > 11904 and ord(word) < 40900) or (ord(word) in letterlist):
        return word
    else:
        return "\n"


def clean_words(words):
    save = []
    i = 1
    for word in words:
        if word != '\n':
            save.append(word)
            i = 1  # start to have a word
        else:
            if i == 1:
                save.append('\n')
                i = 0
            else:
                i = 0
    n = 1
    s = ''
    while n < len(save):
        s += str(save[n])
        n += 1
    return s

for day in range(0, len(datelist)):
    # for day in range(0,2):#test only 2 days
    # go through all date
    wordsofday = []
    for line in range(dateindex[day], dateindex[(day + 1)]):
        # print (ord(data[line][0]))
        for i in range(0, len(data[line])):

            # print (ord(data[line][i]))
            # ord can change word to numbers
            # next step: use number to judge if it is a chinese word
            # chinese range(11904,40900)
            wordsofday.append(delete_non_chn(data[line][i]))

    # print (clean_words(wordsofday))
    buffertxt = open("buffer.txt", "w", -1, "utf-8")
    buffertxt.write(clean_words(wordsofday))
    buffertxt.close()
    buffertxt = open("buffer.txt", "r", -1, "utf-8")

    foodlist = buffertxt.readlines()

    # now clean the foodlist and remove /n from it
    n = 0
    for food in foodlist:
        food = list(str(food))
        food = food[:-1]
        food = str("".join(food))
        foodlist[n] = food
        n += 1
    buffertxt.close()
    # print (foodlist)

    # now start to find positions for food: foodindex
    foodindex = []

    for n in range(0, len(foodlist)):
        try:
            foodindex.append(fdict.index(foodlist[n]))
        except:
            foodindex.append(-1)
            try:
                n = forbid.index(foodlist[n])
                # if n >= 0:
                #	print ("")
                # else:
                #	print ("没有找到  "+foodlist[n])
            except:
                if foodlist[n] not in errorlist:
                    errorlist.append(foodlist[n])

    # print (errorlist)
    # print (foodindex)

    # use foodindex to build a txt file
    xmark = []
    foodresult = open("foodresult.txt", "a", -1, "utf-8")
    writestr = [datelist[day], '	', "0", '	']
    for n in range(0, len(fdict)):
        if n in foodindex:
            xmark.append("x")
            xmark.append("	")
        else:
            xmark.append("	")
    writestr += xmark
    n = 0
    s = ''
    while n < len(writestr):
        s += str(writestr[n])
        n += 1

    foodresult.write(str(s))
    foodresult.write('\n')
    foodresult.close()
    # print (str(s))

# report

print ("已完成处理%s天的记录。结果存储在foodresult.txt" % len(datelist))
print ("\n")

# report error
if len(errorlist) > 0:
    print ("没有找到如下食材:")
    print (errorlist)
