import mockdemo.myCode as myCode


def test_get_meaning_of_life(mocker):

    mocker.patch(
        'mockdemo.myCode.calculate_meaning_of_life',
        lambda: 'wibble'
    )

    actual = myCode.get_meaning_of_life()
    expected = 'The meaning of life is wibble'
    assert expected == actual
