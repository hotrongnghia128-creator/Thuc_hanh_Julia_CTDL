(function () {
  'use strict';
  const mount = document.getElementById('lab-animation');
  const data = window.LabFrames;
  if (!mount || !data || !data.modes) return;
  const names = ['sort', 'bfs', 'dp', 'service'];
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  const state = { mode: 'sort', step: 0, playing: false, frame: null };
  let timer = null;
  const esc = value => String(value).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const fmt = xs => xs.length ? '[' + xs.join(', ') + ']' : '[]';
  mount.innerHTML = `<section class="lab-anim" aria-label="Minh họa từng bước thuật toán" tabindex="0">
    <header class="lab-anim-header"><div><p class="lab-anim-eyebrow">Cùng một ứng dụng giao đơn</p><h3 id="lab-anim-title"></h3><p id="lab-anim-subtitle"></p></div>
      <label class="lab-mode-label">Nội dung minh họa<select id="lab-anim-mode" aria-label="Chọn thuật toán minh họa">${names.map(k => `<option value="${k}">${esc(data.modes[k].title)}</option>`).join('')}</select></label></header>
    <ol class="lab-story-path" aria-label="Luồng ứng dụng"><li data-story="sort">1. Sắp xếp đơn</li><li data-story="bfs">2. Tính thời gian</li><li data-story="dp">3. Chọn kế hoạch</li><li data-story="service">4. Giao và hoàn tác</li></ol>
    <div class="lab-controls" role="group" aria-label="Điều khiển minh họa">
      <button type="button" id="lab-anim-first" aria-label="Về bước đầu">Về đầu</button><button type="button" id="lab-anim-prev" aria-label="Xem bước trước">← Trước</button>
      <button type="button" id="lab-anim-play" aria-label="Tự động chuyển từng bước" aria-pressed="false">Tự chạy</button>
      <button type="button" id="lab-anim-next" aria-label="Xem bước tiếp theo">Tiếp →</button><button type="button" id="lab-anim-last" aria-label="Đến bước cuối">Kết quả</button>
      <output id="lab-anim-counter" aria-label="Vị trí bước hiện tại"></output>
    </div>
    <label class="lab-step-label">Chọn bước <input id="lab-anim-slider" type="range" min="0" value="0" aria-label="Chọn bước minh họa"></label>
    <p class="lab-anim-caption" id="lab-anim-caption" aria-live="polite" aria-atomic="true"></p>
    <div id="lab-anim-scene"></div>
    <p class="lab-anim-question" id="lab-anim-question"></p>
    <p class="lab-anim-help">Dùng nút Trước/Tiếp hoặc thanh bước. Khi vùng minh họa được chọn: phím ←/→ chuyển bước; Home/End tới đầu/cuối. Dữ liệu và trạng thái được dựng từ từng bước thực của thuật toán.</p>
    <p class="lab-motion-note" id="lab-motion-note" hidden>Tùy chọn giảm chuyển động đang bật; hãy dùng điều khiển từng bước.</p>
  </section>`;
  const root = mount.querySelector('.lab-anim');
  const el = id => document.getElementById('lab-anim-' + id);
  function boxes(values, focus, emptyText = 'Rỗng', label = 'Đơn') {
    if (!values.length) return `<span class="lab-empty">${esc(emptyText)}</span>`;
    return values.map((v, i) => `<span class="lab-token ${focus.includes(v) ? 'lab-token-focus' : ''}" aria-label="${label} ${v}${focus.includes(v) ? ', đang xét' : ''}"><small>${label}</small><strong>${esc(v)}</strong>${focus.includes(v) ? '<em>Đang xét</em>' : ''}</span>${i < values.length - 1 ? '<span class="lab-array-divider" aria-hidden="true">·</span>' : ''}`).join('');
  }
  function sortScene(f) {
    return `<div class="lab-sort-scene"><div class="lab-array-strip"><h4>Đoạn đang xét</h4><div class="lab-token-line">${boxes(f.array, f.focus)}</div></div>
      <div class="lab-sort-halves"><div class="lab-array-strip"><h4>Nửa trái chưa ghép</h4><div class="lab-token-line">${boxes(f.left, f.kind === 'compare' ? f.focus : [])}</div></div><div class="lab-array-strip"><h4>Nửa phải chưa ghép</h4><div class="lab-token-line">${boxes(f.right, f.kind === 'compare' ? f.focus : [])}</div></div></div>
      <div class="lab-array-strip lab-result-strip"><h4>Kết quả ghép hiện tại</h4><div class="lab-token-line">${boxes(f.output, f.kind === 'take' || f.kind === 'remainder' ? f.focus : [])}</div></div>
      <p class="lab-anim-rule">Quy tắc ghép: so sánh hai phần tử đầu còn lại; lấy phần tử nhỏ hơn. Khi một nửa hết, chép phần còn lại. Mỗi lần ghép duy trì thứ tự tăng dần.</p></div>`;
  }
  const positions = { 1: [75, 150], 2: [235, 55], 3: [235, 245], 4: [410, 55], 5: [410, 245], 6: [575, 150] };
  function graph(f) {
    const edges = data.edges.map(([u,v]) => {
      const [x1,y1] = positions[u], [x2,y2] = positions[v];
      const considered = f.edge && ((f.edge[0] === u && f.edge[1] === v) || (f.edge[0] === v && f.edge[1] === u));
      const tree = f.parent[u-1] === v || f.parent[v-1] === u;
      return `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" class="lab-edge ${tree ? 'lab-edge-tree' : ''} ${considered ? 'lab-edge-active' : ''}"/>`;
    }).join('');
    const nodes = Object.keys(positions).map(x => {
      const u = Number(x), [cx,cy] = positions[u], status = f.active === u ? 'Đang xét' : f.queue.includes(u) ? 'Trong Q' : f.visited.includes(u) ? 'Đã thăm' : 'Chưa thăm';
      const klass = f.active === u ? 'lab-node-active' : f.queue.includes(u) ? 'lab-node-queued' : f.visited.includes(u) ? 'lab-node-visited' : '';
      return `<g class="lab-node ${klass}"><circle cx="${cx}" cy="${cy}" r="24"/><text x="${cx}" y="${cy+7}" class="lab-node-id">${u}</text><text x="${cx}" y="${cy+45}" class="lab-node-status">${status}</text><text x="${cx}" y="${cy-36}" class="lab-node-distance">d = ${f.dist[u-1] < 0 ? '∞' : f.dist[u-1]}</text></g>`;
    }).join('');
    return `<svg class="lab-graph" viewBox="0 0 650 315" role="img" aria-labelledby="lab-graph-title lab-graph-desc"><title id="lab-graph-title">Bản đồ sáu điểm; BFS xuất phát từ điểm 1</title><desc id="lab-graph-desc">${esc(f.caption)} Hàng đợi ${fmt(f.queue)}. Khoảng cách ${f.dist.map(x=>x<0?'chưa biết':x).join(', ')}.</desc>${edges}${nodes}</svg>`;
  }
  function bfsScene(f) {
    return `<div class="lab-bfs-layout"><div>${graph(f)}<p class="lab-graph-legend"><span class="lab-legend-line">━━</span> Cạnh cây BFS; <span class="lab-legend-dash">┄┄</span> cạnh đang xét. Mỗi cạnh có thời gian 1.</p></div><div class="lab-state-panel"><h4>Hàng đợi Q — đầu ở bên trái</h4><div class="lab-token-line">${boxes(f.queue, f.active === null ? [] : [f.active], 'Q rỗng', 'Đỉnh')}</div><h4>Đỉnh đang xét</h4><p class="lab-state-value">${f.active === null ? 'Không có' : f.active}</p><h4>Thứ tự phát hiện</h4><p>${fmt(f.visited)}</p></div></div>
      <div class="lab-table-scroll"><table class="lab-state-table"><caption>Trạng thái theo đỉnh — khoảng cách là số cạnh ít nhất từ điểm 1</caption><thead><tr><th scope="col">Đỉnh</th>${[1,2,3,4,5,6].map(u=>`<th scope="col">${u}</th>`).join('')}</tr></thead><tbody><tr><th scope="row">Khoảng cách d</th>${f.dist.map(x=>`<td>${x<0?'∞':x}</td>`).join('')}</tr><tr><th scope="row">Cha</th>${f.parent.map(x=>`<td>${x || '∅'}</td>`).join('')}</tr></tbody></table></div>
      <p class="lab-anim-rule">Chi phí mỗi đơn = 2 × khoảng cách tới điểm giao + thời gian phục vụ. Điểm 2/4/6 cho A/B/C nên chi phí cuối là 3/5/7. Chi phí này là đầu vào của bước chọn kế hoạch.</p>`;
  }
  function dpScene(f) {
    const labels = ['0 — chưa xét đơn','1 — A (t=3, v=6)','2 — B (t=5, v=8)','3 — C (t=7, v=10)'];
    return `<p class="lab-dp-formula">F[i,b] = max(F[i−1,b], lợi_ích[i] + F[i−1,b−chi_phí[i]]) khi đủ thời gian; nếu không đủ, giữ F[i−1,b].</p>
      <div class="lab-table-scroll" tabindex="0" aria-label="Bảng quy hoạch động; cuộn ngang nếu cần"><table class="lab-dp-table"><caption>Bảng F — cột là giới hạn thời gian b từ 0 đến 8</caption><thead><tr><th scope="col">i — đơn vừa xét</th>${Array.from({length:9},(_,b)=>`<th scope="col">${b}</th>`).join('')}</tr></thead><tbody>${f.table.map((row,i)=>`<tr><th scope="row">${labels[i]}</th>${row.map((v,b)=>{
        const current=f.cell[0]===i&&f.cell[1]===b, source=f.sources.some(c=>c[0]===i&&c[1]===b);
        return `<td class="${current?'lab-cell-current':source?'lab-cell-source':''}" aria-label="F[${i},${b}] ${v===null?'chưa tính':v}${current?', ô đang xét':source?', ô nguồn':''}">${current?'<span class="lab-cell-mark">● </span>':source?'<span class="lab-cell-mark">◇ </span>':''}${v===null?'·':v}</td>`;
      }).join('')}</tr>`).join('')}</tbody></table></div>
      <p class="lab-dp-legend"><strong>●</strong> ô đang xét; <strong>◇</strong> ô nguồn ở hàng trước; <strong>·</strong> chưa tính. Chỉ số trong bảng là ký hiệu toán học từ 0; khi cài đặt Julia, dùng vị trí mảng từ 1.</p>
      <div class="lab-dp-result"><span>Đơn đã truy vết: <strong>${fmt(f.selected)}</strong></span><span>Giá trị F[3,8]: <strong>${f.table[3][8]===null?'Chưa tính':f.table[3][8]}</strong></span>${f.remaining!==undefined?`<span>Thời gian còn khi truy vết: <strong>${f.remaining}</strong></span>`:''}</div>
      <p class="lab-anim-rule">Lấy giá trị từ hàng i−1 bảo đảm đơn i không được chọn lại. Bảng cần O(nB) phép tính; BFS quyết định chi phí nên thay bản đồ có thể thay kế hoạch.</p>`;
  }
  function serviceScene(f) {
    return `<div class="lab-service-layout"><div class="lab-state-panel"><h4>Hàng đợi chờ giao — FIFO</h4><p class="lab-end-label">Đầu Q → cuối Q</p><div class="lab-token-line">${boxes(f.queue, f.kind==='undo'?[1]:[], 'Không còn đơn chờ')}</div></div><div class="lab-state-panel"><h4>Ngăn xếp lịch sử — LIFO</h4><p class="lab-end-label">Đáy → đỉnh (bên phải)</p><div class="lab-token-line">${boxes(f.completed, f.action===null?[]:[f.action], 'Chưa giao đơn nào')}</div></div></div>
      <div class="lab-metrics"><div><span>Thời gian đã dùng</span><strong>${f.spent} / ${data.budget}</strong></div><div><span>Lợi ích đã nhận</span><strong>${f.earned}</strong></div><div><span>Số đơn đã giao</span><strong>${f.completed.length} / 2</strong></div></div>
      <div class="lab-table-scroll"><table class="lab-state-table"><caption>Trạng thái đơn trong cùng phiên làm việc</caption><thead><tr><th scope="col">Đơn</th><th scope="col">Chi phí</th><th scope="col">Lợi ích</th><th scope="col">Trạng thái xuất CSV</th></tr></thead><tbody>${data.orders.map(o=>`<tr><th scope="row">${o.name} — ${o.id}</th><td>${o.cost}</td><td>${o.benefit}</td><td>${f.completed.includes(o.id)?'Đã giao':f.queue.includes(o.id)?'Chờ giao':'Không chọn'}</td></tr>`).join('')}</tbody></table></div>
      <p class="lab-anim-rule">Bất biến: mỗi đơn được chọn xuất hiện đúng một lần trong Q hoặc lịch sử. Tổng đã dùng bằng tổng chi phí của các đơn đã giao; tổng lợi ích bằng tổng lợi ích các đơn đã giao. Hoàn tác trả lại đúng trạng thái trước thao tác.</p>`;
  }
  function render() {
    const mode=data.modes[state.mode], f=mode.frames[state.step]; state.frame=f;
    el('title').textContent=mode.title; el('subtitle').textContent=mode.subtitle;
    el('caption').textContent=f.caption; el('question').textContent='Câu hỏi quan sát: '+mode.question;
    el('counter').textContent=`Bước ${state.step+1} / ${mode.frames.length}`;
    el('slider').max=mode.frames.length-1;el('slider').value=state.step;
    el('slider').setAttribute('aria-valuetext',`Bước ${state.step+1}: ${f.caption}`);
    el('prev').disabled=el('first').disabled=state.step===0;
    el('next').disabled=el('last').disabled=state.step===mode.frames.length-1;
    mount.querySelectorAll('[data-story]').forEach(n=>{n.classList.toggle('lab-story-active',n.dataset.story===state.mode);if(n.dataset.story===state.mode)n.setAttribute('aria-current','step');else n.removeAttribute('aria-current');});
    el('scene').innerHTML=({sort:sortScene,bfs:bfsScene,dp:dpScene,service:serviceScene})[state.mode](f);
    root.dataset.mode=state.mode;root.dataset.step=state.step;root.dataset.kind=f.kind;
  }
  function stop() {
    if(timer!==null)window.clearInterval(timer);timer=null;state.playing=false;
    el('play').textContent='Tự chạy';el('play').setAttribute('aria-pressed','false');
  }
  function setStep(value, retainPlayback=false) {
    if(!retainPlayback)stop();state.step=Math.max(0,Math.min(data.modes[state.mode].frames.length-1,Math.trunc(Number(value)||0)));render();
    if(state.step===data.modes[state.mode].frames.length-1)stop();
  }
  function selectMode(mode) {
    if(!names.includes(mode))throw new Error('Nội dung minh họa không hợp lệ');
    stop();state.mode=mode;state.step=0;el('mode').value=mode;render();
  }
  function play() {
    if(state.playing){stop();return;}if(reduced.matches)return;
    if(state.step===data.modes[state.mode].frames.length-1)setStep(0);
    state.playing=true;el('play').textContent='Tạm dừng';el('play').setAttribute('aria-pressed','true');
    timer=window.setInterval(()=>setStep(state.step+1,true),1200);
  }
  el('mode').addEventListener('change',e=>selectMode(e.target.value));
  el('prev').addEventListener('click',()=>setStep(state.step-1));el('next').addEventListener('click',()=>setStep(state.step+1));
  el('first').addEventListener('click',()=>setStep(0));el('last').addEventListener('click',()=>setStep(data.modes[state.mode].frames.length-1));
  el('play').addEventListener('click',play);el('slider').addEventListener('input',e=>setStep(e.target.value));
  root.addEventListener('keydown',e=>{
    if(!['ArrowLeft','ArrowRight','Home','End'].includes(e.key))return;
    e.stopPropagation();if(e.target.matches('select,input,textarea'))return;
    e.preventDefault();setStep(e.key==='Home'?0:e.key==='End'?data.modes[state.mode].frames.length-1:state.step+(e.key==='ArrowRight'?1:-1));
  });
  document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});window.addEventListener('beforeprint',stop);
  function motionPreference(){stop();el('play').disabled=reduced.matches;document.getElementById('lab-motion-note').hidden=!reduced.matches;}
  reduced.addEventListener('change',motionPreference);motionPreference();render();
  window.PracticeAnimations={state,selectMode,setStep,steps:mode=>data.modes[mode||state.mode].frames.length,stop};
})();
