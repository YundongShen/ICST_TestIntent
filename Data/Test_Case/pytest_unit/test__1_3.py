import mockdemo.myCode as myCode



def test_get_product(mocker):

    mocker.patch(
        'mockdemo.myCode.DataLoader.load_product',
        lambda self: 'wibble'
    )

    actual = myCode.get_product()

    expected = 'Product is wibble'

    assert expected == actual
