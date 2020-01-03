import socket

class Client:
    def __init__(self, name=''):
        self.client_data = {"name":name,
                            "host":'',
                            "port":8080,
                            "conn":socket.socket()}

    def connect(self, host, port=8080):
        self.client_data["host"] = host
        self.client_data["port"] = port
        self.client_data["conn"].connect((host, port))
        self.send_msg(self.client_data["name"])

    def send_msg(self, text=''):
        self.client_data["conn"].send(str(text).encode('UTF-8'))
        print("Message sent")

    def recv_msg(self, size=1024):
        return self.client_data["conn"].recv(size).decode()
            
    def send_file(self, file_path, byte_size=2048):
        file_obj = open(file_path, 'rb')
        file_data = file_obj.read()
        file_size = len(file_data)
        self.client_data["conn"].send("SZ:{}".format(file_size).encode('UTF-8'))
        self.client_data["conn"].recv(1)
        for i in range(0, file_size, byte_size):
            self.client_data["conn"].send(file_data[:byte_size])
            self.client_data["conn"].recv(1).decode()
            file_data = file_data[byte_size:]
        print("File sent")

    def close(self):
        self.client_data["conn"].close()
        