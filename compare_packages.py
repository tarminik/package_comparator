#!/usr/bin/env python3

import requests
import json
import argparse
from rpm_version_compare import RPMVersionCompare
from collections import defaultdict


# Function to get the list of packages from the API
def get_packages(branch):
    url = f"https://rdb.altlinux.org/api/export/branch_binary_packages/{branch}"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            return response.json()  # Convert data to JSON
        except json.JSONDecodeError:
            raise Exception("Error decoding JSON response from API")
    else:
        raise Exception(f"Error fetching data for {branch}, status code: {response.status_code}")


# Function to combine version and release into a single string
def get_full_version(pkg):
    return f"{pkg['version']}-{pkg['release']}"


# Function to compare package versions using RPM
def compare_versions(vr1, vr2):
    return RPMVersionCompare.rpm_label_compare((0, vr1, ''), (0, vr2, ''))


# Function to group packages by architecture
def group_by_arch(packages):
    grouped_packages = defaultdict(list)
    for pkg in packages:
        arch = pkg['arch']
        grouped_packages[arch].append(pkg)
    return grouped_packages


# Function to compare two lists of packages and find differences
def compare_lists(list1, list2):
    list1_packages = {pkg['name']: pkg for pkg in list1}
    list2_packages = {pkg['name']: pkg for pkg in list2}

    # Packages present in list1 but not in list2, and vice versa
    list1_not_in_list2 = [pkg for pkg in list1_packages if pkg not in list2_packages]
    list2_not_in_list1 = [pkg for pkg in list2_packages if pkg not in list1_packages]

    return list1_not_in_list2, list2_not_in_list1


# Function to compare package versions between branches for all architectures
def compare_versions_across_archs(list1, list2):
    newer_in_list1 = {}

    # Convert package lists to dictionaries for easier comparison by package name
    list1_dict = {pkg['name']: pkg for pkg in list1}
    list2_dict = {pkg['name']: pkg for pkg in list2}

    # Compare package versions between branches
    for name, pkg_list1 in list1_dict.items():
        if name in list2_dict:
            pkg_list2 = list2_dict[name]
            list1_vr = get_full_version(pkg_list1)
            list2_vr = get_full_version(pkg_list2)
            # If the version in list1 is newer, add to the result
            if compare_versions(list1_vr, list2_vr) > 0:
                newer_in_list1[name] = {
                    'list2_version': list2_vr,
                    'list1_version': list1_vr
                }

    return newer_in_list1


# Command-line argument parsing
def parse_args():
    parser = argparse.ArgumentParser(description="Compare ALT Linux branches packages")
    parser.add_argument('--branch1', required=True, help="First branch (e.g., sisyphus)")
    parser.add_argument('--branch2', required=True, help="Second branch (e.g., p10)")
    parser.add_argument('--output', required=False, help="Output file for the comparison result")
    return parser.parse_args()


def main():
    args = parse_args()

    branch1_data = get_packages(args.branch1)
    branch2_data = get_packages(args.branch2)

    # Extract package lists
    branch1_packages = branch1_data['packages']
    branch2_packages = branch2_data['packages']

    # Group packages by architecture
    branch1_packages_by_arch = group_by_arch(branch1_packages)
    branch2_packages_by_arch = group_by_arch(branch2_packages)

    # Results per architecture
    result = {}

    for arch in branch1_packages_by_arch:
        if arch in branch2_packages_by_arch:
            branch1_arch_packages = branch1_packages_by_arch[arch]
            branch2_arch_packages = branch2_packages_by_arch[arch]

            branch1_not_in_branch2, branch2_not_in_branch1 = compare_lists(branch2_arch_packages, branch1_arch_packages)
            branch1_newer = compare_versions_across_archs(branch2_arch_packages, branch1_arch_packages)

            result[arch] = {
                f"{args.branch2}_not_in_{args.branch1}": branch2_not_in_branch1,
                f"{args.branch1}_not_in_{args.branch2}": branch1_not_in_branch2,
                f"{args.branch1}_newer": branch1_newer
            }

    # Output the result
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=4)
    else:
        print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()
