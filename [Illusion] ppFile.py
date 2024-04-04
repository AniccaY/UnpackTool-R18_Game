# [ILLUSION] 
# GAME: RapeLay
# FileType: .pp

import os
from io import BytesIO


def decode(s: bytes, encoding=None):
    if encoding is None:
        return bytes(map(lambda x: (-x) & 0xff, s))
    return bytes(map(lambda x: (-x) & 0xff, s)).decode(encoding)


def encode(s: bytes):
    return bytes(map(lambda x: (-x) & 0xff, s))


class FileItem:
    name: str
    size: int
    data: bytes | bytearray

    def __init__(self, name: bytes | str, size=0, data=None):
        self.name = decode(name, 'ascii') if isinstance(name, bytes) else name
        self.size = size
        self._data = data

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, d):
        self._data = b'' if d is None else decode(d)

    def save_as_file(self, dst_path):
        if not os.path.exists(dst_path):
            os.makedirs(dst_path, exist_ok=True)
        with open(os.path.join(dst_path, self.name), 'wb') as f:
            f.write(self.data)

    def __str__(self):
        return f'< {self.name} | {self.size} >'

    def __repr__(self):
        return self.__str__()


def unpack(path, s_dir):
    dir_, file = os.path.split(path)
    with open(path, 'rb') as f:
        count = int.from_bytes(f.read(4), 'little')
        size = f.read(4)
        out = []
        for i in range(count):
            out.append(FileItem(f.read(32).strip(b'\x00')))

        for i in range(count):
            out[i].size = int.from_bytes(f.read(4), 'little')

        for i in range(count):
            out[i].data = f.read(out[i].size)
    for i in out:
        i.save_as_file(os.path.join(s_dir, os.path.splitext(file)[0]))


def unpack_pp_files(path: str, s_path: str):
    for file in filter(lambda x: x.endswith('.pp'), os.listdir(path)):
        print(file)
        unpack(os.path.join(path, file), s_path)


def pack(path, s_dir):
    pp_name = os.path.basename(path)
    count = 0
    size = 0
    writer = open(os.path.join(s_dir, f'{pp_name}.pp'), 'wb')

    file_names, file_sizes, data_writer = list(), list(), list()

    for file in os.listdir(path):
        with open(os.path.join(path, file), 'rb') as f:
            data = f.read()
            count += 1
            size += len(data)
            file_names.append(encode(file.encode('ascii')).ljust(32, b'\x00'))
            file_sizes.append(int.to_bytes(len(data), 4, 'little'))
            data_writer.append(encode(data))
    writer.write(int.to_bytes(count, 4, 'little'))
    writer.write(int.to_bytes(size, 4, 'little'))
    writer.write(b''.join(file_names))
    writer.write(b''.join(file_sizes))
    writer.write(b''.join(data_writer))

    writer.close()


def pack_pp_files(path: str, s_path: str):
    for pp_dir in os.listdir(path):
        if not os.path.isdir(os.path.join(path, pp_dir)):
            continue
        pack(os.path.join(path, pp_dir), s_path)

