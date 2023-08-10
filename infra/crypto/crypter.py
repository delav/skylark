import base64
from Crypto.Cipher import AES
from django.conf import settings

# 16/24/32位
aes_key = settings.AES_KEY


def ecb_encrypt(plain_text: str):
    # 填充
    plain_text = bytes(plain_text.encode('utf8'))
    bytes_num_to_pad = AES.block_size - (len(plain_text) % AES.block_size)
    byte_to_pad = bytes([bytes_num_to_pad])
    padding = byte_to_pad * bytes_num_to_pad
    plain_text = plain_text + padding
    # aes加密
    model = AES.MODE_ECB  # 定义模式
    aes = AES.new(aes_key.encode('utf8'), model)  # 创建一个aes对象
    en_text = aes.encrypt(plain_text)  # 加密明文
    en_text = base64.encodebytes(en_text)  # 将返回的字节型数据转进行base64编码
    en_text = en_text.decode('utf8')  # 将字节型数据转换成python中的字符串类型
    result = en_text.strip()
    return result


def ecb_decrypt(encrypt_text: str):
    key_bytes = bytes(aes_key, encoding='utf8')
    cipher = AES.new(key_bytes, AES.MODE_ECB)
    # base64解码
    aes_encode_bytes = base64.b64decode(encrypt_text)
    # 解密
    aes_decode_bytes = cipher.decrypt(aes_encode_bytes)
    # 重新编码
    text = str(aes_decode_bytes, encoding='utf8')
    # 去除填充内容
    length = len(text)
    un_padding = ord(text[length - 1])
    result = text[0:length - un_padding]
    return result


if __name__ == '__main__':
    print(ecb_encrypt('123456'))