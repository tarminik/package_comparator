#!/usr/bin/env python3


import requests
import json
import argparse
import rpm


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


# Функция для сравнения двух списков пакетов и поиска различий
def compare_lists(p10_list, sisyphus_list):
    p10_packages = {pkg['name']: pkg for pkg in p10_list}
    sisyphus_packages = {pkg['name']: pkg for pkg in sisyphus_list}

    # Пакеты, которые есть в p10, но нет в sisyphus, и наоборот
    p10_not_in_sisyphus = [pkg for pkg in p10_packages if pkg not in sisyphus_packages]
    sisyphus_not_in_p10 = [pkg for pkg in sisyphus_packages if pkg not in p10_packages]

    return p10_not_in_sisyphus, sisyphus_not_in_p10


# Функция для сравнения версий пакетов между ветками для всех архитектур
def compare_versions_across_archs(p10_packages, sisyphus_packages):
    sisyphus_newer = {}

    # Преобразуем списки пакетов в словари для удобства сравнения по имени пакета
    p10_dict = {pkg['name']: pkg for pkg in p10_packages}
    sisyphus_dict = {pkg['name']: pkg for pkg in sisyphus_packages}

    # Сравниваем версии пакетов между ветками
    for name, pkg_sisyphus in sisyphus_dict.items():
        if name in p10_dict:
            pkg_p10 = p10_dict[name]
            sisyphus_vr = get_full_version(pkg_sisyphus)
            p10_vr = get_full_version(pkg_p10)
            # Если версия в sisyphus новее, добавляем в результат
            if compare_versions(sisyphus_vr, p10_vr) > 0:
                sisyphus_newer[name] = {
                    'p10_version': p10_vr,
                    'sisyphus_version': sisyphus_vr
                }

    return sisyphus_newer


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

    # print("Branch 1 packages (first 5):", [(pkg['name'], pkg['version']) for pkg in branch1_packages[:5]])
    # print("Branch 2 packages (first 5):", [(pkg['name'], pkg['version']) for pkg in branch2_packages[:5]])

    # Сравнение пакетов между ветками
    branch1_not_in_branch2, branch2_not_in_branch1 = compare_lists(branch2_packages, branch1_packages)
    branch1_newer = compare_versions_across_archs(branch2_packages, branch1_packages)

    result = {
        f"{args.branch2}_not_in_{args.branch1}": branch2_not_in_branch1,
        f"{args.branch1}_not_in_{args.branch2}": branch1_not_in_branch2,
        f"{args.branch1}_newer": branch1_newer
    }

    if args.output:
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=4)
    else:
        print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()
