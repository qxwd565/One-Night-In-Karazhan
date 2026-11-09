#!/usr/bin/env python3
"""Enumerate exact source/display transitions and independently check stat decoding."""
import json
from collections import Counter
from karazhan_history import *

def main():
    builds=observations();current={c['id']:c for c in load(ROOT/'cards.json')['cards']};initial=builds[0]['cards'];previous={};rawprev={};transitions=[];numeric=0;raw=[]
    for b in builds:
        diff={};rawdiff={}
        for cid,c in b['cards'].items():
            t=c['Tag'];state=observed_state(cid,c,current[cid],baseline_abilities(initial[cid]))
            assert c['dbfId']==current[cid]['dbfId'] and t['202'] in ('4','5','7')
            for field,tag in [('cost','48'),('attack','47'),('health','45'),('durability','187' if '187' in t else '45')]:
                if field in state:
                    if tag not in t:
                        assert field=='attack' and cid in ('KAR_029','KAR_710m') and state['type']=='MINION' and state[field]==0,(b['build'],cid,field)
                    else:assert state[field]==int(t[tag]),(b['build'],cid,field)
                    numeric+=1
            if cid in previous and (d:=delta(previous[cid],state)):diff[cid]=d
            if cid in rawprev and (d:=delta(rawprev[cid],c)):rawdiff[cid]=d
            previous[cid]=state;rawprev[cid]=c
        if diff:transitions.append({'build':b['build'],'source':b['source'],'changes':diff})
        if rawdiff:raw.append({'build':b['build'],'source':b['source'],'changes':rawdiff})
    put(ROOT/'tools/karazhan-observed-transitions.json',transitions)
    put(ROOT/'tools/karazhan-source-validation.json',{'result':'pass','builds':len(builds),'identitiesPerBuild':len(current),'cardObservations':sum(len(b['cards']) for b in builds),'numericAssertions':numeric,'numericSourcePresenceChecked':True,'omittedZeroTags':{'ids':['KAR_029','KAR_710m'],'field':'attack','meaning':'Actual minions have implicit zero ATK in XML; card type and pinned zero-stat catalog confirm genuine attack0, unlike absent spell combat stats.'},'displayBoundaryBuilds':len(transitions),'rawBoundaryBuilds':len(raw),'latestUpstreamHead':load(ROOT/'tools/karazhan-archive-evidence.json')['upstreamHead'],'allOriginalsInLaunchArchive':set(initial)==set(current),'weaponStorageChange':{'build':'32.0.0.217964','ids':['KAR_028','KAR_063','KAR_094a','KAR_097t'],'meaning':'DURABILITY187 moved to HEALTH45; projected actual durability is unchanged. Not a gameplay change.'},'limits':'234 selected archived builds are not every live build. Exact tags and raw strings are retained in hash-verified shared pools; live Korean dates come from separate sources.'})
    print(json.dumps({'result':'pass','builds':len(builds),'numericAssertions':numeric,'displayTransitions':len(transitions)}))
if __name__=='__main__':main()
