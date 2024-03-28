import re
import pandas as pd

bearing_types = {
    "0": "Радиально-упорные шарикоподшипники",
    "1": "Самоустанавливающиеся шарикоподшипники",
    "2": "Сферические роликоподшипники, сферические упорные роликоподшипники",
    "3": "Конические роликоподшипники",
    "4": "Двухрядные радиальные шарикоподшипники",
    "5": "Упорные шарикоподшипники",
    "6": "Однорядные радиальные шарикоподшипники",
    "7": "Однорядные радиально-упорные шарикоподшипники",
    "8": "Упорные цилиндрические роликоподшипники"
}

def extract_base_designation(identifier):
    matches = re.findall(r"\d{3,}", identifier)  # Находим все последовательности чисел с количеством цифр >= 3
    if matches:
        base_designation = max(matches, key=len)  # Выбираем самую длинную последовательность
        return base_designation
    else:
        return None

# Загрузить файл
df = pd.read_excel("bearings.xls", sheet_name="sheet1")

# Отбор строк с подшипниками
df = df[df["bearing_name"].str.contains(r"подшипник|bearing", case=False)]

# Создать новый лист для типа подшипника
df["base"] = df["bearing_name"].apply(extract_base_designation)

# Вычисление четвертого индекса
df["four_ind"] = df["base"].apply(lambda x: x[-4] if x is not None and len(x) >= 4 else "0")

# Определение типа подшипника
df["bearing_type"] = df["four_ind"].map(bearing_types)

# Сохранение результатов в новый файл
df.to_excel("results.xlsx", index=False)

# Вывести результат
print("Результаты сохранены в новый файл")
