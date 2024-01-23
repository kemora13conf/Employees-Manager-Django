const main = document.querySelector(".main");
let list = document.querySelectorAll(".list");
const sidePanel = document.querySelector(".side-panel");
const closeSidePanelBtn = sidePanel.querySelector('.close-side-panel')
const indicator = document.querySelector('.indicator')

const urls = [
  '/',
  '/employees',
  '/departments',
  '/positions',
  '/primes'
]

let messages = document.querySelector('.messages')
if(messages.children.length != 0){
    setTimeout(
        ()=>{
            messages.innerHTML = ''
            messages.style.display="none"
        }, 3000
    )
}else{
    messages.style.display="none"
}

closeSidePanelBtn.addEventListener('click', (e)=>{
    sidePanel.classList.toggle('side-panel-active');
})

window.addEventListener('click', function(e){
    if (!sidePanel.contains(e.target)){
        sidePanel.classList.remove('side-panel-active');
    }
});

window.addEventListener("popstate", function (e) {
  let state = e.state || {};
  let link = state.link || window.location.pathname;

  list.forEach((item) => {
    item.classList.remove("active");
    if (item.querySelector("button").dataset.link == link) {
      item.classList.add("active");
    }
  });
  loadPage(link);
});

function activeLink() {
  list.forEach((item) => {
    item.classList.remove("active");
    this.classList.add("active");
    let link = this.querySelector("button").dataset.link;
    history.pushState({ link: link }, null, link);
  });
  loadPage();
}
list.forEach((item) => {
  item.addEventListener("click", activeLink);
});

window.addEventListener("load", function (e) {
  let link = window.location.pathname;
  let exist = false;
  list.forEach((item) => {
    item.classList.remove("active");
    if (item.querySelector("button").dataset.link == link) {
      item.classList.add("active");
      exist = true;
    }
  });
  if (!exist) {
    list[0].classList.add("active");
  }
  loadPage();
});

function isErrorPage(link, urls){
  if (urls.includes(link)) return false
  indicator.style.display='none'
  fetch('/api/error_page', { method: "GET" })
    .then(res => res.text())
    .then(res => {
      main.innerHTML = res;
    })
  return true
}
function prepareScript(link){
  var script = document.getElementById("script");
  if (script) {
    script.remove();
  }
  var scriptElement = document.createElement("script");
  var uniqueParam = "timestamp=" + new Date().getTime();
  scriptElement.setAttribute("id", "script");
  scriptElement.src =
    "/static" +
    `${link == "/" ? "/dashboard" : link}` +
    ".js?" +
    uniqueParam;
  scriptElement.defer = true;
  scriptElement.type = "module";
  return scriptElement
}
function loadPage() {
  let link = window.location.pathname;

  if(isErrorPage(link, urls)) return;
  indicator.style.display = 'flex'
  fetch("/api" + `${link == "/" ? "/dashboard" : link+'?page=1'}`, { method: "GET" })
    .then((res) => res.text())
    .then((res) => {
      main.innerHTML = res;
      let scriptElement = prepareScript(link)
      document.head.appendChild(scriptElement);
    });
}

