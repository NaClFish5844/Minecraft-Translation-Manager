import json

en_us_path = './lang/en_us.json'
zh_cn_path = './lang/zh_cn-1.json'
folder_path = './lang/'


def json_read(path):
    with open(path, mode='r', encoding='utf-8') as file:
        lines = file.readlines()
        text = ''
        for i in lines:
            text = text + i
        return_dict = json.loads(text)
        file.close()
    return return_dict


def json_dump(dict, file_name):
    path = folder_path + file_name + '.json'
    json_content = json.dumps(dict, separators=(', \n', ': '), sort_keys=True, ensure_ascii=False)
    with open(path, mode='w', encoding='utf-8') as file:
        file.writelines(json_content)
        file.close()
    return


def intersection(section1, section2):
    inter = list()
    for _ in range(len(section1)):
        pop_key = section1.pop()
        try:
            section2.remove(pop_key)
        except ValueError:
            continue
        else:
            inter.append(pop_key)
    return inter


if __name__ == '__main__':
    en_us_dict = json_read(en_us_path)
    zh_cn_dict = json_read(zh_cn_path)

    en_us_keys = list(en_us_dict.keys())
    zh_cn_keys = list(zh_cn_dict.keys())

    intersection = intersection(en_us_keys, zh_cn_keys)
    intersection_dict = dict()

    for i in intersection:
        en_us_dict.pop(i)
        intersection_dict[i] = zh_cn_dict[i]
        zh_cn_dict.pop(i)

    json_dump(en_us_dict, 'en_us_only')
    json_dump(zh_cn_dict, 'zh_cn_only')
    json_dump(intersection_dict, 'intersection')
