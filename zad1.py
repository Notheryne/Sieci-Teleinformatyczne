import random


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


def even_calc(binary_data):
    """
    checking that bytes are even or not in message
    """
    result = sum([bin(byte).count("1") for byte in binary_data]) % 2
    # print([bin(byte) for byte in binary_data])
    return result


def modulo_sum_100(binary_data):
    """
    checking noise on canal by modulo 100 from sum of chars' ASCII
    """
    return sum(binary_data) % 100


def noisy_canal(binary_data, repeat=True, frequency=0.1):
    """
    creating noise on canal by binary change
    """
    noise = random.randrange(1, 8)
    noise = pow(2, noise)
    binary_data_mut = bytearray(binary_data)
    number_of_noises = int(len(binary_data_mut) * frequency)

    noises_indexes = []

    if repeat:
        for _ in range(1, number_of_noises + 1):
            while True:
                new_append = random.randrange(0, len(binary_data_mut))
                if new_append not in noises_indexes:
                    noises_indexes.append(new_append)
                    break
    else:
        noises_indexes.append(random.randrange(0, len(binary_data_mut)))

    for i in noises_indexes:
        binary_data_mut[i] = binary_data_mut[i] ^ noise
        # binary_data_mut[i] = binary_data_mut[i]&(~(binary_data_mut[i]&noise))

    return binary_data_mut


def xor(a, b):
    result = []

    for i in range(1, len(b)):
        if a[i] == b[i]:
            result.append('0')
        else:
            result.append('1')

    return ''.join(result)


def mod2div(divident, divisor):
    pick = len(divisor)

    tmp = divident[0: pick]

    while pick < len(divident):

        if tmp[0] == '1':
            tmp = xor(divisor, tmp) + divident[pick]
        else:
            tmp = xor('0' * pick, tmp) + divident[pick]

        pick += 1

    if tmp[0] == '1':
        tmp = xor(divisor, tmp)
    else:
        tmp = xor('0' * pick, tmp)

    result = tmp
    return result


def CRC(binary_data):
    global crc_length
    binary_string = ''.join([(bin(x)[2:]) for x in binary_data])
    crc_divider = '100011010'
    crc_length = len(crc_divider) - 1
    check = mod2div(binary_string, crc_divider)

    return check


#############################################################################

original_file = "image.jpg"
send_file = "writtendata.txt"
# reading data from file
binary_data = read_binary_data(original_file)
# print(binary_data)
# print("XXXXXXX")
# [print(bin(x)) for x in binary_data]
# print("XXXXXXX")
# print([bin(byte).count("1") for byte in binary_data])
# print([bin(byte).count("0") for byte in binary_data])
# calculating even number of stream
even_num = str(even_calc(binary_data))
# calculating modulo sum 100 num of stream
mod_num = str(modulo_sum_100(binary_data))
# calculating CRC
crc_num = CRC(binary_data)
# write to file read data
write_binary_data(send_file, binary_data)
# write calculated even number
write_binary_data(send_file, even_num, "a")
# write calculated modulo number
write_binary_data(send_file, mod_num, "a")
# write calculated CRC
write_binary_data(send_file, crc_num, "a")

# read written data
binary_data_2 = read_binary_data(send_file)
# read written even number
even_num_2 = str(int(binary_data_2[-(crc_length + 3):-(crc_length + 2)]))
mod_num_2 = str(int(binary_data_2[-(crc_length + 2):-crc_length]))
crc_num_2 = str(int(binary_data_2[-crc_length:]))
binary_data_2 = binary_data_2[:-(crc_length + 3)]

# make noise on data
binary_data_edit = noisy_canal(binary_data_2)

binary_data_3 = bytes(binary_data_edit)

even_num_3 = str(even_calc(binary_data_3))
mod_num_3 = str(modulo_sum_100(binary_data_3))
crc_num_3 = CRC(binary_data_3)
print("FIRST EVEN NUM vs. NOISED EVEN NUM")
print(even_num_2 + "      :       " + even_num_3)
print("FIRST MOD NUM vs. NOISED MOD NUM")
print(mod_num_2 + "      :       " + mod_num_3)
print("FIRST CRC NUM vs. NOISED CRC NUM")
print(crc_num_2 + "      :       " + crc_num_3)
#############################################################################