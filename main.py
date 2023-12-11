
from pprint import pprint
## Читаем адресную книгу в формате CSV в список contacts_list:
import csv
import re
import io #несколько часов сидел и пытался понять, почему у меня IDE не хочет нормально работать с utf-8, без вот этого ничего не работает

#functions
def check_duplicates(data_, fio_):
    for index_, element in enumerate(data_):
        if fio_[0] == element[0]:
            if fio_[1] == element[1]:
                return True, index_
    return False, -1


def merge_data(list_1, list_2):
    for index in range(0, len(list_1)):
        if list_1[index] == "":
            list_1[index] = list_2[index]

#read
with io.open("phonebook_raw.csv", "r", encoding="UTF-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)


#exp
phone_pattern = r"\+*[7|8]\s*\(*(\d{3})[\)\s\-]*(\d{3})\-*(\d{2})\-*(\d{2})(\s*)\(*(доб.)*\s*(\d+)*\)*"
phone_subst = r"+7(\2)\3-\4-\5 \6\7"


## 1. Выполните пункты 1-3 задания.
headers = contacts_list[0]
contacts_list = contacts_list[1:]
phone_pattern = re.compile(phone_pattern)
fio_pattern = re.compile(r"(\w+)[\s|\,](\w+)[\s|\,](\w+)*")
final_data = []
for raw_row in contacts_list:
    if len(raw_row) > len(headers):
        raw_row = raw_row[:-1]
    joined_row = " ".join(raw_row)
    fio = fio_pattern.search(joined_row)
    if fio == None:
        continue
    fio = fio.group().split()
    raw_row[0 : len(fio)] = fio
    phone = phone_pattern.search(raw_row[5])
    if phone == None:
        raw_row[5] = ""
    else:
        raw_row[5] = phone_pattern.sub(phone_subst, phone.group()).rstrip()

    #dup_check
    if_exists, index = check_duplicates(final_data, raw_row)
    # merge_action
    if if_exists:
        merge_data(final_data[index], raw_row)
    else:
        final_data.append(raw_row)
final_data.insert(0, headers)


## 2. Сохраните получившиеся данные в другой файл.

## Код для записи файла в формате CSV:
with io.open("phonebook.csv", "w", encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(final_data)