import {h} from './base.js'
export function chips(keys,lessons) {
 const names=new Map(lessons.map(x=>[x.code,x.title]))
 return `<ul class="lesson-tags">${keys.map(key=>`<li>${h(names.get(key)||key)}</li>`).join('')}</ul>`
}
