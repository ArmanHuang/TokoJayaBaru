document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('resultModal');
    const modalProducts = document.getElementById('modal-products');
    const prevPageButton = document.getElementById('prevPage');
    const nextPageButton = document.getElementById('nextPage');
    const currentPageSpan = document.getElementById('currentPage');
    const totalPagesSpan = document.getElementById('totalPages');
    const paginationControls = document.getElementById('modal-pagination');
    const closeBtn = document.querySelector('.close');

    let currentProducts = allProductsData || [];
    let currentPage = 1;
    const productsPerPage = 6;

    // Generate HTML produk dengan safe atribut
    function generateProductHTML(productName) {
        const imageUrl = productImagesData[productName] || (staticUrl + "default.png");
        return `
            <div class="product-card" data-product-name="${productName}">
                <img src="${imageUrl}" alt="${productName}" onerror="this.src='${staticUrl}default.png'" />
                <h4>${productName}</h4>
            </div>
        `;
    }

    // Render produk di modal
    function displayProducts(productsToDisplay) {
        console.log("Menampilkan produk:", productsToDisplay);
        const productHTML = productsToDisplay.map(generateProductHTML).join('');
        modalProducts.innerHTML = productHTML;

        console.log("Jumlah elemen product-card setelah render:", modalProducts.querySelectorAll('.product-card').length);

        // Pasang event listener klik tiap product-card
        modalProducts.querySelectorAll('.product-card').forEach(card => {
            card.addEventListener('click', function() {
                const productName = this.dataset.productName;
                console.log(`Produk "${productName}" diklik!`);
                // Tambah logika klik sesuai kebutuhan di sini
            });
        });
    }

    // Update pagination UI
    function updatePagination() {
        if (!prevPageButton || !nextPageButton || !currentPageSpan || !totalPagesSpan || !paginationControls) return;

        const totalPages = Math.max(Math.ceil(currentProducts.length / productsPerPage), 1);
        currentPageSpan.textContent = currentPage;
        totalPagesSpan.textContent = totalPages;
        prevPageButton.disabled = currentPage === 1;
        nextPageButton.disabled = currentPage === totalPages;

        paginationControls.style.display = totalPages > 1 ? 'flex' : 'none';
    }

    // Tampilkan produk per halaman
    function showPage(pageNumber) {
        currentPage = pageNumber;
        const startIndex = (currentPage - 1) * productsPerPage;
        const endIndex = startIndex + productsPerPage;
        const productsOnPage = currentProducts.slice(startIndex, endIndex);
        displayProducts(productsOnPage);
        updatePagination();
    }

    // Inisialisasi tampilan produk dan pagination
    if (currentProducts.length > 0) {
        showPage(1);
    } else {
        modalProducts.innerHTML = '<p>Tidak ada produk yang direkomendasikan.</p>';
        if (paginationControls) paginationControls.style.display = 'none';
    }

    // Event tombol pagination
    if (prevPageButton) {
        prevPageButton.onclick = function() {
            if (currentPage > 1) showPage(currentPage - 1);
        };
    }
    if (nextPageButton) {
        nextPageButton.onclick = function() {
            const totalPages = Math.max(Math.ceil(currentProducts.length / productsPerPage), 1);
            if (currentPage < totalPages) showPage(currentPage + 1);
        };
    }

    // Fungsi tutup modal
    window.closeModal = function() {
        if (!modal) return;
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    };

    if (closeBtn) closeBtn.addEventListener('click', closeModal);
});

function openModal() {
    const modal = document.getElementById("resultModal");
    if (!modal) return;
    modal.style.display = "flex";
    modal.scrollTop = 0;
    document.body.classList.add("modal-open");
}

function closeModal() {
    const modal = document.getElementById("resultModal");
    if (!modal) return;
    modal.style.display = "none";
    document.body.classList.remove("modal-open");
}

// Validasi form usia & pekerjaan
document.addEventListener('DOMContentLoaded', function () {
    const ageInput = document.getElementById('age');
    const genderSelect = document.getElementById('gender');
    const occupationSelect = document.getElementById('occupation');
    const form = document.querySelector('form');

    const usiaValid = {
        'Ibu Rumah Tangga': [17, 65],
        'Karyawan Swasta': [17, 50],
        'Pegawai Kantor': [17, 40],
        'Pekerja Pabrik': [17, 50],
        'Pelajar/Mahasiswa': [17, 35],
        'Teknisi': [17, 50]
    };

    function cekValidasiUsia() {
        const age = parseInt(ageInput.value);
        const occupation = occupationSelect.value;
        const range = usiaValid[occupation];

        if (!isNaN(age) && range) {
            if (age < range[0] || age > range[1]) {
                ageInput.setCustomValidity(`Usia untuk ${occupation} harus antara ${range[0]} hingga ${range[1]} tahun.`);
            } else {
                ageInput.setCustomValidity('');
            }
        } else {
            ageInput.setCustomValidity('');
        }
    }

    function cekValidasiGenderPekerjaan() {
        const gender = genderSelect.value;
        const occupation = occupationSelect.value;

        if (occupation === 'Ibu Rumah Tangga' && gender !== 'Perempuan') {
            occupationSelect.setCustomValidity('Pekerjaan "Ibu Rumah Tangga" hanya dapat dipilih jika jenis kelamin adalah Perempuan.');
        } else {
            occupationSelect.setCustomValidity('');
        }
    }

    function cekSemuaValidasi() {
        cekValidasiUsia();
        cekValidasiGenderPekerjaan();
    }

    if (!ageInput || !genderSelect || !occupationSelect || !form) return;

    ageInput.addEventListener('input', cekSemuaValidasi);
    occupationSelect.addEventListener('change', cekSemuaValidasi);
    genderSelect.addEventListener('change', cekSemuaValidasi);

    form.addEventListener('submit', function (e) {
        cekSemuaValidasi();
        if (!form.checkValidity()) {
            e.preventDefault();
            form.reportValidity();
        }
    });
});
