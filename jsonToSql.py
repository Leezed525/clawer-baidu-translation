#把json变成sql插入语句

import json


def yinstr(s):
    s = str(s)
    s = s.replace("'","\\\'")
    return '\'' + s + '\''

if __name__ == '__main__':
    with open('word_translated.json', encoding="utf-8") as words:
        word_list = json.load(words)
    count = 0
    fp = open('./insertWord.txt', 'w', encoding='utf-8')
    print(yinstr("i'cant'do'this"))
    for word in word_list:
        means = word["means"]
        mean = ""
        if len(means) > 1:
            for i in means:
                mean += i + ";"
        else:
            mean = means[0] + ";"
        # print(word["word"])
        fp.write("INSERT INTO words(id,word,symbols,part,mean,ex,tran) VALUES(%s,%s,%s,%s,%s,%s,%s);\n" % (
            yinstr(word["id"]), yinstr(word["word"]), yinstr(word["symbols"]), yinstr(word["part"]), yinstr(mean),
            yinstr(word["liji"]["ex"]), yinstr(word["liji"]["tran"])))
        count += 1
    print(count)
