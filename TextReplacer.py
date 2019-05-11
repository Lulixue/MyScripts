import re
import os
import math

TextPath = "file.txt"
NewPath = TextPath + "_new"
RepPattern = "（阙(.*?)?字）"
QueChar = '□'
Numlist = {
    "一" : "1",
    "二" : "2",
    "三" : "3",
    "四" : "4",
    "五" : "5",
    "六" : "6",
    "七":  "7",
    "八" : "8",
    "九" : "9",
    "十" : "10",
    "廿" : "20",
    "百" : "100",
    "千" : "1000",
}

print (Numlist)

if os.path.exists(NewPath):
    os.remove(NewPath)

write_f = open(NewPath,'w', encoding="utf-8")

with open(TextPath,'r', encoding="utf-8") as read_f:
    data = read_f.read()
    new_data = data
    print (data)
    que_list = re.findall(RepPattern, data);
    for que in que_list:
        count = 0
        
        if len(que) == 1:
            char = que[0]
            count = int(Numlist.get(char, "0"))
        elif len(que) == 2:
            char = que[0]
            count = int(Numlist.get(char, "0"))
            if count != 10:
                count *= 10
            char = que[1]
            count += int(Numlist.get(char, "0"))
        elif len(que) == 3:
            char = que[0]
            sec_char = que[1]
            if sec_char == '十':
                count = int(Numlist.get(char, "0"))
                count *= 10
            else:
                count = int(Numlist.get(char, "0")) * 100
                count += int(Numlist.get(sec_char, "0")) * 10
            
            char = que[2]
            count += int(Numlist.get(char, "0"))
        
        space_line = ""
        for i in range(count):
            space_line += QueChar
        txt_to_rep = '（阙' + que + '字）'
        print (que, ':', len(que), ",", count)
        print (txt_to_rep, '->', str(space_line))
        new_data = new_data.replace(txt_to_rep, str(space_line))
        # print(new_data)
        print('--------------------------')
    
    write_f.write(new_data)


write_f.close()
