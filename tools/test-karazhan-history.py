#!/usr/bin/env python3
"""Independent literal high-risk regression cases, never generated expectations."""
from date_schema import *
from karazhan_history import ROOT

def state(cid,day):return fold(load(ROOT/'data'/f'{cid}.json'),day)
def check(cid,day,fields):
    actual=state(cid,day)
    for k,v in fields.items():assert json_equal(actual.get(k),v),(cid,day,k,actual.get(k),v)

assert state('KAR_300','2016-08-11') is None
check('KAR_300','2016-08-12',{'cost':1,'attack':2,'health':2,'text':'','races':['BEAST']})
check('KAR_076','2016-08-12',{'cost':7});assert '피해를 5' in state('KAR_076','2016-08-12')['text']
check('KAR_021','2016-08-26',{'cost':4});check('KAR_021','2023-08-22',{'cost':4});check('KAR_021','2023-08-23',{'cost':3})
check('KAR_063','2017-02-28',{'cost':1});check('KAR_063','2017-03-01',{'cost':2});check('KAR_063','2021-03-26',{'cost':1})
check('KAR_114','2019-08-26',{'cost':4});check('KAR_114','2019-08-27',{'cost':5})
check('KAR_065','2021-03-25',{'cost':6,'attack':5,'health':5});check('KAR_065','2021-03-26',{'cost':5,'attack':4,'health':4});check('KAR_065','2023-08-23',{'cost':5,'attack':5,'health':4})
check('KAR_057','2023-08-22',{'cost':6});check('KAR_057','2023-08-23',{'cost':4})
for cid,a,b in [('KAR_077',4,3),('KAR_091',5,4),('KAR_204',5,4)]:
    check(cid,'2023-08-22',{'cost':a});check(cid,'2023-08-23',{'cost':b})
check('KAR_205','2023-08-22',{'health':3});check('KAR_205','2023-08-23',{'health':4})
assert '피해를 6' in state('KAR_076','2023-08-23')['text']
for cid in ('KAR_009','KAR_069'):
    check(cid,'2023-04-04',{'health':1});check(cid,'2023-04-05',{'health':2})
check('KAR_061','2025-03-18',{'cost':7});check('KAR_061','2025-03-19',{'cost':5})
check('KAR_062','2025-03-18',{'attack':1});check('KAR_062','2025-03-19',{'attack':2})
check('KAR_089','2025-11-13',{'cost':1});check('KAR_089','2025-11-14',{'cost':2})
assert 'races' not in state('KAR_036','2017-04-04');check('KAR_036','2017-04-05',{'races':['ELEMENTAL']})
for cid,school in [('KAR_013','HOLY'),('KAR_073','NATURE'),('KAR_075','NATURE'),('KAR_076','FIRE'),('KAR_077','HOLY'),('KAR_091','FIRE')]:
    assert 'spellSchool' not in state(cid,'2021-03-25');check(cid,'2021-03-26',{'spellSchool':school})
assert 'spellSchool' not in state('KAR_004','2099-01-01')
assert '상대편' in state('KAR_069','2021-03-25')['text'];assert '다른 직업' in state('KAR_069','2021-03-26')['text']
assert 'START_OF_GAME' not in state('KAR_096','2018-04-10')['mechanics'];assert 'START_OF_GAME' in state('KAR_096','2018-04-11')['mechanics']
for cid in ('KAR_006','KAR_026','KAR_063','KAR_712'):assert state(cid,'2016-09-02')['mechanics']==[]
check('KAR_004','2016-09-02',{'mechanics':['SECRET']});check('KAR_004a','2016-09-02',{'mechanics':['STEALTH']})
check('KAR_037','2016-09-02',{'mechanics':['BATTLECRY']});check('KAR_710','2016-09-02',{'mechanics':['BATTLECRY']})
for cid in ('KAR_057','KAR_062'):check(cid,'2016-09-02',{'mechanics':['BATTLECRY','DISCOVER']})
check('KAR_030','2016-09-02',{'collectible':False,'text':''});check('KAR_030a','2016-09-02',{'collectible':True,'mechanics':['BATTLECRY']})
check('KAR_029','2016-09-02',{'attack':0,'health':2});check('KAR_710m','2016-09-02',{'attack':0,'health':5})
for cid,dur in [('KAR_028',4),('KAR_063',3),('KAR_094a',2),('KAR_097t',3)]:
    check(cid,'2025-03-18',{'durability':dur});check(cid,'2025-03-19',{'durability':dur});assert 'health' not in state(cid,'2099-01-01')
# Estimated week dates are not an implicit policy to block earlier generation.
t,m=read_card(ROOT,'KAR_004');assert fold(t,'2016-08-25') is None and resolve(t,m,'2016-08-25') is not None and m['release']['status']=='estimated'
assert m['release']['date']=='2016-08-26' and 'beforeDate' not in m['release']
print('Karazhan literal balance, keyword ownership, original identities, typed zero and usability-bound tests passed')
