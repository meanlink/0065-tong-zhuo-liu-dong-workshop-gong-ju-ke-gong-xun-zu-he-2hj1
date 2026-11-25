import {empty,h,badge,notice} from './base.js'
import {heading,choices,feedback,table} from './view.js'
import {canEdit,wire} from './forms.js'
import {groups,run,state,merge} from './pairing_store.js'
import {attendance} from './attendance_store.js'
import {lessons} from './lesson_catalog.js'
import {chips} from './lesson_badges.js'
function holdLine(view) {
 if(view.held) return `${badge('停签中','held')}<span class="hold-note">共训组合正在按原门槛重算，算完前暂停签发新教案。</span>`
 const last=view.last_merge_job
 const note=last?.status==='failed'
  ?`上次合卡重算失败（${h(last.error||'')}），已保留旧版组合供查，可再次合卡重试或手动重算。`
  :last?'上次合卡重算已完成，恢复签发新教案。':'当前没有合卡重算任务，可正常签发新教案。'
 return `${badge('签发已恢复','approved')}<span class="hold-note">${note}</span>`
}
export async function render(root,session) {
 const [rows,modules,view,pupilData]=await Promise.all([groups(),lessons(),state(),attendance()])
 const editable=canEdit(session)
 root.innerHTML=heading('共训分组','最少共同签收人数和 Jaccard 相似度同时达标才连边。连通组的每条边保留人数分母。')+`
 <p class="hold-line">${holdLine(view)}</p>
 ${editable?`<form class="pair-line"><label>相似度下限<input name="threshold" required type="number" min=".01" max="1" step=".01" value=".6"></label><label>共同签收下限<input name="common" required type="number" min="2" max="50" value="2"></label><button>计算组合</button>${feedback}</form>
 <form class="pair-line merge-line"><label>副卡<select name="alias">${choices(pupilData.pupils,r=>r.code+' · '+r.cohort)}</select></label><label>正卡<select name="primary">${choices(pupilData.pupils,r=>r.code+' · '+r.cohort)}</select></label><button>合卡</button>${feedback}</form>`:''}
 ${view.merges.length?table(['副卡','正卡','合卡时间','操作人'],view.merges.map(m=>[m.alias,m.primary_code,String(m.merged_at).slice(0,16).replace('T',' '),m.merged_by])):''}
 <section class="pair-trays">${rows.map(r=>`<article class="panel">${chips(r.members,modules)}${table(['课程 A','课程 B','共同','去重总数','相似度'],r.evidence.map(x=>[x.left,x.right,x.shared,x.union,x.ratio]))}</article>`).join('')||empty('暂无共训分组。先确认签到与观察单，再计算。')}</section>`
 wire(root.querySelector('form.pair-line'),run,()=>render(root,session))
 const mergeForm=root.querySelector('form.merge-line')
 if(mergeForm) mergeForm.onsubmit=async event=>{
  event.preventDefault()
  const form=event.currentTarget,button=form.querySelector('button'),status=form.querySelector('[role=status]')
  button.disabled=true
  let refresh=false
  try {
   const result=await merge(Object.fromEntries(new FormData(form)))
   notice(status,result.message,Boolean(result.failed))
   refresh=true
  } catch(error) {
   notice(status,error.message,true)
  } finally {
   button.disabled=false
   if(refresh) await render(root,session)
  }
 }
}
