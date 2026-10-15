from pathlib import Path
from urllib.parse import urlsplit,unquote,urljoin
from bs4 import BeautifulSoup
import json,os,shutil,subprocess,tempfile,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
def check(root,origin=None):
 routes=json.loads((root/'seo-routes.json').read_text());titles=set();descs=set()
 for route in routes['routes']:
  file=root/route/'index.html';s=BeautifulSoup(file.read_text(),'html.parser')
  assert len(s.select('h1'))==1,route
  title=s.title.get_text();desc=s.find('meta',attrs={'name':'description'})['content'];assert title not in titles and desc not in descs,route;titles.add(title);descs.add(desc)
  assert len(s.get_text(' ',strip=True))>500,route
  for script in s.select('script[type="application/ld+json"]'):json.loads(script.string)
  for el in s.select('[src],link[href],a[href]'):
   value=el.get('src',el.get('href',''));v=urlsplit(value)
   if v.scheme or v.netloc:continue
   dest=(file.parent/unquote(v.path)).resolve() if v.path else file
   if dest.is_dir():dest=dest/'index.html'
   assert dest.exists(),(route,value,dest)
   if v.fragment and dest.suffix=='.html':
    other=BeautifulSoup(dest.read_text(),'html.parser');assert other.find(id=v.fragment),(route,value)
  if route=='photo-to-cross-hatching/':assert s.html['data-tool-style']=='cross' and s.select_one('#art')
  if route=='minimalist-line-art/':assert s.html['data-tool-mode']=='minimal' and s.select_one('#art')
  if origin:
   expected=origin+'/'+route;assert s.select_one('link[rel="canonical"]')['href']==expected
   if route in routes['locales'].values():
    alternates={a['hreflang']:a['href'] for a in s.select('link[hreflang]')};assert len(alternates)==7
    for lang,path in routes['locales'].items():assert alternates[lang]==origin+'/'+path
  else:assert not s.select('link[rel="canonical"]')
 if origin:
  xml=ET.parse(root/'sitemap.xml');locs={el.text for el in xml.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')};assert locs=={origin+'/'+p for p in routes['routes']};assert 'Sitemap: '+origin+'/sitemap.xml' in (root/'robots.txt').read_text()
 print(len(routes['routes']),'static pages verified',origin or '(domain unconfigured)')
check(ROOT)
with tempfile.TemporaryDirectory() as temp:
 copy=Path(temp)/'site';shutil.copytree(ROOT,copy,ignore=shutil.ignore_patterns('.git','.venv','__pycache__'))
 origin='https://seo-test.invalid/photo-tool';subprocess.run([os.sys.executable,str(copy/'tools/build-seo.py')],env={**os.environ,'SITE_URL':origin},check=True,stdout=subprocess.DEVNULL);check(copy,origin)
print('SEO checks passed, including a production-style subdirectory build.')
