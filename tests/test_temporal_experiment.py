"""Synthetic fixtures exercise software only; these are never scientific results."""
import json
from pathlib import Path
import pytest
np = pytest.importorskip("numpy")
pytest.importorskip("sklearn")
from research_agent.experiment import read_config, main
from research_agent.experiments.data import load_windows, corrupt, features, views
from research_agent.experiments.metrics import threshold, frozen_risk, risk_curve


def windows():
    rows=[]
    for split in ('train','calibration','validation','test'):
        for recording in range(2):
            for i in range(6):
                t=np.linspace(-.5,0,16)
                label=i%2
                x=.4 + .08*(label*2-1)*(t+.5) + .005*i
                boxes=np.column_stack([x,np.full(16,.5),np.full(16,.1),np.full(16,.2)])
                rows.append({'id':f'{split}-{recording}-{i}', 'recording_id':f'{split}-{recording}',
                    'video_id':f'{split}-{recording}', 'pedestrian_id':str(i), 'split':split,
                    'label_source':'synthetic_test', 'label':label, 'prediction_horizon_s':1.0,
                    'timestamps_s':t.tolist(), 'boxes':boxes.tolist(), 'ego_speed_mps':[5.0]*16})
    return rows


def write_rows(tmp_path, rows):
    path=tmp_path/'data.jsonl'
    path.write_text(''.join(json.dumps(r)+'\n' for r in rows))
    return path


def config():
    path=Path(__file__).resolve().parents[1]/'configs/experiments/temporal-consistency.json'
    c=read_config(path)
    c.update(seeds=[11],bootstrap_repetitions=10)
    return c


def test_split_leakage_and_future_features_rejected(tmp_path):
    rows=windows()
    assert len(load_windows(write_rows(tmp_path,rows),1.0))==48
    rows[-1]['recording_id']=rows[0]['recording_id']
    with pytest.raises(ValueError,match='crosses'):
        load_windows(write_rows(tmp_path,rows),1.0)
    rows=windows();rows[0]['timestamps_s'][-1]=.1
    with pytest.raises(ValueError,match='zero'):
        load_windows(write_rows(tmp_path,rows),1.0)


def test_temporal_views_preserve_target_time_and_speed_units():
    row=windows()[0]
    altered=corrupt(row,'burst_drop',.5,np.random.default_rng(1))
    assert altered['timestamps_s'][0]==-.5 and altered['timestamps_s'][-1]==0
    assert altered['label']==row['label']
    assert features(altered).shape==features(row).shape==(20,)
    # A time-based slope remains correct after frame dropping.
    assert features(altered)[15]==pytest.approx(features(row)[15])
    assert all(v['timestamps_s'][0]==-.5 and v['timestamps_s'][-1]==0 for v in views(row))


def test_risk_and_frozen_threshold_are_distinct():
    y=np.array([0,1,1,0]);p=np.array([.1,.9,.2,.8]);score=np.array([.9,.8,.7,.6])
    assert risk_curve(y,p,score,[.5])['matched_coverage_risk']['0.5']==0
    cut=threshold(score,.5)
    assert frozen_risk(y,p,score,cut)=={'coverage':.5,'risk':0.0}
    assert frozen_risk(y,p,score,2.0)=={'coverage':0.0,'risk':None}


def test_explicit_approval_required(tmp_path):
    with pytest.raises(SystemExit) as exc:
        main(['--data',str(tmp_path/'missing'),'--output',str(tmp_path/'result')])
    assert exc.value.code==2 and not (tmp_path/'result').exists()


def test_cpu_synthetic_software_smoke(tmp_path):
    from research_agent.experiments.runner import run_experiment
    data=write_rows(tmp_path,windows())
    result=run_experiment(data,config(),tmp_path/'out')
    assert result['data_kind']=='synthetic_test'
    assert len(result['results'])==10  # 2 representations x 5 conditions, 1 fixture seed
    assert (tmp_path/'out/predictions.jsonl').exists()
    for r in result['results']:
        assert r['methods']['repeat_view_control']==r['methods']['calibrated_confidence']
        if r['representation']=='last':
            # Endpoints are unchanged, so temporal sampling cannot change last-frame predictions.
            assert r['methods']['temporal_consistency']['aurc']==pytest.approx(r['methods']['calibrated_confidence']['aurc'])
    assert 'Synthetic tests are not research findings' in (tmp_path/'out/report.md').read_text()
