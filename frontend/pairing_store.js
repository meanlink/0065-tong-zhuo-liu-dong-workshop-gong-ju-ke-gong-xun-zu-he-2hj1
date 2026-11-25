import {api,waitJob} from './base.js'
export const groups=()=>api('/api/pairings')
export const state=()=>api('/api/pairings/state')
export async function run(data) {
 const {job_id}=await api('/api/pairings','POST',{threshold:Number(data.threshold),common:Number(data.common)})
 return waitJob(job_id)
}
export async function merge(data) {
 const result=await api('/api/pairings/merge','POST',data)
 if(!result.job_id) return result
 try {
  await waitJob(result.job_id)
  return {...result,message:'合卡完成，共训组合已按原门槛重算，签发已恢复'}
 } catch(error) {
  const job=await api(`/api/jobs/${result.job_id}`).catch(()=>null)
  if(job&&(job.status==='queued'||job.status==='running'))
   return {...result,message:'合卡已保存，重算仍在进行，本页会显示恢复状态'}
  return {...result,failed:true,message:`合卡已保存，但重算失败：${error.message}（旧版组合已保留供查）`}
 }
}
