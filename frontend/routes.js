import {mount} from './base.js'
import {render as modules} from './modules.js'
import {render as checkins} from './checkins.js'
import {render as pairings} from './pairings.js'
import {render as circuits} from './circuits.js'

const pages = {
  modules: '教具与课程',
  checkins: '签到与回收',
  pairings: '共训分组',
  circuits: '外出教案'
}
const renderers = {modules, checkins, pairings, circuits}
mount({title: '同桌 · 流动工坊工具课共训组合', kicker: '绕城流动工坊 · 共训教案', pages, render: (key, root, session) => renderers[key](root, session)})
