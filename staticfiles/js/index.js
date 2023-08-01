window.addEventListener('DOMContentLoaded', (event) => {
    const checkboxes = document.querySelectorAll('[type=checkbox]');
    styleCheckboxes();

    function styleCheckboxes() {
        checkboxes.forEach(item => {
            item.addEventListener('click', function (e) {
                if (!this.checked && this.parentElement.classList.contains('checked')) {
                    this.parentElement.classList.remove("checked");
                } else {
                    this.parentElement.classList.add("checked");
                }
            })
        })
    }
})