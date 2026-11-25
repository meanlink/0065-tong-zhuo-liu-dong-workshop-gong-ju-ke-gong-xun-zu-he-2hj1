import {api,waitJob} from './base.js'
export const groups=()=>api('/api/pairings')
export async function run(data) {
 const {job_id}=await api('/api/pairings','POST',{threshold:Number(data.threshold),common:Number(data.common)})
 return waitJob(job_id)
}
