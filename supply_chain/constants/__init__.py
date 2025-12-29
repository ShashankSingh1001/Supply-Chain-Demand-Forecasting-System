from pathlib import Path

# ================================
# PROJECT ROOT & BASE PATHS
# ================================

# Get project root
PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()

# Base directories
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
CONFIG_DIR = PROJECT_ROOT / "configs"
LOGS_DIR = PROJECT_ROOT / "logs"

# ================================
# DATA INGESTION
# ================================

# Artifact directories
DATA_INGESTION_DIR = ARTIFACTS_DIR / "data_ingestion"

# Required raw files
REQUIRED_RAW_FILES = [
    "train.csv",
    "test.csv",
    "items.csv",
    "stores.csv",
    "holidays_events.csv",
    "oil.csv",
    "transactions.csv"
]

# Raw file paths (for easy access)
RAW_FILES = {
    "train": RAW_DATA_DIR / "train.csv",
    "test": RAW_DATA_DIR / "test.csv",
    "items": RAW_DATA_DIR / "items.csv",
    "stores": RAW_DATA_DIR / "stores.csv",
    "holidays_events": RAW_DATA_DIR / "holidays_events.csv",
    "oil": RAW_DATA_DIR / "oil.csv",
    "transactions": RAW_DATA_DIR / "transactions.csv"
}

# Config file
DATA_INGESTION_CONFIG = CONFIG_DIR / "data_ingestion.yaml"

# ================================
# FUTURE PIPELINE CONSTANTS
# ================================

# DATA TRANSFORMATION
# (to be added when building transformation pipeline)

# FORECASTING
# (to be added when building forecasting pipeline)

# INVENTORY OPTIMIZATION
# (to be added when building optimization pipeline)


if __name__ == "__main__":
    print("=" * 60)
    print("SUPPLY CHAIN CONSTANTS")
    print("=" * 60)
    print(f"\n📁 Project Root: {PROJECT_ROOT}")
    print(f"📁 Raw Data: {RAW_DATA_DIR}")
    print(f"📁 Artifacts: {ARTIFACTS_DIR}")
    print(f"\n📄 Required Files ({len(REQUIRED_RAW_FILES)}):")
    for file in REQUIRED_RAW_FILES:
        print(f"   - {file}")
    print("=" * 60)