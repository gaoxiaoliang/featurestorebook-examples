```Shell
python3.12 -m venv .venv
source .venv/bin/activate
pip install invoke
pip install "hopsworks[python,great-expectations]==4.2.10"
export HOPSWORKS_API_KEY=Ex...
export AQICN_API_KEY=75...
inv clean
inv features
```
# Install Dependencies
```Shell
pip install hopsworks[great-expectations]
```
# Set Environment Variables 
```Shell
export AQICN_API_KEY=75...
```
# Create the Feature Store and Backfill Data
```Shell
python 1_air_quality_feature_backfill.py
```
