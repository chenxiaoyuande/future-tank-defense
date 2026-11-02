from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile
import json
import re
from PIL import Image
from io import BytesIO
from release_info import DIST_DIR, package_name, manifest
from project_paths import ROOT as root

with ZipFile(DIST_DIR/package_name()) as archive:
    assert archive.testzip() is None
    paths=set(archive.namelist())
    assert json.loads(archive.read('version.json')) == manifest()
    assert json.loads(archive.read('builder-meta.json'))['version'] == manifest()['version']
    config=json.loads(archive.read('assets/index.json'))
    assert config['zorder']==['Splash','HomeDecor','Scene','Atmosphere','Actor','Brain','Health','Frame','Hud','Ability','Buff','Campaign','Notice','StageCard','UIAction','Wallet']
    assert not any(path.startswith('.build/') or '/node_modules/' in path for path in paths)
    assert 'tools/project.py' in paths and 'tests/brain_test.go.txt' in paths
    for backdrop in config['backdrops']:
        assert isinstance(backdrop['bitmapResolution'],int)
        image=Image.open(BytesIO(archive.read('assets/'+backdrop['path'])))
        assert image.size==(backdrop['imageWidth'],backdrop['imageHeight'])
    names={}
    for name in config['zorder']:
        assert name+'.spx' in paths
        data=json.loads(archive.read(f'assets/sprites/{name}/index.json'))
        names[name]={c['name'] for c in data['costumes']}
        for c in data['costumes']:
            assert f'assets/sprites/{name}/'+c['path'] in paths
            assert isinstance(c['bitmapResolution'],int)
    for direction in ['up','right','down','left']:
        for frame in range(6):
            assert f'plant-{direction}-{frame}' in names['Actor']
        for frame in range(8):
            for variant in range(3):
                assert f'zombie-{variant}-{direction}-{frame}' in names['Actor']
    for i in range(7):
        assert f'pop-{i}' in names['Actor']
    for i in range(11):
        assert f'cooldown-{i}' in names['Atmosphere']
    for i in range(4):
        assert f'mega-{i}' in names['Actor']
    for i in range(10):
        assert f'burst-{i}' in names['Actor']
    assert 'ready' in names['Ability'] and 'ready-lit' in names['Ability']
    assert {f'wait-{i}' for i in range(1,6)} <= names['Ability']
    for f in range(5):
        assert f'grow-{f}' in names['Actor']
        assert f'portal-{f}' in names['Actor']
    for kind,total in [(0,5),(1,1),(2,3)]:
        for h in range(total+1): assert f'hp-{kind}-{h}' in names['Health']
    for kind in range(4):
        for f in range(2): assert f'pickup-{kind}-{f}' in names['Actor']
        assert f'picked-{kind}' in names['Buff']
    for f in range(2):
        for prefix in ['missile','fire-missile','fire-seed']: assert f'{prefix}-{f}' in names['Actor']
    for f in range(8): assert f'cherry-burst-{f}' in names['Actor']
    for seconds in range(1,9):
        assert f'speed-{seconds}' in names['Buff']
        assert f'pepper-{seconds}' in names['Buff']
    for charges in range(1,4):
        for seconds in range(1,11): assert f'shield-{charges}-{seconds}' in names['Buff']
    for name in ['dash-warning','dash-trail','fire-trail','nut-shield','pepper-aura','speed-wake','upgrade','weapon-ready']:
        assert name in names['Atmosphere']
    labels=0
    for path in paths:
        if path.endswith('.svg'):
            doc=ET.fromstring(archive.read(path))
            assert not list(doc.iter('{http://www.w3.org/2000/svg}text')), path
            labels+=sum(bool(n.get('aria-label')) for n in doc.iter())
    assert labels>=25
    assert 'REAMD.md' in paths and 'README.md' in paths
    for name in ['GAMEPLAY.md','ARCHITECTURE.md','DEVELOPMENT.md','CHANGELOG.md']:
        assert f'docs/{name}' in paths
    for name,frames in [('boss-poses.gif',28),('boss-warnings.gif',50)]:
        with Image.open(BytesIO(archive.read(f'docs/media/{name}'))) as animation:
            assert animation.is_animated and animation.n_frames==frames
    for name in ['boss-detail.png','level-select.png','coop-garden.png','four-bosses.png']:
        assert f'docs/media/{name}' in paths
    assert 'tools/boss_art.py' in paths and 'tools/campaign_art.py' in paths
    assert '双人' in archive.read('REAMD.md').decode('utf-8')
    assert {f'boss-{n}' for n in range(4)} <= names['Actor']
    for theme in range(4):
        for pose, frames in [('idle',4),('cast',2),('hit',1),('rage',4)]:
            for frame in range(frames):
                name=f'boss-{theme}-{pose}-{frame}'
                assert name in names['Actor']
                costume=next(c for c in json.loads(archive.read('assets/sprites/Actor/index.json'))['costumes'] if c['name']==name)
                assert (costume['imageWidth'],costume['imageHeight'],costume['x'],costume['y'])==(72,76,36,38)
    assert {f'menu-{m}-{n}' for m in [1,2] for n in range(1,21)} <= names['Notice']
    assert {f'scene-{n}' for n in range(1,21)} == names['Scene']
    assert {f'evolution-{n}' for n in range(6)} <= names['Notice']
    assert {f'savepanel-{mode}-{n}' for mode in [1,2] for n in range(21)} <= names['Notice']
    for folder in ['Frame','Notice','Campaign','Wallet','Atmosphere','Buff','Ability','StageCard','UIAction']:
        data=json.loads(archive.read(f'assets/sprites/{folder}/index.json'))
        for costume in data['costumes']:
            doc=ET.fromstring(archive.read(f"assets/sprites/{folder}/{costume['path']}"))
            text_labels=[node.get('aria-label','') for node in doc.iter()]
            if costume['name'].endswith('-en'):
                assert not any(re.search(r'[\u4e00-\u9fff]',label) for label in text_labels),costume['name']
            elif any(re.search(r'[\u4e00-\u9fff]',label) for label in text_labels):
                assert costume['name']+'-en' in names[folder],(folder,costume['name'])
    for tier in range(1,6):
        for player in [1,2]:
            for direction in ['up','right','down','left']:
                assert {f'evo-{tier}-p{player}-{direction}-{frame}' for frame in range(6)} <= names['Actor']
        for prefix,total in [('seed',2),('missile',2),('fire-seed',2),('fire-missile',2),('mega',4),('burst',10)]:
            assert {f'evo-{tier}-{prefix}-{n}' for n in range(total)} <= names['Actor']
        assert {f'evo-{tier}-{name}' for name in ['seed-trail','missile-trail','mega-trail','fire-trail']} <= names['Atmosphere']
    assert {f'coin-{n}' for n in range(10)} <= names['Wallet']
    assert {f'save-{n}' for n in range(4)} <= names['Wallet']
    for kind in range(4):
        for phase in ['warn','active']:
            assert {f'zone-{kind}-{phase}-{n}' for n in [0,1]} <= names['Actor']
        assert f'warning-{kind}' in names['Campaign']
        assert {f'boss-{kind}-{n}' for n in range(11)} <= names['Campaign']
    catalog=json.loads(archive.read('data/level-catalog.json'))
    assert len(catalog)==20 and len({tuple(s['rows']) for s in catalog})==20
    assert [s['level'] for s in catalog if s['boss']]==[5,10,15,20]
    for stage in catalog:
        assert {f"stage-{stage['level']}-{k}" for k in range(stage['target']+1)} <= names['Campaign']
    for direction in ['up','right','down','left']:
        assert {f'partner-{direction}-{n}' for n in range(6)} <= names['Actor']
    assert {'clear','win','lose','pause'} <= names['Notice']
    assert '击退10只' not in archive.read('builder-meta.json').decode('utf-8')
    for role in range(3):
        signatures=set()
        for tier in range(6):
            for player in [1,2]:
                for direction in ['up','right','down','left']:
                    assert {f'hero-{role}-{tier}-p{player}-{direction}-{f}' for f in range(6)} <= names['Actor']
            signatures.add(archive.read(f'assets/sprites/Actor/hero-{role}-{tier}-p1-right-0.svg'))
            assert {f'role-shot-{role}-{tier}-{f}' for f in range(2)} <= names['Actor']
            for suffix in ['', '-en']:
                assert f'class-lab-{role}-{tier}{suffix}' in names['Notice']
                assert {f'class-{role}-{tier}-{bits}{suffix}' for bits in range(4)} <= names['UIAction']
        assert len(signatures)==6
    assert {f'brain-open-{f}' for f in range(4)} <= names['Actor']
    assert {f'brain-barrier-{n}-{f}' for n in range(1,11) for f in range(4)} <= names['Actor']
    assert {f'brain-barrier-{n}-{f}' for n in range(1,11) for f in range(4)} <= names['Brain']
    assert 'docs/media/brain-barrier.png' in paths and 'tools/brain_art.py' in paths
    for suffix in ['', '-en']:
        assert {'home'+suffix,'class-select'+suffix,'settings'+suffix} <= names['Notice']
        assert {f'stage-{n}-{status}{suffix}' for n in range(1,21) for status in range(5)} <= names['StageCard']
        assert {f'home-{n}-{status}{suffix}' for n in range(4) for status in [0,1]} <= names['UIAction']
    for name in ['animated-home.gif','profession-evolution.gif','profession-routes.png','class-select.png']:
        assert f'docs/media/{name}' in paths
    print(f'Checked {len(paths)} resources: 20 maps, 40 menus, 4 bosses, 4 warning/active zone types, all stage HUDs, and {labels} outlined labels.')
