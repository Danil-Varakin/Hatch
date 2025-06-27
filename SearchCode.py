def SearchInsertIndexInTokenList(MatchTokenList: list[tuple], SourceCodeTokenList: list[tuple]):
    print("Начало функции SearchInsertIndexInTokenList")
    print(f"MatchTokenList: {MatchTokenList}")
    print(f"SourceCodeTokenList: {SourceCodeTokenList}")

    IsPassDictionary = [{"IndexString": "", "CurentSourceCodeTokenIndex": 0, "SourceCodeNestingLevel": 0, "SourceCodeRelativeNestingLevel": 0}]
    print(f"Инициализация IsPassDictionary: {IsPassDictionary}")

    FlagFirstCircle = True
    print(f"Инициализация FlagFirstCircle: {FlagFirstCircle}")

    NestingMap = MatchNestingLevelInsertALL(MatchTokenList)
    print(f"Создание NestingMap: {NestingMap}")

    for MatchTokenIndex in range(len(MatchTokenList)):
        print(f"Цикл по MatchTokenList, текущий индекс: {MatchTokenIndex}")

        if MatchTokenList[MatchTokenIndex][1] == '...':
            print(f"Обнаружен токен '...', вызов IsPass для MatchTokenIndex: {MatchTokenIndex}")
            IsPassDictionary, FlagFirstCircle = IsPass(MatchTokenList, MatchTokenIndex, SourceCodeTokenList, IsPassDictionary, FlagFirstCircle, NestingMap)
            print(f"После IsPass: IsPassDictionary = {IsPassDictionary}, FlagFirstCircle = {FlagFirstCircle}")

        if MatchTokenList[MatchTokenIndex][1] == ">>>":
            print(f"Обнаружен токен '>>>', вызов IsInsert для MatchTokenIndex: {MatchTokenIndex}")
            ResultTokenInsert = IsInsert(MatchTokenList, MatchTokenIndex, SourceCodeTokenList, IsPassDictionary, FlagFirstCircle, NestingMap)
            print(f"Результат IsInsert: {ResultTokenInsert}")
            if ResultTokenInsert:
                print(f"Возвращаем результат IsInsert: {ResultTokenInsert}")
                return ResultTokenInsert

    print("Цикл завершён, возвращаем 0")
    return 0


def ComparisonToken(MatchTokenList, MatchTokenIndex, SourceCodeTokenList, SourceCodeTokenIndex, SourceCodeNestingLevel, FlagFirstCircle, SourceCodeRelativeNestingLevel, NestingMap):
    print(f"Начало функции ComparisonToken, MatchTokenIndex: {MatchTokenIndex}, SourceCodeTokenIndex: {SourceCodeTokenIndex}")

    ComparisonIndex = 1
    NumberTokenMatch = 0
    NumberTokenSource = 0
    ComparisonSourceCodeNestingLevel = 0
    ComprasionSourceCodeRelativeNestingLevel = 0
    print(f"Инициализация: ComparisonIndex = {ComparisonIndex}, NumberTokenMatch = {NumberTokenMatch}, NumberTokenSource = {NumberTokenSource}, ComparisonSourceCodeNestingLevel = {ComparisonSourceCodeNestingLevel}, ComprasionSourceCodeRelativeNestingLevel = {ComprasionSourceCodeRelativeNestingLevel}")

    if FlagFirstCircle:
        print(f"FlagFirstCircle = True, проверка NestingMap[{MatchTokenIndex + 1}][0]: {NestingMap[MatchTokenIndex + 1][0]}")
        if NestingMap[MatchTokenIndex + 1][0] == -1:
            print(f"NestingMap[{MatchTokenIndex + 1}][0] == -1, обновляем SourceCodeRelativeNestingLevel")
            SourceCodeRelativeNestingLevel = SourceNestingLevelChange(SourceCodeRelativeNestingLevel, SourceCodeTokenList, SourceCodeTokenIndex, 0)
            print(f"SourceCodeRelativeNestingLevel после обновления: {SourceCodeRelativeNestingLevel}")
        SourceCodeNestingLevel = SourceNestingLevelChange(SourceCodeNestingLevel, SourceCodeTokenList, SourceCodeTokenIndex, 0)
        print(f"SourceCodeNestingLevel после обновления: {SourceCodeNestingLevel}")

    while MatchTokenIndex + 1 + ComparisonIndex < len(MatchTokenList) and MatchTokenList[MatchTokenIndex + 1 + ComparisonIndex][1] not in ["...", ">>>"]:
        print(f"Цикл while, ComparisonIndex: {ComparisonIndex}")
        NumberTokenMatch = NumberTokenMatch + 1
        print(f"Увеличиваем NumberTokenMatch: {NumberTokenMatch}")

        if NestingMap[MatchTokenIndex + 1][0] == -1:
            print(f"NestingMap[{MatchTokenIndex + 1}][0] == -1, обновляем ComprasionSourceCodeRelativeNestingLevel")
            ComprasionSourceCodeRelativeNestingLevel = SourceNestingLevelChange(ComprasionSourceCodeRelativeNestingLevel, SourceCodeTokenList, SourceCodeTokenIndex, ComparisonIndex)
            print(f"ComprasionSourceCodeRelativeNestingLevel после обновления: {ComprasionSourceCodeRelativeNestingLevel}")

        ComparisonSourceCodeNestingLevel = SourceNestingLevelChange(ComparisonSourceCodeNestingLevel, SourceCodeTokenList, SourceCodeTokenIndex, ComparisonIndex)
        print(f"ComparisonSourceCodeNestingLevel после обновления: {ComparisonSourceCodeNestingLevel}")

        if MatchTokenList[MatchTokenIndex + 1 + ComparisonIndex][1] != SourceCodeTokenList[SourceCodeTokenIndex + ComparisonIndex][1]:
            print(f"Токены не совпадают: MatchTokenList[{MatchTokenIndex + 1 + ComparisonIndex}][1] = {MatchTokenList[MatchTokenIndex + 1 + ComparisonIndex][1]}, SourceCodeTokenList[{SourceCodeTokenIndex + ComparisonIndex}][1] = {SourceCodeTokenList[SourceCodeTokenIndex + ComparisonIndex][1]}")
            ComparisonSourceCodeNestingLevel = 0
            ComprasionSourceCodeRelativeNestingLevel = 0
            print(f"Сброс: ComparisonSourceCodeNestingLevel = {ComparisonSourceCodeNestingLevel}, ComprasionSourceCodeRelativeNestingLevel = {ComprasionSourceCodeRelativeNestingLevel}")
            break

        NumberTokenSource = NumberTokenSource + 1
        print(f"Увеличиваем NumberTokenSource: {NumberTokenSource}")
        ComparisonIndex = ComparisonIndex + 1
        print(f"Увеличиваем ComparisonIndex: {ComparisonIndex}")

    print(f"Возвращаем: ComparisonIndex = {ComparisonIndex}, NumberTokenMatch = {NumberTokenMatch}, NumberTokenSource = {NumberTokenSource}, SourceCodeNestingLevel = {SourceCodeNestingLevel}, ComparisonSourceCodeNestingLevel = {ComparisonSourceCodeNestingLevel}, SourceCodeRelativeNestingLevel = {SourceCodeRelativeNestingLevel}, ComprasionSourceCodeRelativeNestingLevel = {ComprasionSourceCodeRelativeNestingLevel}")
    return ComparisonIndex, NumberTokenMatch, NumberTokenSource, SourceCodeNestingLevel, ComparisonSourceCodeNestingLevel, SourceCodeRelativeNestingLevel, ComprasionSourceCodeRelativeNestingLevel


def SourceNestingLevelChange(SourceCodeNestingLevel, SourceCodeTokenList, SourceCodeTokenIndex, ComparisonIndex):

    if SourceCodeTokenList[SourceCodeTokenIndex + ComparisonIndex][1] in ["{", "(", "["]:
        SourceCodeNestingLevel = SourceCodeNestingLevel + 1

    if SourceCodeTokenList[SourceCodeTokenIndex + ComparisonIndex][1] in ["}", ")", "]"]:
        SourceCodeNestingLevel = SourceCodeNestingLevel - 1

    return SourceCodeNestingLevel


def IsPass(MatchTokenList, MatchTokenIndex, SourceCodeTokenList, IsPassDictionary, FlagFirstCircle, NestingMap):
    print(f"Начало функции IsPass, MatchTokenIndex: {MatchTokenIndex}, FlagFirstCircle: {FlagFirstCircle}")
    print(f"IsPassDictionary: {IsPassDictionary}")

    IsPassOutputDictionary = []
    print(f"Инициализация IsPassOutputDictionary: {IsPassOutputDictionary}")

    if IsPassDictionary:
        skip_rest = False
        print(f"Проверка условия skip_rest, MatchTokenIndex + 1: {MatchTokenIndex + 1}, len(MatchTokenList): {len(MatchTokenList)}")
        if MatchTokenIndex + 1 < len(MatchTokenList) and MatchTokenList[MatchTokenIndex + 1][1] == '>>>':
            skip_rest = True
            print(f"Обнаружен '>>>', skip_rest = True")

        if not skip_rest:
            for IsPassOutput in IsPassDictionary:
                print(f"Цикл по IsPassDictionary, текущий элемент: {IsPassOutput}")
                SourceCodeNestingLevel = IsPassOutput["SourceCodeNestingLevel"]
                SourceCodeRelativeNestingLevel = IsPassOutput["SourceCodeRelativeNestingLevel"]
                StartCurentSourceCodeTokenIndex = IsPassOutput["CurentSourceCodeTokenIndex"]
                print(f"SourceCodeNestingLevel: {SourceCodeNestingLevel}, SourceCodeRelativeNestingLevel: {SourceCodeRelativeNestingLevel}, StartCurentSourceCodeTokenIndex: {StartCurentSourceCodeTokenIndex}")

                CounterMatches = 0
                print(f"Инициализация CounterMatches: {CounterMatches}")

                for SourceCodeTokenIndex in range(StartCurentSourceCodeTokenIndex, len(SourceCodeTokenList)):
                    print(f"Цикл по SourceCodeTokenList, SourceCodeTokenIndex: {SourceCodeTokenIndex}")

                    if MatchTokenIndex + 1 < len(MatchTokenList):
                        if not FlagFirstCircle:
                            if NestingMap[MatchTokenIndex + 1][0] == -1:
                                print(f"FlagFirstCircle = False, обновляем SourceCodeRelativeNestingLevel")
                                SourceCodeRelativeNestingLevel = SourceNestingLevelChange(SourceCodeRelativeNestingLevel, SourceCodeTokenList, SourceCodeTokenIndex, 0)
                                print(f"SourceCodeNestingLevel после обновления: {SourceCodeRelativeNestingLevel}")
                            else:
                                print(f"FlagFirstCircle = False, обновляем SourceCodeNestingLevel")
                                SourceCodeNestingLevel = SourceNestingLevelChange(SourceCodeNestingLevel, SourceCodeTokenList, SourceCodeTokenIndex, 0)
                                print(f"SourceCodeNestingLevel после обновления: {SourceCodeNestingLevel}")


                        if SourceCodeTokenList[SourceCodeTokenIndex] == MatchTokenList[MatchTokenIndex + 1]:
                            print(f"Токены совпадают: SourceCodeTokenList[{SourceCodeTokenIndex}] = {SourceCodeTokenList[SourceCodeTokenIndex]}, MatchTokenList[{MatchTokenIndex + 1}] = {MatchTokenList[MatchTokenIndex + 1]}")
                            StartSourceCodeRelativeNestingLevel = SourceCodeRelativeNestingLevel
                            StartSourceCodeNestingLevel = SourceCodeNestingLevel
                            print(f"Сохранение начальных значений: StartSourceCodeRelativeNestingLevel = {StartSourceCodeRelativeNestingLevel}, StartSourceCodeNestingLevel = {StartSourceCodeNestingLevel}")

                            ComparisonIndex, NumberTokenMatch, NumberTokenSource, SourceCodeNestingLevel, ComparisonSourceCodeNestingLevel, SourceCodeRelativeNestingLevel, ComprasionSourceCodeRelativeNestingLevel = ComparisonToken(MatchTokenList, MatchTokenIndex, SourceCodeTokenList, SourceCodeTokenIndex, SourceCodeNestingLevel, FlagFirstCircle, SourceCodeRelativeNestingLevel, NestingMap)
                            print(f"Результат ComparisonToken: ComparisonIndex = {ComparisonIndex}, NumberTokenMatch = {NumberTokenMatch}, NumberTokenSource = {NumberTokenSource}")

                            if NumberTokenSource == NumberTokenMatch:
                                print(f"NumberTokenSource ({NumberTokenSource}) == NumberTokenMatch ({NumberTokenMatch})")
                                IndexString = IsPassOutput["IndexString"] + str(CounterMatches) + '/'
                                print(f"Обновление IndexString: {IndexString}")

                                if NestingMap[MatchTokenIndex + ComparisonIndex][0] != -1:
                                    print(f"NestingMap[{MatchTokenIndex + ComparisonIndex}][0] = {NestingMap[MatchTokenIndex + ComparisonIndex][0]}, проверка уровней вложенности")
                                    if NestingMap[MatchTokenIndex + ComparisonIndex][0] == SourceCodeNestingLevel + ComparisonSourceCodeNestingLevel:
                                        CurentSourceCodeTokenIndex = ComparisonIndex + SourceCodeTokenIndex
                                        SourceCodeNestingLevel = SourceCodeNestingLevel + ComparisonSourceCodeNestingLevel
                                        CounterMatches += 1
                                        print(f"Успешное совпадение, обновление: CurentSourceCodeTokenIndex = {CurentSourceCodeTokenIndex}, SourceCodeNestingLevel = {SourceCodeNestingLevel}, CounterMatches = {CounterMatches}")
                                        IsPassOutputDictionary.append({"IndexString": IndexString, "CurentSourceCodeTokenIndex": CurentSourceCodeTokenIndex, "SourceCodeNestingLevel": SourceCodeNestingLevel, "SourceCodeRelativeNestingLevel": SourceCodeRelativeNestingLevel})
                                        print(f"Добавлен элемент в IsPassOutputDictionary: {IsPassOutputDictionary[-1]}")

                                        if (PassInNestingMarkers(MatchTokenIndex, MatchTokenList) != 0 and PassInNestingMarkers(MatchTokenIndex, MatchTokenList)[1] < MatchTokenIndex + ComparisonIndex + 1) or (PassInNestingMarkers(MatchTokenIndex + ComparisonIndex, MatchTokenList) != 0 and PassInNestingMarkers(MatchTokenIndex + ComparisonIndex, MatchTokenList)[0] ==  MatchTokenIndex + ComparisonIndex):
                                            print(f"PassInNestingMarkers вернул True, прерываем цикл")
                                            break
                                        SourceCodeNestingLevel = StartSourceCodeNestingLevel
                                        SourceCodeRelativeNestingLevel = StartSourceCodeRelativeNestingLevel
                                        print(f"Восстановление: SourceCodeNestingLevel = {SourceCodeNestingLevel}, SourceCodeRelativeNestingLevel = {SourceCodeRelativeNestingLevel}")
                                else:
                                    print(f"NestingMap[{MatchTokenIndex + ComparisonIndex}][0] == -1, проверка относительных уровней вложенности")
                                    if NestingMap[MatchTokenIndex + ComparisonIndex][1] == ComprasionSourceCodeRelativeNestingLevel + SourceCodeRelativeNestingLevel or NestingMap[MatchTokenIndex + ComparisonIndex][1] == 0:
                                        CurentSourceCodeTokenIndex = ComparisonIndex + SourceCodeTokenIndex
                                        SourceCodeRelativeNestingLevel = SourceCodeRelativeNestingLevel + ComprasionSourceCodeRelativeNestingLevel
                                        print(f"Успешное совпадение, обновление: CurentSourceCodeTokenIndex = {CurentSourceCodeTokenIndex}, SourceCodeRelativeNestingLevel = {SourceCodeRelativeNestingLevel}")
                                        IsPassOutputDictionary.append({"IndexString": IndexString, "CurentSourceCodeTokenIndex": CurentSourceCodeTokenIndex, "SourceCodeNestingLevel": SourceCodeNestingLevel, "SourceCodeRelativeNestingLevel": SourceCodeRelativeNestingLevel})
                                        print(f"Добавлен элемент в IsPassOutputDictionary: {IsPassOutputDictionary[-1]}")
                                        CounterMatches += 1
                                        print(f"Увеличиваем CounterMatches: {CounterMatches}")

                                        if (PassInNestingMarkers(MatchTokenIndex, MatchTokenList) != 0 and PassInNestingMarkers(MatchTokenIndex, MatchTokenList)[1] < MatchTokenIndex + ComparisonIndex + 1) or (PassInNestingMarkers(MatchTokenIndex + ComparisonIndex, MatchTokenList) != 0 and PassInNestingMarkers(MatchTokenIndex + ComparisonIndex, MatchTokenList)[0] ==  MatchTokenIndex + ComparisonIndex):
                                            print(f"PassInNestingMarkers вернул True, прерываем цикл")
                                            break
                                        SourceCodeNestingLevel = StartSourceCodeNestingLevel
                                        SourceCodeRelativeNestingLevel = StartSourceCodeRelativeNestingLevel
                                        print(f"Восстановление: SourceCodeNestingLevel = {SourceCodeNestingLevel}, SourceCodeRelativeNestingLevel = {SourceCodeRelativeNestingLevel}")
                                    if NestingMap[MatchTokenIndex + ComparisonIndex + 1][0] != -1:
                                        SourceCodeRelativeNestingLevel = 0
                                        print(f"NestingMap[{MatchTokenIndex + ComparisonIndex + 1}][0] != -1, сброс SourceCodeRelativeNestingLevel: {SourceCodeRelativeNestingLevel}")
        else:
            print(f"skip_rest = True, возвращаем текущие IsPassDictionary и FlagFirstCircle")
            return IsPassDictionary, FlagFirstCircle

    if FlagFirstCircle:
        FlagFirstCircle = False
        print(f"FlagFirstCircle = True, установка FlagFirstCircle = False")

    print(f"Возвращаем: IsPassOutputDictionary = {IsPassOutputDictionary}, FlagFirstCircle = {FlagFirstCircle}")
    return IsPassOutputDictionary, FlagFirstCircle


def IsInsert(MatchTokenList, MatchTokenIndex, SourceCodeTokenList, IsPassDictionary, FlagFirstCircle, NestingMap):


    MatchNestingLevel = InsertNestingLevel(MatchTokenList)
    print(f"Создание MatchNestingLevel: {MatchNestingLevel}")

    if MatchTokenIndex > 0 and MatchTokenIndex + 1 < len(MatchTokenList):
        print(f"Проверка условий: MatchTokenIndex > 0 ({MatchTokenIndex}) и MatchTokenIndex + 1 < len(MatchTokenList) ({MatchTokenIndex + 1} < {len(MatchTokenList)})")
        if MatchTokenList[MatchTokenIndex - 1][1] != '...' and MatchTokenList[MatchTokenIndex + 1][1] == '...':
            print(f"Условие: MatchTokenList[{MatchTokenIndex - 1}][1] != '...' ({MatchTokenList[MatchTokenIndex - 1][1]}) и MatchTokenList[{MatchTokenIndex + 1}][1] == '...'")
            if len(IsPassDictionary) > 1:
                print(f"len(IsPassDictionary) > 1 ({len(IsPassDictionary)}), возвращаем 0")
                return 0
            elif len(IsPassDictionary) == 1:
                print(f"len(IsPassDictionary) == 1, создание ResultTokenInsert")
                ResultTokenInsert = {'Prev': IsPassDictionary[0]["CurentSourceCodeTokenIndex"] - 1}
                print(f"ResultTokenInsert: {ResultTokenInsert}")
                return ResultTokenInsert

    IsInsertOutputList = []
    print(f"Инициализация IsInsertOutputList: {IsInsertOutputList}")

    if IsPassDictionary:
        print(f"IsPassDictionary не пустой, начало цикла по IsPassDictionary")
        for IsPassOutput in IsPassDictionary:
            print(f"Текущий элемент IsPassDictionary: {IsPassOutput}")
            CurentSourceCodeTokenIndex = IsPassOutput["CurentSourceCodeTokenIndex"]
            SourceCodeNestingLevel = IsPassOutput["SourceCodeNestingLevel"]
            SourceCodeRelativeNestingLevel = IsPassOutput["SourceCodeRelativeNestingLevel"]
            print(f"Извлечение: CurentSourceCodeTokenIndex = {CurentSourceCodeTokenIndex}, SourceCodeNestingLevel = {SourceCodeNestingLevel}, SourceCodeRelativeNestingLevel = {SourceCodeRelativeNestingLevel}")

            if (MatchTokenList[MatchTokenIndex - 1][1] == "..." and MatchTokenList[MatchTokenIndex + 1][1] != '...') or (MatchTokenList[MatchTokenIndex - 1][1] != "..." and MatchTokenList[MatchTokenIndex + 1][1] != '...'):
                print(f"Условие выполнено: MatchTokenList[{MatchTokenIndex - 1}][1] = {MatchTokenList[MatchTokenIndex - 1][1]}, MatchTokenList[{MatchTokenIndex + 1}][1] = {MatchTokenList[MatchTokenIndex + 1][1]}")
                SourceCodeTokenIndex = CurentSourceCodeTokenIndex
                print(f"Установка SourceCodeTokenIndex: {SourceCodeTokenIndex}")

                while SourceCodeTokenIndex < len(SourceCodeTokenList):
                    SourceCodeInsertIndex = SourceCodeTokenIndex
                    if MatchTokenIndex != 1:
                        print(f"MatchTokenIndex != 1 ({MatchTokenIndex}), проверка NestingMap")
                        if NestingMap[MatchTokenIndex + 1][0] == -1:
                            print(f"NestingMap[{MatchTokenIndex + 1}][0] == -1, обновляем SourceCodeRelativeNestingLevel")
                            SourceCodeRelativeNestingLevel = SourceNestingLevelChange(SourceCodeRelativeNestingLevel, SourceCodeTokenList, SourceCodeTokenIndex, 0)
                            print(f"SourceCodeRelativeNestingLevel после обновления: {SourceCodeRelativeNestingLevel}")
                        SourceCodeNestingLevel = SourceNestingLevelChange(SourceCodeNestingLevel, SourceCodeTokenList, SourceCodeTokenIndex, 0)
                        print(f"SourceCodeNestingLevel после обновления: {SourceCodeNestingLevel}")

                    if MatchTokenIndex + 1 < len(MatchTokenList):
                        print(f"MatchTokenIndex + 1 < len(MatchTokenList) ({MatchTokenIndex + 1} < {len(MatchTokenList)})")
                        if SourceCodeTokenList[SourceCodeTokenIndex] == MatchTokenList[MatchTokenIndex + 1]:
                            print(f"Токены совпадают: SourceCodeTokenList[{SourceCodeTokenIndex}] = {SourceCodeTokenList[SourceCodeTokenIndex]}, MatchTokenList[{MatchTokenIndex + 1}] = {MatchTokenList[MatchTokenIndex + 1]}")
                            StartSourceCodeRelativeNestingLevel = SourceCodeRelativeNestingLevel
                            StartSourceCodeNestingLevel = SourceCodeNestingLevel
                            print(f"Сохранение начальных значений: StartSourceCodeRelativeNestingLevel = {StartSourceCodeRelativeNestingLevel}, StartSourceCodeNestingLevel = {StartSourceCodeNestingLevel}")

                            ComparisonIndex, NumberTokenMatch, NumberTokenSource, SourceCodeNestingLevel, ComparisonSourceCodeNestingLevel, SourceCodeRelativeNestingLevel, ComprasionSourceCodeRelativeNestingLevel = ComparisonToken(MatchTokenList, MatchTokenIndex, SourceCodeTokenList, SourceCodeTokenIndex, SourceCodeNestingLevel, FlagFirstCircle, SourceCodeRelativeNestingLevel, NestingMap)
                            print(f"Результат ComparisonToken: ComparisonIndex = {ComparisonIndex}, NumberTokenMatch = {NumberTokenMatch}, NumberTokenSource = {NumberTokenSource}, SourceCodeNestingLevel = {SourceCodeNestingLevel}, ComparisonSourceCodeNestingLevel = {ComparisonSourceCodeNestingLevel}, SourceCodeRelativeNestingLevel = {SourceCodeRelativeNestingLevel}, ComprasionSourceCodeRelativeNestingLevel = {ComprasionSourceCodeRelativeNestingLevel}")

                            if NumberTokenSource == NumberTokenMatch:
                                print(f"NumberTokenSource ({NumberTokenSource}) == NumberTokenMatch ({NumberTokenMatch})")
                                if MatchNestingLevel[0] != -1:
                                    print(f"MatchNestingLevel[0] != -1 ({MatchNestingLevel[0]})")
                                    if NestingMap[MatchTokenIndex + ComparisonIndex][0] == SourceCodeNestingLevel + ComparisonSourceCodeNestingLevel:
                                        print(f"NestingMap[{MatchTokenIndex + ComparisonIndex}][0] ({NestingMap[MatchTokenIndex + ComparisonIndex][0]}) == SourceCodeNestingLevel + ComparisonSourceCodeNestingLevel ({SourceCodeNestingLevel + ComparisonSourceCodeNestingLevel})")
                                        IsInsertOutputList.append({'Next': SourceCodeInsertIndex})
                                        print(f"Добавлен элемент в IsInsertOutputList: {{'Next': {SourceCodeInsertIndex}}}")

                                        if (PassInNestingMarkers(MatchTokenIndex, MatchTokenList) != 0 and PassInNestingMarkers(MatchTokenIndex, MatchTokenList)[1] < MatchTokenIndex + ComparisonIndex + 1) or (PassInNestingMarkers(MatchTokenIndex + ComparisonIndex, MatchTokenList) != 0 and PassInNestingMarkers(MatchTokenIndex + ComparisonIndex, MatchTokenList)[0] ==  MatchTokenIndex + ComparisonIndex):
                                            print(f"PassInNestingMarkers вернул True, прерываем цикл")
                                            break
                                        SourceCodeNestingLevel = StartSourceCodeNestingLevel
                                        SourceCodeRelativeNestingLevel = StartSourceCodeRelativeNestingLevel
                                        print(f"Восстановление: SourceCodeNestingLevel = {SourceCodeNestingLevel}, SourceCodeRelativeNestingLevel = {SourceCodeRelativeNestingLevel}")
                                        SourceCodeTokenIndex += 1
                                        print(f"Увеличиваем SourceCodeTokenIndex: {SourceCodeTokenIndex}")
                                    else:
                                        SourceCodeTokenIndex += 1
                                        print(f"Условие вложенности не выполнено, увеличиваем SourceCodeTokenIndex: {SourceCodeTokenIndex}")
                                else:
                                    print(f"MatchNestingLevel[0] == -1, проверка относительных уровней")
                                    if NestingMap[MatchTokenIndex + ComparisonIndex][1] == SourceCodeRelativeNestingLevel + ComprasionSourceCodeRelativeNestingLevel:
                                        print(f"NestingMap[{MatchTokenIndex + ComparisonIndex}][1] ({NestingMap[MatchTokenIndex + ComparisonIndex][1]}) == SourceCodeRelativeNestingLevel + ComprasionSourceCodeRelativeNestingLevel ({SourceCodeRelativeNestingLevel + ComprasionSourceCodeRelativeNestingLevel})")
                                        IsInsertOutputList.append({'Next': SourceCodeInsertIndex})
                                        print(f"Добавлен элемент в IsInsertOutputList: {{'Next': {SourceCodeInsertIndex}}}")

                                        if (PassInNestingMarkers(MatchTokenIndex, MatchTokenList) != 0 and PassInNestingMarkers(MatchTokenIndex, MatchTokenList)[1] < MatchTokenIndex + ComparisonIndex + 1) or (PassInNestingMarkers(MatchTokenIndex + ComparisonIndex, MatchTokenList) != 0 and PassInNestingMarkers(MatchTokenIndex + ComparisonIndex, MatchTokenList)[0] ==  MatchTokenIndex + ComparisonIndex):
                                            print(f"PassInNestingMarkers вернул True, прерываем цикл")
                                            break
                                        SourceCodeNestingLevel = StartSourceCodeNestingLevel
                                        SourceCodeRelativeNestingLevel = StartSourceCodeRelativeNestingLevel
                                        print(f"Восстановление: SourceCodeNestingLevel = {SourceCodeNestingLevel}, SourceCodeRelativeNestingLevel = {SourceCodeRelativeNestingLevel}")
                                        SourceCodeTokenIndex += 1
                                        print(f"Увеличиваем SourceCodeTokenIndex: {SourceCodeTokenIndex}")
                                    elif NestingMap[MatchTokenIndex + ComparisonIndex][1] == 0 and MatchTokenList[MatchTokenIndex + ComparisonIndex][1] not in ["}", ")", "]"]:
                                        print(f"NestingMap[{MatchTokenIndex + ComparisonIndex}][1] == 0 и MatchTokenList[{MatchTokenIndex + ComparisonIndex}][1] ({MatchTokenList[MatchTokenIndex + ComparisonIndex][1]}) не в ['}}', ')', ']']")
                                        IsInsertOutputList.append({'Next': SourceCodeInsertIndex})
                                        print(f"Добавлен элемент в IsInsertOutputList: {{'Next': {SourceCodeInsertIndex}}}")

                                        if (PassInNestingMarkers(MatchTokenIndex, MatchTokenList) != 0 and PassInNestingMarkers(MatchTokenIndex, MatchTokenList)[1] < MatchTokenIndex + ComparisonIndex + 1) or (PassInNestingMarkers(MatchTokenIndex + ComparisonIndex, MatchTokenList) != 0 and PassInNestingMarkers(MatchTokenIndex + ComparisonIndex, MatchTokenList)[0] ==  MatchTokenIndex + ComparisonIndex):
                                            print(f"PassInNestingMarkers вернул True, прерываем цикл")
                                            break
                                        SourceCodeNestingLevel = StartSourceCodeNestingLevel
                                        SourceCodeRelativeNestingLevel = StartSourceCodeRelativeNestingLevel
                                        print(f"Восстановление: SourceCodeNestingLevel = {SourceCodeNestingLevel}, SourceCodeRelativeNestingLevel = {SourceCodeRelativeNestingLevel}")
                                        SourceCodeTokenIndex += 1
                                        print(f"Увеличиваем SourceCodeTokenIndex: {SourceCodeTokenIndex}")
                                    else:
                                        SourceCodeTokenIndex += 1
                                        print(f"Условие не выполнено, увеличиваем SourceCodeTokenIndex: {SourceCodeTokenIndex}")
                            else:
                                SourceCodeTokenIndex += 1
                                print(f"NumberTokenSource != NumberTokenMatch, увеличиваем SourceCodeTokenIndex: {SourceCodeTokenIndex}")
                        else:
                            SourceCodeTokenIndex += 1
                            print(f"Токены не совпадают, увеличиваем SourceCodeTokenIndex: {SourceCodeTokenIndex} и токен {SourceCodeTokenList[SourceCodeTokenIndex]}")

        print(f"Проверка результата IsInsertOutputList, длина: {len(IsInsertOutputList)}")
        if len(IsInsertOutputList) > 1 or len(IsInsertOutputList) == 0:
            print(f"len(IsInsertOutputList) > 1 или == 0, возвращаем 0")
            return 0
        else:
            print(f"len(IsInsertOutputList) == 1, возвращаем IsInsertOutputList[0]: {IsInsertOutputList[0] if IsInsertOutputList else 0}")
            return IsInsertOutputList[0] if IsInsertOutputList else 0

def InsertNestingLevel(MatchTokenList: list[tuple]):
    NestingMap = MatchNestingLevelInsertALL(MatchTokenList)
    for i, MatchToken in enumerate(MatchTokenList):
        if MatchToken[1] == ">>>":
            return NestingMap[i]
    return 0


def GetBracketIndicesForEllipsis(MatchTokenList: list[tuple]):
    stack = []
    IsNestingMarkerPairsDictionary = CheckMatchNestingMarkerPairs(MatchTokenList)
    IsNestingDefined = True
    result = []
    for i, MatchToken in enumerate(MatchTokenList):
        if MatchToken[1] == '...' and i > 0:
            bracket_index = stack[-1][0] if stack and IsNestingDefined else -1
            result.append({"EllipsisIndex": i, "BracketIndex": bracket_index})
        elif MatchToken[1] in ["{", "(", "["] and IsNestingMarkerPairsDictionary.get(i, [False])[0]:
            stack.append((i, MatchToken[1]))
            IsNestingDefined = True
        elif MatchToken[1] in ["}", ")", "]"] and IsNestingMarkerPairsDictionary.get(i, [False])[0]:
            if stack:
                stack.pop()

    return result


def MatchNestingLevelInsertALL(MatchTokenList: list[tuple]):
    NestingMap = []
    CounterNesting = 0
    CounterRelativeNesting = 0
    IsNestingDefined = True
    BracketIndicesForEllipsis = GetBracketIndicesForEllipsis(MatchTokenList)
    BetweenEllipsis = set()

    for i, CurentBracket in enumerate(BracketIndicesForEllipsis):
        for NextBracket in BracketIndicesForEllipsis[i + 1:]:
            if CurentBracket["BracketIndex"] == NextBracket["BracketIndex"] and CurentBracket["BracketIndex"]:
                BetweenEllipsis.update(range(CurentBracket["EllipsisIndex"] + 1, NextBracket["EllipsisIndex"]))
    for i, MatchToken in enumerate(MatchTokenList):
        if i in BetweenEllipsis:
            IsNestingDefined, CounterRelativeNesting = CheckCounterNesting( MatchToken, CounterRelativeNesting, IsNestingDefined, i)
            NestingMap.append((-1,CounterRelativeNesting))
        else:
            IsNestingDefined, CounterNesting = CheckCounterNesting( MatchToken, CounterNesting, IsNestingDefined, i)
            NestingMap.append((CounterNesting if IsNestingDefined else -1,0))
    return NestingMap

def CheckCounterNesting( MatchToken,CounterNesting, IsNestingDefined, index):
    if MatchToken[1] == '...' and index > 0:
        if CounterNesting == 0:
            IsNestingDefined = False
    elif MatchToken[1] in ["{", "(", "["]:
        CounterNesting += 1
        IsNestingDefined = True
    elif MatchToken[1] in ["}", ")", "]"]:
        CounterNesting -= 1
    return IsNestingDefined, CounterNesting

def SearchInsertIndexInSourseCode(MatchTokenList: list[tuple], SourceCodeTokenList: list[tuple]):
    InsertIndexInTokenList = SearchInsertIndexInTokenList(MatchTokenList, SourceCodeTokenList)
    print(InsertIndexInTokenList)
    if InsertIndexInTokenList == 0:
        return 0
    TokenDirection, TokenPosition = list(InsertIndexInTokenList.items())[0]
    print(TokenPosition)
    TokenValue = SourceCodeTokenList[TokenPosition][1]
    CounterIdenticalToken = 0
    for SourceCodeTokenIndex in range(TokenPosition + 1):
        print(SourceCodeTokenList[SourceCodeTokenIndex])
        if SourceCodeTokenList[SourceCodeTokenIndex][1] == TokenValue:
            print('aaaaaaaaaaaaaaaa')
            CounterIdenticalToken = CounterIdenticalToken + 1
    return [TokenDirection, CounterIdenticalToken, TokenValue]


def CheckMatchNestingMarkerPairs(MatchTokenList: list[tuple]):
    IsNestingMarkerPairsDictionary = {}
    stack = []
    DictionaryNestingMarker = {')': '(', '}': '{', ']': '['}
    NestingMarkerList = [(i, MatchToken[1]) for i, MatchToken in enumerate(MatchTokenList) if MatchToken[1] in ["{", "(", "[", "}", ")", "]"]]

    for index, _ in NestingMarkerList:
        IsNestingMarkerPairsDictionary[index] = [False, -1]

    for i, (IndexOnMatch, NestingMarker) in enumerate(NestingMarkerList):
        if NestingMarker in ["{", "(", "["]:
            stack.append((IndexOnMatch, NestingMarker, i))
        elif NestingMarker in ["}", ")", "]"]:
            for j in range(len(stack) - 1, -1, -1):
                if stack[j][1] == DictionaryNestingMarker[NestingMarker]:
                    OpenNestingMarkerIndexOnMatch, _, _ = stack.pop(j)
                    IsNestingMarkerPairsDictionary[OpenNestingMarkerIndexOnMatch] = [True, IndexOnMatch]
                    IsNestingMarkerPairsDictionary[IndexOnMatch] = [True, OpenNestingMarkerIndexOnMatch]
                    break
    return IsNestingMarkerPairsDictionary


def PassInNestingMarkers(IndexPassInMatch, MatchTokenList):

    IsNestingMarkerPairsDictionary = CheckMatchNestingMarkerPairs(MatchTokenList)

    MarkerList = [[index, IsPaired, PairedIndex] for index, [IsPaired, PairedIndex] in IsNestingMarkerPairsDictionary.items()]

    ClosestPair = None

    for index, IsPaired, PairedIndex in MarkerList:
        if IsPaired and index <= IndexPassInMatch <= PairedIndex:


            ClosestPair = [index, PairedIndex]
    if ClosestPair: return ClosestPair
    else: return 0