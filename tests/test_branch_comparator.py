import unittest
from branch_comparator import BranchComparator


class TestBranchComparator(unittest.TestCase):

    def setUp(self):
        self.branch1_data = {
            "packages": [
                {"name": "pkg1", "version": "1.2.3", "release": "alt1", "arch": "x86_64"},
                {"name": "pkg2", "version": "1.2.3", "release": "alt2", "arch": "x86_64"},
            ]
        }
        self.branch2_data = {
            "packages": [
                {"name": "pkg1", "version": "1.2.3", "release": "alt1", "arch": "x86_64"},
                {"name": "pkg2", "version": "1.2.3", "release": "alt1", "arch": "x86_64"},
            ]
        }
        self.comparator = BranchComparator('branch1', 'branch2')

    def test_compare_branches(self):
        self.comparator.get_packages = lambda branch: self.branch1_data if branch == 'branch1' else self.branch2_data
        result = self.comparator.compare_branches()

        # Проверяем, что архитектура x86_64 есть в результатах
        self.assertIn('x86_64', result)
        # Проверяем, что pkg2 в первой ветке новее
        self.assertIn('branch1_newer', result['x86_64'])
        self.assertIn('pkg2', result['x86_64']['branch1_newer'])


if __name__ == '__main__':
    unittest.main()
