def read_file_stripped(file):
    for line in file:
        line = line.strip()
        if line:
            yield line.strip()
