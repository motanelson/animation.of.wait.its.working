import struct

def create_empty_sector():
    return bytearray(2048)

def create_pvd(volume_name="MYISO"):
    total_sectors = 20
    pvd = bytearray(2048)
    pvd[0:1] = b'\x01'
    pvd[1:6] = b'CD001'
    pvd[6:7] = b'\x01'
    pvd[40:72] = volume_name.ljust(32).encode('ascii')
    pvd[80:84] = struct.pack('<I', total_sectors)
    pvd[84:88] = struct.pack('>I', total_sectors)
    return pvd

def create_directory_record(name, start_sector, size, is_file=True):
    record = bytearray(34 + len(name))
    record[0:1] = struct.pack('B', len(record))
    record[2:6] = struct.pack('<I', start_sector)
    record[10:14] = struct.pack('<I', size)
    record[25:26] = struct.pack('B', 1 if is_file else 2)
    record[32:33] = struct.pack('B', len(name))
    record[33:33+len(name)] = name.encode('ascii')
    return record

def create_root_directory():
    root_dir = bytearray(2048)
    root_dir[0:34] = create_directory_record(".", 17, 1024, is_file=False)
    root_dir[34:68] = create_directory_record("..", 17, 1024, is_file=False)
    root_dir[68:102] = create_directory_record("HELLO.TXT;1", 18, 11, is_file=True)
    return root_dir

def create_data_area(content):
    data = bytearray(2048)
    data[0:len(content)] = content.encode('ascii')
    return data

def create_iso(output_file="my_iso.iso"):
    with open(output_file, "wb") as iso_file:
        for _ in range(16):
            iso_file.write(create_empty_sector())
        iso_file.write(create_pvd())
        iso_file.write(create_root_directory())
        iso_file.write(create_data_area("hello world"))
        for _ in range(19, 20):
            iso_file.write(create_empty_sector())

    print(f"ISO criada com sucesso: {output_file}")

create_iso()
