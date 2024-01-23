import Alert from "./Alert/Alert.js";
import ConfirmAlert from "./Alert/ConfirmAlert.js";

const table = document.querySelector(".main-list");
const tbody = table.querySelector("tbody");
const addBtn = document.querySelector(".list-add-btn");
const alertContainer = document.querySelector(".alerts-container");
const popupContainer = document.querySelector(".popup-container");

const trash = document.querySelectorAll(".fa-trash");
const edit = document.querySelectorAll(".fa-user-edit");

const csrfToken = document.cookie
  .split("; ")
  .find((cookie) => cookie.startsWith("csrftoken="))
  .split("=")[1];

addBtn.addEventListener('click', (e) => {
    const url = `/get_department_form`;
    const options = {
      method: "GET",
    };
    fetch(url, options)
      .then((res) => res.text())
      .then((res) => {
        let sidePanel = document.querySelector(".side-panel");
        let sidePanelBody = sidePanel.querySelector('.side-panel-body')

        sidePanel.classList.toggle('side-panel-active')
        sidePanelBody.innerHTML = res;
      });
});

trash.forEach((el) => {
  el.addEventListener("click", (e) => {
    const id = e.target.dataset.id;
    popupContainer.appendChild(
      new ConfirmAlert({
        message: {
          confirmText: "Are you sure you want to delete this department ?",
          confirmTitle: "Delete Department",
        },
        parent: popupContainer,
        onConfirm: () => {
          const url = `/api/departments/${id}`;
          const options = {
            method: "DELETE",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": csrfToken,
            },
          };
          fetch(url, options)
            .then((res) => res.json())
            .then((res) => {
              if (res.status === "success") {
                alertContainer.appendChild(
                  new Alert(
                    {
                      type: "success",
                      msg_title: "SUCCES",
                      msg_text: "Department deleted successfully",
                    },
                    alertContainer
                  ).render()
                );
                console.log(e.target.parentElement.parentElement);
                tbody.removeChild(
                  e.target.parentElement.parentElement.parentElement
                );
              } else {
                alertContainer.appendChild(
                  new Alert(
                    {
                      type: "error",
                      msg_title: "ERROR",
                      msg_text: "Something went wrong",
                    },
                    alertContainer
                  ).render()
                );
              }
            });
        },
      }).render()
    );
  });
});

edit.forEach((el) => {
  el.addEventListener("click", function (e) {
    const id = e.target.dataset.id;
    const url = `/get_department_form?id=${id}`;
    const options = {
      method: "GET",
      headers: {
        "X-CSRFToken": csrfToken,
      },
    };
    fetch(url, options)
      .then((res) => res.text())
      .then((res) => {
        let sidePanel = document.querySelector(".side-panel");
        let sidePanelBody = sidePanel.querySelector('.side-panel-body')

        sidePanel.classList.toggle('side-panel-active')
        sidePanelBody.innerHTML = res;
      });
  });
});


// get the next or previous page of the table
const main = document.querySelector(".main");
const next = document.querySelector('.next')
const prev = document.querySelector('.prev')

next.addEventListener('click', ()=>{
  loadPage(Number(next.dataset.page) + 1)
})
prev.addEventListener('click', ()=>{
  loadPage(Number(next.dataset.page) - 1)
})

function loadPage(page) {
  main.children[0].classList.toggle('loading')
  var script = document.getElementById("script");
  if (script) {
    script.remove();
  }
  let link = window.location.pathname;
  fetch("/api" + `${link}?page=${page}`, { method: "GET" })
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
