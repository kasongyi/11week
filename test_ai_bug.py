
import pytest
from bug3_logic import find_max


# 1. 정상 테스트
def test_find_max_normal():
    assert find_max([70, 85, 60, 95]) == 95


# 2. 최고점이 첫 번째에 있는 경우
def test_find_max_first():
    assert find_max([100, 80, 60]) == 100


# 3. 최고점이 마지막에 있는 경우
def test_find_max_last():
    assert find_max([70, 85, 95]) == 95


# 4. 원소가 하나인 경우 (경계값)
def test_find_max_one():
    assert find_max([80]) == 80


# 5. 빈 리스트인 경우 (예외)
def test_find_max_empty():
    with pytest.raises(IndexError):
        find_max([])


# 6. 원소가 두 개인 경우 (경계값)
def test_find_max_two():
    assert find_max([70, 90]) == 90
