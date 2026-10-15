#!/usr/bin/env python3
"""Generate crawlable locale pages and intent-specific tools. Set SITE_URL for production metadata."""
from pathlib import Path
from urllib.parse import urlparse
from html import escape
import json,os,re
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
config=json.loads((ROOT/'site.config.json').read_text())
SITE=os.environ.get('SITE_URL',config.get('siteUrl','')).rstrip('/')
if SITE and (urlparse(SITE).scheme not in ('https','http') or not urlparse(SITE).netloc or urlparse(SITE).query or urlparse(SITE).fragment):raise ValueError('SITE_URL must be an absolute HTTP(S) URL, optionally including a deployment subdirectory.')
raw=(ROOT/'i18n.js').read_text();translations=json.loads(raw.split('const translations=',1)[1].split(';\n',1)[0])
LOCALES={'en':'','zh-CN':'zh/','ja':'ja/','es':'es/','pt':'pt/','ko':'ko/'}
NAMES={'en':'English','zh-CN':'简体中文','ja':'日本語','es':'Español','pt':'Português','ko':'한국어'}
META={
'en':['Photo to Line Art Converter – Free Hatching & Cross-Hatching','Convert photos to line art with hatching, cross-hatching and minimalist blue-ink styles. Free online converter, local processing and watermark-free PNG downloads.'],
'zh-CN':['照片转线条画工具｜交叉排线与极简排线画','免费在线将照片转换为线条画、交叉排线画或简笔蓝墨画。支持调整密度、线宽与对比度，本地处理，无水印 PNG 下载。'],
'ja':['写真を線画に変換｜無料ハッチング・クロスハッチング','写真をハッチングやクロスハッチング、シンプルな青いインク画に変換。ブラウザ内処理、登録不要、透かしなしの PNG 保存。'],
'es':['Foto a dibujo de líneas – Tramado gratis online','Convierte fotos en arte de líneas, tramado cruzado o ilustraciones minimalistas. Procesamiento local y descarga PNG gratis, sin registro ni marca de agua.'],
'pt':['Foto para desenho de linhas – Hachura grátis online','Transforme fotos em arte de linhas, hachura cruzada ou ilustrações minimalistas. Processamento local e PNG grátis, sem cadastro nem marca-d’água.'],
'ko':['사진을 선화로 변환 | 무료 해칭·크로스해칭 도구','사진을 세밀한 해칭, 크로스해칭 또는 간결한 파란 잉크 선화로 바꿔 보세요. 브라우저 내 처리, 가입 없이 워터마크 없는 PNG 다운로드.']}
ARTICLES={
'photo-to-cross-hatching/':{'title':'Photo to Cross-Hatching Converter – Free Online','h1':'Photo to Cross-Hatching','desc':'Turn a photo into cross-hatching line art online. Layer intersecting strokes in darker areas, adjust line density and download a watermark-free PNG.','mode':'detail','style':'cross','intro':'Turn photographic shadows into intersecting ink strokes. Adjust the result beside your original and download a PNG.','sections':[
('What this cross-hatching converter does','Cross-hatching builds dark areas from two sets of intersecting lines. In this converter, the first layer follows the image’s light and dark values. A second layer appears in darker regions. That makes shaded faces, rocky slopes and dark objects read as line-based images rather than blocks of flat grey. The result is produced by a deterministic browser algorithm, not a generative AI model.'),
('Choose a photo with readable shadows','Start with a clear subject and a background that does not compete with it. A well-lit portrait, a still life or a landscape with distinct sunlit and shaded areas is a useful starting point. Tiny foliage, image noise and patterned clothing can produce dense strokes. If a photo looks crowded, reduce density or contrast before increasing line width.'),
('Adjust density before thickness','The controls change different parts of the drawing. Density changes the spacing between lines. Width changes the amount of ink in each stroke. Contrast changes which image values become more strongly shaded. Try the Classic preset first, reduce density if the drawing fills in, then adjust width to suit the size you will use. Select Cross-hatching under More settings to return to this page’s default line direction.'),
('Download and print within the image’s resolution','PNG output has a longest side of up to 2000 pixels and does not enlarge small originals. It is a raster image, not a vector or plotter path. For a print, check the pixel dimensions against the physical size you need: 2000 pixels at 300 pixels per inch is about 6.7 inches. A lower print density can support a larger print, with less fine detail.'),
('Cross-hatching is different from outline tracing','This tool describes tone with lines. It does not remove the background automatically, trace a continuous contour, or turn the picture into a closed-shape coloring page. For a sparser landscape interpretation, try the minimalist mode. The original photograph and the output remain separate so you can judge how much detail the strokes retain.')],
'links':[('minimalist-line-art/','Try minimalist line art'),('guides/hatching-vs-cross-hatching/','Compare hatching and cross-hatching')]},
'minimalist-line-art/':{'title':'Minimalist Line Art Generator – Photo to Simple Hatching','h1':'Minimalist Line Art','desc':'Create minimalist hatching art from a photo. Simplify textures, leave highlights white and draw pale blue skies with blue-ink shadows. Free PNG download.','mode':'minimal','style':'diagonal','intro':'Reduce fine texture to a few readable regions, open white highlights and simple blue-ink hatching.','sections':[
('A simpler kind of photo-to-line-art effect','The illustrative mode simplifies a photograph before drawing it. It reduces fine texture, merges small tonal patches and removes isolated ink marks. Broad shaded regions receive single lines or crossed strokes, while bright regions remain white. This is a minimalist hatching effect, rather than a single-line drawing or an automatic outline trace.'),
('Why snow mountains make a useful example','A snow-covered mountain against a clear blue sky has distinct shapes: a relatively uniform sky, white snow and dark slopes. The current algorithm looks for blue sky connected to the top of the image and draws it with pale cyan parallel lines. It uses the selected ink color for the subject’s shaded areas. Cloudy skies, blue buildings and blue shadows can confuse that color-based separation.'),
('What to keep and what to leave blank','A minimalist result does not need every crack, leaf or small contrast change. Begin with a photograph that has a strong silhouette and broad light areas. Use the side-by-side view to judge whether the main shape is still recognizable. Adjust contrast if too much of the subject disappears; lower density if the retained regions look heavy. The result is an automatic interpretation and will not make the same decisions as a human illustrator.'),
('Use the controls without losing the simple look','Keep the line width modest and change one setting at a time. Density controls the spacing within each retained region. The foreground ink and paper background can be customized. Illustrative mode uses a fixed pale cyan for detected sky; it does not reproduce all of the original photograph’s colors. White highlights are intentional empty paper, not transparency.'),
('Save the drawing for your own layout','Download a watermark-free PNG, with a longest side up to 2000 pixels. Use your own source photograph or an image you are allowed to transform. The converter does not provide an SVG, a continuous pen path or a ready-to-cut stencil. Handmade works in the artist section are separate from the images generated by this tool.')],
'links':[('photo-to-cross-hatching/','Try detailed cross-hatching'),('guides/hatching-vs-cross-hatching/','Read the technique comparison')]}}
GUIDE='guides/hatching-vs-cross-hatching/'
GUIDE_SECTIONS=[
('Hatching uses one family of lines','Parallel lines can make a picture look light or dark without filling it with grey paint. Lines that are farther apart leave more visible paper. Narrower gaps and heavier strokes add ink. The lines may be diagonal, horizontal or vertical. In a handmade drawing, their placement can also describe the subject’s form. This converter uses fixed direction choices rather than a reconstructed three-dimensional surface.'),
('Cross-hatching adds another direction','Cross-hatching places another set of strokes across the first. The overlap gives dark areas more visual weight. In the detailed mode here, extra strokes are reserved for darker regions; white highlights do not receive the same stack of lines. Start with cross-hatching when you want more visible shading or an engraving-like density, then reduce line width if the output becomes difficult to read.'),
('Minimalist hatching changes the amount of information','Minimalism is a choice about which information stays, not a third line direction. A drawing can use parallel or crossed lines and still be sparse. Our illustrative renderer smooths fine texture, groups tonal regions, leaves bright regions blank and uses pale cyan for a detected clear sky. It aims for broad shapes instead of recording every change in the source photograph.'),
('Choose a mode for the picture you have','For textured stone, a face with clear lighting or an object with strong shade, detailed cross-hatching can retain more of the photograph. For a bright snow scene or a simple high-contrast subject, illustrative hatching may produce clearer areas of white paper. The same settings will not suit every subject. Keep the original visible while trying the two renderers, and inspect the downloaded image at its actual size.'),
('Density, width and contrast are separate controls','Density changes how frequently lines appear across the picture. Width changes the thickness of each stroke. Contrast affects how strongly bright and dark source values separate. Increasing all three can cover the paper quickly. A useful sequence is to choose the mode, find a comfortable density, and only then adjust width and contrast. Keep one setting unchanged while comparing another so you can see what caused the difference.'),
('Line art does not always mean an outline','Photo-to-line-art search results cover several different products: contour extraction, a single continuous path, pencil simulations and hatching. This website focuses on hatching. It does not promise subject-aware contour tracing, a single-line portrait, editable vector paths or closed coloring-book shapes. Those tasks need different processing. Stating the distinction helps you decide whether the downloadable PNG fits your intended project.'),
('Exporting a line-based picture','The artwork is drawn on a raster canvas and downloaded as PNG. The longest side is capped at 2000 pixels, and small source images are not enlarged. A larger pixel count is useful for printing, but it does not make the file a vector. Fine lines can look different after resizing; preview the PNG at the size you will actually display or print. Uploaded photos are processed locally, without a conversion API or an account.')]

def tag(soup,name,attrs=None,text=None):
 el=soup.new_tag(name,attrs=attrs or {});
 if text is not None:el.string=text
 return el

def local_href(target,path):
 prefix='../'*len([x for x in path.strip('/').split('/') if x])
 return prefix+target if target else prefix or './'

def metadata(soup,path,lang,title,desc,kind='home'):
 soup.html['lang']=lang;soup.html['data-page-kind']=kind;soup.html['data-site-root']='../'*len([x for x in path.strip('/').split('/') if x]) or './'
 soup.title.string=title;soup.find('meta',attrs={'name':'description'})['content']=desc
 for el in soup.select('link[rel="canonical"],link[hreflang],script[type="application/ld+json"],meta[property^="og:"],meta[name^="twitter:"]'):el.decompose()
 url=SITE+'/'+path if SITE else None
 if SITE:
  soup.head.append(tag(soup,'link',{'rel':'canonical','href':url}))
  if kind=='home':
   for l,p in LOCALES.items():soup.head.append(tag(soup,'link',{'rel':'alternate','hreflang':l,'href':SITE+'/'+p}))
   soup.head.append(tag(soup,'link',{'rel':'alternate','hreflang':'x-default','href':SITE+'/'}))
 for key,value in {'og:type':'website' if kind=='home' else 'article','og:title':title,'og:description':desc,'og:site_name':'Photo to Line Art','og:locale':lang.replace('-','_')}.items():soup.head.append(tag(soup,'meta',{'property':key,'content':value}))
 for key,value in {'twitter:card':'summary','twitter:title':title,'twitter:description':desc}.items():soup.head.append(tag(soup,'meta',{'name':key,'content':value}))
 if url:soup.head.append(tag(soup,'meta',{'property':'og:url','content':url}))
 # Only facts that are implemented. No ratings, testimonials or search-result promises.
 entity={'@context':'https://schema.org','@type':'WebApplication' if kind!='guide' else 'Article','name':title,'inLanguage':lang,'description':desc}
 if kind!='guide':entity.update({'applicationCategory':'MultimediaApplication','operatingSystem':'Any','isAccessibleForFree':True,'browserRequirements':'Requires JavaScript and Canvas support'})
 if url:entity['url']=url
 script=tag(soup,'script',{'type':'application/ld+json'});script.string=json.dumps(entity,ensure_ascii=False);soup.head.append(script)
 for el in soup.select('[src],link[href]'):
  attr='src' if el.has_attr('src') else 'href';v=el[attr]
  if not v.startswith(('https:','http:','data:','#')):el[attr]=local_href(v,path)
 for a in soup.select('a[href]'):
  href=a.get('data-root-href',a['href'])
  if not href.startswith(('http:','https:','#','mailto:')):
   a['data-root-href']=href;a['href']=local_href(href,path)
 for el in soup.select('canvas'):
  names={'originalArt':'Original snow mountain photograph','art':'Generated hatching line art preview','exOriginal':'Original snow mountain photo','exDiagonal':'Detailed hatching example','exCross':'Minimalist hatching example'}
  el['role']='img';el['aria-label']=names.get(el.get('id'),'Line art preview')

def links(soup,lang,path):
 label=translations[lang].get('seoExplore','Explore line art')
 nav=tag(soup,'nav',{'class':'seo-links','aria-label':label});nav.append(tag(soup,'strong',text=label))
 for target,text in [('photo-to-cross-hatching/','Photo to cross-hatching'),('minimalist-line-art/','Minimalist line art'),(GUIDE,'Hatching vs cross-hatching')]:
  a=tag(soup,'a',{'href':local_href(target,path),'data-root-href':target,'lang':'en'},text);nav.append(a)
 soup.footer.append(nav)
 languages=tag(soup,'nav',{'class':'language-links','aria-label':'Languages'})
 for l,p in LOCALES.items():languages.append(tag(soup,'a',{'href':local_href(p,path),'hreflang':l,'lang':l,'data-root-href':p},NAMES[l]))
 soup.footer.append(languages)

def write(path,soup):
 output=ROOT/path/'index.html' if path else ROOT/'index.html';output.parent.mkdir(parents=True,exist_ok=True);output.write_text(str(soup))

for lang,path in LOCALES.items():
 soup=BeautifulSoup((ROOT/'templates/home.html').read_text(),'html.parser')
 for el in soup.select('[data-i18n]'):
  if el['data-i18n'] in translations[lang]:el.string=translations[lang][el['data-i18n']]
 soup.select_one('#imageName').string=translations[lang]['demo']
 for option in soup.select('#language option'):
  if option.get('value')==lang:option['selected']=''
  else:option.attrs.pop('selected',None)
 section=tag(soup,'section',{'class':'site-section seo-intro','id':'line-art-guide'});section.append(tag(soup,'h2',{'data-i18n':'seoHeading'},translations[lang]['seoHeading']))
 section.append(tag(soup,'p',{'data-i18n':'seoText'},translations[lang]['seoText']));soup.select_one('#examples').insert_before(section)
 links(soup,lang,path);metadata(soup,path,lang,*META[lang]);write(path,soup)

for path,data in ARTICLES.items():
 soup=BeautifulSoup((ROOT/'index.html').read_text(),'html.parser');soup.html['data-tool-mode']=data['mode'];soup.html['data-tool-style']=data['style']
 for sel in ['.seo-intro','#examples','#how','#artist','#faq']:
  el=soup.select_one(sel)
  if el:el.decompose()
 h=soup.h1;h.clear();h.string=data['h1'];soup.select_one('.intro').clear();soup.select_one('.intro').string=data['intro']
 for a in soup.header.select('nav a'):
  if a.get('href')!='#create':a['href']=a['href'] if a['href'].startswith('http') else './'+a['href']
 for heading,text in data['sections']:
  sec=tag(soup,'section',{'class':'site-section guide-copy'});sec.append(tag(soup,'h2',text=heading));sec.append(tag(soup,'p',text=text));soup.main.append(sec)
 for target,text in data['links']:
  soup.main.append(tag(soup,'a',{'class':'guide-link','href':target},text))
 # Root page links are regenerated for this path, not copied with English relative hrefs.
 for el in soup.select('footer .seo-links,footer .language-links'):el.decompose()
 links(soup,'en',path)
 # Base template assets, not already rewritten parent paths.
 metadata(soup,path,'en',data['title'],data['desc'],'tool');write(path,soup)

soup=BeautifulSoup((ROOT/'index.html').read_text(),'html.parser');soup.main.clear();soup.main['class']='guide-page';soup.main.attrs.pop('id',None)
soup.main.append(tag(soup,'h1',text='Hatching vs Cross-Hatching'))
soup.main.append(tag(soup,'p',{'class':'intro'},'Compare parallel lines, crossed strokes and minimalist hatching before choosing a photo-to-line-art style.'))
for heading,text in GUIDE_SECTIONS:
 sec=tag(soup,'section',{'class':'site-section guide-copy'});sec.append(tag(soup,'h2',text=heading));sec.append(tag(soup,'p',text=text));soup.main.append(sec)
for target,text in [('', 'Open the photo-to-line-art converter'),('photo-to-cross-hatching/','Try cross-hatching'),('minimalist-line-art/','Try minimalist hatching')]:soup.main.append(tag(soup,'a',{'class':'guide-link','href':target or './'},text))
for el in soup.select('script[src],footer .seo-links,footer .language-links'):el.decompose()
# Guide pages are fully static; expose real locale links rather than a nonfunctional selector.
soup.select_one('#language').decompose()
for a in soup.header.select('nav a'):a['href']='./'+a['href']
links(soup,'en',GUIDE);metadata(soup,GUIDE,'en','Hatching vs Cross-Hatching: Line Art Techniques Compared','Learn the differences between hatching, cross-hatching and minimalist line art. Choose a photo, tune line density and understand PNG export limits.','guide');write(GUIDE,soup)

urls=list(LOCALES.values())+list(ARTICLES)+[GUIDE]
robots='User-agent: *\nAllow: /\n'
if SITE:
 from xml.etree.ElementTree import Element,SubElement,tostring
 ns='http://www.sitemaps.org/schemas/sitemap/0.9';root=Element('urlset',xmlns=ns)
 for path in urls:SubElement(SubElement(root,'url'),'loc').text=SITE+'/'+path
 (ROOT/'sitemap.xml').write_bytes(tostring(root,encoding='utf-8',xml_declaration=True));robots+='\nSitemap: '+SITE+'/sitemap.xml\n'
else:
 (ROOT/'sitemap.xml').unlink(missing_ok=True)
 print('SITE_URL not configured: no invented canonical, hreflang or sitemap URLs emitted.')
(ROOT/'robots.txt').write_text(robots)
(ROOT/'seo-routes.json').write_text(json.dumps({'siteUrl':SITE,'routes':urls,'locales':LOCALES},indent=2))
print('Generated',len(urls),'HTML pages.')
