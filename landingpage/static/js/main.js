// Open Modal Function
function openModal(category) {
    console.log("openModal dipanggil dengan kategori:", category);
    const modal = document.getElementById('productModal');
    const modalTitle = document.getElementById('modal-title');
    const modalProducts = document.getElementById('modal-products');
    const paginationControls = document.getElementById('modal-pagination');
    const prevPageButton = document.getElementById('prevPage');
    const nextPageButton = document.getElementById('nextPage');
    const currentPageSpan = document.getElementById('currentPage');
    const totalPagesSpan = document.getElementById('totalPages');

    modalProducts.innerHTML = ''; // Clear previous product list
    const staticUrl = document.getElementById('static-url')?.dataset?.staticUrl || ''; 

    const titles = {
        'peralatan-dapur': 'Peralatan Dapur',
        'elektronik': 'Elektronik',
        'perkakas': 'Perkakas',
        'perlengkapan-rumah': 'Perlengkapan Rumah',
        'pupuk': 'Pupuk',
        'souvenir': 'Souvenir'
    };
    modalTitle.innerHTML = titles[category] || 'Products';

    let currentProducts = [];
    let currentPage = 1;
    const productsPerPage = 6;

    function displayProducts(productsToDisplay) {
        let productHTML = productsToDisplay.map(product => `
            <div class="product-card" data-product-name="${product.name}">
                <img src="${product.image}" alt="${product.name}" style="width: 100px; height: 100px; object-fit: contain; background-color: #f5f5f5;" />
                <h4>${product.name}</h4>
            </div>
        `).join('');
        modalProducts.innerHTML = productHTML;

        modalProducts.querySelectorAll('.product-card').forEach(card => {
            card.addEventListener('click', function () {
                const productName = this.dataset.productName;
                console.log(`Produk "${productName}" diklik!`);
            });
        });
    }

    function updatePagination() {
        const totalPages = Math.ceil(currentProducts.length / productsPerPage) || 1;
        currentPageSpan.textContent = currentPage;
        totalPagesSpan.textContent = totalPages;
        prevPageButton.disabled = currentPage === 1;
        nextPageButton.disabled = currentPage === totalPages;

        paginationControls.style.display = totalPages > 1 ? 'flex' : 'none';
    }

    function showPage(pageNumber) {
        currentPage = pageNumber;
        const startIndex = (currentPage - 1) * productsPerPage;
        const endIndex = startIndex + productsPerPage;
        const productsOnPage = currentProducts.slice(startIndex, endIndex);
        displayProducts(productsOnPage);
        updatePagination();
    }

    // FETCH products dari backend sesuai kategori
    fetch(`/get-products/${category}/`)
        .then(response => {
            if (!response.ok) throw new Error("Gagal mengambil data produk");
            return response.json();
        })
        .then(data => {
            currentProducts = data.products; // format: [{name: ..., image: ...}]
            if (currentProducts.length === 0) {
                modalProducts.innerHTML = '<p>Tidak ada produk dalam kategori ini.</p>';
                paginationControls.style.display = 'none';
                return;
            }
            showPage(1); // Tampilkan halaman pertama
        })
        .catch(error => {
            console.error("Terjadi kesalahan saat mengambil produk:", error);
            modalProducts.innerHTML = '<p>Gagal memuat produk.</p>';
        });

    // Judul kategori warna biru (opsional)
    const categoriesWithBlueTitle = ['peralatan-dapur', 'elektronik', 'perkakas', 'perlengkapan-rumah', 'pupuk', 'souvenir'];
    if (categoriesWithBlueTitle.includes(category)) {
        modalTitle.classList.add('blue-title');
    } else {
        modalTitle.classList.remove('blue-title');
    }

    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden'; // Disable scroll when modal is open

    // Pagination button events
    prevPageButton.onclick = function () {
        if (currentPage > 1) {
            showPage(currentPage - 1);
        }
    };

    nextPageButton.onclick = function () {
        const totalPages = Math.ceil(currentProducts.length / productsPerPage) || 1;
        if (currentPage < totalPages) {
            showPage(currentPage + 1);
        }
    };
}


// Close Modal Function (remains the same)
function closeModal() {
    const modal = document.getElementById('productModal');
    modal.style.display = 'none';
    document.body.style.overflow = 'auto'; // Re-enable scroll when modal is closed
    console.log("Modal ditutup.");
}

// Close modal when clicking outside the modal content (remains the same)
window.onclick = function(event) {
    if (event.target === document.getElementById("productModal")) {
        closeModal();
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const mobileMenu = document.getElementById('mobile-menu');
    const navLinks = document.getElementById('nav-links');

    mobileMenu.addEventListener('click', function() {
        this.classList.toggle('active');
        navLinks.classList.toggle('active');

        // Lock body scroll when menu is open
        if(navLinks.classList.contains('active')) {
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = '';
        }
    });

    // Close menu when clicking on a link
    document.querySelectorAll('#nav-links a').forEach(link => {
        link.addEventListener('click', function() {
            mobileMenu.classList.remove('active');
            navLinks.classList.remove('active');
            document.body.style.overflow = '';
        });
    });

    console.log("DOMContentLoaded selesai.");
});
