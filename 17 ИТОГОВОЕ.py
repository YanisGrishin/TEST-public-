spisok = '3 11 4 5 9 17 11 13 27 45 8'
spisok = [int(x) for x in spisok.split()]
user_number = int(input("Введите целое число больше 0 и не более 45: "))

try:
    if 0 < user_number <= max(spisok):
        spisok.append(user_number)
        print("Список до сортировки: ", spisok)
        spisok.sort()
        print("Список после сортировки по возрастанию: ", spisok)
    else:
        raise ValueError
except:
    print("Введено некорректное число, попробуйте еще раз")
else:
    def binary_search(user_number, spisok):
        left, right = 0, len(spisok)
        while left < right:
            middle = (right + left) // 2
            if spisok[middle] < user_number:
                left = middle + 1
            else:
                right = middle
        return left
    print("Индекс введенного числа в списке: ", binary_search(user_number, spisok) - 1)
finally:
    print("Программа завершена")