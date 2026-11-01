import mockdemo.myCode as myCode

def test_build_url(mocker):

    mocker.patch.object(myCode, 'BASE_URL', 'http://localhost/products')

    actual = myCode.build_url(minPrice=100, maxPrice=500, order='desc')
    expected = 'http://localhost/products?minPrice=100&maxPrice=500&order=desc'
    assert expected == actual
