import {empty,h} from './base.js'
import {heading,feedback,table} from './view.js'
import {canEdit,wire} from './forms.js'
import {groups,run} from './pairing_store.js'
import {lessons} from './lesson_catalog.js'
import {chips} from './lesson_badges.js'
export async function render(root,session) {
 const [rows,modules]=await Promise.all([groups(),lessons()])
 root.innerHTML=heading('共训分组','最少共同签收人数和 Jaccard 相似度同时达标才连边。连通组的每条边保留人数分母。')+`
 ${canEdit(session)?`<form class="pair-line"><label>相似度下限<input name="threshold" required type="number" min=".01" max="1" step=".01" value=".6"></label><label>共同签收下限<input name="common" required type="number" min="2" max="50" value="2"></label><button>计算组合</button>${feedback}</form>`:''}
 <section class="pair-trays">${rows.map(r=>`<article class="panel">${chips(r.members,modules)}${table(['课程 A','课程 B','共同','去重总数','相似度'],r.evidence.map(x=>[x.left,x.right,x.shared,x.union,x.ratio]))}</article>`).join('')||empty('暂无共训分组。先确认签到与观察单，再计算。')}</section>`
 wire(root.querySelector('form'),run,()=>render(root,session))
}
