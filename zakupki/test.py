from manager import KTRUManager

valid_ktru_number = '26.20.17.110-00000037'
ktru_version_int = 10
ktru_version_str = "10"

ktruManager = KTRUManager()
# скачать инфу по номеру ктру
data = ktruManager.get_ktru_info(valid_ktru_number)
# должна появится запись в requests
# должна появится запись в Ktru
# должна появится запись в ktruVersion
# должна появится запись в KtruChars


# скачать инфу по номеру ктру и номеру версии
# data = KTRUManager.get_ktru_info(valid_ktru_namber, ktru_version_int)

# скачать инфу по номеру ктру (не существующему)
# скачать инфу по номеру ктру  и номеру версии (не существующей)

# выгрузить из БД инфу по номеру ктру
# выгрузить из БД инфу по номеру ктру и номеру версии

for k, v in data.items():
    print(k, v)
