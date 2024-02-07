import unittest
from modules.shell_env_to_json import ShellEnvToJSON


class test_env_to_json(unittest.TestCase):

    def test_env_exports_to_json(self):
        __expected = {
            "TEST1": "'foo'",
            "TEST2": "'bar'",
            "TEST3": "'Alice'",
            "TEST4": "'Bob'",
            "TEST6": "'foo'",
            "TEST7": "'bar'",
        }
        __setj = ShellEnvToJSON()
        __setj.exports_only = False
        __read = __setj.scan_file('./tests/mock_env_exports_to_json.sh')

        self.assertDictEqual(__expected, __read, 'Read all variable-like = statements')

        __expected = {
            "TEST1": "'foo'",
            "TEST2": "'bar'",
            "TEST6": "'foo'",
        }
        __setj = ShellEnvToJSON()
        __read = __setj.scan_file('./tests/mock_env_exports_to_json.sh')

        self.assertDictEqual(__expected, __read, 'Read exports only (default)')


if __name__ == '__main__':
    unittest.main()
