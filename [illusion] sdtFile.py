# [ILLUSION]
# GAME: SexyBeach3
# FileType: .sdt
# unserialize illusion old games (.sdt) format files to csv

import os, sys


def read_str(f):
    size = int.from_bytes(f.read(4), 'little')
    s = bytes(map(lambda x: x ^ 0xff, f.read(size))).strip(b'\x00')
    return s


def decode_str(b):
    # default: shift-jis
    global is_cn
    a1, a2 = 'gbk', 'shift-jis' if is_cn else 'shift-jis', 'gbk'
    try:
        return b.decode(a1)
    except:
        return b.decode(a2)


def read_str_to_null(f, sep=''):
    out = []
    while True:
        d = read_str(f)
        if d == b'':
            break
        out.append(decode_str(d))
        f.read(1)
    return sep.join(out)


def read_block(f):
    index = int.from_bytes(f.read(4), 'little')
    out = [str(index)]
    out.append(decode_str(read_str(f)))
    out.append(decode_str(read_str(f)))
    f.read(1)
    f.read(4)
    dia = []
    while (d:= read_str(f)) != b'':
        dia.append(d.decode('gbk'))
        f.read(1)
    out.append(''.join(dia))
    return out


def parse(path, s_path):
    with open(path, 'rb') as f:
        f.read(4)
        file_name = read_str(f).decode('shift-jis')
        print(file_name)
        f.read(8)
        count = int.from_bytes(f.read(8), 'little')
        f.read(4)
        out = []
        for i in range(count):
            flag = f.read(1)[0]
            if flag == 0:
                d = read_str_to_null(f, '\n')
                out.append(d)
            elif flag == 1:
                out.append(','.join(read_block(f)))
            # print(f.tell())
        open(s_path, 'w', encoding='utf-8-sig').write('\n'.join(out))

if __name__ == '__main__':
    path = sys.argv[1]
    if len(sys.argv) >= 3:
        is_cn = False if sys.argv[2] == 0 else True
    else:
        id_cn = False
    dir_, fn = os.path.split(path)
    parse(path, os.path.join(dir_, fn.replace('.sdt', '.csv')))
