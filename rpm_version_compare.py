import re

class RPMVersionCompare:
    """
    A class to mimic the functionality of rpm.labelCompare for comparing RPM version strings.
    """

    @staticmethod
    def rpm_label_compare(evr1, evr2):
        """
        Compare two RPM version strings in the format (epoch, version, release).
        evr1 and evr2 are tuples in the form (epoch, version, release).
        Returns:
            1 if evr1 is newer,
           -1 if evr2 is newer,
            0 if both are identical.
        """
        epoch1, version1, release1 = evr1
        epoch2, version2, release2 = evr2

        # Compare epoch first (numerically)
        epoch1 = int(epoch1) if epoch1 else 0
        epoch2 = int(epoch2) if epoch2 else 0
        if epoch1 > epoch2:
            return 1
        elif epoch1 < epoch2:
            return -1

        # If epochs are equal, compare version (using rpm-style version comparison)
        vercmp_result = RPMVersionCompare.rpmvercmp(version1, version2)
        if vercmp_result != 0:
            return vercmp_result

        # If versions are equal, compare release
        return RPMVersionCompare.rpmvercmp(release1, release2)

    @staticmethod
    def rpmvercmp(v1, v2):
        """
        Compare two version or release strings according to RPM rules.
        This function mimics the RPM version comparison logic.
        """
        # Split versions into alphanumeric components
        def split_components(s):
            return re.findall(r'(\d+|[a-zA-Z]+|\~)', s)

        v1_components = split_components(v1)
        v2_components = split_components(v2)

        # Compare components one by one
        for a, b in zip(v1_components, v2_components):
            if a.isdigit() and b.isdigit():
                # Compare numbers numerically
                a_num = int(a)
                b_num = int(b)
                if a_num > b_num:
                    return 1
                elif a_num < b_num:
                    return -1
            else:
                # Compare alphabetic components lexicographically
                if a > b:
                    return 1
                elif a < b:
                    return -1

        # If all components are equal so far, compare lengths
        if len(v1_components) > len(v2_components):
            return 1
        elif len(v1_components) < len(v2_components):
            return -1

        # Versions are identical
        return 0
