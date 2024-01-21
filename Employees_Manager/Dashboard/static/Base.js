const main = document.querySelector('.main');
let list = document.querySelectorAll('.list');

function activeLink(){
    list.forEach(item => {
        item.classList.remove('active');
        this.classList.add('active');
        let link = this.querySelector('button').dataset.link;
        history.pushState({link: link}, null, link);
    })
    loadPage();
}
list.forEach(item => {
    item.addEventListener("click", activeLink)
})

window.addEventListener('load', function(e){
    let link = window.location.pathname;
    let exist = false;
    list.forEach(item => {
        item.classList.remove('active');
        if(item.querySelector('button').dataset.link == link){
            item.classList.add('active');
            exist = true;
        }
    })
    if(!exist){
        list[0].classList.add('active');
    }
    loadPage();
})

function loadPage(){
    let link = window.location.pathname;
    fetch('/api' + `${link == '/' ? '/dashboard': link}`, {method: 'GET'})
        .then(res => res.text())
        .then(res => {
            main.innerHTML = res;
        })
}