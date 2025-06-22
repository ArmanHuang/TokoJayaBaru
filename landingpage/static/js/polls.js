document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('resultModal');
    const modalProducts = document.getElementById('modal-products');
    const prevPageButton = document.getElementById('prevPage');
    const nextPageButton = document.getElementById('nextPage');
    const currentPageSpan = document.getElementById('currentPage');
    const totalPagesSpan = document.getElementById('totalPages');
    const paginationControls = document.getElementById('modal-pagination');
    const closeBtn = document.querySelector('.close');

    let currentProducts = allProductsData;
    let currentPage = 1;
    const productsPerPage = 6;

    function generateProductHTML(productName) {
        const imageUrl = productImagesData[productName];
        return `
            <div class="product-card" data-product-name="${productName}">
                <img src="${imageUrl}" alt="${productName}">
                <h4>${productName}</h4>
            </div>
        `;
    }

    function displayProducts(productsToDisplay) {
        console.log("Menampilkan produk:", productsToDisplay);
        const productHTML = productsToDisplay.map(product => generateProductHTML(product)).join('');
        modalProducts.innerHTML = productHTML;

        console.log("Jumlah elemen product-card setelah render:", modalProducts.querySelectorAll('.product-card').length);

        modalProducts.querySelectorAll('.product-card').forEach(card => {
            card.addEventListener('click', function() {
                const productName = this.dataset.productName;
                console.log(`Produk "${productName}" diklik!`);
                // Tambahkan logika yang diinginkan di sini
            });
            console.log("Event listener ditambahkan ke:", card);
        });
    }

    function updatePagination() {
        const totalPages = Math.ceil(currentProducts.length / productsPerPage) || 1;
        currentPageSpan.textContent = currentPage;
        totalPagesSpan.textContent = totalPages;
        prevPageButton.disabled = currentPage === 1;
        nextPageButton.disabled = currentPage === totalPages;

        if (totalPages > 1) {
            paginationControls.style.display = 'flex';
        } else {
            paginationControls.style.display = 'none';
        }
    }

    function showPage(pageNumber) {
        currentPage = pageNumber;
        const startIndex = (currentPage - 1) * productsPerPage;
        const endIndex = startIndex + productsPerPage;
        const productsOnPage = currentProducts.slice(startIndex, endIndex);
        displayProducts(productsOnPage);
        updatePagination();
    }

    if (currentProducts && currentProducts.length > 0) {
        showPage(1);
    } else {
        modalProducts.innerHTML = '<p>Tidak ada produk yang direkomendasikan.</p>';
        paginationControls.style.display = 'none';
    }

    prevPageButton.onclick = function() {
        if (currentPage > 1) {
            showPage(currentPage - 1);
        }
    };

    nextPageButton.onclick = function() {
        const totalPages = Math.ceil(currentProducts.length / productsPerPage) || 1;
        if (currentPage < totalPages) {
            showPage(currentPage + 1);
        }
    };

    window.closeModal = function() {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    };

    if (closeBtn) {
        closeBtn.addEventListener('click', closeModal);
    }
});


function openModal() {
    document.getElementById("resultModal").style.display = "flex";
    document.body.classList.add("modal-open");
}

function closeModal() {
    document.getElementById("resultModal").style.display = "none";
    document.body.classList.remove("modal-open");
}

document.addEventListener('DOMContentLoaded', function () {
    const ageInput = document.getElementById('age');
    const genderSelect = document.getElementById('gender');
    const occupationSelect = document.getElementById('occupation');
    const form = document.querySelector('form');

    // Rentang usia sesuai pekerjaan
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

    // Gabungkan pengecekan validasi
    function cekSemuaValidasi() {
        cekValidasiUsia();
        cekValidasiGenderPekerjaan();
    }

    // Event listener untuk interaksi user
    ageInput.addEventListener('input', cekSemuaValidasi);
    occupationSelect.addEventListener('change', cekSemuaValidasi);
    genderSelect.addEventListener('change', cekSemuaValidasi);

    form.addEventListener('submit', function (e) {
        cekSemuaValidasi();
        if (!form.checkValidity()) {
            e.preventDefault(); // Jangan kirim kalau ada yang invalid
            form.reportValidity(); // Tampilkan pesan error
        }
    });
});
