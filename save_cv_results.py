"""Run cross-validation on example data for a series of different models,
and save relevant results from each model for further evaluation."""

# Import spotify API tools and modeling functions
from spotify_tools import *
from model_tools import *

# Set file numbers to process
filerange = range(0, 201)

# Set up model search parameters
n_trees = [50, 100, 200]
n_depth = [2, 4, 6, 8, 10, 12]
p_list = ['l1', 'l2']
c_list = [.001, .1, 1, 10, 100]

# Iterate over the files
for i_file in filerange:
    # Skip this file if it doesn't exist, open it otherwise
    fpath = 'Data/data_artist_{}.pkl'.format(i_file)
    if not os.path.exists(fpath):
        continue
    with open(fpath, 'rb') as f:
        data = pickle.load(f)

    # Exclude if the recommended tracks list was empty
    if data[2][3]:
        # Set the save path for the cross-validation results
        save_name = 'cv_results_artist_{}.pkl'.format(i_file)
        save_path = 'Data/{}'.format(save_name)

        # Skip this file if it already exists
        if os.path.exists(save_path):
            print('Skipped: ', save_name)
            continue

        # Split the data into training and test sets
        splits = split_df(data[2][5])

        # Set up the models to test
        all_models = []
        all_models.extend(RFC_list(n_trees, n_depth))
        all_models.extend(LR_list(p_list, c_list))
        all_models.extend(SVC_list(c_list))

        # Test the models on the real data and the randomized data
        results = []
        results_baseline = []
        for model in all_models:
            results.append(run_cv(model, splits[0], splits[2]))
            results_baseline.append(run_cv(model, splits[0], splits[4]))

        # Compute hold-out scores and delete estimators (to save space)
        key_order = ['fit_time', 'score_time', 'train_score', 'test_score', 'holdout_score', 'y_pred', 'y_pred_proba']
        for n, r in enumerate(results):
            holdout_scores = []
            y_preds = []
            y_preds_proba = []
            for est in r['estimator']:
                y_pred = est.predict(splits[1])
                y_preds.append(y_pred)
                holdout = metrics.recall_score(splits[3], y_pred)
                holdout_scores.append(holdout)
                # Compute class probabilities if model is LR or RFC
                if est['model'].__class__.__name__ in ['LogisticRegression', 'RandomForestClassifier']:
                    y_pp = est.predict_proba(splits[1])
                else:
                    y_pp = None
                y_preds_proba.append(y_pp)
            r['holdout_score'] = np.array(holdout_scores)
            r['y_pred'] = y_preds
            r['y_pred_proba'] = y_preds_proba
            del r['estimator']
            # Reorder keys
            results[n] = {k:r[k] for k in key_order}

        for n, r in enumerate(results_baseline):
            holdout_scores = []
            y_preds = []
            y_preds_proba = []
            for est in r['estimator']:
                y_pred = est.predict(splits[1])
                y_preds.append(y_pred)
                holdout = metrics.recall_score(splits[5], y_pred)
                holdout_scores.append(holdout)
                # Compute class probabilities if model is LR or RFC
                if est['model'].__class__.__name__ in ['LogisticRegression', 'RandomForestClassifier']:
                    y_pp = est.predict_proba(splits[1])
                else:
                    y_pp = None
                y_preds_proba.append(y_pp)
            r['holdout_score'] = np.array(holdout_scores)
            r['y_pred'] = y_preds
            r['y_pred_proba'] = y_preds_proba
            del r['estimator']
            # Reorder keys
            results_baseline[n] = {k:r[k] for k in key_order}

        # Save the results
        with open(save_path, 'wb') as f:
            pickle.dump([save_name, splits, all_models, results, results_baseline], f)
        print('Saved: ', save_name)