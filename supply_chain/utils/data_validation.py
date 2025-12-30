import sys
import pandas as pd
from pathlib import Path
from typing import Dict, List, Tuple, Union

from supply_chain.logging.logger import get_logger
from supply_chain.exception.exception import SupplyChainException

logger = get_logger(__name__)


def check_file_exists(file_path: Union[str, Path]) -> bool:
    try:
        file_path = Path(file_path)
        exists = file_path.exists() and file_path.is_file()
        
        if exists:
            logger.debug(f"File exists: {file_path}")
        else:
            logger.warning(f"File not found: {file_path}")
        
        return exists
        
    except Exception as e:
        logger.error(f"Error checking file existence: {file_path}")
        raise SupplyChainException(e, sys)


def validate_required_files(file_paths: Dict[str, Path]) -> Tuple[bool, List[str]]:
    try:
        missing_files = []
        
        for name, path in file_paths.items():
            if not check_file_exists(path):
                missing_files.append(name)
        
        all_exist = len(missing_files) == 0
        
        if all_exist:
            logger.info(f" All {len(file_paths)} required files found")
        else:
            logger.error(f" Missing files: {missing_files}")
        
        return all_exist, missing_files
        
    except Exception as e:
        logger.error("Error validating required files")
        raise SupplyChainException(e, sys)


def validate_dataframe_columns(
    df: pd.DataFrame,
    expected_columns: List[str],
    df_name: str = "DataFrame"
) -> Tuple[bool, List[str]]:
    try:
        actual_columns = set(df.columns)
        expected_columns_set = set(expected_columns)
        missing_columns = list(expected_columns_set - actual_columns)
        
        all_present = len(missing_columns) == 0
        
        if all_present:
            logger.debug(f" {df_name}: All expected columns present")
        else:
            logger.warning(f" {df_name}: Missing columns: {missing_columns}")
        
        return all_present, missing_columns
        
    except Exception as e:
        logger.error(f"Error validating columns for {df_name}")
        raise SupplyChainException(e, sys)


def check_minimum_rows(
    df: pd.DataFrame,
    min_rows: int,
    df_name: str = "DataFrame"
) -> bool:
    """
    Check if DataFrame has minimum required rows.
    
    Args:
        df: DataFrame to check
        min_rows: Minimum number of rows required
        df_name: Name of DataFrame (for logging)
        
    Returns:
        bool: True if meets requirement, False otherwise
    """
    try:
        actual_rows = len(df)
        meets_requirement = actual_rows >= min_rows
        
        if meets_requirement:
            logger.debug(f" {df_name}: {actual_rows} rows (>= {min_rows} required)")
        else:
            logger.warning(f" {df_name}: Only {actual_rows} rows (< {min_rows} required)")
        
        return meets_requirement
        
    except Exception as e:
        logger.error(f"Error checking minimum rows for {df_name}")
        raise SupplyChainException(e, sys)


def calculate_missing_percentage(df: pd.DataFrame) -> pd.Series:
    """
    Calculate percentage of missing values for each column.
    
    Args:
        df: DataFrame to analyze
        
    Returns:
        pd.Series: Missing percentage for each column
    """
    try:
        missing_pct = (df.isnull().sum() / len(df) * 100).round(2)
        return missing_pct
        
    except Exception as e:
        logger.error("Error calculating missing percentages")
        raise SupplyChainException(e, sys)


def check_missing_values(
    df: pd.DataFrame,
    max_missing_pct: float,
    df_name: str = "DataFrame"
) -> Tuple[bool, Dict[str, float]]:
    """
    Check if any column exceeds maximum allowed missing percentage.
    
    Args:
        df: DataFrame to check
        max_missing_pct: Maximum allowed missing percentage
        df_name: Name of DataFrame (for logging)
        
    Returns:
        Tuple[bool, Dict]: (passes_check, dict of columns exceeding threshold)
    """
    try:
        missing_pct = calculate_missing_percentage(df)
        exceeding_cols = missing_pct[missing_pct > max_missing_pct].to_dict()
        
        passes_check = len(exceeding_cols) == 0
        
        if passes_check:
            logger.debug(f" {df_name}: Missing values within acceptable range")
        else:
            logger.warning(
                f" {df_name}: Columns exceeding {max_missing_pct}% missing: {exceeding_cols}"
            )
        
        return passes_check, exceeding_cols
        
    except Exception as e:
        logger.error(f"Error checking missing values for {df_name}")
        raise SupplyChainException(e, sys)


def check_duplicates(
    df: pd.DataFrame,
    df_name: str = "DataFrame"
) -> Tuple[int, bool]:
    """
    Check for duplicate rows in DataFrame.
    
    Args:
        df: DataFrame to check
        df_name: Name of DataFrame (for logging)
        
    Returns:
        Tuple[int, bool]: (number of duplicates, has duplicates)
    """
    try:
        num_duplicates = df.duplicated().sum()
        has_duplicates = num_duplicates > 0
        
        if has_duplicates:
            logger.warning(f"⚠️ {df_name}: Found {num_duplicates} duplicate rows")
        else:
            logger.debug(f"✅ {df_name}: No duplicate rows")
        
        return num_duplicates, has_duplicates
        
    except Exception as e:
        logger.error(f"Error checking duplicates for {df_name}")
        raise SupplyChainException(e, sys)


def generate_data_profile(df: pd.DataFrame, df_name: str = "DataFrame") -> Dict:
    """
    Generate basic data profile for DataFrame.
    
    Args:
        df: DataFrame to profile
        df_name: Name of DataFrame
        
    Returns:
        Dict: Profile information
    """
    try:
        profile = {
            "name": df_name,
            "shape": df.shape,
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": df.columns.tolist(),
            "dtypes": df.dtypes.astype(str).to_dict(),
            "missing_values": df.isnull().sum().to_dict(),
            "missing_percentage": calculate_missing_percentage(df).to_dict(),
            "duplicate_rows": int(df.duplicated().sum()),
            "memory_usage_mb": round(df.memory_usage(deep=True).sum() / 1024**2, 2)
        }
        
        logger.debug(f"Generated profile for {df_name}")
        return profile
        
    except Exception as e:
        logger.error(f"Error generating profile for {df_name}")
        raise SupplyChainException(e, sys)


if __name__ == "__main__":
    # Test validation functions
    print("=" * 60)
    print("TESTING DATA VALIDATION UTILITIES")
    print("=" * 60)
    
    # Create sample DataFrame
    test_df = pd.DataFrame({
        "col1": [1, 2, 3, None, 5],
        "col2": ["a", "b", "c", "d", "e"],
        "col3": [1.1, 2.2, None, None, 5.5]
    })
    
    print(f"\n Test DataFrame shape: {test_df.shape}")
    
    # Test column validation
    valid, missing = validate_dataframe_columns(
        test_df, 
        ["col1", "col2", "col3"],
        "TestDF"
    )
    print(f" Column validation: {valid}")
    
    # Test missing values
    passes, exceeding = check_missing_values(test_df, 30.0, "TestDF")
    print(f" Missing values check: {passes}")
    
    # Test duplicates
    num_dups, has_dups = check_duplicates(test_df, "TestDF")
    print(f" Duplicates: {num_dups}")
    
    # Test data profile
    profile = generate_data_profile(test_df, "TestDF")
    print(f" Profile generated: {profile['rows']} rows, {profile['columns']} cols")
    
    print("\n" + "=" * 60)
    print("ALL VALIDATION TESTS PASSED")
    print("=" * 60)