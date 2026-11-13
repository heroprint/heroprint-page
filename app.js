const reduceMotion=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if(window.gsap&&window.ScrollTrigger&&!reduceMotion){
 gsap.registerPlugin(ScrollTrigger);
 gsap.to('.hero-bg',{scale:1.18,yPercent:8,ease:'none',scrollTrigger:{trigger:'.hero',start:'top top',end:'bottom top',scrub:true}});
 const stages=gsap.utils.toArray('.stage');
 const show=i=>{stages.forEach((s,j)=>{s.inert=i!==j;s.setAttribute('aria-hidden',String(i!==j));s.classList.toggle('active',i===j);gsap.to(s,{opacity:i===j?1:0,y:i===j?0:(j<i?-30:30),duration:.4,overwrite:true})});gsap.to('.orb',{rotate:i*55,scale:1+i*.04,duration:.65,overwrite:true})};
 show(0);
 stages.forEach((el,i)=>ScrollTrigger.create({trigger:'.story',start:()=>`top+=${i*window.innerHeight} top`,end:()=>`top+=${(i+1)*window.innerHeight} top`,onEnter:()=>show(i),onEnterBack:()=>show(i)}));
 gsap.utils.toArray('.split img,.materials img,.portfolio-card').forEach(el=>gsap.from(el,{y:55,opacity:0,duration:.85,scrollTrigger:{trigger:el,start:'top 88%'}}));
}
const form=document.querySelector('#projectForm');
if(form)form.addEventListener('submit',e=>{e.preventDefault();const note=document.querySelector('#formNote');if(note)note.textContent='Deine Angaben sind vollständig. Der echte Versand wird im nächsten Schritt an E-Mail oder ein Formular-Backend angebunden.';});

const menuToggle=document.querySelector('.menu-toggle');
const mainNav=document.querySelector('#mainNav');
if (menuToggle && mainNav) {
 const mobileMenu = window.matchMedia('(max-width: 760px)');
 const background = document.querySelectorAll('main, footer, .mobile-cta, .skip-link, .nav > .brand, .nav > .pill');
 const previousInert = new Map();
 const isOpen = () => menuToggle.getAttribute('aria-expanded') === 'true';
 const closeMenu = (restoreFocus = false) => {
  menuToggle.setAttribute('aria-expanded', 'false');
  menuToggle.setAttribute('aria-label', 'Menü öffnen');
  mainNav.classList.remove('open');
  document.body.classList.remove('menu-open');
  previousInert.forEach((inert, element) => { element.inert = inert; });
  previousInert.clear();
  if (restoreFocus) menuToggle.focus();
 };
 menuToggle.addEventListener('click', () => {
  if (isOpen()) { closeMenu(true); return; }
  if (!mobileMenu.matches) return;
  background.forEach(element => { previousInert.set(element, element.inert); element.inert = true; });
  menuToggle.setAttribute('aria-expanded', 'true');
  menuToggle.setAttribute('aria-label', 'Menü schließen');
  mainNav.classList.add('open');
  document.body.classList.add('menu-open');
  mainNav.querySelector('a').focus();
 });
 mainNav.querySelectorAll('a').forEach(a => a.addEventListener('click', () => closeMenu()));
 document.addEventListener('keydown', event => {
  if (!isOpen()) return;
  if (event.key === 'Escape') { closeMenu(true); return; }
  if (event.key !== 'Tab') return;
  const items = [menuToggle, ...mainNav.querySelectorAll('a')];
  const index = items.indexOf(document.activeElement);
  const next = (index + (event.shiftKey ? -1 : 1) + items.length) % items.length;
  event.preventDefault();
  items[next].focus();
 });
 mobileMenu.addEventListener('change', () => { if (!mobileMenu.matches) closeMenu(); });
}
