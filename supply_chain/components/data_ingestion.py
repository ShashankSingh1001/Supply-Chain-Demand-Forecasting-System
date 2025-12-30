import sys
import pandas as pd
from pathlib import Path
from typing import Dict
from datetime import datetime

from supply_chain.logging.logger import get_logger
from supply_chain.exception.exception import SupplyChainException
from supply_chain.constants import REQUIRED_RAW_FILES
from supply_chain.entity.config_entity import DataIngestionConfig
from supply_chain.entity.artifact_entity import DataIngestionArtifact
from supply_chain.utils.common import (
    save_json,
    save_dataframe,
    create_directories,
    get_file_size,
    get_timestamp
)
from supply_chain.utils.data_validation import (
    validate_required_files,
    check_minimum_rows,
    check_missing_values,
    check_duplicates,
    generate_data_profile
)

logger = get_logger(__name__)


class DataIngestion:
    """
    Data Ingestion component.
    Reads raw CSV files, validates, and saves to artifacts.
    """
    
    def __init__(self, config: DataIngestionConfig):
        """
        Initialize DataIngestion component.
        
        Args:
            config: DataIngestionConfig object
        """
        self.config = config
        self.ingestion_report = {
            "timestamp": get_timestamp("%Y-%m-%d %H:%M:%S"),
            "files_processed": {},
            "validation_results": {},
            "errors": []
        }
        logger.info("DataIngestion component initialized")
    
    def validate_raw_files(self) -> bool:
        """
        Validate that all required raw files exist.
        """
        try:
            logger.info("Validating raw files...")
            
            all_exist, missing_files = validate_required_files(self.config.raw_data_paths)
            
            if not all_exist:
                error_msg = f"Missing required files: {missing_files}"
                logger.error(error_msg)
                self.ingestion_report["errors"].append(error_msg)
                raise FileNotFoundError(error_msg)
            
            logger.info(f"All {len(REQUIRED_RAW_FILES)} required files found")
            return True
            
        except Exception as e:
            logger.error("Raw file validation failed")
            raise SupplyChainException(e, sys)
    
    def read_csv_file(
        self,
        file_path: Path,
        file_name: str
    ) -> pd.DataFrame:
        """
        Read a CSV file with appropriate settings.
        """
        try:
            logger.info(f"Reading {file_name} from {file_path}")
            
            # Get date columns for this file
            date_cols = self.config.date_columns.get(file_name, [])
            
            # Read CSV
            if self.config.chunk_size:
                # Read in chunks (for very large files)
                chunks = []
                for chunk in pd.read_csv(
                    file_path,
                    parse_dates=date_cols if date_cols else False,
                    chunksize=self.config.chunk_size
                ):
                    chunks.append(chunk)
                df = pd.concat(chunks, ignore_index=True)
            else:
                # Read entire file
                df = pd.read_csv(
                    file_path,
                    parse_dates=date_cols if date_cols else False
                )
            
            logger.info(f" Loaded {file_name}: shape {df.shape}")
            return df
            
        except Exception as e:
            logger.error(f"Error reading {file_name}")
            raise SupplyChainException(e, sys)
    
    def validate_dataframe(
        self,
        df: pd.DataFrame,
        file_name: str
    ) -> Dict:
        try:
            validation_results = {
                "file": file_name,
                "shape": df.shape,
                "checks_passed": True,
                "issues": []
            }
            
            if not self.config.enable_validation:
                logger.info(f"Validation disabled for {file_name}")
                return validation_results
            
            logger.info(f"Validating {file_name}...")
            
            # Check minimum rows
            min_rows_dict = self.config.validation_rules.get("min_rows", {})
            if file_name in min_rows_dict:
                min_rows = min_rows_dict[file_name]
                if not check_minimum_rows(df, min_rows, file_name):
                    issue = f"Row count {len(df)} below minimum {min_rows}"
                    validation_results["issues"].append(issue)
                    validation_results["checks_passed"] = False
            
            # Check missing values
            max_missing_pct = self.config.validation_rules.get("max_missing_percentage", 30.0)
            passes, exceeding = check_missing_values(df, max_missing_pct, file_name)
            if not passes:
                issue = f"Columns with high missing values: {exceeding}"
                validation_results["issues"].append(issue)
                # Don't fail, just warn
            
            # Check duplicates
            if self.config.validation_rules.get("check_duplicates", True):
                num_dups, has_dups = check_duplicates(df, file_name)
                if has_dups:
                    validation_results["duplicate_rows"] = num_dups
            
            logger.info(f"Validation complete for {file_name}")
            return validation_results
            
        except Exception as e:
            logger.error(f"Error validating {file_name}")
            raise SupplyChainException(e, sys)
    
    def preprocess_dataframe(
        self,
        df: pd.DataFrame,
        file_name: str
    ) -> pd.DataFrame:
        try:
            logger.info(f"Preprocessing {file_name}...")
            original_shape = df.shape
            
            # Drop rows where all values are NaN
            if self.config.drop_all_nan_rows:
                df = df.dropna(how='all')
                logger.debug(f"Dropped rows with all NaN values")
            
            # Drop duplicate rows
            if self.config.drop_duplicates:
                df = df.drop_duplicates()
                logger.debug(f"Dropped duplicate rows")
            
            # Convert 'onpromotion' to boolean if present
            if self.config.convert_onpromotion_to_bool and 'onpromotion' in df.columns:
                df['onpromotion'] = df['onpromotion'].astype(bool)
                logger.debug(f"Converted 'onpromotion' to boolean")
            
            new_shape = df.shape
            if original_shape != new_shape:
                logger.info(f"Shape changed: {original_shape} → {new_shape}")
            
            logger.info(f"Preprocessing complete for {file_name}")
            return df
            
        except Exception as e:
            logger.error(f"Error preprocessing {file_name}")
            raise SupplyChainException(e, sys)
    
    def save_processed_data(
        self,
        df: pd.DataFrame,
        file_name: str
    ) -> Path:
        """
        Save processed DataFrame to artifact directory.
        """
        try:
            # Create output filename
            output_filename = f"{file_name}_ingested.{self.config.save_format}"
            output_path = self.config.artifact_dir / output_filename
            
            # Save DataFrame
            save_dataframe(df, output_path, format=self.config.save_format)
            
            file_size = get_file_size(output_path)
            logger.info(f"Saved {file_name} to {output_path} ({file_size})")
            
            return output_path
            
        except Exception as e:
            logger.error(f"Error saving {file_name}")
            raise SupplyChainException(e, sys)
    
    def process_single_file(
        self,
        file_name: str,
        file_path: Path
    ) -> Dict:
        """
        Process a single raw file through the complete pipeline.
        """
        try:
            logger.info(f"{'='*60}")
            logger.info(f"Processing: {file_name}")
            logger.info(f"{'='*60}")
            
            # Read file
            df = self.read_csv_file(file_path, file_name)
            
            # Validate
            validation_results = self.validate_dataframe(df, file_name)
            
            # Preprocess
            df = self.preprocess_dataframe(df, file_name)
            
            # Generate profile (if enabled)
            profile = None
            if self.config.include_profiling:
                profile = generate_data_profile(df, file_name)
            
            # Save
            output_path = self.save_processed_data(df, file_name)
            
            # Record results
            results = {
                "status": "success",
                "input_file": str(file_path),
                "output_file": str(output_path),
                "shape": df.shape,
                "validation": validation_results,
                "profile": profile
            }
            
            logger.info(f"Successfully processed {file_name}")
            return results
            
        except Exception as e:
            logger.error(f"Error processing {file_name}")
            error_msg = str(e)
            self.ingestion_report["errors"].append(f"{file_name}: {error_msg}")
            return {
                "status": "failed",
                "file": file_name,
                "error": error_msg
            }
    
    def generate_ingestion_report(self) -> Path:
        """
        Generate and save ingestion report.
        """
        try:
            report_path = self.config.artifact_dir / "ingestion_report.json"
            save_json(report_path, self.ingestion_report)
            logger.info(f"Ingestion report saved to {report_path}")
            return report_path
            
        except Exception as e:
            logger.error("Error generating ingestion report")
            raise SupplyChainException(e, sys)
    
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """
        Main method to orchestrate the complete data ingestion pipeline.
        
        Returns:
            DataIngestionArtifact: Artifact containing ingestion results
        """
        try:
            logger.info("="*60)
            logger.info("STARTING DATA INGESTION PIPELINE")
            logger.info("="*60)
            
            start_time = datetime.now()
            
            # Create artifact directory
            create_directories([self.config.artifact_dir])
            
            # Validate raw files exist
            self.validate_raw_files()
            
            # Track processed files
            processed_files = {}
            validation_results = {}
            
            # Process each file
            for file_name, file_path in self.config.raw_data_paths.items():
                results = self.process_single_file(file_name, file_path)
                self.ingestion_report["files_processed"][file_name] = results
                
                # Track successful files
                if results["status"] == "success":
                    processed_files[file_name] = Path(results["output_file"])
                    validation_results[file_name] = results.get("validation", {})
            
            # Calculate total time
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            self.ingestion_report["duration_seconds"] = round(duration, 2)
            
            # Count successes and failures
            success_count = sum(
                1 for r in self.ingestion_report["files_processed"].values()
                if r["status"] == "success"
            )
            total_files = len(self.config.raw_data_paths)
            failed_count = total_files - success_count
            
            all_success = success_count == total_files
            
            # Add summary to report
            self.ingestion_report["summary"] = {
                "total_files": total_files,
                "successful": success_count,
                "failed": failed_count,
                "all_success": all_success
            }
            
            # Generate report file
            report_path = None
            if self.config.generate_report:
                report_path = self.generate_ingestion_report()
            
            # Create artifact
            artifact = DataIngestionArtifact(
                success=all_success,
                artifact_dir=self.config.artifact_dir,
                processed_files=processed_files,
                report_path=report_path,
                timestamp=get_timestamp("%Y-%m-%d %H:%M:%S"),
                duration_seconds=duration,
                files_processed_count=success_count,
                files_failed_count=failed_count,
                validation_results=validation_results,
                errors=self.ingestion_report["errors"],
                summary=self.ingestion_report["summary"]
            )
            
            # Log completion status
            logger.info("="*60)
            logger.info(artifact.get_status_message())
            logger.info("="*60)
            
            return artifact
            
        except Exception as e:
            logger.error("Data ingestion pipeline failed")
            raise SupplyChainException(e, sys)


if __name__ == "__main__":
    # Test data ingestion component
    try:
        print("Testing DataIngestion component...")
        
        # Load config
        config = DataIngestionConfig.from_yaml()
        print(f"Config loaded: save_format={config.save_format}")
        
        # Initialize component
        ingestion = DataIngestion(config)
        print(f"DataIngestion initialized")
        
        # Run ingestion
        artifact = ingestion.initiate_data_ingestion()
        
        print(f"\n{artifact.get_status_message()}")
        print(f"Artifact directory: {artifact.artifact_dir}")
        print(f"Processed files: {len(artifact.processed_files)}")
        print(f"Report path: {artifact.report_path}")
        
        if artifact.success:
            print("\n DATA INGESTION TEST PASSED")
        else:
            print("\n DATA INGESTION TEST COMPLETED WITH WARNINGS")
            print(f"Errors: {artifact.errors}")
        
    except Exception as e:
        print(f"\nTEST FAILED: {e}")