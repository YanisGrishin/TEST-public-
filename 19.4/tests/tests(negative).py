import os

from api import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()

def test_add_new_pet_negative_age(name='Kitty', animal_type='catminator', age='-3', pet_photo='images/2.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert age not in result['age']
    assert age < 0