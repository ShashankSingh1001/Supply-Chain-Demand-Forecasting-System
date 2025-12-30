import sys
from typing import Optional

from supply_chain.logging.logger import get_logger
from supply_chain.exception.exception import SupplyChainException
from supply_chain.entity.config_entity import DataIngestionConfig
from supply_chain.entity.artifact_entity import DataIngestionArtifact
from supply_chain.components.data_ingestion import DataIngestion

logger = get_logger(__name__)


class TrainingPipeline:
    """
    Training Pipeline orchestrator.
    Coordinates all stages of the ML pipeline.
    """
    
    def __init__(self):
        """Initialize the training pipeline."""
        logger.info("="*60)
        logger.info("INITIALIZING TRAINING PIPELINE")
        logger.info("="*60)
        self.data_ingestion_artifact: Optional[DataIngestionArtifact] = None
    
    def start_data_ingestion(self) -> DataIngestionArtifact:
        """
        Start the data ingestion stage of the pipeline.
        
        Returns:
            DataIngestionArtifact: Results from data ingestion
        """
        try:
            logger.info("\n" + "="*60)
            logger.info("STAGE 1: DATA INGESTION")
            logger.info("="*60)
            
            # Load configuration
            logger.info("Loading data ingestion configuration...")
            data_ingestion_config = DataIngestionConfig.from_yaml()
            
            # Initialize data ingestion component
            logger.info("Initializing data ingestion component...")
            data_ingestion = DataIngestion(config=data_ingestion_config)
            
            # Execute data ingestion
            logger.info("Executing data ingestion pipeline...")
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            
            # Store artifact for use in subsequent stages
            self.data_ingestion_artifact = data_ingestion_artifact
            
            # Log results
            logger.info("\n" + "="*60)
            logger.info("DATA INGESTION STAGE COMPLETED")
            logger.info("="*60)
            logger.info(data_ingestion_artifact.get_status_message())
            logger.info(f"Artifact directory: {data_ingestion_artifact.artifact_dir}")
            logger.info(f"Processed files: {len(data_ingestion_artifact.processed_files)}")
            if data_ingestion_artifact.report_path:
                logger.info(f"Report saved at: {data_ingestion_artifact.report_path}")
            
            # Raise exception if ingestion failed
            if not data_ingestion_artifact.success:
                error_msg = f"Data ingestion failed with errors: {data_ingestion_artifact.errors}"
                logger.error(error_msg)
                raise Exception(error_msg)
            
            return data_ingestion_artifact
            
        except Exception as e:
            logger.error("Data ingestion stage failed")
            raise SupplyChainException(e, sys)
    
    # Placeholder methods for future pipeline stages
    # Will be implemented when building those components
    
    # def start_data_transformation(self) -> DataTransformationArtifact:
    #     """
    #     Start the data transformation stage.
    #     
    #     Returns:
    #         DataTransformationArtifact: Results from data transformation
    #     """
    #     try:
    #         logger.info("\n" + "="*60)
    #         logger.info("STAGE 2: DATA TRANSFORMATION")
    #         logger.info("="*60)
    #         
    #         # Implementation will go here
    #         pass
    #         
    #     except Exception as e:
    #         logger.error("Data transformation stage failed")
    #         raise SupplyChainException(e, sys)
    
    # def start_forecasting(self) -> ForecastingArtifact:
    #     """
    #     Start the forecasting stage.
    #     
    #     Returns:
    #         ForecastingArtifact: Results from forecasting
    #     """
    #     try:
    #         logger.info("\n" + "="*60)
    #         logger.info("STAGE 3: FORECASTING")
    #         logger.info("="*60)
    #         
    #         # Implementation will go here
    #         pass
    #         
    #     except Exception as e:
    #         logger.error("Forecasting stage failed")
    #         raise SupplyChainException(e, sys)
    
    # def start_inventory_optimization(self) -> InventoryOptimizationArtifact:
    #     """
    #     Start the inventory optimization stage.
    #     
    #     Returns:
    #         InventoryOptimizationArtifact: Results from optimization
    #     """
    #     try:
    #         logger.info("\n" + "="*60)
    #         logger.info("STAGE 4: INVENTORY OPTIMIZATION")
    #         logger.info("="*60)
    #         
    #         # Implementation will go here
    #         pass
    #         
    #     except Exception as e:
    #         logger.error("Inventory optimization stage failed")
    #         raise SupplyChainException(e, sys)
    
    def run_pipeline(self) -> bool:
        """
        Run the complete training pipeline.
        Currently only runs data ingestion stage.
        Future stages will be added as components are built.
        
        Returns:
            bool: True if pipeline completes successfully
            
        Raises:
            SupplyChainException: If any stage fails
        """
        try:
            logger.info("\n" + "="*60)
            logger.info("STARTING COMPLETE TRAINING PIPELINE")
            logger.info("="*60)
            
            # Stage 1: Data Ingestion
            data_ingestion_artifact = self.start_data_ingestion()
            
            # Stage 2: Data Transformation (TODO)
            # data_transformation_artifact = self.start_data_transformation()
            
            # Stage 3: Forecasting (TODO)
            # forecasting_artifact = self.start_forecasting()
            
            # Stage 4: Inventory Optimization (TODO)
            # optimization_artifact = self.start_inventory_optimization()
            
            logger.info("\n" + "="*60)
            logger.info("TRAINING PIPELINE COMPLETED SUCCESSFULLY")
            logger.info("="*60)
            logger.info(f"Data ingestion: {data_ingestion_artifact.files_processed_count} files processed")
            logger.info(f"Duration: {data_ingestion_artifact.duration_seconds:.2f}s")
            logger.info("="*60)
            
            return True
            
        except Exception as e:
            logger.error("Training pipeline failed")
            logger.error("="*60)
            logger.error("TRAINING PIPELINE FAILED")
            logger.error("="*60)
            raise SupplyChainException(e, sys)


if __name__ == "__main__":
    # Test the training pipeline
    try:
        print("\n" + "="*60)
        print("TESTING TRAINING PIPELINE")
        print("="*60 + "\n")
        
        # Initialize and run pipeline
        pipeline = TrainingPipeline()
        success = pipeline.run_pipeline()
        
        if success:
            print("\n" + "="*60)
            print("TRAINING PIPELINE TEST PASSED")
            print("="*60)
        else:
            print("\n" + "="*60)
            print("TRAINING PIPELINE TEST COMPLETED WITH WARNINGS")
            print("="*60)
            
    except Exception as e:
        print("\n" + "="*60)
        print(f"TRAINING PIPELINE TEST FAILED")
        print(f"Error: {e}")
        print("="*60)
        import traceback
        traceback.print_exc()