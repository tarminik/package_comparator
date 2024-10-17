#!/usr/bin/env python3

import argparse
import json
from branch_comparator import BranchComparator

# Command-line argument parsing
def parse_args():
    parser = argparse.ArgumentParser(description="Compare ALT Linux branches packages")
    parser.add_argument('--branch1', required=True, help="First branch (e.g., sisyphus)")
    parser.add_argument('--branch2', required=True, help="Second branch (e.g., p10)")
    parser.add_argument('--output', required=False, help="Output file for the comparison result")
    return parser.parse_args()

def main():
    args = parse_args()

    comparator = BranchComparator(args.branch1, args.branch2)
    result = comparator.compare_branches()

    # Output the result
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=4)
    else:
        print(json.dumps(result, indent=4))

if __name__ == "__main__":
    main()
