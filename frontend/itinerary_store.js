import {api} from './base.js'
export const stops=()=>api('/api/circuits')
export const sign=({code,group,notes})=>api('/api/circuits/'+encodeURIComponent(code)+'/plan','POST',{group,notes})
