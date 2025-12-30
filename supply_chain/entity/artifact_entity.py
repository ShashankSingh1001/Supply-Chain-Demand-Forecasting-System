from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime


@dataclass
class DataIngestionArtifact:
    success: bool
    artifact_dir: Path
    processed_files: Dict[str, Path]
    report_path: Optional[Path]
    timestamp: str
    duration_seconds: float
    files_processed_count: int
    files_failed_count: int
    validation_results: Dict[str, Dict] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    summary: Dict = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate artifact after initialization."""
        # Ensure artifact_dir is Path object
        if isinstance(self.artifact_dir, str):
            self.artifact_dir = Path(self.artifact_dir)
        
        # Ensure report_path is Path object if provided
        if self.report_path and isinstance(self.report_path, str):
            self.report_path = Path(self.report_path)
        
        # Convert processed_files values to Path objects
        self.processed_files = {
            k: Path(v) if isinstance(v, str) else v
            for k, v in self.processed_files.items()
        }
    
    def get_status_message(self) -> str:
        """
        Get human-readable status message.
        
        Returns:
            str: Status message
        """
        if self.success:
            return f"Successfully processed {self.files_processed_count} files in {self.duration_seconds:.2f}s"
        else:
            return f"Processed {self.files_processed_count} files with {self.files_failed_count} failures"
    
    def to_dict(self) -> Dict:
        """
        Convert artifact to dictionary.
        
        Returns:
            Dict: Dictionary representation
        """
        return {
            "success": self.success,
            "artifact_dir": str(self.artifact_dir),
            "processed_files": {k: str(v) for k, v in self.processed_files.items()},
            "report_path": str(self.report_path) if self.report_path else None,
            "timestamp": self.timestamp,
            "duration_seconds": self.duration_seconds,
            "files_processed_count": self.files_processed_count,
            "files_failed_count": self.files_failed_count,
            "validation_results": self.validation_results,
            "errors": self.errors,
            "summary": self.summary
        }


# Placeholder for future pipeline artifacts
# Will be added when building those pipelines

# @dataclass
# class DataTransformationArtifact:
#     """Output artifact from Data Transformation component."""
#     success: bool
#     train_path: Path
#     test_path: Path
#     feature_store_path: Path
#     transformation_report_path: Path

# @dataclass
# class ForecastingArtifact:
#     """Output artifact from Forecasting component."""
#     success: bool
#     model_path: Path
#     predictions_path: Path
#     metrics: Dict
#     forecast_report_path: Path

# @dataclass
# class InventoryOptimizationArtifact:
#     """Output artifact from Inventory Optimization component."""
#     success: bool
#     optimization_results_path: Path
#     recommendations: Dict
#     optimization_report_path: Path


if __name__ == "__main__":
    # Test artifact creation
    print("=" * 60)
    print("TESTING ARTIFACT ENTITY")
    print("=" * 60)
    
    # Create sample artifact
    artifact = DataIngestionArtifact(
        success=True,
        artifact_dir=Path("artifacts/data_ingestion"),
        processed_files={
            "train": Path("artifacts/data_ingestion/train_ingested.parquet"),
            "test": Path("artifacts/data_ingestion/test_ingested.parquet")
        },
        report_path=Path("artifacts/data_ingestion/report.json"),
        timestamp="2025-12-30 15:30:00",
        duration_seconds=45.5,
        files_processed_count=7,
        files_failed_count=0,
        summary={"total": 7, "successful": 7}
    )
    
    print(f"\nArtifact created successfully!")
    print(f"Status: {artifact.get_status_message()}")
    print(f"Artifact directory: {artifact.artifact_dir}")
    print(f"Processed files: {len(artifact.processed_files)}")
    print(f"Report path: {artifact.report_path}")
    
    # Test to_dict conversion
    artifact_dict = artifact.to_dict()
    print(f"\nConverted to dict with {len(artifact_dict)} keys")
    
    print("\n" + "=" * 60)
    print("ARTIFACT ENTITY TEST PASSED")
    print("=" * 60)