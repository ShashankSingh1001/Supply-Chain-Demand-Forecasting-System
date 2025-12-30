import sys
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, Optional

from supply_chain.logging.logger import get_logger
from supply_chain.exception.exception import SupplyChainException
from supply_chain.constants import (
    RAW_FILES,
    DATA_INGESTION_DIR,
    DATA_INGESTION_CONFIG
)
from supply_chain.utils.common import read_yaml

logger = get_logger(__name__)


@dataclass
class DataIngestionConfig:
    raw_data_paths: Dict[str, Path]
    artifact_dir: Path
    save_format: str
    enable_validation: bool
    chunk_size: Optional[int]
    date_columns: Dict[str, list]
    validation_rules: Dict
    drop_all_nan_rows: bool
    drop_duplicates: bool
    convert_onpromotion_to_bool: bool
    generate_report: bool
    include_profiling: bool
    
    @classmethod
    def from_yaml(cls, config_path: Path = None):
        """
        Create DataIngestionConfig from YAML file.
        """
        try:
            if config_path is None:
                config_path = DATA_INGESTION_CONFIG
            
            logger.info(f"Loading data ingestion config from: {config_path}")
            config = read_yaml(config_path)
            
            return cls(
                raw_data_paths=RAW_FILES,
                artifact_dir=DATA_INGESTION_DIR,
                save_format=config.get("save_format", "parquet"),
                enable_validation=config.get("enable_validation", True),
                chunk_size=config.get("chunk_size"),
                date_columns=config.get("date_columns", {}),
                validation_rules=config.get("validation", {}),
                drop_all_nan_rows=config.get("drop_all_nan_rows", True),
                drop_duplicates=config.get("drop_duplicates", True),
                convert_onpromotion_to_bool=config.get("convert_onpromotion_to_bool", True),
                generate_report=config.get("generate_report", True),
                include_profiling=config.get("include_profiling", True)
            )
            
        except Exception as e:
            logger.error(f"Error loading config from {config_path}")
            raise SupplyChainException(e, sys)


# Placeholder for future pipeline configs
# Will be added when building those pipelines

# @dataclass
# class DataTransformationConfig:
#     """Configuration for Data Transformation component."""
#     pass

# @dataclass
# class ForecastingConfig:
#     """Configuration for Forecasting component."""
#     pass

# @dataclass
# class InventoryOptimizationConfig:
#     """Configuration for Inventory Optimization component."""
#     pass


if __name__ == "__main__":
    # Test config loading
    try:
        print("=" * 60)
        print("TESTING CONFIG ENTITY")
        print("=" * 60)
        
        config = DataIngestionConfig.from_yaml()
        
        print(f"\nConfig loaded successfully!")
        print(f"Save format: {config.save_format}")
        print(f"Validation enabled: {config.enable_validation}")
        print(f"Artifact directory: {config.artifact_dir}")
        print(f"Number of raw files: {len(config.raw_data_paths)}")
        
        print("\n" + "=" * 60)
        print("CONFIG ENTITY TEST PASSED")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nTEST FAILED: {e}")