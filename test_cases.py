from m_client import Client as Client_local
from pymemcache.client.base import Client
import unittest
import const


class TestMemcache(unittest.TestCase):
    def setUp(self):
        #Using client model developed as part of asssignment
        self.client_local = Client_local(const.server_address, 9889)
        # Using pymemcache Client
        self.client_regular = Client((const.server_address, 9889))

    def tearDown(self):
        self.client_regular.close()
        self.client_local.close()

    def test_local_set_success(self):
        self.assertTrue(self.client_local.set("test_key", "test_value", 0, 900), True)

    def test_local_set_failure(self):
        try:
            self.client_local.set("test_key", "test_value", 'str', 900)
        except Exception as e:
            self.assertTrue(e.args[0], 'Error writing data to Server')

    def test_local_get_success(self):
        self.client_local.set("test_key", "test_value", 0, 900)
        self.assertEqual(self.client_local.get("test_key"), b'test_value')

    def test_local_get_failure(self):
        self.assertFalse(self.client_local.get("test_key1"))

    def test_regular_set_failure(self):
        try:
            self.client_regular.set(key="test_key_reg", value="test_value", flags='str', expire=900, noreply=False)
        except Exception as e:
            self.assertTrue(e.args[0], b'set')

    def test_regular_set_success(self):
        self.assertTrue(self.client_regular.set(key="test_key_reg", value="test_value", flags = 0, expire=900, noreply=False))

    def test_regular_get_success(self):
        self.client_regular.set(key="test_key_reg", value="test_value", flags=0, expire=900, noreply=False)
        self.assertEqual(self.client_regular.get(key="test_key_reg"), b'test_value')

    def test_regular_get_failure(self):
        self.assertIsNone(self.client_regular.get(key="test_key_reg1"))

    #***Interesting test case***#
    def test_local_data_beyond_buffer(self):
        value = "a" * 10 * const.buffer_size
        self.client_local.set("test_key_max", value, 0, 900)
        self.assertEqual(self.client_local.get("test_key_max"), value.encode('utf-8'))
