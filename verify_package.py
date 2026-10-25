from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile
import json
from PIL import Image
from io import BytesIO

root=Path(__file__).resolve().parent
with ZipFile(root.parent/'暮光花园-双人闯关版.xbp') as archive:
    assert archive.testzip() is None
    paths=set(archive.namelist())
    config=json.loads(archive.read('assets/index.json'))
    assert config['zorder']==['Scene','Atmosphere','Actor','Health','Frame','Hud','Ability','Buff','Campaign','Notice']
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
    assert 'README.md' in paths
    assert '双人' in archive.read('README.md').decode('utf-8')
    assert 'boss' in names['Actor']
    assert {f'menu-{m}-{n}' for m in [1,2] for n in [1,2,3]} <= names['Notice']
    assert {f'scene-{n}' for n in [1,2,3]} == names['Scene']
    for direction in ['up','right','down','left']:
        assert {f'partner-{direction}-{n}' for n in range(6)} <= names['Actor']
    assert {'clear','win','lose','pause'} <= names['Notice']
    assert '击退10只' not in archive.read('builder-meta.json').decode('utf-8')
    print(f'Checked {len(paths)} resources: three zombie models, HP, dash/growth, missiles, four pickups, all timers, docs, and {labels} outlined labels.')
