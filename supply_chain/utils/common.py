"""
Common utility functions for Supply Chain Optimization project.
Helper functions used across multiple components.
"""

import os
import sys
import json
import yaml
import pandas as pd
from pathlib import Path
from typing import Any, Dict, List, Union
from datetime import datetime

from supply_chain.logging.logger import get_logger
from supply_chain.exception.exception import SupplyChainException

logger = get_logger(__name__)


def read_yaml(file_path: Union[str, Path]) -> Dict:
    """
    Read YAML configuration file.
    
    Args:
        file_path: Path to YAML file
        
    Returns:
        Dict: Configuration dictionary
        
    Raises:
        SupplyChainException: If file cannot be read
    """
    try:
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"YAML file not found: {file_path}")
        
        with open(file_path, "r") as f:
            config = yaml.safe_load(f)
        
        logger.info(f"Successfully loaded YAML config from: {file_path}")
        return config if config else {}
        
    except Exception as e:
        logger.error(f"Error reading YAML file: {file_path}")
        raise SupplyChainException(e, sys)


def save_json(file_path: Union[str, Path], data: Dict) -> None:
    try:
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4, default=str)
        
        logger.info(f"Successfully saved JSON to: {file_path}")
        
    except Exception as e:
        logger.error(f"Error saving JSON file: {file_path}")
        raise SupplyChainException(e, sys)


def load_json(file_path: Union[str, Path]) -> Dict:
    try:
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"JSON file not found: {file_path}")
        
        with open(file_path, "r") as f:
            data = json.load(f)
        
        logger.info(f"Successfully loaded JSON from: {file_path}")
        return data
        
    except Exception as e:
        logger.error(f"Error loading JSON file: {file_path}")
        raise SupplyChainException(e, sys)


def save_dataframe(
    df: pd.DataFrame,
    file_path: Union[str, Path],
    format: str = "parquet"
) -> None:
    try:
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        if format.lower() == "parquet":
            df.to_parquet(file_path, index=False, engine='pyarrow')
        elif format.lower() == "csv":
            df.to_csv(file_path, index=False)
        elif format.lower() == "pickle":
            df.to_pickle(file_path)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        logger.info(f"Successfully saved DataFrame to: {file_path} (format: {format})")
        
    except Exception as e:
        logger.error(f"Error saving DataFrame to: {file_path}")
        raise SupplyChainException(e, sys)


def load_dataframe(
    file_path: Union[str, Path],
    format: str = "parquet"
) -> pd.DataFrame:
    try:
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if format.lower() == "parquet":
            df = pd.read_parquet(file_path, engine='pyarrow')
        elif format.lower() == "csv":
            df = pd.read_csv(file_path)
        elif format.lower() == "pickle":
            df = pd.read_pickle(file_path)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        logger.info(f"Successfully loaded DataFrame from: {file_path} (shape: {df.shape})")
        return df
        
    except Exception as e:
        logger.error(f"Error loading DataFrame from: {file_path}")
        raise SupplyChainException(e, sys)


def create_directories(directories: List[Union[str, Path]]) -> None:
    try:
        for directory in directories:
            dir_path = Path(directory)
            dir_path.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Directory ensured: {dir_path}")
        
        logger.info(f"Successfully ensured {len(directories)} directories exist")
        
    except Exception as e:
        logger.error("Error creating directories")
        raise SupplyChainException(e, sys)


def get_file_size(file_path: Union[str, Path]) -> str:
    try:
        file_path = Path(file_path)
        if not file_path.exists():
            return "File not found"
        
        size_bytes = file_path.stat().st_size
        
        # Convert to human-readable format
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        
        return f"{size_bytes:.2f} PB"
        
    except Exception as e:
        logger.warning(f"Error getting file size for: {file_path}")
        return "Unknown"


def get_timestamp(format: str = "%Y%m%d_%H%M%S") -> str:
    return datetime.now().strftime(format)


if __name__ == "__main__":
    # Test utility functions
    print("=" * 60)
    print("TESTING COMMON UTILITIES")
    print("=" * 60)
    
    # Test timestamp
    print(f"\n⏰ Current timestamp: {get_timestamp()}")
    
    # Test directory creation
    test_dirs = ["test_artifacts/sample1", "test_artifacts/sample2"]
    create_directories(test_dirs)
    print(f"✅ Created test directories")
    
    # Test JSON save/load
    test_data = {
        "test": "data",
        "timestamp": get_timestamp(),
        "numbers": [1, 2, 3]
    }
    test_json_path = Path("test_artifacts/test.json")
    save_json(test_json_path, test_data)
    loaded_data = load_json(test_json_path)
    print(f"✅ JSON save/load working: {loaded_data}")
    
    # Test DataFrame save/load
    test_df = pd.DataFrame({
        "col1": [1, 2, 3],
        "col2": ["a", "b", "c"]
    })
    test_parquet_path = Path("test_artifacts/test.parquet")
    save_dataframe(test_df, test_parquet_path, format="parquet")
    loaded_df = load_dataframe(test_parquet_path, format="parquet")
    print(f"✅ DataFrame save/load working: shape {loaded_df.shape}")
    
    # Test file size
    file_size = get_file_size(test_parquet_path)
    print(f"✅ File size: {file_size}")
    
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED")
    print("=" * 60)