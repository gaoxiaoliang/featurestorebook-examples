# Requirements
- OS: macOS 12.7.6 (Intel, x86_64)
- Python 3.11.9
# Install Dependencies
```Shell
pip install hopsworks==4.2.10 pandas==2.1.4 pyarrow==22.0.0
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
## Note on Feature View Versions
When running the line:
```Python
X_train, X_test, y_train, y_test = feature_view.train_test_split(0.2)
```
Hopsworks internally automatically creates a new version of the `feature_view`, as indicated by logs like:
```
VersionWarning: Incremented version to `8`.
```
However, the Python variable `feature_view` still shows its original version (e.g., 1).

Interestingly, when the model is finally created using:
```Python
titanic_model = mr.python.create_model(..., feature_view=feature_view, ...)
titanic_model.save(model_dir)
```
Hopsworks actually binds the model to the latest feature view version (the one created internally by `train_test_split`), not the version that the variable `feature_view` appears to reference.

This behavior can be counterintuitive: although your code variable seems unchanged, Hopsworks updates the version behind the scenes. Keep this in mind when tracking feature view versions or reproducing experiments.
# Install Dependencies
```Shell
pip install "hopsworks[python]"
```
# Daily Pipeline
```Shell
python scheduled-titanic-feature-pipeline-daily.py && python scheduled-titanic-batch-inference-daily.py
```
