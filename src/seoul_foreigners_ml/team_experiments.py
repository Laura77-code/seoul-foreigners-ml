"""Shared, reproducible experiments for role notebooks 02-04."""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.svm import SVR, SVC
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import StratifiedKFold, KFold, cross_validate
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, balanced_accuracy_score, roc_auc_score, confusion_matrix, mean_absolute_error, mean_squared_error, r2_score
from sklearn.inspection import permutation_importance
from sklearn.base import clone

RANDOM_STATE = 42
CV_FOLDS = 5
N_JOBS = 1
POSITIVE_LABEL = 1
REGRESSION_TARGET = 'Q11'
CLASSIFICATION_TARGET = 'high_satisfaction'


def locate_root():
    cwd=Path.cwd().resolve()
    for directory in (cwd, *cwd.parents):
        if (directory/'data'/'processed'/'seoul_foreigners_modeling_master.csv').exists():
            return directory
    raise FileNotFoundError('Run notebook 01 first; modeling_master.csv not found.')


def load_shared_data(root=None):
    root=Path(root) if root else locate_root()
    directory=root/'data'/'processed'
    master=pd.read_csv(directory/'seoul_foreigners_modeling_master.csv')
    train_ids=pd.read_csv(directory/'train_ids.csv')['ID']
    test_ids=pd.read_csv(directory/'test_ids.csv')['ID']
    assert master['ID'].is_unique and train_ids.is_unique and test_ids.is_unique
    assert not set(train_ids)&set(test_ids), 'Train/test overlap'
    assert set(train_ids)|set(test_ids)==set(master['ID']), 'Split does not cover master data'
    assert len(master)==2500 and len(train_ids)==2000 and len(test_ids)==500
    assert (master[CLASSIFICATION_TARGET]==(master[REGRESSION_TARGET]>=8).astype(int)).all()
    indexed=master.set_index('ID',drop=False)
    train=indexed.loc[train_ids.tolist()].copy()
    test=indexed.loc[test_ids.tolist()].copy()
    return root,master,train,test


def validate_features(frame, nominal, ordinal, numeric):
    groups={'nominal':nominal,'ordinal':ordinal,'numeric':numeric}
    features=sum(groups.values(),[])
    if len(set(features))!=len(features):
        raise ValueError('Feature assigned to multiple groups: '+str(pd.Series(features).value_counts().loc[lambda x:x>1].to_dict()))
    missing=sorted(set(features)-set(frame.columns))
    if missing: raise ValueError('Missing dataset columns: '+str(missing))
    illegal={'ID','Q11','high_satisfaction', 'Q14','Q4_1','Q4_2','Q4_3','Q4_4','Q4_5','Q4_6','Q4_7', 'Q10_1','Q10_2','Q10_3','Q10_4','Q10_5', 'RIM_WT','RIM_WT1'} & set(features)
    if illegal: raise ValueError('Excluded/target-proximal features in core model: '+str(illegal))
    if not features: raise ValueError('Empty features')
    return features


def preprocessing(nominal,ordinal,numeric):
    # A feature can be all-missing in one fold; constant imputation keeps its shape.
    categorical=Pipeline([
        ('impute',SimpleImputer(strategy='most_frequent',keep_empty_features=True)),
        ('encode',OneHotEncoder(handle_unknown='ignore',sparse_output=False))
    ])
    numeric_pipeline=Pipeline([
        ('impute',SimpleImputer(strategy='median',keep_empty_features=True)),
        ('scale',StandardScaler())
    ])
    transformers=[]
    if nominal: transformers.append(('nominal',categorical,nominal))
    if ordinal: transformers.append(('ordinal',numeric_pipeline,ordinal))
    if numeric: transformers.append(('numeric',numeric_pipeline,numeric))
    return ColumnTransformer(transformers=transformers, remainder='drop',verbose_feature_names_out=True)


def candidates(task,nominal,ordinal,numeric):
    def pipe(est): return Pipeline([('preprocess',preprocessing(nominal,ordinal,numeric)),('model',est)])
    if task=='regression':
        return {
          'DummyMean':pipe(DummyRegressor(strategy='mean')),
          'LinearRegression':pipe(LinearRegression()),
          'SVR_RBF':pipe(SVR(C=1.0,epsilon=0.1,kernel='rbf',gamma='scale')),
          'RandomForest':pipe(RandomForestRegressor(n_estimators=200,max_depth=8,min_samples_leaf=3,random_state=RANDOM_STATE,n_jobs=N_JOBS))
        }
    return {
       'DummyMostFrequent':pipe(DummyClassifier(strategy='most_frequent')),
       'LogisticRegression':pipe(LogisticRegression(C=1.0,max_iter=2000,solver='lbfgs',random_state=RANDOM_STATE)),
       'SVC_RBF':pipe(SVC(C=1.0,kernel='rbf',gamma='scale',probability=True,random_state=RANDOM_STATE)),
       'RandomForest':pipe(RandomForestClassifier(n_estimators=200,max_depth=8,min_samples_leaf=3,random_state=RANDOM_STATE,n_jobs=N_JOBS))
    }


def cv_compare(train,nominal,ordinal,numeric,task):
    features=validate_features(train,nominal,ordinal,numeric)
    y=train[REGRESSION_TARGET if task=='regression' else CLASSIFICATION_TARGET]
    X=train[features]
    if task=='regression':
        cv=KFold(n_splits=CV_FOLDS,shuffle=True,random_state=RANDOM_STATE)
        scoring={'rmse':'neg_root_mean_squared_error','mae':'neg_mean_absolute_error','r2':'r2'}
    else:
        cv=StratifiedKFold(n_splits=CV_FOLDS,shuffle=True,random_state=RANDOM_STATE)
        scoring={'f1':'f1','f1_macro':'f1_macro','balanced_accuracy':'balanced_accuracy','accuracy':'accuracy','roc_auc':'roc_auc'}
    rows=[]
    for name,pipeline in candidates(task,nominal,ordinal,numeric).items():
        scores=cross_validate(pipeline,X,y,cv=cv,scoring=scoring,n_jobs=N_JOBS,error_score='raise')
        row={'model':name,'task':task}
        for metric in scoring:
            values=scores['test_'+metric]
            if metric in {'rmse','mae'}: values=-values
            row['cv_'+metric+'_mean']=float(np.mean(values))
            row['cv_'+metric+'_std']=float(np.std(values))
        rows.append(row)
    table=pd.DataFrame(rows)
    score_col='cv_rmse_mean' if task=='regression' else 'cv_f1_macro_mean'
    # Tie resolved by simpler order, without test information.
    table=table.sort_values(score_col,ascending=(task=='regression'),kind='stable').reset_index(drop=True)
    return table


def evaluate_winner(train,test,nominal,ordinal,numeric,task,model_name):
    features=validate_features(train,nominal,ordinal,numeric)
    target=REGRESSION_TARGET if task=='regression' else CLASSIFICATION_TARGET
    pipe=candidates(task,nominal,ordinal,numeric)[model_name]
    pipe.fit(train[features],train[target])
    y_true=test[target]
    pred=pipe.predict(test[features])
    if task=='regression':
        metrics={'model':model_name,'task':task,
            'mae':mean_absolute_error(y_true,pred),
            'rmse':float(np.sqrt(mean_squared_error(y_true,pred))),
            'r2':r2_score(y_true,pred)}
        confusion=None
    else:
        scores=pipe.predict_proba(test[features])[:,list(pipe.named_steps['model'].classes_).index(POSITIVE_LABEL)]
        metrics={'model':model_name,'task':task,
            'accuracy':accuracy_score(y_true,pred),
            'precision':precision_score(y_true,pred,zero_division=0),
            'recall':recall_score(y_true,pred,zero_division=0),
            'f1':f1_score(y_true,pred,zero_division=0),
            'f1_macro':f1_score(y_true,pred,average='macro',zero_division=0),
            'balanced_accuracy':balanced_accuracy_score(y_true,pred),
            'roc_auc':roc_auc_score(y_true,scores)}
        confusion=pd.DataFrame(confusion_matrix(y_true,pred,labels=[0,1]),index=['actual_0','actual_1'],columns=['pred_0','pred_1'])
    return pipe,pd.DataFrame([metrics]),confusion


def feature_permutation(model,test,features,task,n_repeats=5):
    # Test-set permutation importance is descriptive only, not used for selection.
    target=REGRESSION_TARGET if task=='regression' else CLASSIFICATION_TARGET
    scoring='neg_root_mean_squared_error' if task=='regression' else 'f1'
    result=permutation_importance(model,test[features],test[target],scoring=scoring,n_repeats=n_repeats,random_state=RANDOM_STATE,n_jobs=N_JOBS)
    return pd.DataFrame({'feature':features,'importance_mean':result.importances_mean,'importance_std':result.importances_std}).sort_values('importance_mean',ascending=False)
