const main = document.querySelector(".main");
let list = document.querySelectorAll(".list");
const sidePanel = document.querySelector(".side-panel");
const closeSidePanelBtn = sidePanel.querySelector('.close-side-panel')

let messages = document.querySelector('.messages')
console.log(messages.children.length)
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

function loadPage() {
  var script = document.getElementById("script");
  if (script) {
    script.remove();
  }
  let link = window.location.pathname;
  fetch("/api" + `${link == "/" ? "/dashboard" : link+'?page=2'}`, { method: "GET" })
    .then((res) => res.text())
    .then((res) => {
      main.innerHTML = res;
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
      document.head.appendChild(scriptElement);
    });
}

