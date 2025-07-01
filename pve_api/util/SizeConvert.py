def to_string_size(size_number):
    suffix = ["B", "KB", "MB", "GB", "TB", "PB"]
    counter = 0
    while size_number >= 1024 and counter < len(suffix)-1:
        size_number /= 1024
        counter += 1
    return "{:.2f} {}".format(size_number, suffix[counter])

def to_number_size(size_string):
    ...