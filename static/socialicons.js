const $ = s => document.querySelectorAll(s)
const on = (ev, el, cb) =>
  el.addEventListener(ev, e => cb(e, el))
$('a').forEach(el =>
  on('click', el, e => e.preventDefault())
)
