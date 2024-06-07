# [Jellyfish]
# GAME: sisters～夏の最後の日～ (Sisters: Last Day of Summer)
# FileType: .isa
# unpack/repack "Sisters: Last Day of Summer" (.isa) format files;
# GameVersion: English from Steam

import os


def unpack_isa(path: str, output_path: str):
    with open(path, 'rb') as f:
        sig = f.read(12)
        if sig != b'ISM ENGLISH ':
            raise "Error sign"
        os.makedirs(output_path, exist_ok=True)
        count = int.from_bytes(f.read(4), 'little')
        for _ in range(count):
            meta_data = f.read(64)
            file_name = meta_data[:meta_data.find(b'\x00')].decode('shift-jis')
            file_ptr = int.from_bytes(meta_data[52:56], 'little')
            file_size = int.from_bytes(meta_data[56:60], 'little')

            pos = f.tell()
            f.seek(file_ptr)
            open(os.path.join(output_path, file_name), 'wb').write(f.read(file_size))
            f.seek(pos)


def pack_isa(path_dir: str, output_dir: str):
    file_name = os.path.basename(path_dir) + '.isa'
    with open(os.path.join(output_dir, file_name), 'wb') as fw:
        fw.write(b'ISM ENGLISH ')
        files = os.listdir(path_dir)
        fw.write(int.to_bytes(len(files), 4, 'little'))
        metas = []
        fw.write(bytes(64 * len(files)))
        ptr = fw.tell()
        for file in files:
            with open(os.path.join(path_dir, file), 'rb') as f:
                data = f.read()

                metas.append(b''.join((file.encode('shift-jis').ljust(52, b'\x00'),
                                       int.to_bytes(ptr, 4, 'little'),
                                       int.to_bytes(len(data), 4, 'little'),
                                       bytes(4))))
                ptr += fw.write(data)
        fw.seek(16)
        fw.write(b''.join(metas))


def test_unpack():
    path = r"D:\Sisters\data"
    s_path = r"D:\Sisters\unpack"
    for file in filter(lambda x: x.endswith('.isa'), os.listdir(path)):
        unpack_isa(os.path.join(path, file), os.path.join(s_path, file.split('.')[0]))


def test_pack():
    path = r"D:\Sisters\unpack"
    s_path = r"D:\Sisters\out"
    os.makedirs(s_path, exist_ok=True)
    for dir_ in os.listdir(path):
        pack_isa(os.path.join(path, dir_), s_path)
