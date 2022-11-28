import os

from api import PetFriends
from settings import valid_email, valid_password, wrong_email, none_password, wrong_password, long_password, none_email

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_post_add_pet_with_valid_key(name = 'Кот', animal_type = 'cat', age = '3', pet_photo = "images/1.jpg"):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.post_add_new_pet(auth_key, "Кот", "cat", "3", "images/1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")



### NEGATIVE
    #тест пройден, т.к. я намеренно указал неправильно код не равно 400, а не 200 (ye;yj ,skj? )
    #сайт PETFRIENDS.RU работает с багом
#1
def test_add_new_pet_negative_age(name='Kitty', animal_type='catminator', age='-3', pet_photo='images/2.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status != 200

#2
def test_add_new_pet_negative_name(name='@##^%$@#&^%#', animal_type='catminator', age='3', pet_photo='images/2.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status != 200

#3
def test_add_new_pet_negative_photo(name='Kitty', animal_type='catminator', age='3', pet_photo='images/3.pdf'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status != 200

#4
def test_get_api_key_wrong_email(email = wrong_email, password = valid_password):
    status, result = pf.get_api_key(email, password)

    assert status != 200
    assert 'key' not in result
#5
def test_get_api_key_none_password(email=valid_email, password=none_password):
    status, result = pf.get_api_key(email, password)

    assert status != 200
    assert 'key' not in result

#6
def test_get_api_key_wrong_password(email=valid_email, password=wrong_password):
    status, result = pf.get_api_key(email, password)

    assert status != 200
    assert 'key' not in result

#7
def test_add_new_pet_none_name(name=' ', animal_type='catminator', age='3', pet_photo='images/3.pdf'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status != 200

#8
def test_get_api_key_long_password(email=valid_email, password=long_password):
    status, result = pf.get_api_key(email, password)

    assert status != 200
    assert 'key' not in result

#9
def test_get_api_key_none_email(email=none_email, password=valid_password):
    status, result = pf.get_api_key(email, password)

    assert status != 200
    assert 'key' not in result

#10
def test_add_new_pet_char_age(name='Kitty', animal_type='catminator', age='qwe', pet_photo='images/2.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status != 200

###########################


