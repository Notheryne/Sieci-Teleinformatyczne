class Packet:
    def __init__(self, number, data):
        self.number = number
        self.data = data


def read_binary_data(data_file_name):
    with open(data_file_name, "rb") as binary_file:
        # Read the whole file at once
        return binary_file.read()


def convert(bytes_data):
    return [bin(byte) for byte in bytes_data]


