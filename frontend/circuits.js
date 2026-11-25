import {h,badge} from './base.js'
import {heading,choices,feedback} from './view.js'
import {wire} from './forms.js'
import {stops,sign} from './itinerary_store.js'
import {groups} from './pairing_store.js'
import {lessons} from './lesson_catalog.js'
import {chips} from './lesson_badges.js'
import {tutor} from './workshop_terms.js'
export async function render(root,session){
 const [rows,combinations,modules]=await Promise.all([stops(),groups(),lessons()])
 root.innerHTML=heading('外出教案','驻点日程固定。审签前确认教具、课程总时长和带教老师。')+`<ol class="itinerary">${rows.map(r=>`<li><time>${h(r.workshop_on)}</time><section><h2>${h(r.site)}</h2><p>${r.duration} 分钟 · ${r.kits} 套 · ${h(r.tutors.map(x=>tutor[x]).join('、'))}</p>
 ${r.lessons?`${badge('教案已发','approved')}${chips(r.lessons,modules)}<p>${r.expected_minutes} 分钟 / ${r.expected_kits} 套 · ${h(r.notes)}</p>`:
 session.role==='reviewer'?`<form class="compact-form"><input name="code" type="hidden" value="${h(r.code)}"><label>共训组合<select name="group" required><option value="">选择组合</option>${choices(combinations,x=>x.members.join(' + '),x=>x.group_key)}</select></label><label>教案备注<input name="notes" required minlength="4"></label><button>签发驻点教案</button>${feedback}</form>`:badge('待签')}</section></li>`).join('')}</ol>`
 for(const form of root.querySelectorAll('form')) wire(form,sign,()=>render(root,session))
}
