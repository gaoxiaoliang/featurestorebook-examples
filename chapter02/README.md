# Requirements
- OS: macOS 12.7.6 (Intel, x86_64)
- Python 3.11.9
# Install Dependencies
```Shell
pip install "hopsworks==4.2.*" pandas==2.1.4 pyarrow==22.0.0
```
# Set Environment Variables
```Shell
export HOPSWORKS_API_KEY=Ex...
```
# Create the Feature Store and Backfill Data
```Shell
python titanic-feature-group-backfill.py
```
# Install Dependencies
```Shell
brew install libomp
pip install xgboost==3.1.2 scikit-learn==1.8.0 seaborn==0.13.2
```
# Train model and register
```Shell
python titanic-training-pipeline.py
```
