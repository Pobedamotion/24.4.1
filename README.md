# 24.4.1 PetFriends API Tests

## Task
API tests for PetFriends website using requests library.

## Tests included

- test_get_api_key_for_valid_user — gets API key ✅
- test_get_all_pets_with_valid_key — gets list of pets ✅
- test_add_new_pet_with_valid_data — adds new pet ✅
- test_delete_pet — deletes pet ✅
- test_update_pet_info — updates pet info ✅

## How to run

Install libraries:
pip install requests pytest

Add your credentials to settings.py:
valid_email = 'your_email@mail.com'
valid_password = 'your_password'

Run tests:
pytest tests/test_pet_friends.py

## Results

5 passed in 15.99s ✅
