import unittest
from rpm_version_compare import RPMVersionCompare

class TestRPMVersionCompare(unittest.TestCase):

    def test_compare_epoch(self):
        evr1 = ('1', '1.2.3', 'alt1')
        evr2 = ('0', '1.2.3', 'alt1')
        self.assertEqual(RPMVersionCompare.rpm_label_compare(evr1, evr2), 1)
        self.assertEqual(RPMVersionCompare.rpm_label_compare(evr2, evr1), -1)
        self.assertEqual(RPMVersionCompare.rpm_label_compare(evr1, evr1), 0)

    def test_compare_version(self):
        evr1 = ('0', '1.2.4', 'alt1')
        evr2 = ('0', '1.2.3', 'alt1')
        self.assertEqual(RPMVersionCompare.rpm_label_compare(evr1, evr2), 1)
        self.assertEqual(RPMVersionCompare.rpm_label_compare(evr2, evr1), -1)
        self.assertEqual(RPMVersionCompare.rpm_label_compare(evr1, evr1), 0)

    def test_compare_release(self):
        evr1 = ('0', '1.2.3', 'alt2')
        evr2 = ('0', '1.2.3', 'alt1')
        self.assertEqual(RPMVersionCompare.rpm_label_compare(evr1, evr2), 1)
        self.assertEqual(RPMVersionCompare.rpm_label_compare(evr2, evr1), -1)
        self.assertEqual(RPMVersionCompare.rpm_label_compare(evr1, evr1), 0)

if __name__ == '__main__':
    unittest.main()
