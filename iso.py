import struct

# Setor vazio (2048 bytes)
def create_empty_sector():
    return bytearray(2048)

# Primary Volume Descriptor (PVD)
def create_pvd(volume_name="MYISO"):
    total_sectors = 20
    pvd = bytearray(2048)
    pvd[0:1] = b'\x01'  # Tipo de descritor
    pvd[1:6] = b'CD001'  # Identificador ISO
    pvd[6:7] = b'\x01'  # Versão do descritor
    for n in range(7,40):
        nn=n+1
        pvd[n:nn] = b'\x20'
    pvd[40:72] = volume_name.ljust(32).encode('ascii')  # Nome do volume
    pvd[80:84] = struct.pack('<I', total_sectors)  # Número total de setores (little-endian)
    pvd[84:88] = struct.pack('>I', total_sectors)  # Número total de setores (big-endian)
    pvd[120:121] = b'\x01'
    pvd[123:124] = b'\x01'
    pvd[124:125] = b'\x01'
    pvd[127:128] = b'\x01'
    pvd[129:130] = b'\x08'
    pvd[130:131] = b'\x08'
    pvd[132:133] = b'\x0A'
    pvd[139:140] = b'\x0A'
    pvd[140:141] = b'\x16'
    pvd[151:152] = b'\x17'
    pvd[156:157] = b'\x22'
    pvd[158:162] = struct.pack('<I', 18)  # Número total de setores (little-endian)
    pvd[165:169] = struct.pack('<I', 18)  # Número total de setores (little-endian)
    pvd[172:173] = b'\x08'
    pvd[174:175] = b'\x7d'
    pvd[175:176] = b'\x01'
    pvd[176:177] = b'\x1a'
    pvd[177:178] = b'\x13'
    pvd[179:180] = b'\x1c'
    pvd[181:182] = b'\x02'
    pvd[184:185] = b'\x01'
    pvd[187:188] = b'\x01'
    pvd[188:189] = b'\x01'
    for n in range(0xbe,0x36f):
        nn=n+1
        pvd[n:nn] = b'\x20'
    return pvd

# Registro de diretório alinhado
def create_directory_record(name, start_sector, size, is_file=True):
    record_length = 34 + len(name)
    record = bytearray(record_length)
    record[0:1] = struct.pack('B', record_length)  # Tamanho do registro
    record[2:6] = struct.pack('<I', start_sector)  # Setor inicial
    record[10:14] = struct.pack('<I', size)  # Tamanho do arquivo
    record[25:26] = struct.pack('B', 1 if is_file else 2)  # Flags (1 = arquivo)
    record[32:33] = struct.pack('B', len(name))  # Comprimento do nome
    record[33:33 + len(name)] = name.encode('ascii')  # Nome
    return record

# Diretório raiz com alinhamento correto
def create_root_directory():
    root_dir = bytearray(2048)
    current_dir = create_directory_record(".", 17, 2048, is_file=False)
    parent_dir = create_directory_record("..", 17, 2048, is_file=False)
    hello_file = create_directory_record("HELLO.TXT", 18, 11, is_file=True)
    
    # Adiciona os registros ao setor e preenche com zeros se necessário
    entries = current_dir + parent_dir + hello_file
    root_dir[0:len(entries)] = entries
    return root_dir

# Conteúdo do arquivo
def create_data_area(content):
    data = bytearray(2048)
    data[0:len(content)] = content.encode('ascii')
    return data

# Função principal para criar o ISO
def create_iso(output_file="my_iso.iso"):
    with open(output_file, "wb") as iso_file:
        # 16 setores vazios reservados
        for _ in range(16):
            iso_file.write(create_empty_sector())
        
        # Setor 16: PVD
        iso_file.write(create_pvd())
        
        # Setor 17: Diretório raiz
        iso_file.write(create_root_directory())
        
        # Setor 18: Dados do arquivo
        iso_file.write(create_data_area("hello world"))
        
        # Preenche setores adicionais para garantir alinhamento correto
        for _ in range(19, 20):
            iso_file.write(create_empty_sector())

    print(f"ISO criada com sucesso: {output_file}")

# Executa a função principal
print("\033c\033[43;30m\n")
create_iso()
