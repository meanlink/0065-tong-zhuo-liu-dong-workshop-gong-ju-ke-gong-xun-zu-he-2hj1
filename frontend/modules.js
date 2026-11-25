import {h} from './base.js'
import {heading} from './view.js'
import {tutor} from './workshop_terms.js'
import {lessons} from './lesson_catalog.js'
export async function render(root) {
 const rows=await lessons()
 root.innerHTML=heading('教具与课程','每项共训课程有固定时长、教具套数和带教老师。')+`<div class="tool-tabs">${rows.map(r=>`<article class="tool-card"><div><small>${h(r.code)}</small><h2>${h(r.title)}</h2><p>${h(r.kit)} · ${h(tutor[r.tutor_key])}</p></div>
 <dl><div><dt>分钟</dt><dd>${r.minutes}</dd></div><div><dt>套件</dt><dd>${r.units}</dd></div><div><dt>学员凭证</dt><dd>${r.valid}</dd></div></dl></article>`).join('')}</div>`
}
