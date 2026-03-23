/* ================================================================
   ESTATEPRO — Main JS
   ================================================================ */

document.addEventListener("DOMContentLoaded", function () {

    /* ── CATEGORY SPEC FIELDS (Add / Edit property) ─────────── */
    const categorySelect = document.getElementById("category-select");
    const specContainer  = document.getElementById("dynamic-spec-fields");

    if (categorySelect && specContainer) {
        function loadSpecs(categoryId) {
            if (!categoryId) { specContainer.innerHTML = ""; return; }
            specContainer.innerHTML = '<div class="text-white py-2"><span class="spinner-border spinner-border-sm me-2"></span>Loading specifications…</div>';
            fetch(`/properties/get-category-specifications/?category_id=${categoryId}`)
                .then(r => r.json())
                .then(data => {
                    specContainer.innerHTML = "";
                    if (!data.fields || !data.fields.length) {
                        specContainer.innerHTML = '<p class="text-muted small mt-2">No specification fields for this category.</p>';
                        return;
                    }
                    data.fields.forEach(field => {
                        const wrapper = document.createElement('div');
                        wrapper.className = 'mb-3';
                        if (field.type === "text") {
                            wrapper.innerHTML = `<label class="form-label text-white fw-semibold">${field.name}</label><input type="text" name="spec_${field.id}" class="form-control" placeholder="${field.name}">`;
                        } else if (field.type === "number") {
                            wrapper.innerHTML = `<label class="form-label text-white fw-semibold">${field.name}</label><input type="number" name="spec_${field.id}" class="form-control" placeholder="${field.name}">`;
                        } else if (field.type === "boolean") {
                            wrapper.innerHTML = `<div class="form-check mt-2"><input class="form-check-input" type="checkbox" name="spec_${field.id}" id="spec_check_${field.id}"><label class="form-check-label text-white" for="spec_check_${field.id}">${field.name}</label></div>`;
                        }
                        specContainer.appendChild(wrapper);
                    });
                })
                .catch(() => { specContainer.innerHTML = '<p class="text-danger small">Failed to load specifications.</p>'; });
        }
        categorySelect.addEventListener("change", function () { loadSpecs(this.value); });
        if (categorySelect.value) loadSpecs(categorySelect.value);
    }


    /* ── GLOBAL SPINNER ─────────────────────────────────────── */
    window.showSpinner = function(msg) {
        const sp = document.getElementById('globalSpinner');
        if (!sp) return;
        document.getElementById('spinnerMsg').textContent = msg || 'Processing…';
        sp.style.display = 'flex';
    };


    /* ── SEARCH SUGGESTIONS (legacy propertySearch id) ──────── */
    const legacyInput = document.getElementById("propertySearch");
    const legacyBox   = document.getElementById("searchSuggestions");
    if (legacyInput && legacyBox) {
        let debounce;
        legacyInput.addEventListener("keyup", function() {
            clearTimeout(debounce);
            const q = this.value.trim();
            if (q.length < 2) { legacyBox.innerHTML = ""; legacyBox.style.display = "none"; return; }
            debounce = setTimeout(() => {
                fetch(`/properties/search-suggestions/?q=${encodeURIComponent(q)}`)
                    .then(r => r.json())
                    .then(data => {
                        if (!data.length) { legacyBox.style.display = "none"; return; }
                        legacyBox.innerHTML = data.map(item =>
                            `<div class="suggestion-item" data-val="${item.title||item}">${item.title||item}</div>`
                        ).join('');
                        legacyBox.style.display = "block";
                    })
                    .catch(() => {});
            }, 280);
        });
    }

    /* ── SUGGESTION CLICK ───────────────────────────────────── */
    document.addEventListener("click", function(e) {
        if (e.target.classList.contains("suggestion-item") || e.target.closest(".suggestion-item")) {
            const item = e.target.closest(".suggestion-item") || e.target;
            const inp = document.getElementById("propertySearch") || document.getElementById("heroSearchInput") || document.getElementById("filterSearchInput");
            if (inp) inp.value = item.dataset.val || item.innerText.trim();
            document.querySelectorAll('.suggestions-box').forEach(b => { b.style.display='none'; b.innerHTML=''; });
        }
    });

});

/* ── GALLERY IMAGE SWITCHER ─────────────────────────────────── */
function changeMainImage(imageUrl) {
    const img = document.getElementById("mainPropertyImage");
    if (img) {
        img.style.opacity = '0.6';
        setTimeout(() => { img.src = imageUrl; img.style.opacity = '1'; }, 200);
    }
}
