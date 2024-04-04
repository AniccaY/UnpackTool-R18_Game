def decrypt(data: bytearray):
    key = [255, 255, 255, 21, 80, 15, 255, 255, 255, 202, 2, 255, 21, 80, 255]
    for i in range(len(data)):
        data[i] = data[i] ^ key[i % len(key)]

