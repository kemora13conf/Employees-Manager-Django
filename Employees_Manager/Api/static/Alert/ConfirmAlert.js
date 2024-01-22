export default class ConfirmAlert {
    constructor(props) {
        this.msg = props.message;
        this.parent = props.parent;
        this.onConfirm = props.onConfirm;
        this.onCancel = props.onCancel;

        this.confirmMessage = document.createElement("div");
        this.confirmTitle = document.createElement("h2");
        this.confirmText = document.createElement("p");
        this.confirmButtons = document.createElement("div");
        this.okButton = document.createElement("button");
        this.cancelButton = document.createElement("button");

        this.createConfirmAttributes();
    }

    createConfirmAttributes() {
        this.parent.classList.add("popup-container-active")
        this.confirmMessage.setAttribute("class", "confirm-alert");
        this.confirmTitle.innerHTML = this.msg.confirmTitle;
        this.confirmText.innerHTML = this.msg.confirmText;

        this.confirmButtons.setAttribute("class", "confirm-buttons");
        this.okButton.innerHTML = "OK";
        this.okButton.addEventListener("click", this.handleConfirm.bind(this));

        this.cancelButton.innerHTML = "Cancel";
        this.cancelButton.addEventListener("click", this.handleCancel.bind(this));

        this.confirmButtons.append(this.cancelButton, this.okButton);

        let closeConfirm = () => {
            this.confirmMessage.classList.add('closed-confirm');
            if (this.parent.hasChildNodes(this.confirmMessage)) {
                this.parent.removeChild(this.confirmMessage);
                this.parent.classList.toggle("popup-container-active");
            }
        };

        this.okButton.addEventListener("click", closeConfirm);
        this.cancelButton.addEventListener("click", closeConfirm);

        this.confirmMessage.append(this.confirmTitle, this.confirmText, this.confirmButtons);
    }

    handleConfirm() {
        if (typeof this.onConfirm === 'function') {
            this.onConfirm();
        }
    }

    handleCancel() {
        if (typeof this.onCancel === 'function') {
            this.onCancel();
        }
    }

    render() {
        return this.confirmMessage;
    }
}
