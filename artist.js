// Add the artist's actual information here. Keep fields empty until confirmed.
const artistConfig = {
  name: '',
  shopUrl: '',
  // Up to three original artwork photos: { src: 'artworks/work-1.jpg', alt: 'Work title' }
  artworks: []
};
function validShopUrl(value){try{const url=new URL(value);return ['https:','http:'].includes(url.protocol)?url.href:null}catch{return null}}
function setupArtist(){
 const link=document.getElementById('artistShop'),credit=document.getElementById('artistCredit'),gallery=document.getElementById('artistGallery'),pending=document.getElementById('artistPending');
 const url=validShopUrl(artistConfig.shopUrl);link.hidden=!url;if(url)link.href=url;
 credit.hidden=!artistConfig.name;credit.textContent=artistConfig.name?t('artistCredit',{artist:artistConfig.name}):'';
 gallery.replaceChildren();
 for(const work of artistConfig.artworks.slice(0,3)){
  if(!work.src)continue;
  let parsed;try{parsed=new URL(work.src,location.href)}catch{continue}if(!['http:','https:','file:'].includes(parsed.protocol))continue;
  const img=document.createElement('img');img.src=parsed.href;img.alt=work.alt||t('artistCredit',{artist:artistConfig.name||t('brand')});img.loading='lazy';img.onerror=()=>{img.remove();gallery.hidden=!gallery.children.length;pending.hidden=!!url};gallery.append(img);
 }
 gallery.hidden=!gallery.children.length;pending.hidden=!!url;
}
document.addEventListener('DOMContentLoaded',setupArtist);
document.addEventListener('line-art-language-change',setupArtist);
