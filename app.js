const reduceMotion=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if(window.gsap&&window.ScrollTrigger&&!reduceMotion){
 gsap.registerPlugin(ScrollTrigger);
 gsap.to('.hero-bg',{scale:1.18,yPercent:8,ease:'none',scrollTrigger:{trigger:'.hero',start:'top top',end:'bottom top',scrub:true}});
 const stages=gsap.utils.toArray('.stage');
 const show=i=>{stages.forEach((s,j)=>{s.classList.toggle('active',i===j);gsap.to(s,{opacity:i===j?1:0,y:i===j?0:(j<i?-30:30),duration:.4,overwrite:true})});gsap.to('.orb',{rotate:i*55,scale:1+i*.04,duration:.65,overwrite:true})};
 stages.forEach((el,i)=>ScrollTrigger.create({trigger:'.story',start:()=>`top+=${i*window.innerHeight} top`,end:()=>`top+=${(i+1)*window.innerHeight} top`,onEnter:()=>show(i),onEnterBack:()=>show(i)}));
 gsap.utils.toArray('.split img,.materials img,.portfolio-card').forEach(el=>gsap.from(el,{y:55,opacity:0,duration:.85,scrollTrigger:{trigger:el,start:'top 88%'}}));
}
const form=document.querySelector('#projectForm');
if(form)form.addEventListener('submit',e=>{e.preventDefault();const note=document.querySelector('#formNote');if(note)note.textContent='Deine Angaben sind vollständig. Der echte Versand wird im nächsten Schritt an E-Mail oder ein Formular-Backend angebunden.';});
