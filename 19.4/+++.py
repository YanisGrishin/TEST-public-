def test_add_new_pet_negative_age(name='Richi', animal_type='немецкая овчарка', age='-3', pet_photo='images/dog.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(val_email, val_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 400
    assert age not in result['age']
    assert int(age) < 0