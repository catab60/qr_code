size = 21
level = 1
mask = 7
ec_level = "Q"
message = "HELLO WORLD"
image_size = 30



















no_data_zone = []
no_data_leftSide = []

def after_ecc_var(version, ec_level):
    ec_level_table = {
        1: {"L": 7,"M": 10,"Q": 13,"H": 17},
        2: {"L": 10,"M": 16,"Q": 22,"H": 28},
        3: {"L": 15,"M": 26,"Q": 18,"H": 22},
        4: {"L": 20,"M": 18,"Q": 26,"H": 16},
        5: {"L": 26,"M": 24,"Q": 18,"H": 22},
        6: {"L": 18,"M": 16,"Q": 24,"H": 28},
        7: {"L": 20,"M": 18,"Q": 18,"H": 26},
        8: {"L": 24,"M": 20,"Q": 20,"H": 26},
        9: {"L": 30,"M": 22,"Q": 20,"H": 24},
        10: {"L": 18,"M": 26,"Q": 24,"H": 28},
        11: {"L": 20,"M": 30,"Q": 28,"H": 24},
        12: {"L": 24,"M": 22,"Q": 26,"H": 28},
        13: {"L": 26,"M": 22,"Q": 24,"H": 22},
        14: {"L": 30,"M": 24,"Q": 20,"H": 24},
        15: {"L": 22,"M": 24,"Q": 30,"H": 24},
        16: {"L": 24,"M": 18,"Q": 24,"H": 30},
        17: {"L": 28,"M": 28,"Q": 28,"H": 28},
        18: {"L": 30,"M": 26,"Q": 28,"H": 28},
        19: {"L": 28,"M": 26,"Q": 26,"H": 26},
        20: {"L": 28,"M": 26,"Q": 30,"H": 28},
        21: {"L": 28,"M": 26,"Q": 28,"H": 30},
        22: {"L": 28,"M": 28,"Q": 30,"H": 24},
        23: {"L": 30,"M": 28,"Q": 30,"H": 30},
        24: {"L": 30,"M": 28,"Q": 30,"H": 30},
        25: {"L": 26,"M": 28,"Q": 30,"H": 30},
        26: {"L": 28,"M": 28,"Q": 28,"H": 30},
        27: {"L": 30,"M": 28,"Q": 30,"H": 30},
        28: {"L": 30,"M": 28,"Q": 30,"H": 30},
        29: {"L": 30,"M": 28,"Q": 30,"H": 30},
        30: {"L": 30,"M": 28,"Q": 30,"H": 30},
        31: {"L": 30,"M": 28,"Q": 30,"H": 30},
        32: {"L": 30,"M": 28,"Q": 30,"H": 30},
        33: {"L": 30,"M": 28,"Q": 30,"H": 30},
        34: {"L": 30,"M": 28,"Q": 30,"H": 30},
        35: {"L": 30,"M": 28,"Q": 30,"H": 30},
        36: {"L": 30,"M": 28,"Q": 30,"H": 30},
        37: {"L": 30,"M": 28,"Q": 30,"H": 30},
        38: {"L": 30,"M": 28,"Q": 30,"H": 30},
        39: {"L": 30,"M": 28,"Q": 30,"H": 30},
        40: {"L": 30,"M": 28,"Q": 30,"H": 30},
    }

    if version in ec_level_table and ec_level in ec_level_table[version]:
        return ec_level_table[version][ec_level]



def generate_qr_traversal_order(version=1, k=True, reserved=None):
    if reserved is None:
        reserved = set()
    else:
        reserved = set(reserved)
    
    size = version * 4 + 17
    coordinates = []
    added_coords = set()
    direction_up = True

    if k:
        k = 1
    else:
        k = 2
    

    for col in range(size - k, 0, -2):
        pair = (col, col - 1)
        if direction_up:
            rows = range(size - 1, -1, -1)
        else:
            rows = range(size)
        
        for y in rows:
            for x in pair:
                coord = (x, y)
                if coord not in reserved and coord not in added_coords:
                    coordinates.append(coord)
                    added_coords.add(coord)
        
        direction_up = not direction_up
    
    if size % 2 == 1:
        remaining_col = 0
        if direction_up:
            rows = range(size - 1, -1, -1)
        else:
            rows = range(size)
        
        for y in rows:
            coord = (remaining_col, y)
            if coord not in reserved and coord not in added_coords:
                coordinates.append(coord)
                added_coords.add(coord)
    
    return coordinates



















def encode_qr_data(data, version, ec_level, mode="Alphanumeric"):
    mode_indicators = {
        "Numeric":      "0001",
        "Alphanumeric": "0010",
        "Byte":         "0100",
    }
    if mode not in mode_indicators:
        raise ValueError("Unsupported mode")
    mode_bits = mode_indicators[mode]

    if mode == "Numeric":
        if version >= 1 and version <= 9:
            count_indicator_length = 10
        elif version >= 10 and version <= 26:
            count_indicator_length = 12
        elif version >= 27 and version <= 40:
            count_indicator_length = 14
    elif mode == "Alphanumeric":
        if version >= 1 and version <= 9:
            count_indicator_length = 9
        elif version >= 10 and version <= 26:
            count_indicator_length = 11
        elif version >= 27 and version <= 40:
            count_indicator_length = 13
    elif mode == "Byte":
        if version >= 1 and version <= 9:
            count_indicator_length = 8
        elif version >= 10 and version <= 26:
            count_indicator_length = 16
        elif version >= 27 and version <= 40:
            count_indicator_length = 16
    else:
        count_indicator_length = 0

    encoded_payload = ""
    if mode == "Numeric":
        i = 0
        while i < len(data):
            if i + 3 <= len(data):
                group = data[i:i+3]
                encoded_payload += format(int(group), '010b')
                i += 3
            elif i + 2 == len(data):
                group = data[i:i+2]
                encoded_payload += format(int(group), '07b')
                i += 2
            else:
                group = data[i]
                encoded_payload += format(int(group), '04b')
                i += 1

    elif mode == "Alphanumeric":
        alphanum_table = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:"
        i = 0
        while i < len(data) - 1:
            first = alphanum_table.index(data[i])
            second = alphanum_table.index(data[i+1])
            value = first * 45 + second
            encoded_payload += format(value, '011b')
            i += 2
        if i < len(data):
            value = alphanum_table.index(data[i])
            encoded_payload += format(value, '06b')

    elif mode == "Byte":
        for c in data:
            encoded_payload += format(ord(c), '08b')

    else:
        raise ValueError("Unsupported mode")


    count = len(data) if mode != "ECI" else 0
    count_bits = format(count, '0{}b'.format(count_indicator_length)) if count_indicator_length > 0 else ""
    full_bit_stream = mode_bits + count_bits + encoded_payload


    capacity_table = {
        1: {"L": 19, "M": 16, "Q": 13, "H": 9},
        2: {"L": 34, "M": 28, "Q": 22, "H": 16},
        3: {"L": 55, "M": 44, "Q": 34, "H": 26},
        4: {"L": 80, "M": 64, "Q": 48, "H": 36},
        5: {"L": 108, "M": 86, "Q": 62, "H": 46},
        6: {"L": 136, "M": 108, "Q": 76, "H": 60},
        7: {"L": 156, "M": 124, "Q": 88, "H": 66},
        8: {"L": 194, "M": 154, "Q": 110, "H": 86},
        9: {"L": 232, "M": 182, "Q": 132, "H": 100},
        10: {"L": 274, "M": 216, "Q": 154, "H": 122},
        11: {"L": 324, "M": 254, "Q": 180, "H": 140},
        12: {"L": 370, "M": 290, "Q": 206, "H": 158},
        13: {"L": 428, "M": 334, "Q": 244, "H": 180},
        14: {"L": 461, "M": 365, "Q": 261, "H": 197},
        15: {"L": 523, "M": 415, "Q": 295, "H": 223},
        16: {"L": 589, "M": 453, "Q": 325, "H": 253},
        17: {"L": 647, "M": 507, "Q": 367, "H": 283},
        18: {"L": 721, "M": 563, "Q": 397, "H": 313},
        19: {"L": 795, "M": 627, "Q": 445, "H": 341},
        20: {"L": 861, "M": 669, "Q": 485, "H": 385},
        21: {"L": 932, "M": 714, "Q": 512, "H": 406},
        22: {"L": 1006, "M": 782, "Q": 568, "H": 442},
        23: {"L": 1094, "M": 860, "Q": 614, "H": 464},
        24: {"L": 1174, "M": 914, "Q": 664, "H": 514},
        25: {"L": 1276, "M": 1000, "Q": 718, "H": 538},
        26: {"L": 1370, "M": 1062, "Q": 754, "H": 596},
        27: {"L": 1468, "M": 1128, "Q": 808, "H": 628},
        28: {"L": 1531, "M": 1193, "Q": 871, "H": 661},
        29: {"L": 1631, "M": 1267, "Q": 911, "H": 701},
        30: {"L": 1735, "M": 1373, "Q": 985, "H": 745},
        31: {"L": 1843, "M": 1455, "Q": 1033, "H": 793},
        32: {"L": 1955, "M": 1541, "Q": 1115, "H": 845},
        33: {"L": 2071, "M": 1631, "Q": 1171, "H": 901},
        34: {"L": 2191, "M": 1725, "Q": 1231, "H": 961},
        35: {"L": 2306, "M": 1812, "Q": 1286, "H": 986},
        36: {"L": 2434, "M": 1914, "Q": 1354, "H": 1054},
        37: {"L": 2566, "M": 1992, "Q": 1426, "H": 1096},
        38: {"L": 2702, "M": 2102, "Q": 1502, "H": 1142},
        39: {"L": 2812, "M": 2216, "Q": 1582, "H": 1222},
        40: {"L": 2956, "M": 2334, "Q": 1666, "H": 1276}
    }
    if version in capacity_table and ec_level in capacity_table[version]:
        capacity = capacity_table[version][ec_level] * 8
    else:
        raise ValueError("Unsupported version or error correction level")


    if len(full_bit_stream) < capacity:
        terminator_length = min(4, capacity - len(full_bit_stream))
        full_bit_stream += "0" * terminator_length


    while len(full_bit_stream) % 8 != 0:
        full_bit_stream += "0"

    pad_bytes = ["11101100", "00010001"]
    pad_index = 0
    while len(full_bit_stream) < capacity:
        full_bit_stream += pad_bytes[pad_index % 2]
        pad_index += 1


    full_bit_stream = full_bit_stream[:capacity]


    codewords = " ".join(full_bit_stream[i:i+8] for i in range(0, len(full_bit_stream), 8))
    return codewords

















def generate_final_codewords(encoded_bit_string, ec_count):

    data_codewords = [int(b, 2) for b in encoded_bit_string.split()]
    

    gf_exp = [0] * 512
    gf_log = [0] * 256
    x = 1
    for i in range(255):
        gf_exp[i] = x
        gf_log[x] = i
        x <<= 1
        if x & 0x100:
            x ^= 0x11D
    for i in range(255, 512):
        gf_exp[i] = gf_exp[i - 255]
    

    def gf_mul(a, b):
        if a == 0 or b == 0:
            return 0
        return gf_exp[(gf_log[a] + gf_log[b]) % 255]
    

    generator = [1]
    for i in range(ec_count):
        generator = [gf_mul(g, gf_exp[i]) ^ (generator[j] if j < len(generator) else 0)
                     for j, g in enumerate([0] + generator)]
    

    msg_poly = data_codewords + [0] * ec_count
    for i in range(len(data_codewords)):
        coef = msg_poly[i]
        if coef != 0:
            for j in range(len(generator)):
                msg_poly[i + j] ^= gf_mul(generator[j], coef)
    

    ec_codewords = msg_poly[-ec_count:]
    
    return [format(cw, '08b') for cw in data_codewords + ec_codewords]









def mark_leftside(debug=False):
    startpoint = (0,9)
    em = []

    for i in range(startpoint[0], 6):
        for j in range(startpoint[1],size-8):
            if debug:
                cells[i][j].config(bg="green")
            em.append((i,j))
    
    
    return em





def create_black_white_bmp(matrix, filename="output.bmp", pixel_size=1):

    n = len(matrix)
    bordered_matrix = [[0] * (n + 4) for _ in range(2)]
    for row in matrix:
        bordered_matrix.append([0, 0] + row + [0, 0])
    bordered_matrix.extend([[0] * (n + 4) for _ in range(2)])

    n_bordered = len(bordered_matrix)
    scaled_width = n_bordered * pixel_size
    scaled_height = n_bordered * pixel_size
    file_size = 54 + 3 * scaled_width * scaled_height
    bmp_header = bytearray([
        0x42, 0x4D,
        file_size & 0xFF, (file_size >> 8) & 0xFF, (file_size >> 16) & 0xFF, (file_size >> 24) & 0xFF,
        0, 0, 0, 0,
        54, 0, 0, 0
    ])
    dib_header = bytearray([
        40, 0, 0, 0,
        scaled_width & 0xFF, (scaled_width >> 8) & 0xFF, (scaled_width >> 16) & 0xFF, (scaled_width >> 24) & 0xFF,
        scaled_height & 0xFF, (scaled_height >> 8) & 0xFF, (scaled_height >> 16) & 0xFF, (scaled_height >> 24) & 0xFF,
        1, 0,
        24, 0,
        0, 0, 0, 0,
        0, 0, 0, 0,
        0, 0, 0, 0,
        0, 0, 0, 0,
        0, 0, 0, 0,
        0, 0, 0, 0
    ])
    pixel_data = bytearray()
    for row in reversed(bordered_matrix):
        for _ in range(pixel_size):
            for pixel in row:
                color = [255, 255, 255] if pixel == 0 else [0, 0, 0]
                for _ in range(pixel_size):
                    pixel_data.extend(color)
            padding = (4 - (scaled_width * 3) % 4) % 4
            pixel_data.extend([0] * padding)
    with open(filename, "wb") as f:
        f.write(bmp_header)
        f.write(dib_header)
        f.write(pixel_data)












def get_qr_mask(level, index):
    qr_masks = {
        "L": ["111011111000100", "111001011110011", "111110110101010", "111100010011101", "110011000101111", "110001100011000", "110110001000001", "110100101110110"],
        "M": ["101010000010010", "101000100100101", "101111001111100", "101101101001011", "100010111111001", "100000011001110", "100111110010111", "100101010100000"],
        "Q": ["011010101011111", "011000001101000", "011111100110001", "011101000000110", "010010010110100", "010000110000011", "010111011011010", "010101111101101"],
        "H": ["001011010001001", "001001110111110", "001110011100111", "001100111010000", "000011101100010", "000001001010101", "000110100001100", "000100000111011"]
    }
    return qr_masks.get(level, [None])[index-1]

def get_version_mask(ver):
    version_values = {
        7: "000111110010010100",
        8: "001000010110111100",
        9: "001001101010011001",
        10: "001010010011010011",
        11: "001011101111110110",
        12: "001100011101100010",
        13: "001101100001000111",
        14: "001110011000001101",
        15: "001111100100101000",
        16: "010000101101111000",
        17: "010001010001011101",
        18: "010010101000010111",
        19: "010011010100110010",
        20: "010100100110100110",
        21: "010101011010000011",
        22: "010110100011001001",
        23: "010111011111101100",
        24: "011000111011000100",
        25: "011001000111100001",
        26: "011010111110101011",
        27: "011011000010001110",
        28: "011100110000011010",
        29: "011101001100111111",
        30: "011110110101110101",
        31: "011111001001010000",
        32: "100000100111010101",
        33: "100001011011110000",
        34: "100010100010111010",
        35: "100011011110011111",
        36: "100100101100001011",
        37: "100101010000101110",
        38: "100110101001100100",
        39: "100111010101000001",
        40: "101000110001101001",
    }
    return version_values.get(ver, [None])

def apply_version_mask(code):
    f_v = {
        0:[(0,size-11),(size-11,0)],
        1:[(0,size-10),(size-10,0)],
        2:[(0,size-9),(size-9,0)],
        3:[(1,size-11),(size-11,1)],
        4:[(1,size-10),(size-10,1)],
        5:[(1,size-9),(size-9,1)],
        6:[(2,size-11),(size-11,2)],
        7:[(2,size-10),(size-10,2)],
        8:[(2,size-9),(size-9,2)],
        9:[(3,size-11),(size-11,3)],
        10:[(3,size-10),(size-10,3)],
        11:[(3,size-9),(size-9,3)],
        12:[(4,size-11),(size-11,4)],
        13:[(4,size-10),(size-10,4)],
        14:[(4,size-9),(size-9,4)],
        15:[(5,size-11),(size-11,5)],
        16:[(5,size-10),(size-10,5)],
        17:[(5,size-9),(size-9,5)],
    }

    for key, value in f_v.items():
        for i in value:
            if code[key] == "1":
                cells[i[0]][i[1]] = 1



def apply_qr_mask(code, debug=False):
    f_n = {
        0:[(0,8), (8, size-1)],
        1:[(1,8), (8, size-2)],
        2:[(2,8), (8, size-3)],
        3:[(3,8), (8, size-4)],
        4:[(4,8), (8, size-5)],
        5:[(5,8), (8, size-6)],
        6:[(7,8), (8, size-7)],
        7:[(8,8), (size-8, 8)],
        8:[(8,7), (size-7, 8)],
        9:[(8,5), (size-6, 8)],
        10:[(8,4), (size-5, 8)],
        11:[(8,3), (size-4, 8)],
        12:[(8,2), (size-3, 8)],
        13:[(8,1), (size-2, 8)],
        14:[(8,0), (size-1, 8)],
    }
    for key, value in f_n.items():
        for i in value:
            if debug:
                if key%2==0:
                    cells[i[0]][i[1]].config(bg="blue")
                else:
                    cells[i[0]][i[1]].config(bg="yellow")
            else:
                if code[key] == "1":
                    cells[i[0]][i[1]] = 1
                    no_data_zone.append((i[0],i[1]))
                else:
                    no_data_zone.append((i[0],i[1]))


    dark_module = cells[8][size-8] = 1
    no_data_zone.append((8,size-8))










    
    

cells = []

for i in range(size):
    line = []
    for j in range(size):
        line.append(0)
    cells.append(line)


def add_position_identifier():
    for i in range(7):
        for j in range(7):
            if i==0 or j==0 or i==6 or j==6:
                cells[i][j] = 1
            if i>=2 and i<=4 and j>=2 and j<=4:
                cells[i][j] = 1
            no_data_zone.append((i, j))

    for i in range(7):
        for j in range(7):
            if i==0 or j==0 or i==6 or j==6:
                cells[i+size-7][j] = 1

            if i>=2 and i<=4 and j>=2 and j<=4:
                cells[i+size-7][j] = 1

            no_data_zone.append((i+size-7, j))

    for i in range(7):
        for j in range(7):
            if i==0 or j==0 or i==6 or j==6:
                cells[i][j+size-7] = 1
            if i>=2 and i<=4 and j>=2 and j<=4:
                cells[i][j+size-7] = 1
            
            no_data_zone.append((i, j+size-7))


    for i in range(8):
        no_data_zone.append((i, 7))
        no_data_zone.append((7, i))

        no_data_zone.append((i+size-8, 7))
        no_data_zone.append((size-8, i))

        no_data_zone.append((i, size-8))
        no_data_zone.append((7, i+size-8))

    

    

def add_timing_structure():
    first_start_point = (6, size-(7+2))
    first_current_cell = first_start_point
    second_start_point = (8, 6)
    second_current_cell = second_start_point
    cells[first_start_point[0]][first_start_point[1]] = 1
    cells[second_start_point[0]][second_start_point[1]] = 1

    while(first_current_cell[1]>7):
        no_data_zone.append((first_current_cell[0], first_current_cell[1]))
        no_data_zone.append((first_current_cell[0], first_current_cell[1]-1))
        cells[first_current_cell[0]][first_current_cell[1]] = 1
        first_current_cell=(first_current_cell[0], first_current_cell[1]-2)

    while(second_current_cell[0]<size-7):
        no_data_zone.append((second_current_cell[0], second_current_cell[1]))
        no_data_zone.append((second_current_cell[0]-1, second_current_cell[1]))
        cells[second_current_cell[0]][second_current_cell[1]] = 1
        second_current_cell=(second_current_cell[0]+2, second_current_cell[1])



def add_mask(mask_type):
    for (row, column) in FINAL_ORDER:
        if mask_type == 0 and (row + column) % 2 == 0:
            if cells[column][row] == 1:
                cells[column][row] = 0
            elif cells[column][row] == 0:
                cells[column][row] = 1
        elif mask_type == 1 and row % 2 == 0:
            if cells[column][row] == 1:
                cells[column][row] = 0
            elif cells[column][row] == 0:
                cells[column][row] = 1
        elif mask_type == 2 and column % 3 == 0:
            if cells[column][row] == 1:
                cells[column][row] = 0
            elif cells[column][row] == 0:
                cells[column][row] = 1
        elif mask_type == 3 and (row + column) % 3 == 0:
            if cells[column][row] == 1:
                cells[column][row] = 0
            elif cells[column][row] == 0:
                cells[column][row] = 1
        elif mask_type == 4 and ((row // 2) + (column // 3)) % 2 == 0:
            if cells[column][row] == 1:
                cells[column][row] = 0
            elif cells[column][row] == 0:
                cells[column][row] = 1
        elif mask_type == 5 and ((row * column) % 2) + ((row * column) % 3) == 0:
            if cells[column][row] == 1:
                cells[column][row] = 0
            elif cells[column][row] == 0:
                cells[column][row] = 1
        elif mask_type == 6 and (((row * column) % 2) + ((row * column) % 3)) % 2 == 0:
            if cells[column][row] == 1:
                cells[column][row] = 0
            elif cells[column][row] == 0:
                cells[column][row] = 1
        elif mask_type == 7 and (((row + column) % 2) + ((row * column) % 3)) % 2 == 0:
            if cells[column][row] == 1:
                cells[column][row] = 0
            elif cells[column][row] == 0:
                cells[column][row] = 1




def place_alignment_patterns(version):
    grid_size = 21 + 4 * (version - 1)
    if version == 1:
        return []
    n_align = version // 7 + 2
    if n_align == 2:
        alignment_positions = [6, grid_size - 7]
    else:
        step = (grid_size - 13) // (n_align - 1)
        if step % 2 == 1:
            step += 1
        alignment_positions = [6] + [6 + i * step for i in range(1, n_align - 1)] + [grid_size - 7]

    finder_overlap = {
        (alignment_positions[0], alignment_positions[0]),
        (alignment_positions[0], alignment_positions[-1]),
        (alignment_positions[-1], alignment_positions[0])
    }

    for x in alignment_positions:
        for y in alignment_positions:
            if (x, y) in finder_overlap:
                continue
            cells[y][x] = 1
            for i in range(-2,3):
                for j in range(-2,3):
                    cells[y+i][x+j] = 1
                
                    no_data_zone.append((y+i, x+j))
            
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if not (i==0 and j==0):
                        cells[y+i][x+j] = 0

            

    return alignment_positions





binary_string = encode_qr_data(data=message, version=level, ec_level=ec_level, mode="Alphanumeric")
codewords = generate_final_codewords(binary_string, after_ecc_var(level, ec_level))




add_position_identifier() 
place_alignment_patterns(level)
add_timing_structure()






apply_qr_mask(get_qr_mask(ec_level, mask))


if level >= 7:
    apply_version_mask(get_version_mask(level)[::-1])






orderRIGHT = generate_qr_traversal_order(level, True,no_data_zone+mark_leftside())
no_data_zone += orderRIGHT
orderLEFT = generate_qr_traversal_order(level, False,no_data_zone)





FINAL_ORDER = orderRIGHT + orderLEFT




finalEMBED = ""
for i in codewords:
    finalEMBED += str(i)









for i in range(len(FINAL_ORDER)):
    if finalEMBED[i]=="1":
        cells[FINAL_ORDER[i][0]][FINAL_ORDER[i][1]] = 1




add_mask(mask-1)




FINAL_MATRIX = []

for i in range(size):
    line = []
    for j in range(size):
        line.append(0)
    FINAL_MATRIX.append(line)



for i in range(size):
    for j in range(size):
        if cells[i][j] == 1:
            FINAL_MATRIX[j][i] = 1



create_black_white_bmp(FINAL_MATRIX, pixel_size=image_size)


