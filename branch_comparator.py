import requests
import json
from collections import defaultdict
from rpm_version_compare import RPMVersionCompare


class BranchComparator:
    def __init__(self, branch1, branch2):
        self.branch1 = branch1
        self.branch2 = branch2

    def get_packages(self, branch):
        url = f"https://rdb.altlinux.org/api/export/branch_binary_packages/{branch}"
        response = requests.get(url)
        if response.status_code == 200:
            try:
                return response.json()  # Convert data to JSON
            except json.JSONDecodeError:
                raise Exception("Error decoding JSON response from API")
        else:
            raise Exception(f"Error fetching data for {branch}, status code: {response.status_code}")

    def group_by_arch(self, packages):
        grouped_packages = defaultdict(list)
        for pkg in packages:
            arch = pkg['arch']
            grouped_packages[arch].append(pkg)
        return grouped_packages

    def compare_lists(self, list1, list2):
        list1_packages = {pkg['name']: pkg for pkg in list1}
        list2_packages = {pkg['name']: pkg for pkg in list2}

        # Packages present in list1 but not in list2, and vice versa
        list1_not_in_list2 = [pkg for pkg in list1_packages if pkg not in list2_packages]
        list2_not_in_list1 = [pkg for pkg in list2_packages if pkg not in list1_packages]

        return list1_not_in_list2, list2_not_in_list1

    def compare_versions_across_archs(self, list1, list2):
        newer_in_list1 = {}

        list1_dict = {pkg['name']: pkg for pkg in list1}
        list2_dict = {pkg['name']: pkg for pkg in list2}

        # Compare package versions between branches
        for name, pkg_list1 in list1_dict.items():
            if name in list2_dict:
                pkg_list2 = list2_dict[name]
                list1_vr = f"{pkg_list1['version']}-{pkg_list1['release']}"
                list2_vr = f"{pkg_list2['version']}-{pkg_list2['release']}"
                # If the version in list1 is newer, add to the result
                if RPMVersionCompare.rpm_label_compare((0, list1_vr, ''), (0, list2_vr, '')) > 0:
                    newer_in_list1[name] = {
                        'list1_version': list1_vr,
                        'list2_version': list2_vr
                    }

        return newer_in_list1

    def compare_branches(self):
        branch1_data = self.get_packages(self.branch1)
        branch2_data = self.get_packages(self.branch2)

        # Extract package lists
        branch1_packages = branch1_data['packages']
        branch2_packages = branch2_data['packages']

        # Group packages by architecture
        branch1_packages_by_arch = self.group_by_arch(branch1_packages)
        branch2_packages_by_arch = self.group_by_arch(branch2_packages)

        # Results per architecture
        result = {}

        for arch in branch1_packages_by_arch:
            if arch in branch2_packages_by_arch:
                branch1_arch_packages = branch1_packages_by_arch[arch]
                branch2_arch_packages = branch2_packages_by_arch[arch]

                branch1_not_in_branch2, branch2_not_in_branch1 = self.compare_lists(branch1_arch_packages,
                                                                                    branch2_arch_packages)
                branch1_newer = self.compare_versions_across_archs(branch1_arch_packages, branch2_arch_packages)

                result[arch] = {
                    f"{self.branch2}_not_in_{self.branch1}": branch2_not_in_branch1,
                    f"{self.branch1}_not_in_{self.branch2}": branch1_not_in_branch2,
                    f"{self.branch1}_newer": branch1_newer
                }

        return result
