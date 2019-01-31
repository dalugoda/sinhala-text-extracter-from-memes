import codecs


def get_unicode_mapper():
    mapper_file = codecs.open("unicode_map.txt", "r", "utf-8")
    maps = dict()
    lines = mapper_file.read().split("\n")

    for line in lines:
        line = line.split("\t")
        key = line[0]
        value = line[1].replace("\r", "")
        maps[key] = value
        mapper_file.close()

    return maps


def get_unicode_text(mapper, text):
    for key in mapper:
        text = text.replace(key, mapper.get(key))

    return text
