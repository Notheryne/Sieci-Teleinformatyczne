import random
import math


def read_binary_data(data_file_name):
    with open(data_file_name, "rb") as binary_file:
        # Read the whole file at once
        binary_data = binary_file.read()
    return binary_data


def write_binary_data(destination_file_name, binary_data, conf="wb"):
    # Pass "wb" to write a new file, or "ab" to append
    with open(destination_file_name, conf) as binary_file:
        # Write text or bytes to the file
        binary_file.write(binary_data)


def even_bit_calc(binary_data):
    result = sum([bin(byte).count("1") for byte in binary_data]) % 2
    # print([bin(byte) for byte in binary_data])
    return result


def modulo_sum(text):
    summary = 0
    for t in text:
        summary += ord(t)
    return summary % 200


def noisy_canal(binary_data, error):
    binary_data_mut = bytearray(binary_data)
    z = len(binary_data_mut)
    no_of_errors = math.ceil(error * len(binary_data_mut))
    indexes = [random.randint(0, len(binary_data_mut))] * no_of_errors
    for i in indexes:
        steer = binary_data_mut[i]
        if steer == 0:
            binary_data_mut[i] = 1
        else:
            binary_data_mut[i] = 0

    return binary_data_mut


original_file = "mydata.txt"
send_file = "writtendata.txt"
binary_data = read_binary_data(original_file)
even = str(even_bit_calc(binary_data))

org_sum = modulo_sum(open(original_file, 'r').read())
send_sum = modulo_sum(open(send_file, 'r').read())

print(org_sum, send_sum)

write_binary_data(send_file, binary_data)
write_binary_data(send_file, even, "a")

binary_data_2 = read_binary_data(send_file)

binary_data_edit = noisy_canal(binary_data_2, 0.1)

even_calc_edit = even_bit_calc(binary_data_edit)
print(even_calc_edit)




