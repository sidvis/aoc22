import pytest

from helpers.inputs import AocData, DataParser

class TestAocData():
    def test_from_str(self):
        s = (
        "1a\n"
        "2b\n"
        "3c"
        )
        d = AocData.from_str(s)
        assert d.data == ['1a', '2b', '3c']

    def test_from_file(self, tmp_path):
        import os
        p = os.path.join(tmp_path, "test")
        with open(p, 'w') as f:
            f.write(
                "1a\n"
                "2b\n"
                "3c"
            )

        d = AocData.from_file(p)
        assert d.data == ['1a', '2b', '3c']

    def test_split_group(self):
        s = (
        "1a\n"
        "\n"
        "\n"
        "2b\n"
        "3c"
        )
        d = AocData.from_str(s)
        L = d.split_groups(sep='')
        assert len(L) == 3
        assert L[0].data == ['1a']
        assert L[1].data == []
        assert L[2].data == ['2b', '3c']


class TestDataParser():
    def test_constructor_single(self):
        with pytest.raises(AssertionError):
            p = DataParser(int, sep=',')

        p = DataParser(int)

    def test_constructor_multiple(self):
        with pytest.raises(AssertionError):
            p = DataParser(int, int, sep=None)

        p = DataParser(int,int,sep=',')

    def test_parse_line_single(self):
        p = DataParser(int)
        assert p.parse_line("1") == int(1)

        with pytest.raises(ValueError):
            p.parse_line("a")

    def test_parse_line_multiple(self):
        p = DataParser(int, str, sep=',', check_len=True)
        assert p.parse_line("1,a") == (1, 'a')

        with pytest.raises(AssertionError):
            p.parse_line("1")

        with pytest.raises(AssertionError):
            p.parse_line("1,a,b")
