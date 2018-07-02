import os
import cchardet
import re
# coding = gbk


def get_file_list(p):
    p = str(p)
    if p == "":
        return []

    p = p.replace("/", "\\")
    if p[-1] != "\\":
        p = p + "\\"

    listdir = os.listdir(p)
    sub_files = []
    for f in listdir:
        path = p + f
        if not os.path.isfile(path):
            continue

        if not re.match("([0-9]+)\\.txt", f):
            continue

        name, ext = os.path.splitext(path)
        if ext != ".txt":
            continue
        sub_files.append(path)

    return sub_files


def get_encoding(file):
    with open(file, 'rb') as my_f:
        return cchardet.detect(my_f.read())['encoding']


# has risks of incompatible characters
def append_contents(o_file, f_path, encoding):
    try:
        in_file = open(f_path, "r", encoding=encoding)
        all_lines = in_file.readlines()
        o_file.writelines(all_lines)
        in_file.close()
        return True
    except (UnicodeEncodeError, UnicodeDecodeError) as e:
        print(e)
        return False


# copy file contents for sure
def append_binaries(f_path):
    try:
        o_file = open(all_file, 'ab')
        in_file = open(f_path, "rb")
        contents = in_file.read()
        o_file.write(contents)
        o_file.close()
        return True
    except (FileExistsError, FileNotFoundError) as e:
        print(e)
        return False


all_file = "all.txt"
txt_files = get_file_list(".")
print(txt_files)
os.remove(all_file)
for f in txt_files:
    out_file = open(all_file, 'a')
    enc_type = get_encoding(f)
    print("append {0} encoding: {1} ".format(f, enc_type))
    out_file.write('\r\n')
    ret = append_contents(out_file, f, enc_type)
    out_file.close()
    if not ret:
        append_binaries(f)


print("Merge Completed!")
