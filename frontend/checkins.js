import {h,badge} from './base.js'
import {heading,choices,feedback,table} from './view.js'
import {canEdit,wire} from './forms.js'
import {lessons} from './lesson_catalog.js'
import {attendance,record} from './attendance_store.js'
import {pass,checkState} from './workshop_terms.js'
export async function render(root,session) {
 const [data,modules]=await Promise.all([attendance(),lessons()])
 const mergedInto=new Map((data.merges||[]).map(m=>[m.alias,m.primary_code]))
 root.innerHTML=heading('签到与回收','只把有效教育卡、已收回观察单的签收纳入共训分组。')+`<div class="attendance-wall">
 <section><ul class="pupil-line">${data.pupils.map(p=>`<li><b>${h(p.code)}</b> <small>${h(p.cohort)} · ${h(pass[p.pass])}</small>${mergedInto.has(p.code)?` ${badge('已合入 '+mergedInto.get(p.code),'closed')}`:''}</li>`).join('')}</ul>${table(['教育卡','课程','日期','观察单'],data.attendance.map(r=>[r.pupil,r.lesson,r.seen,checkState[r.checked]]))}</section>
 ${canEdit(session)?`<form class="panel compact-form"><h2>签到卡</h2><label>学员<select name="pupil">${choices(data.pupils,r=>r.code+' · '+r.cohort)}</select></label><label>课程<select name="lesson">${choices(modules,r=>r.title)}</select></label><label>日期<input name="seen" type="date" value="2026-11-24" required></label>
 <label>观察单<select name="checked"><option value="true">收回观察单</option><option value="false">待收回</option></select></label><button>登记课卡</button>${feedback}</form>`:''}</div>`
 wire(root.querySelector('form'),record,()=>render(root,session))
}
