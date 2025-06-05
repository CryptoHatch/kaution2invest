#!/usr/bin/env python3
"""
Script to run tests and generate a report.
"""

import argparse
from utils.test_utils import generate_test_report, compare_with_previous_report

def main():
    parser = argparse.ArgumentParser(description='Run tests and generate a report')
    parser.add_argument('--output', '-o', default='test_report.json',
                      help='Output file for the test report (default: test_report.json)')
    parser.add_argument('--compare', '-c', action='store_true',
                      help='Compare with previous report')
    
    args = parser.parse_args()
    
    print("Running tests...")
    report = generate_test_report(args.output)
    
    print(f"\nTest Results: {report['passed']}/{report['total_tests']} tests passed ({report['pass_percentage']}%)")
    
    if args.compare:
        comparison = compare_with_previous_report(report, args.output)
        if 'is_first_run' in comparison:
            print(f"\n{comparison['message']}")
        else:
            test_diff = comparison['test_count_change']
            rate_diff = comparison['pass_rate_change']
            
            if test_diff != 0:
                test_change = 'increased' if test_diff > 0 else 'decreased'
                print(f"\nTest count has {test_change} by {abs(test_diff)} since last run.")
                
            rate_change = 'improved' if rate_diff >= 0 else 'decreased'
            print(f"Pass rate has {rate_change} by {abs(rate_diff)}% since last run.")
    
    print(f"\nReport saved to {args.output}")

if __name__ == '__main__':
    main() 