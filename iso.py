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
    pvd[40:72] = volume_name.ljust(32).encode('ascii')  # Nome do volume
    pvd[80:84] = struct.pack('<I', total_sectors)  # Número total de setores (little-endian)
    pvd[84:88] = struct.pack('>I', total_sectors)  # Número total de setores (big-endian)
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
create_iso()
