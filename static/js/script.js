document.addEventListener("DOMContentLoaded", function () {

    /* ================= CATEGORY SPECIFICATIONS ================= */

    const categorySelect = document.getElementById("category-select");
    const specContainer = document.getElementById("dynamic-spec-fields");

    if (categorySelect && specContainer) {

        function loadSpecs(categoryId) {

            if (!categoryId) {
                specContainer.innerHTML = "";
                return;
            }

            fetch(`/properties/get-specs/?category_id=${categoryId}`)
            .then(response => response.json())
            .then(data => {

                specContainer.innerHTML = "";

                if (!data.fields) return;

                data.fields.forEach(field => {

                    let html = "";

                    if (field.type === "text") {
                        html = `
                        <div class="mb-3">
                            <label class="form-label">${field.name}</label>
                            <input type="text"
                                   name="spec_${field.id}"
                                   class="form-control">
                        </div>`;
                    }

                    if (field.type === "number") {
                        html = `
                        <div class="mb-3">
                            <label class="form-label">${field.name}</label>
                            <input type="number"
                                   name="spec_${field.id}"
                                   class="form-control">
                        </div>`;
                    }

                    if (field.type === "boolean") {
                        html = `
                        <div class="form-check mb-3">
                            <input class="form-check-input"
                                   type="checkbox"
                                   name="spec_${field.id}">
                            <label class="form-check-label">
                                ${field.name}
                            </label>
                        </div>`;
                    }

                    specContainer.insertAdjacentHTML("beforeend", html);

                });

            })
            .catch(error => console.error("Spec loading error:", error));
        }

        categorySelect.addEventListener("change", function () {
            loadSpecs(this.value);
        });

        /* Load specs automatically if category already selected (Edit page) */
        if (categorySelect.value) {
            loadSpecs(categorySelect.value);
        }
    }



    /* ================= PROPERTY SEARCH ================= */

    const searchInput = document.getElementById("propertySearch");
    const suggestionBox = document.getElementById("searchSuggestions");

    if (searchInput && suggestionBox) {

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
                    html += `<div class="suggestion-item">${item}</div>`;
                });

                suggestionBox.innerHTML = html;

            })
            .catch(error => console.error("Search error:", error));

        });

    }



    /* ================= CLICK SUGGESTION ================= */

    document.addEventListener("click", function(e){

        if(e.target.classList.contains("suggestion-item")){

            const searchInput = document.getElementById("propertySearch");
            const suggestionBox = document.getElementById("searchSuggestions");

            if(searchInput){
                searchInput.value = e.target.innerText;
            }

            if(suggestionBox){
                suggestionBox.innerHTML = "";
            }

        }

    });

});


/* ================= IMAGE CHANGE ================= */

function changeMainImage(imageUrl) {

    const img = document.getElementById("mainPropertyImage");

    if(img){
        img.src = imageUrl;
    }

}