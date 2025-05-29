import pytest


@pytest.fixture(scope='class')
def login():
    a = '123'
    print("输入账号密码登陆")


class TestLogin:
    def test_1(self):
        print("用例1")

    def test_2(self, login):
        print("用例2")

    def test_3(self, login):
        print("用例3")

    def test_4(self):
        print("用例4")


if __name__ == '__main__':
    pytest.main()