"""Pinned Karazhan observations and explicitly dated ordinary-match specs."""
import copy,re,hashlib,json
from pathlib import Path
from date_schema import *
SOURCE='537ecd58630a527af3dc2c8aef4badecd9d33972'
ROOT=Path(__file__).resolve().parents[1]
RACES={'2':('DRAENEI','드레나이'),'11':('UNDEAD','언데드'),'14':('MURLOC','멀록'),'15':('DEMON','악마'),'17':('MECHANICAL','기계'),'18':('ELEMENTAL','정령'),'20':('BEAST','야수'),'23':('PIRATE','해적'),'24':('DRAGON','용족')}
SCHOOLS={'1':'ARCANE','2':'FIRE','3':'FROST','4':'NATURE','5':'HOLY','6':'SHADOW','7':'FEL'}
TYPES={'4':'MINION','5':'SPELL','7':'WEAPON'}
CLASSES={'0':'NEUTRAL','1':'DEATHKNIGHT','2':'DRUID','3':'HUNTER','4':'MAGE','5':'PALADIN','6':'PRIEST','7':'ROGUE','8':'SHAMAN','9':'WARLOCK','10':'WARRIOR','12':'NEUTRAL'}
KEYWORDS={'189':'WINDFURY','190':'TAUNT','191':'STEALTH','192':'SPELLPOWER','194':'DIVINE_SHIELD','197':'CHARGE','217':'DEATHRATTLE','218':'BATTLECRY','219':'SECRET','220':'COMBO','215':'OVERLOAD','311':'CANT_BE_TARGETED_BY_SPELLS','332':'CANT_BE_TARGETED_BY_HERO_POWERS','363':'POISONOUS','212':'ENRAGED','791':'RUSH','443':'CHOOSE_ONE','415':'DISCOVER','1211':'ELUSIVE','968':'START_OF_GAME'}

def observations(root=ROOT):
    manifest=load(root/'tools/karazhan-archive-evidence.json');pool={}
    for p in (root/'tools/archive-states').glob('*.json'):pool.update(load(p))
    def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
    for key,value in pool.items():assert hashlib.sha256(canon(value)).hexdigest()[:20]==key
    refs={};result=[]
    for b in manifest['builds']:
        refs.update(b['changedStates'])
        for cid in b.get('removedIds',[]):refs.pop(cid)
        cards={cid:copy.deepcopy(pool[key]) for cid,key in refs.items()}
        assert len(cards)==b['cardCount'] and hashlib.sha256(canon(cards)).hexdigest()==b['extractedCardsSha256']
        result.append(dict(b,cards=cards))
    return result

def display(raw,cid):
    text=(raw or '').replace('[x]','')
    text=re.sub(r'[$#](?=\d)', '', text)
    text=text.replace(':&', ':')
    if '{' in text or ':&' in text:raise ValueError('Unresolved native display template: '+cid+' '+text)
    return BREAK.sub('<br></br>',text)

def baseline_abilities(card):
    return sorted(name for tag,name in KEYWORDS.items() if int(card['Tag'].get(tag,0))>0)

def abilities(cid,text,initial):
    values=set(initial)
    if cid in ('KAR_057','KAR_062'):values.add('DISCOVER')
    if cid=='KAR_096' and '<b>개전' in text:values.add('START_OF_GAME')
    return sorted(values)

def observed_state(cid,card,current,initial):
    tags=card['Tag'];kind=TYPES[tags['202']]
    state={'id':cid,'dbfId':card['dbfId'],'name':card['name'],'type':kind,
           'cardClass':CLASSES[tags.get('199','0')],'classes':copy.deepcopy(current['classes']),
           'rarity':current['rarity'],'collectible':bool(int(tags.get('321','0'))),
           'cost':int(tags.get('48','0')),'text':display(card['rawText'],cid)}
    if kind in ('MINION','WEAPON'):state['attack']=int(tags.get('47','0'))
    if kind=='MINION':state['health']=int(tags.get('45','0'))
    if kind=='WEAPON':state['durability']=int(tags.get('187',tags.get('45','0')))
    race=tags.get('200','0')
    if race!='0':state['races']=[RACES[race][0]];state['race']=RACES[race][1]
    school=tags.get('1635','0')
    if school!='0':state['spellSchool']=SCHOOLS[school]
    state['mechanics']=abilities(cid,state['text'],initial)
    return state

def reconstruct(current,builds,dates,releases=None):
    timeline={};gaps=[];evidence=[];cid=current['id'];prior=None;canonical=None
    release=(releases or load(ROOT/'tools/karazhan-release-policy.json')['cards'])[cid]
    day=release['date'];first=builds[0]['cards'][cid];initial=baseline_abilities(first)
    for b in builds:
        n=b['build'].split('.')[-1];card=b['cards'].get(cid)
        if card is None:continue
        state=observed_state(cid,card,current,initial)
        if prior is None:
            canonical=copy.deepcopy(state);timeline[day]=copy.deepcopy(state)
            evidence.append({'date':day,'build':b['build'],'source':b['source'],'fields':sorted(state),'availabilityStatus':release['status']})
        else:
            changes=delta(prior,state)
            if changes:
                rule=dates.get(n)
                if rule:
                    when=rule['date'];assert when>=day,(cid,when,day)
                    canonical=apply(canonical,changes)
                    if when in timeline:
                        baseline=fold({d:v for d,v in timeline.items() if d<when}) or {}
                        timeline[when]=delta(baseline,canonical)
                    else:timeline[when]=changes
                    evidence.append({'date':when,'build':b['build'],'source':b['source'],'dateSource':rule['sources'],'fields':sorted(changes),'kind':rule.get('kind','archive-change'),'dateConfidence':rule.get('dateConfidence','qualified')})
                else:
                    gaps.append({'beforeBuild':previous['build'],'firstObservedBuild':b['build'],'source':b['source'],'changes':changes,'status':'unresolved-effective-Korean-date; not emitted as dated history'})
        prior=state;previous=b
    timeline=dict(sorted(timeline.items()));validate_timeline(timeline)
    return timeline,gaps,evidence
