# -*- coding: utf-8 -*-

# 校验和的守卫，调试用。真实打包用的代码不开源
class ChecksumGuard():
    def get_checksum(self, data):
        return b'\7'*32
    def valid_checksum(self, data, checksum):
        return False



