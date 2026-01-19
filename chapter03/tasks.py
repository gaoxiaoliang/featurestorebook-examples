from invoke import task

@task
def clean(c):
    c.run('python clean_hopsworks_resources.py')

@task
def backfill(c):
    c.run('python 1_air_quality_feature_backfill.py')

@task
def features(c):
    c.run('python 2_air_quality_feature_pipeline.py')
