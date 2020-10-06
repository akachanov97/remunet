import os
import socket

import rns


class RemouteController(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(RemouteController, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.__host = os.getenv("REMUSERVER_HOST", "localhost")
        self.__port = int(os.getenv("REMUSERVER_PORT", 10001))

        self.__local_storage = os.getenv("LOCAL_STORAGE", "tmp_storage")

    @property
    def server(self):
        return "{}:{}".format(self.__host, self.__port)

    @staticmethod
    def __build_log(msg):
        package = rns.RNS(_code=rns.Code.OUTPUT, _buffer=msg)
        return package.pack()

    @staticmethod
    def __build_request(msg):
        package = rns.RNS(_code=rns.Code.COMMAND, _buffer=msg)
        return package.pack()

    @staticmethod
    def __fmt(raw_resp):
        pkg = rns.RNS()
        pkg.unpack(raw_resp)

        if pkg.code == rns.Code.RESPONSE_OK.value:
            return True
        elif pkg.code == rns.Code.COMMAND.value:
            return pkg.buffer
        elif pkg.code == rns.Code.RESPONSE_INT.value:
            raise KeyboardInterrupt
        else:
            return None

    def __send(self, pkg):
        __socket = socket.socket()
        try:

            __socket.connect((self.__host, self.__port))
            __socket.send(pkg)
            respose = __socket.recv(1024)
        except ConnectionRefusedError:
            print("Error! Host \"{}\" not allowed!".format(self.server))
            return False
        finally:
            __socket.close()

        return self.__fmt(respose)

    def __dump(self, pkg):
        with open(self.__local_storage, "ab") as _output:
            _output.write(pkg+b'\n')

    def write(self, msg):
        pkg = self.__build_log(msg)
        if self.__send(pkg):
            return
        
        self.__dump(pkg)

    def input(self, msg):
        pkg = self.__build_request(msg)
        response = self.__send(pkg)
        if not response:
            return ""

        return response
