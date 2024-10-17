#!/usr/bin/env python3

import requests
import json
import argparse
import rpm
from collections import defaultdict


# Функция для получения списка пакетов с API
def get_packages(branch):
    url = f"https://rdb.altlinux.org/api/export/branch_binary_packages/{branch}"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            return response.json()  # Преобразуем данные в формат JSON
        except json.JSONDecodeError:
            raise Exception("Error decoding JSON response from API")
    else:
        raise Exception(f"Error fetching data for {branch}, status code: {response.status_code}")


# Функция для объединения версии и релиза пакета в одну строку
def get_full_version(pkg):
    return f"{pkg['version']}-{pkg['release']}"


# Функция для сравнения версий пакетов с использованием RPM
def compare_versions(vr1, vr2):
    return rpm.labelCompare((None, vr1, ''), (None, vr2, ''))


# Функция для группировки пакетов по архитектурам
def group_by_arch(packages):
    grouped_packages = defaultdict(list)
    for pkg in packages:
        arch = pkg['arch']
        grouped_packages[arch].append(pkg)
    return grouped_packages


# Функция для сравнения двух списков пакетов и поиска различий
def compare_lists(list1, list2):
    list1_packages = {pkg['name']: pkg for pkg in list1}
    list2_packages = {pkg['name']: pkg for pkg in list2}

    # Пакеты, которые есть в list1, но нет в list2, и наоборот
    list1_not_in_list2 = [pkg for pkg in list1_packages if pkg not in list2_packages]
    list2_not_in_list1 = [pkg for pkg in list2_packages if pkg not in list1_packages]

    return list1_not_in_list2, list2_not_in_list1


# Функция для сравнения версий пакетов между ветками для всех архитектур
def compare_versions_across_archs(list1, list2):
    newer_in_list1 = {}

    # Преобразуем списки пакетов в словари для удобства сравнения по имени пакета
    list1_dict = {pkg['name']: pkg for pkg in list1}
    list2_dict = {pkg['name']: pkg for pkg in list2}

    # Сравниваем версии пакетов между ветками
    for name, pkg_list1 in list1_dict.items():
        if name in list2_dict:
            pkg_list2 = list2_dict[name]
            list1_vr = get_full_version(pkg_list1)
            list2_vr = get_full_version(pkg_list2)
            # Если версия в list1 новее, добавляем в результат
            if compare_versions(list1_vr, list2_vr) > 0:
                newer_in_list1[name] = {
                    'list2_version': list2_vr,
                    'list1_version': list1_vr
                }

    return newer_in_list1


# Парсинг аргументов командной строки
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

    # Извлекаем список пакетов из поля 'packages'
    branch1_packages = branch1_data['packages']
    branch2_packages = branch2_data['packages']

    # Группируем пакеты по архитектурам
    branch1_packages_by_arch = group_by_arch(branch1_packages)
    branch2_packages_by_arch = group_by_arch(branch2_packages)

    # Результат по каждой архитектуре
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

    # Выводим результат
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=4)
    else:
        print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()
