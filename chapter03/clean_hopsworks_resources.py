import hopsworks

project = hopsworks.login(engine='python')

fs = project.get_feature_store()
ms = project.get_model_serving()
mr = project.get_model_registry()

def delete_model(model_name):
    models = mr.get_models(name=model_name)
    for model in models:
        print(f'Deleting model: {model.name} (version: {model.version})')
        try:
            model.delete()
        except Exception:
            print(f'Failed to delete model {model_name} (version: {model.version}).')

def delete_feature_view(feature_view):
    feature_views = fs.get_feature_view(name=feature_view)
    if feature_views is None:
        return

    for fv in feature_views:
        print(f'Deleting feature view: {fv.name} (version: {fv.version})')
        try:
            fv.delete()
        except Exception:
            print(f'Failed to delete feature view {fv.name} (version: {fv.version}).')

def delete_feature_group(feature_group, project_name):
    feature_groups = fs.get_feature_groups(name=feature_group)

    for fg in feature_groups:
        print(f'Deleting feature group: {fg.name} (version: {fg.version})')
        try:
            fg.delete()
        except Exception:
            print(f'Failed to delete feature group {fg.name} (version: {fg.version}).')


delete_model('air_quality_xgboost_model')
delete_feature_view('air_quality_fv')
for feature_group in ['air_quality', 'weather', 'air_quality_fv_1_logging_transformed', 'air_quality_fv_1_logging_untransformed', 'aq_predictions']:
    delete_feature_group(feature_group, project.name)
