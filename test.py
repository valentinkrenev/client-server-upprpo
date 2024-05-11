import unittest
from client import generate_hamming_code, register_user, send_message
from server import generate_hamming_code as server_generate_hamming_code, check_hamming_code, num_of_zero, is_name_unique

class TestClient(unittest.TestCase):
    def test_generate_hamming_code(self):
        self.assertEqual(generate_hamming_code('1011'), '1011010')
        self.assertEqual(generate_hamming_code('110'), '110010')
        self.assertEqual(generate_hamming_code('1111'), '11111000')
        self.assertEqual(generate_hamming_code('0'), '0010')
        self.assertEqual(generate_hamming_code(''), '0000')  # наличие пустой строки


    def test_register_user(self):
        # тестовые примеры для функции register_user
        # предполагая, что сервер недоступен во время тестирования, типа имитируем ответы сервера
        # проверка успешной регистрации
        self.assertIsNotNone(register_user('TestUser1'))
        # наличие уже занятого имени
        self.assertIsNone(register_user('TestUser1'))


    def test_send_message(self):
        #тож иммитация сервака
        self.assertIsNone(send_message('123', 'TestReceiver', 'TestMessage'))


class TestServer(unittest.TestCase):
    def test_generate_hamming_code(self):
        # хэминг на серваке
        self.assertEqual(server_generate_hamming_code('1011'), '1011010')
        self.assertEqual(server_generate_hamming_code('110'), '110010')
        self.assertEqual(server_generate_hamming_code('1111'), '11111000')
        self.assertEqual(server_generate_hamming_code('0'), '0010')
        self.assertEqual(server_generate_hamming_code(''), '0000')


    def test_check_hamming_code(self):
        self.assertEqual(check_hamming_code('1011010'), '1011010')  # нет ошибок
        self.assertEqual(check_hamming_code('1111010'), '1111010')  #однобитовая ошибка
        self.assertEqual(check_hamming_code('0010010'), '0010010')  # двухбитовая ошибка
        self.assertEqual(check_hamming_code('1011110'), '1011110')  # трёхьитовая
        self.assertEqual(check_hamming_code('1111111'), '1111111')  # ну для всех битиков


    def test_num_of_zero(self):
        self.assertEqual(num_of_zero(5), '000005')
        self.assertEqual(num_of_zero(100), '000100')
        self.assertEqual(num_of_zero(1000), '001000')
        self.assertEqual(num_of_zero(10000), '010000')
        self.assertEqual(num_of_zero(100000), '100000')


    def test_is_name_unique(self):
        global name_to_id
        name_to_id = {'TestUser1': 1, 'TestUser2': 2}
        self.assertFalse(is_name_unique('TestUser1'))
        self.assertFalse(is_name_unique('TestUser2'))
        self.assertTrue(is_name_unique('TestUser3'))


if __name__ == '__main__':
    unittest.main()
