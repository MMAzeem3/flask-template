def file_to_upper(file):
    file_path = f'raw/{file}'
    if not open(file_path):
        print('file does not exist')
        return(-1)
    filelines = open(file_path).read().splitlines()
    filelines = [line.upper() for line in filelines]
    new_file = f'processed/{file}'
    with open(new_file, 'w') as f:
        for line in filelines:
            f.write(line+"\n")