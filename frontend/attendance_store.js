import {api} from './base.js'
export const attendance=()=>api('/api/checkins')
export const record=body=>api('/api/checkins','POST',{...body,checked:body.checked==='true'})
