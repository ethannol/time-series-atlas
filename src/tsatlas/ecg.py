"""Patient-disjoint annotated-beat recognition with auditable capped training folds."""
import json
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from .data import ROOT,write_json
from .common import start_run,finish_run,save_frame,markdown_table
from .classification import rate

CLASSES=['N','S','V','F']
MODELS=['majority','template','logistic','forest']
SEED=20261031


def beat_features(waveforms,rr):
    wave=np.asarray(waveforms,dtype=float);rr=np.asarray(rr,dtype=float)
    if wave.ndim!=2 or wave.shape[1]!=60 or rr.shape!=(len(wave),) or not np.isfinite(wave).all() or not np.isfinite(rr).all() or (rr<0).any():
        raise ValueError('Expected finite aligned60-sample waveforms and nonnegative RR')
    amplitude=np.ptp(wave,axis=1)
    normalized=(wave-np.median(wave,axis=1)[:,None])/np.maximum(amplitude[:,None],1e-6)
    extras=np.c_[np.log(np.maximum(amplitude,1e-6)),np.log(np.maximum(rr,1e-6))]
    return normalized,extras


def fold_indices(beats,mapping,fold,cap=1000):
    groups=np.array([mapping[str(p)] for p in beats['person']]);test=np.flatnonzero(groups==fold)
    rng=np.random.default_rng(SEED+fold);selected=[]
    for person in sorted(set(beats['person'][groups!=fold])):
        index=np.flatnonzero((beats['person']==person)&(groups!=fold))
        selected.extend(np.sort(rng.choice(index,cap,replace=False)) if len(index)>cap else index)
    train=np.sort(np.asarray(selected,dtype=int))
    if set(beats['person'][train])&set(beats['person'][test]):raise ValueError('Patient leakage')
    return train,test


def fit_fold(waveforms,beats,train,test,fold):
    if set(beats['person'][train])&set(beats['person'][test]):raise ValueError('Patient leakage')
    shape,extra=beat_features(waveforms,beats['previous_rr_seconds'])
    y=beats['label'][train];classes,counts=np.unique(y,return_counts=True)
    if len(classes)<2:raise ValueError('Training fold has fewer than two classes; report as unevaluable')
    templates=np.stack([shape[train][y==label].mean(axis=0) for label in classes])
    distance=(shape[test]**2).sum(axis=1)[:,None]-2*shape[test]@templates.T+(templates**2).sum(axis=1)[None,:]
    predictions={'majority':np.repeat(classes[counts.argmax()],len(test)),'template':classes[distance.argmin(axis=1)]}
    pca=PCA(n_components=20,svd_solver='full',whiten=False)
    train_x=np.c_[pca.fit_transform(shape[train]),extra[train]];test_x=np.c_[pca.transform(shape[test]),extra[test]]
    logistic=make_pipeline(StandardScaler(),LogisticRegression(C=1,class_weight='balanced',max_iter=1000))
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always');logistic.fit(train_x,y)
    predictions['logistic']=logistic.predict(test_x)
    forest=RandomForestClassifier(n_estimators=100,max_depth=12,min_samples_leaf=10,class_weight='balanced_subsample',random_state=SEED+fold,n_jobs=1)
    forest.fit(train_x,y);predictions['forest']=forest.predict(test_x)
    audit={'fold':fold,'train_beats':len(train),'test_beats':len(test),'training_people':sorted(set(map(str,beats['person'][train]))),
           'test_people':sorted(set(map(str,beats['person'][test]))),'training_classes':dict(zip(map(str,classes),map(int,counts))),
           'templates':{str(label):values.tolist() for label,values in zip(classes,templates)},
           'pca':{'components':pca.components_.tolist(),'mean':pca.mean_.tolist(),'explained_variance_ratio':pca.explained_variance_ratio_.tolist()},
           'logistic':{'classes':logistic[-1].classes_.tolist(),'mean':logistic[0].mean_.tolist(),'scale':logistic[0].scale_.tolist(),
                       'coefficient':logistic[-1].coef_.tolist(),'intercept':logistic[-1].intercept_.tolist(),'iterations':logistic[-1].n_iter_.tolist(),
                       'warnings':[str(w.message) for w in caught]},
           'forest':{'n_estimators':100,'max_depth':12,'min_samples_leaf':10,'class_weight':'balanced_subsample','random_state':SEED+fold,
                     'n_jobs':1,'classes':forest.classes_.tolist(),'node_counts':[int(t.tree_.node_count) for t in forest.estimators_],
                     'feature_importances':forest.feature_importances_.tolist()},
           'degenerate_waveforms_in_input':int((np.ptp(waveforms,axis=1)<1e-6).sum()),'rr_floors_in_input':int((beats['previous_rr_seconds']<1e-6).sum())}
    rows=[]
    for model,values in predictions.items():
        rows.append(pd.DataFrame({'beat_index':test,'fold':fold,'record':beats['record'][test],'person':beats['person'][test],
                                  'sample':beats['sample'][test],'symbol':beats['symbol'][test],'truth':beats['label'][test],'model':model,'prediction':values}))
    return pd.concat(rows,ignore_index=True),audit


def classification_scores(truth,prediction):
    y=np.asarray(truth);p=np.asarray(prediction)
    if y.ndim!=1 or y.shape!=p.shape or not len(y) or not np.isin(y,CLASSES).all() or not np.isin(p,CLASSES).all():
        raise ValueError('Unknown/misaligned class labels')
    confusion=np.array([[int(((y==a)&(p==b)).sum()) for b in CLASSES] for a in CLASSES])
    per_class=[]
    for i,label in enumerate(CLASSES):
        tp=int(confusion[i,i]);support=int(confusion[i].sum());predicted=int(confusion[:,i].sum());denom=support+predicted
        per_class.append({'class':label,'support':support,'predicted':predicted,'precision':rate(tp,predicted),
                          'recall':rate(tp,support),'f1':2*tp/denom if denom else 0.,'f1_denominator_zero':denom==0})
    supported=[r for r in per_class if r['support']>0]
    return {'n':len(y),'accuracy':float(np.mean(y==p)),'macro_f1':float(np.mean([r['f1'] for r in per_class])),
            'supported_macro_f1':float(np.mean([r['f1'] for r in supported])),
            'supported_macro_recall':float(np.mean([r['recall'] for r in supported])),'supported_classes':len(supported),
            'confusion':confusion.tolist(),'class_order':CLASSES,'per_class':per_class}


def run():
    out,started=start_run('ecg');input_data=np.load(ROOT/'data/snapshots/ecg-beats.npz',allow_pickle=False)
    waves=input_data['waveforms'];beats=input_data['beats']
    fold_manifest=json.loads((ROOT/'studies/ecg/folds.json').read_text());mapping=fold_manifest['patient_to_fold']
    if mapping['201']!=mapping[fold_manifest['record_to_patient']['202']]:raise ValueError('Shared person split')
    frames=[];training_membership=[];audits={}
    for fold in range(5):
        train,test=fold_indices(beats,mapping,fold)
        prediction,audit=fit_fold(waves,beats,train,test,fold);frames.append(prediction);audits[str(fold)]=audit
        training_membership.append(pd.DataFrame({'fold':fold,'beat_index':train,'person':beats['person'][train],'record':beats['record'][train],
                                                  'sample':beats['sample'][train],'label':beats['label'][train]}))
    predictions=pd.concat(frames,ignore_index=True)
    for model,g in predictions.groupby('model'):
        if len(g)!=len(beats) or not g.beat_index.is_unique or set(g.beat_index)!=set(range(len(beats))):raise ValueError('Incomplete out-of-person test coverage')
    save_frame(predictions,out/'predictions.csv.gz');save_frame(pd.concat(training_membership,ignore_index=True),out/'training-membership.csv.gz')
    write_json(out/'model-audit.json',audits)
    metrics={model:classification_scores(g.truth,g.prediction) for model,g in predictions.groupby('model')}
    write_json(out/'metrics.json',{'primary':metrics,'people':len(mapping),'records':len(set(beats['record'])),'beats':len(beats)})
    person_rows=[];class_rows=[];fold_rows=[]
    for (person,model),g in predictions.groupby(['person','model']):
        score=classification_scores(g.truth,g.prediction)
        person_rows.append({'person':person,'model':model,**{k:score[k] for k in ['n','accuracy','supported_macro_f1','supported_macro_recall','supported_classes']}})
        class_rows.extend([{'person':person,'model':model,**r} for r in score['per_class']])
    for (fold,model),g in predictions.groupby(['fold','model']):
        score=classification_scores(g.truth,g.prediction);fold_rows.append({'fold':int(fold),'model':model,**{k:score[k] for k in ['n','accuracy','macro_f1','supported_macro_recall','supported_classes']}})
    people=pd.DataFrame(person_rows);people.to_csv(out/'person-scores.csv',index=False)
    pd.DataFrame(class_rows).to_csv(out/'person-class-scores.csv',index=False);pd.DataFrame(fold_rows).to_csv(out/'fold-scores.csv',index=False)
    fig,axes=plt.subplots(1,2,figsize=(12,4.7));colors=['#6b7280','#d97706','#2563eb','#0f766e']
    labels=['Majority','Class template','Logistic','Forest']
    for i,model in enumerate(MODELS):
        recalls=[r['recall'] if r['recall'] is not None else np.nan for r in metrics[model]['per_class']]
        axes[0].bar(np.arange(4)+(i-1.5)*.19,recalls,width=.18,label=labels[i],color=colors[i])
    axes[0].set_xticks(range(4),CLASSES);axes[0].set_ylim(0,1);axes[0].set_ylabel('Pooled class recall');axes[0].legend(fontsize=8)
    axes[1].boxplot([people[people.model==m].supported_macro_recall for m in MODELS],tick_labels=labels,showfliers=True)
    axes[1].set_ylim(0,1);axes[1].set_ylabel('Per-person recall over present classes');axes[1].tick_params(axis='x',rotation=15)
    fig.suptitle('43 unseen-at-test people • 100,662 annotated beats • fixed patient-disjoint folds');fig.tight_layout();fig.savefig(out/'people-and-classes.png');plt.close(fig)
    fig,ax=plt.subplots(figsize=(8,4))
    for label,template in audits['0']['templates'].items():ax.plot(np.arange(60)/120-.25,template,label=label)
    ax.set_xlabel('Seconds relative to expert beat center');ax.set_ylabel('Beat-local normalized amplitude')
    ax.set_title('Fold 0 training class templates (no test beats)');ax.legend();fig.tight_layout();fig.savefig(out/'training-templates.png');plt.close(fig)
    table=markdown_table(['Method','Macro F1 (four fixed groups)','Accuracy','Macro class recall'],[[model,f"{metrics[model]['macro_f1']:.3f}",f"{metrics[model]['accuracy']:.3f}",f"{metrics[model]['supported_macro_recall']:.3f}"] for model in MODELS])
    support=markdown_table(['Group','Included symbols','Beats','People with group'],[[c,{'N':'N,L,R,e,j','S':'A,a,J,S','V':'V,E','F':'F'}[c],int((beats['label']==c).sum()),len(set(beats['person'][beats['label']==c]))] for c in CLASSES])
    report=f'''# Do heartbeat patterns transfer to people absent from training?

Every retained person is tested once in a fold that excludes that person from
training. The two recordings of patient 201 remain together. Performance by
class and person matters alongside the pooled score; 100,662 beats still provide
only 43 independent patient groups in this selected historic benchmark.

{table}

![Recognition by class and person](people-and-classes.png)

{support}

## What the models were given

This is classification **given expert beat locations**, not an end-to-end beat
detector. Windows use a quarter second before and after that location; previous
RR also uses annotation times. Four paced recordings are excluded and MLII is
selected by name, including its reversed channel position in record 114.
The N benchmark group includes bundle-branch and escape beats: N is not a
healthy-person diagnosis. Other symbols, missing prior RR and waveform boundaries
are counted in the [source audit](../../intake/ecg.json).

All five folds were fixed before fitting. Training is capped at 1,000 randomly
selected beats per person, without label balancing in that sample selection;
every eligible held-out beat is scored. PCA and fitted feature scaling use only
that fold's training people. Template, logistic and forest are different pipelines,
not a controlled comparison of model families with every other choice identical.

![Training-only normalized templates](training-templates.png)

## How to read the variation

Primary macro F1 averages all four declared classes. Per-person summaries average
only the classes actually present for that person and show their support counts;
they have a different denominator. A rare absent class has undefined recall,
not perfect recognition. Read [person/class support](person-class-scores.csv),
[person scores](person-scores.csv) and [fold scores](fold-scores.csv) beside the plot.
The benchmark deliberately includes unusual rhythms. Scores do not estimate
population prevalence, diagnostic effectiveness or future clinical performance.

The [model audit](model-audit.json) retains training/test people, PCA/scaler/logistic
parameters, templates, forest settings and diagnostics. Forest trees are refitted
by the deterministic reproduction command; their saved hard predictions are
independently scoreable. [Training membership](training-membership.csv.gz) exposes
every capped sample; [test predictions](predictions.csv.gz) expose every outcome.

[Design](../../../studies/ecg/DESIGN.md) · [Story](../../../studies/ecg/STORY.md) ·
[Metrics](metrics.json) · [Run evidence](run.json). Run `uv run atlas ecg`.
Contains information from the MIT-BIH Arrhythmia Database v1.0.0 (Moody and Mark,
2005), DOI10.13026/C2F305, made available under Open Data Commons Attribution1.0.
'''
    (out/'REPORT.md').write_text(report)
    finish_run('ecg',out,started,{'folds':5,'seed':SEED,'training_beats_per_person_cap':1000,'classes':CLASSES,'models':MODELS})


if __name__=='__main__':run()
