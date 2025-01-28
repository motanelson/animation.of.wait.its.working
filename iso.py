import struct

# Função para criar um setor de 2048 bytes preenchido com zeros
def create_empty_sector():
    return bytearray(2048)

# Função para criar o Primary Volume Descriptor (PVD)
def create_pvd(volume_name="MYISO"):
    pvd = bytearray(2048)
    pvd[0:1] = b'\x01'  # Tipo de descritor (1 = PVD)
    pvd[1:6] = b'CD001'  # Identificador do padrão ISO 9660
    pvd[40:72] = volume_name.ljust(32).encode('ascii')  # Nome do volume
    pvd[80:88] = struct.pack('<I', 1)  # Tamanho do volume (em setores)
    pvd[120:124] = struct.pack('<I', 1)  # Tamanho do volume (em setores)
    return pvd

# Função para criar um Directory Record
def create_directory_record(name, start_sector, size, is_file=True):
    record = bytearray(34)
    record[0:1] = struct.pack('B', len(record))  # Tamanho do registro
    record[2:6] = struct.pack('<I', start_sector)  # Setor inicial
    record[10:18] = struct.pack('<Q', size)  # Tamanho do arquivo
    record[25:26] = struct.pack('B', 1 if is_file else 2)  # Flags (arquivo ou diretório)
    record[33:33+len(name)] = name.encode('ascii')  # Nome do arquivo/diretório
    return record

# Função para criar o diretório raiz
def create_root_directory():
    root_dir = bytearray(2048)
    # Adiciona a entrada do diretório atual (.)
    root_dir[0:34] = create_directory_record(".", 17, 2048, is_file=False)
    # Adiciona a entrada do diretório pai (..)
    root_dir[34:68] = create_directory_record("..", 17, 2048, is_file=False)
    # Adiciona a entrada do arquivo hello.txt
    root_dir[68:102] = create_directory_record("HELLO.TXT;1", 18, 11, is_file=True)
    return root_dir

# Função para criar a área de dados com o conteúdo do arquivo
def create_data_area(content):
    data = bytearray(2048)
    data[0:len(content)] = content.encode('ascii')
    return data

# Função principal para criar a ISO
def create_iso(output_file="my_iso.iso"):
    with open(output_file, "wb") as iso_file:
        # Escreve 16 setores vazios (reservados para boot, etc.)
        for _ in range(16):
            iso_file.write(create_empty_sector())
        
        # Escreve o Primary Volume Descriptor (PVD)
        iso_file.write(create_pvd())
        
        # Escreve o diretório raiz
        iso_file.write(create_root_directory())
        
        # Escreve a área de dados com o conteúdo do arquivo
        iso_file.write(create_data_area("hello world"))
        
        # Preenche o restante da ISO com setores vazios (opcional)
        for _ in range(17, 20):
            iso_file.write(create_empty_sector())

    print(f"ISO criada com sucesso: {output_file}")

# Executa a função principal
create_iso()