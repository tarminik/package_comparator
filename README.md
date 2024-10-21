# Package Comparator CLI

## Description

This CLI tool compares binary packages between two ALT Linux branches (e.g., `sisyphus` and `p10`) and outputs the differences in JSON format. The tool supports comparison across all architectures available for each branch.

## Installation

1. Clone the repository and navigate to the project directory:

   ```bash
   git clone https://github.com/tarminik/package_comparator.git
   cd package_comparator
   ```
2. Ensure you have Python 3.x and the necessary dependencies installed. Use the following command to install them:
   ```bash
   pip install -r requirements.txt
   ```
   
3. Make the script executable:
   ```bash
   chmod +x compare_packages.py
   ```

## Usage

The tool compares the binary packages of two ALT Linux branches and outputs the result in JSON format. You can specify the branch names and an optional file to save the result.

Example command:
```bash
./compare_packages.py --branch1 sisyphus --branch2 p10 --output result.json
```

### Parameters:
 - ```--branch1``` – The first branch to compare (e.g., sisyphus).
 - ```--branch2``` – The second branch to compare (e.g., p10).
 - ```--output``` – (Optional) The file to save the comparison result. If not provided, the result will be printed to the console.

This will compare the packages from the two branches across all supported architectures and output the differences in the `result.json` file.

## Result Format (result.json)

The result is a JSON object with the following structure:
```
{
    "arch1": {
        "branch2_not_in_branch1": [
            "package_name1",
            "package_name2",
            ...
        ],
        "branch1_not_in_branch2": [
            "package_name3",
            "package_name4",
            ...
        ],
        "branch1_newer": {
            "package_name5": {
                "branch1_version": "version-release",
                "branch2_version": "version-release"
            },
            "package_name6": {
                "branch1_version": "version-release",
                "branch2_version": "version-release"
            },
            ...
        }
    },
    "arch2": {
        ...
    }
}
```

### Explanation:
 - "arch1": Represents the architecture (e.g., `x86_64`, `i586`, etc.). The result is separated by architectures.
 - "branch2_not_in_branch1": Lists the packages that are present in `branch2` but not in `branch1`.
 - "branch1_not_in_branch2": Lists the packages that are present in `branch1` but not in `branch2`.
 - "branch1_newer": A nested object showing packages where the version in `branch1` is newer than in `branch2`. Each package has its version in both branches.


## Running Unit Tests

This project includes unit tests to validate the comparison logic.

### Running All Tests

To run all unit tests in the project, use the following command:

```bash
python3 -m unittest discover -s tests
```

This command will search for and execute all test files located in the `tests` directory.

### Running Specific Test Files

If you want to run tests for a specific module, for example, the tests for `rpm_version_compare`, use this command:

```bash
python3 -m unittest tests.test_rpm_version_compare
```

You can also run tests for `branch_comparator`:

```bash
python3 -m unittest tests.test_branch_comparator
```

### Adding New Tests

If you want to add new tests, place them in the `tests/` directory following this structure:

```
tests/
├── test_rpm_version_compare.py
└── test_branch_comparator.py
```

Make sure to follow the `unittest` framework structure when writing new test cases.
