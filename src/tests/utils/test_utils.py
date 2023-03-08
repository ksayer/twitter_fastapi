import re

import pytest

from src.utils import get_available_name, get_random_string


@pytest.mark.parametrize('file_name', ['asdasdfgjfghfabSa', 'afghjkcvbrtrsGsas.txt'])
def test_get_available_name_free_name(file_name):
    available_name = get_available_name(file_name)
    assert file_name == available_name


@pytest.mark.parametrize('file_fixture', ['qwswqasjs', 'asxqasdsa.txt'], indirect=True)
def test_get_available_name_used_name(file_fixture):
    available_name = get_available_name(file_fixture)
    assert file_fixture != available_name
    assert re.match(r'^\w+_\w{5}\.{0,1}\w*$', available_name)


def test_get_random_string():
    string = get_random_string()
    assert len(string) == 5
    string = get_random_string(7)
    assert len(string) == 7
    string = get_random_string(100, 'qaSz1')
    assert all(s in 'qaSz1' for s in string)
