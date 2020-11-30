from src.field import ZpField


def test_zp_field_invert():
    field = ZpField(order=11)

    assert field.invert(3) == 4
    assert field.invert(12) == 1
    assert field.invert(24) == 6
    assert field.invert(-1) == 10
    assert field.invert(-50) == 9


def test_zp_field_modulus():
    field = ZpField(order=11)

    assert field.modulus(11) == 0
    assert field.modulus(12) == 1
    assert field.modulus(24) == 2
    assert field.modulus(-1) == 10
    assert field.modulus(-56) == 10
