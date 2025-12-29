import sys
from typing import Optional


def get_detailed_error_message(error: Exception, error_detail: sys) -> str:
    # Extract traceback information
    _, _, exc_tb = error_detail.exc_info()
    
    # Get the file name where the error occurred
    file_name = exc_tb.tb_frame.f_code.co_filename
    
    # Get the line number where the error occurred
    line_number = exc_tb.tb_lineno
    
    # Get the function/method name where error occurred
    function_name = exc_tb.tb_frame.f_code.co_name
    
    # Construct detailed error message
    error_message = (
        f"Error occurred in module [{file_name}] "
        f"at line [{line_number}] "
        f"in function [{function_name}]: "
        f"{str(error)}"
    )
    
    return error_message


class SupplyChainException(Exception):
    def __init__(self, error_message: Exception, error_detail: sys):
        super().__init__(error_message)
        self.error_message = get_detailed_error_message(error_message, error_detail)
    
    def __str__(self) -> str:
        """Return the detailed error message when exception is printed"""
        return self.error_message
    
    def __repr__(self) -> str:
        """Return the class name and error message for debugging"""
        return f"SupplyChainException: {self.error_message}"


# Example usage and testing
if __name__ == "__main__":
    # Test the custom exception
    def test_function():
        """Test function that raises an exception"""
        try:
            # Simulate an error
            x = 1 / 0
        except Exception as e:
            raise SupplyChainException(e, sys)
    
    # Run test
    try:
        test_function()
    except SupplyChainException as sce:
        print("Caught custom exception:")
        print(sce)
        print(f"\nException representation: {repr(sce)}")