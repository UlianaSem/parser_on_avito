import src.utils


def test_get_sorting_type():
    assert src.utils.get_sorting_type(' По умолчанию') == ''
    assert src.utils.get_sorting_type('по дате') == 3
    assert src.utils.get_sorting_type('сначала дешевле  ') == 1
    assert src.utils.get_sorting_type('сначала дороже') == 2
    assert src.utils.get_sorting_type('непонятно что') == ''
