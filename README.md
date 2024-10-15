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

4. (Optional) Move the script to /usr/local/bin for easy access from anywhere:
   ```bash
   sudo cp compare_packages.py /usr/local/bin/package_comparator
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