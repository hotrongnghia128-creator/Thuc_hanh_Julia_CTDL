const fs=require('fs'),path=require('path'),assert=require('assert');
const {pathToFileURL}=require('url');
const {chromium}=require('C:/Users/DELL/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root=path.resolve(__dirname,'../..'),qa=path.join(__dirname,'qa');fs.mkdirSync(qa,{recursive:true});
(async()=>{
 const browser=await chromium.launch({channel:'msedge',headless:true});
 const page=await browser.newPage({viewport:{width:1366,height:900},acceptDownloads:true});
 const errors=[],external=[];page.on('pageerror',e=>errors.push(String(e)));page.on('request',r=>{if(/^https?:/.test(r.url()))external.push(r.url());});
 await page.goto(pathToFileURL(path.join(root,'Thuc_hanh_CTDL_GT_Julia_2026_10_09.html')).href);
 assert.equal(await page.locator('.quiz li').count(),5);assert.equal(await page.locator('.lesson-section').count(),14);
 assert(!await page.locator('body').innerText().then(t=>t.includes('Đáp án câu hỏi cuối buổi')));
 const pending=page.waitForEvent('download');await page.locator('#download-code').click();await (await pending).saveAs(path.join(qa,'student_download.jl'));
 assert(fs.readFileSync(path.join(qa,'student_download.jl')).equals(fs.readFileSync(path.join(root,'TH_2026_10_09_Sinh_vien.jl'))));
 const finals={};for(const mode of ['sort','bfs','dp','service']){
   finals[mode]=await page.evaluate(mode=>{PracticeAnimations.selectMode(mode);PracticeAnimations.setStep(PracticeAnimations.steps()-1);return PracticeAnimations.state;},mode);
 }
 fs.writeFileSync(path.join(qa,'animation_final_states.json'),JSON.stringify(finals));
 assert.deepEqual(finals.bfs.frame.dist,[0,1,1,2,2,3]);
 assert.equal(finals.dp.frame.optimal,14);assert.deepEqual(finals.dp.frame.selected,[1,2]);
 assert.equal(finals.service.frame.spent,8);assert.equal(finals.service.frame.earned,14);
 await page.evaluate(()=>{PracticeAnimations.selectMode('service');PracticeAnimations.setStep(2);});
 const undo=await page.evaluate(()=>PracticeAnimations.state);
 fs.writeFileSync(path.join(qa,'undo_state.json'),JSON.stringify(undo));
 assert.equal(undo.frame.spent,0);assert.equal(undo.frame.earned,0);assert.deepEqual(undo.frame.queue,[1,2]);assert.deepEqual(undo.frame.completed,[]);
 await page.locator('#projection').click();await page.keyboard.press('ArrowRight');assert.equal((await page.evaluate(()=>PracticeLesson.state())).index,1);await page.keyboard.press('Escape');assert(!(await page.evaluate(()=>PracticeLesson.state())).active);
 for(const width of [390,900,1366]){
  await page.setViewportSize({width,height:900});
  for(const mode of ['sort','bfs','dp','service']){await page.evaluate(mode=>PracticeAnimations.selectMode(mode),mode);assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'page overflow '+width+mode);}
 }
 await page.setViewportSize({width:1366,height:900});await page.evaluate(()=>PracticeLesson.project(true));
 for(let i=0;i<14;i++){await page.evaluate(i=>PracticeLesson.setSlide(i),i);assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'projection overflow '+i);}
 await page.evaluate(()=>{PracticeLesson.setSlide(4);PracticeAnimations.selectMode('bfs');PracticeAnimations.setStep(10);});await page.screenshot({path:path.join(qa,'bfs_projector.png')});
 await page.evaluate(()=>{dispatchEvent(new Event('beforeprint'));dispatchEvent(new Event('beforeprint'));});
 assert(!(await page.evaluate(()=>document.body.classList.contains('projecting'))));
 await page.evaluate(()=>dispatchEvent(new Event('afterprint')));
 assert((await page.evaluate(()=>PracticeLesson.state())).active);
 assert(await page.evaluate(()=>document.body.classList.contains('projecting')));
 await page.evaluate(()=>{PracticeLesson.project(false);PracticeAnimations.selectMode('dp');PracticeAnimations.setStep(PracticeAnimations.steps()-1);});
 await page.locator('#lab-animation').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(qa,'dp.png')});
 await page.locator('#roadmap').screenshot({path:path.join(qa,'roadmap.png')});
 await page.evaluate(()=>scrollTo(0,0));await page.screenshot({path:path.join(qa,'lesson.png')});
 await page.emulateMedia({media:'print'});await page.evaluate(()=>dispatchEvent(new Event('beforeprint')));
 await page.pdf({path:path.join(root,'Thuc_hanh_CTDL_GT_Julia_2026_10_09.pdf'),preferCSSPageSize:true,printBackground:true});
 for(const [source,name] of [['worksheet_preview','Phieu_thuc_hanh_CTDL_GT_2026_10_09'],['teacher_preview','Huong_dan_giang_vien_CTDL_GT_2026_10_09']]){
  await page.goto(pathToFileURL(path.join(__dirname,source+'.html')).href);await page.pdf({path:path.join(root,name+'.pdf'),preferCSSPageSize:true,printBackground:true});
 }
 assert.deepEqual(errors,[]);assert.deepEqual(external,[]);await browser.close();
 console.log(JSON.stringify({status:'HTML_PDF_PASS',slides:14,animations:4,steps:74,downloads:1,viewports:[390,900,1366],errors,external}));
})().catch(e=>{console.error(e);process.exit(1);});
