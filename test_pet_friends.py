def generate_string(num):
    return "x" * num

def russian_chars():
    return 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

def special_chars():
    return '|\\/!@#$%^&*()-_=+`~?"№;:[]{}'

import pytest
from petfriends.api import PetFriends
from petfriends.settings import valid_email, valid_password

pf = PetFriends()


def test_get_api_key_for_valid_user():
    """Тест получения API ключа для валидного пользователя"""
    status, result = pf.get_api_key(valid_email, valid_password)
    assert status == 200
    assert 'key' in result


@pytest.mark.parametrize("filter", ['', 'my_pets'],
                         ids=['empty string', 'only my pets'])
def test_get_all_pets_with_valid_key(filter):
    """Параметризованный тест получения списка питомцев"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

@pytest.mark.parametrize("filter", [
    generate_string(255),
    generate_string(1001),
    russian_chars(),
    special_chars(),
    123
], ids=['255 symbols', 'more than 1000 symbols', 'russian', 'specials', 'digit'])
def test_get_all_pets_with_negative_filter(filter):
    """Баг: сервер возвращает 500 вместо 400 при некорректном filter"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 500  # баг сервера — должно быть 400

def test_add_new_pet_with_valid_data():
    """Тест добавления нового питомца с валидными данными"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(
        auth_key,
        name='Мурзик',
        animal_type='кот',
        age='2',
        pet_photo='petfriends/images/cat.jpg'
    )
    assert status == 200
    assert result['name'] == 'Мурзик'


def test_delete_pet():
    """Тест удаления питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    pet_id = my_pets['pets'][0]['id']
    status, result = pf.delete_pet(auth_key, pet_id)
    assert status == 200


def test_update_pet_info():
    """Тест обновления информации о питомце"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    pet_id = my_pets['pets'][0]['id']
    status, result = pf.update_pet_info(
        auth_key, pet_id,
        name='Барсик',
        animal_type='кот',
        age='3'
    )
    assert status == 200
    assert result['name'] == 'Барсик'

def test_add_pet_without_photo():
    """Позитивный тест добавления питомца без фото"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(
        auth_key, name='Пушок', animal_type='кот', age='1')
    assert status == 200
    assert result['name'] == 'Пушок'

def test_add_photo_to_pet():
    """Позитивный тест добавления фото к питомцу"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_photo_of_pet(
        auth_key, pet_id, 'petfriends/images/cat.jpg')
    assert status == 200

def test_get_api_key_with_wrong_password():
    """Негативный тест — неверный пароль"""
    status, result = pf.get_api_key(valid_email, 'wrong_password')
    assert status == 403

def test_get_api_key_with_wrong_email():
    """Негативный тест — неверный email"""
    status, result = pf.get_api_key('wrong@email.com', valid_password)
    assert status == 403

def test_get_pets_with_wrong_key():
    """Негативный тест — неверный ключ"""
    auth_key = {'key': 'wrong_key_123'}
    status, result = pf.get_list_of_pets(auth_key, '')
    assert status == 403

def test_add_pet_with_empty_name():
    """Баг: сайт принимает питомца с пустым именем"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(
        auth_key, name='', animal_type='кот', age='1')
    assert status == 200

def test_add_pet_with_empty_age():
    """Баг: сайт принимает питомца с пустым возрастом"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(
        auth_key, name='Барсик', animal_type='кот', age='')
    assert status == 200

def test_get_only_my_pets():
    """Позитивный тест — получить только своих питомцев"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, 'my_pets')
    assert status == 200

def test_add_pet_with_long_name():
    """Баг: сайт принимает питомца с очень длинным именем"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(
        auth_key, name='А' * 1000, animal_type='кот', age='1')
    assert status == 200

def test_delete_not_existing_pet():
    """Баг: сайт возвращает 200 при удалении несуществующего питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.delete_pet(auth_key, '000000')
    assert status == 200