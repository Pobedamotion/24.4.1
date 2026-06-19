# PetFriends API Tests

## Task
API tests for PetFriends website using requests + parametrize.
Found 6 bugs in the system through negative and parametrized testing.

## Tests - 21 total

Parametrized tests:
- test_get_all_pets_with_valid_key[empty string, only my pets] ✅
- test_get_all_pets_with_negative_filter[255, 1000, russian, specials, digit] ✅

Plus 15 individual tests (positive/negative/destructive)

## Bugs found
- Empty name accepted (should reject)
- Empty age accepted (should reject)
- Very long name accepted (should reject)
- Deleting non-existing pet returns 200 (should be 404)
- Invalid filter values cause 500 error (should be 400)

## How to run
pip install requests pytest
pytest tests/test_pet_friends.py -v

## Results
21 passed in 39.97s ✅
