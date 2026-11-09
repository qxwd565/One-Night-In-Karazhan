#!/usr/bin/env python3
"""Reproduce date-first history from pinned originals and explicit source policies."""
import copy,json,subprocess
from date_schema import *
from karazhan_history import SOURCE,ROOT,observations,reconstruct

def original(path):
    try:return json.loads(subprocess.check_output(['git','show',SOURCE+':'+path],cwd=ROOT))
    except subprocess.CalledProcessError:raise RuntimeError('Pinned source unavailable; require checkout fetch-depth: 0')

def main():
    catalog=original('cards.json');builds=observations();dates=load(ROOT/'tools/karazhan-effective-dates.json')['builds'];release=load(ROOT/'tools/karazhan-release-policy.json')['cards'];changed=0
    original_ids={p.stem for p in (ROOT/'data').glob('*.json') if p.stem!='history'}
    assert original_ids=={c['id'] for c in catalog['cards']}
    for current in catalog['cards']:
        cid=current['id'];path=ROOT/'data'/f'{cid}.json';doc=load(path)
        if 'card' not in doc:
            validate_timeline(doc);assert (ROOT/'metadata'/path.name).exists();continue
        pristine=original('data/'+path.name);assert doc==pristine
        assert not (ROOT/'metadata'/path.name).exists()
        timeline,gaps,evidence=reconstruct(current,builds,dates,release)
        latest=fold(timeline);fields=sorted({k for d in timeline.values() for k in d if k!='__remove'}|{x for d in timeline.values() for x in d.get('__remove',[])})
        meta={'schema':'hscard-date-metadata-1','id':cid,'timezone':'Asia/Seoul','release':release[cid],
              'availabilityScope':'Korean ordinary constructed-match use, including generated exact original entities. Preload, reveal and PvE do not count. Later-wing earliest-generation dates remain qualified.',
              'baselineStatus':'partially-verified','confidenceNote':'All57 original identities, initial numbers, Korean archive text and card types checked in launch archive. Noncollectible rarity, earlier-than-wing generation and unverified wording effective dates remain explicitly qualified.',
              'sourceCommit':SOURCE,'originalSource':pristine,'currentCatalog':current,
              'canonicalFields':fields,'currentOnlyFields':sorted(set(current)-set(fields)-{'releasedAt','releaseStatus'}),
              'historicalEvidence':evidence,'undatedEvidence':gaps,
              'keywordAbilityEvidence':{'source':'tools/karazhan-ability-policy.json'},
              'legacyMechanicsConvention':{'present':'mechanics' in current,'original':current.get('mechanics',[]),'canonicalBaseline':latest['mechanics']},
              'behaviorEvidence':'tools/karazhan-behavior-audit.json','sourceHistory':'tools/original-date-first-history.json'}
        if not current['collectible']:
            meta['fieldUncertainty']={'rarity':{'status':'unresolved-historical-display','retainedValue':current['rarity'],'meaning':'Pinned exporter value retained. Raw archive rarity tags and absence remain observations, not proof of dated visible rarity change.'}}
        put(ROOT/'metadata'/path.name,meta);put(path,timeline);changed+=1
    put(ROOT/'tools/original-date-first-history.json',original('data/history.json'))
    print(json.dumps({'migrated':changed,'sourceCommit':SOURCE,'cards':len(catalog['cards'])}))
if __name__=='__main__':main()
