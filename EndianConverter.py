import struct
import sys
import os

src_file = "C:\\Users\\user\\Desktop\\app.bin"

# main body
if sys.argv.__len__() > 1:
    # 参数获取
    src_file = sys.argv[1]
else:
    # 文本输入
    src_file = input("Source Bin Path: ")

if not os.path.exists(src_file):
    print('File Path Invalid! Exiting...')
    exit(1)

dst_file = src_file[0:(src_file.__len__()-4)]
dst_i_file = dst_file
dst_file += "_le.bin"
dst_i_file += ".i"
print("Source file: {0}\nTarget File: {1}\n\t{2}".format(src_file, dst_file, dst_i_file))

try:
    sf = open(src_file, "rb")
    df = open(dst_file, "wb")
    dif = open(dst_i_file, "w")

    buf_tmp = [b'0' for x in range(0, 4)]
    contents = sf.read()
    buf_size = contents.__len__()
    # 不足4个字节,自动补0
    extra_size = (buf_size % 4)
    if extra_size > 0:
        buf_size += (4 - extra_size)
        contents = contents + b'0000'

    for i in range(0, buf_size, 4):
        buf_tmp[3] = contents[i]
        buf_tmp[2] = contents[i+1]
        buf_tmp[1] = contents[i+2]
        buf_tmp[0] = contents[i+3]

        if (i > 0) and ((i % 16) == 0):
            dif.write("\n")
        for j in range(0, 4):
            dif.write(str.format("0x%02x," % buf_tmp[j]))

        # pack into bytes flow
        tmp_bytes = struct.pack("4B", buf_tmp[0], buf_tmp[1], buf_tmp[2], buf_tmp[3])
        df.write(tmp_bytes)
finally:
    if dif:
        dif.close()
    if sf:
        sf.close()
    if df:
        df.close()
    print("Error Occurs! Convert Failed!")
    exit(1)

print("Convert Completed!")
