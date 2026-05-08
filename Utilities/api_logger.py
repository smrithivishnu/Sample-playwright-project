"""
API Logger Utility Module

This module provides centralized logging functionality for API tests.
Can be imported and used across different test files to maintain consistent logging.
"""

import json
import os
from datetime import datetime


class APILogger:
    """
    Centralized API logging utility for consistent test execution tracking
    """
    
    def __init__(self, log_file_name="api_execution_log.txt"):
        """
        Initialize the API logger with a specific log file name
        """
        self.log_file_name = log_file_name
        log_dir = os.path.join(os.getcwd(), "logs")
        os.makedirs(log_dir, exist_ok=True)

        self.log_file_path = os.path.join(log_dir, log_file_name)

        # Ensure log directory exists
        log_dir = os.path.dirname(self.log_file_path)
        os.makedirs(log_dir, exist_ok=True)
    
    def log_api_execution(self, test_name, payload_data, response_data, execution_time=None):
        """
        Log API execution details for tracking and debugging
        """
        timestamp = execution_time or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        log_entry = f"""
        === API Execution Log ===
        Timestamp: {timestamp}
        Test Name: {test_name}

        Request Payload:
        {json.dumps(payload_data, indent=2)}

        Response Data:
        {json.dumps(response_data, indent=2)}

        {'='*50}
        """
        
        # Append to log file
        try:
            with open(self.log_file_path, 'a') as log_file:
                log_file.write(log_entry)
                print(f"API execution logged: {test_name}")
        except Exception as e:
            print(f"Error writing to log file: {e}")
    
    def save_execution_log(self):
        """
        Save the current execution log to a file
        """
        try:
            with open(self.log_file_path, 'w') as log_file:
                json.dump(self.execution_log, log_file, indent=2)
                print(f"Execution log saved to {self.log_file_path}")
        except Exception as e:
            print(f"Error saving log file: {e}")
    
    def get_execution_log(self):
        """
        Get the current execution log
        """
        try:
            with open(self.log_file_path, 'r') as log_file:
                return log_file.read()
        except Exception as e:
            print(f"Error reading log file: {e}")
            return ""
    
    def clear_execution_log(self):
        """
        Clear the current execution log
        """
        try:
            with open(self.log_file_path, 'w') as log_file:
                log_file.write("")
                print(f"Execution log cleared")
        except Exception as e:
            print(f"Error clearing log file: {e}")
    
    def get_log_summary(self):
        """
        Get a summary of the execution log
        """
        content = self.get_execution_log()
        if not content:
            return "No executions logged"
        
        # Count occurrences of "Test Name:" to get number of executions
        total_executions = content.count("Test Name:")
        
        return f"Log contains {total_executions} executions"
