import logging
import os
from datetime import datetime
from pathlib import Path

# Create logs directory if it doesn't exist
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Generate log file name with current date
LOG_FILE = f"{datetime.now().strftime('%Y-%m-%d')}.log"
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE)

# Custom formatter with colors for console output
class ColoredFormatter(logging.Formatter):
    """Custom formatter with color coding for different log levels"""
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'        # Reset
    }
    
    def format(self, record):
        # Add color to levelname for console output
        if hasattr(self, 'use_color') and self.use_color:
            levelname = record.levelname
            if levelname in self.COLORS:
                record.levelname = f"{self.COLORS[levelname]}{levelname}{self.COLORS['RESET']}"
        return super().format(record)


def get_logger(name: str = None) -> logging.Logger:
    """
    Get or create a logger with the specified name.
    
    Args:
        name (str): Name of the logger (usually __name__ from calling module)
    
    Returns:
        logging.Logger: Configured logger instance
    """
    # Use provided name or default to 'supply_chain'
    logger_name = name if name else 'supply_chain'
    logger = logging.getLogger(logger_name)
    
    # Only configure if handlers haven't been added yet (avoid duplicate logs)
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        
        # File handler - logs everything to file
        file_handler = logging.FileHandler(LOG_FILE_PATH)
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            fmt='[%(asctime)s] - %(levelname)s - %(name)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        
        # Console handler - logs INFO and above to terminal with colors
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = ColoredFormatter(
            fmt='[%(asctime)s] - %(levelname)s - %(name)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_formatter.use_color = True
        console_handler.setFormatter(console_formatter)
        
        # Add both handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        # Prevent propagation to root logger (avoid duplicate logs)
        logger.propagate = False
    
    return logger


# Create a default logger for direct imports
logger = get_logger('supply_chain')


if __name__ == "__main__":
    # Test the logger
    test_logger = get_logger('test_module')
    
    test_logger.debug("This is a DEBUG message (file only)")
    test_logger.info("This is an INFO message (file + console)")
    test_logger.warning("This is a WARNING message")
    test_logger.error("This is an ERROR message")
    test_logger.critical("This is a CRITICAL message")
    
    print(f"\n Log file created at: {LOG_FILE_PATH}")