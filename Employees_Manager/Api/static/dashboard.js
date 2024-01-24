const count = document.querySelector('.count');
const recent = document.querySelector('.recent');
const resize = () => {
    recent.style.maxHeight = count.offsetHeight + 'px';
}
resize();
window.addEventListener('resize', resize);