document.addEventListener("DOMContentLoaded", function() {

    const categorySelect = document.querySelector("select[name='category']");
    const specContainer = document.getElementById("dynamic-spec-fields");

    categorySelect.addEventListener("change", function() {

        const categoryId = this.value;

        if (!categoryId) {
            specContainer.innerHTML = "";
            return;
        }

        fetch(`/properties/get-specs/?category_id=${categoryId}`)
            .then(response => response.json())
            .then(data => {

                specContainer.innerHTML = "";

                data.fields.forEach(field => {

                    let inputField = "";

                    if (field.type === "text") {
                        inputField = `<input type="text" name="spec_${field.id}" class="form-control mb-3" placeholder="${field.name}">`;
                    }

                    if (field.type === "number") {
                        inputField = `<input type="number" name="spec_${field.id}" class="form-control mb-3" placeholder="${field.name}">`;
                    }

                    if (field.type === "boolean") {
                        inputField = `
                            <div class="form-check mb-3">
                                <input class="form-check-input" type="checkbox" name="spec_${field.id}">
                                <label class="form-check-label">${field.name}</label>
                            </div>
                        `;
                    }

                    specContainer.innerHTML += inputField;
                });

            });
    });

});


document.addEventListener("DOMContentLoaded", function () {

    const categorySelect = document.getElementById("category-select");
    const specContainer = document.getElementById("dynamic-spec-fields");

    categorySelect.addEventListener("change", function () {

        const categoryId = this.value;
        specContainer.innerHTML = "";

        if (!categoryId) return;

        fetch(`/properties/get-specs/?category_id=${categoryId}`)
            .then(response => response.json())
            .then(data => {

                data.fields.forEach(field => {

                    let fieldHTML = "";

                    if (field.type === "text") {
                        fieldHTML = `
                            <div class="mb-3">
                                <label class="form-label">${field.name}</label>
                                <input type="text"
                                       name="spec_${field.id}"
                                       class="form-control">
                            </div>
                        `;
                    }

                    if (field.type === "number") {
                        fieldHTML = `
                            <div class="mb-3">
                                <label class="form-label">${field.name}</label>
                                <input type="number"
                                       name="spec_${field.id}"
                                       class="form-control">
                            </div>
                        `;
                    }

                    if (field.type === "boolean") {
                        fieldHTML = `
                            <div class="form-check mb-3">
                                <input class="form-check-input"
                                       type="checkbox"
                                       name="spec_${field.id}">
                                <label class="form-check-label">
                                    ${field.name}
                                </label>
                            </div>
                        `;
                    }

                    specContainer.insertAdjacentHTML("beforeend", fieldHTML);
                });

            });

    });

});


document.addEventListener("DOMContentLoaded", function () {

    const categorySelect = document.getElementById("category-select");
    const specContainer = document.getElementById("dynamic-spec-fields");

    function loadSpecs(categoryId) {

        fetch(`/properties/get-specs/?category_id=${categoryId}`)
            .then(response => response.json())
            .then(data => {

                specContainer.innerHTML = "";

                data.fields.forEach(field => {

                    let value = "{{ spec_values|safe }}";
                });
            });
    }

    loadSpecs(categorySelect.value);

});



function changeMainImage(imageUrl) {
    document.getElementById("mainPropertyImage").src = imageUrl;
}


const searchInput = document.getElementById("propertySearch");
const suggestionBox = document.getElementById("searchSuggestions");

searchInput.addEventListener("keyup", function(){

    let query = this.value;

    if(query.length < 2){
        suggestionBox.innerHTML = "";
        return;
    }

    fetch(`/properties/search-suggestions/?q=${query}`)

    .then(response => response.json())

    .then(data => {

        let html = "";

        data.forEach(item => {

            html += `
            <div class="suggestion-item">
                ${item}
            </div>
            `;

        });

        suggestionBox.innerHTML = html;

    });

});


document.addEventListener("click", function(e){

if(e.target.classList.contains("suggestion-item")){

searchInput.value = e.target.innerText;
suggestionBox.innerHTML = "";

}

});