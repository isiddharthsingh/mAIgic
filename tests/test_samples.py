import pytest

def test_addition():
    assert 2 + 2 == 4

def test_subtraction():
    assert 5 - 3 == 2

def test_multiplication():
    assert 3 * 3 == 9

def test_division():
    assert 8 / 2 == 4

def test_string_equality():
    assert "hello".upper() == "HELLO"

def test_list_append():
    lst = [1, 2, 3]
    lst.append(4)
    assert lst == [1, 2, 3, 4]

def test_dictionary_key():
    d = {"name": "Alice", "age": 30}
    assert "name" in d
    assert d["name"] == "Alice"

def test_raise_error():
    with pytest.raises(ZeroDivisionError):
        1 / 0
