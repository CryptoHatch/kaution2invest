"""
Utilities for test reporting and management.
"""

import subprocess
import datetime
import json
import os

def generate_test_report(output_file='test_report.json'):
    """
    Run the tests and generate a report of the results.
    
    Args:
        output_file (str): Path to save the JSON report
        
    Returns:
        dict: Report data
    """
    # Run pytest with JSON output
    result = subprocess.run(
        ['pytest', '--json-report', '--json-report-file=none'],
        capture_output=True,
        text=True
    )
    
    # Extract test results
    passed = result.stdout.count('PASSED')
    failed = result.stdout.count('FAILED')
    total = passed + failed
    
    # Create report
    report = {
        'timestamp': datetime.datetime.now().isoformat(),
        'total_tests': total,
        'passed': passed,
        'failed': failed,
        'pass_percentage': round((passed / total) * 100, 2) if total > 0 else 0,
        'command_output': result.stdout
    }
    
    # Save report to file
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
            
    return report

def compare_with_previous_report(current_report, previous_report_file='test_report.json'):
    """
    Compare current test results with previous report.
    
    Args:
        current_report (dict): Current test report
        previous_report_file (str): Path to previous report
        
    Returns:
        dict: Comparison data
    """
    if not os.path.exists(previous_report_file):
        return {
            'is_first_run': True,
            'message': 'No previous report found for comparison'
        }
    
    # Load previous report
    with open(previous_report_file, 'r') as f:
        previous_report = json.load(f)
    
    # Compare
    comparison = {
        'previous_timestamp': previous_report['timestamp'],
        'current_timestamp': current_report['timestamp'],
        'test_count_change': current_report['total_tests'] - previous_report['total_tests'],
        'pass_rate_change': current_report['pass_percentage'] - previous_report['pass_percentage'],
        'is_improved': current_report['pass_percentage'] >= previous_report['pass_percentage']
    }
    
    return comparison

if __name__ == '__main__':
    # Example usage
    report = generate_test_report()
    print(f"Test Report: {report['passed']}/{report['total_tests']} tests passed ({report['pass_percentage']}%)")
    
    # Compare with previous if available
    comparison = compare_with_previous_report(report)
    if 'is_first_run' not in comparison:
        change = comparison['pass_rate_change']
        direction = 'improved' if change >= 0 else 'decreased'
        print(f"Pass rate has {direction} by {abs(change)}% since last run") 