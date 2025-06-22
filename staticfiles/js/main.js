// Open Modal Function
function openModal(category) {
    console.log("openModal dipanggil dengan kategori:", category);
    const modal = document.getElementById('productModal');
    console.log("Elemen modal:", modal);
    const modalTitle = document.getElementById('modal-title');
    const modalProducts = document.getElementById('modal-products');
    const paginationControls = document.getElementById('modal-pagination');
    const prevPageButton = document.getElementById('prevPage');
    const nextPageButton = document.getElementById('nextPage');
    const currentPageSpan = document.getElementById('currentPage');
    const totalPagesSpan = document.getElementById('totalPages');

    modalProducts.innerHTML = ''; // Clear previous product list
    const staticUrl = document.getElementById('static-url').dataset.staticUrl;

    // Define all products
    const allProducts = {
        dapur: [
            'Baskom', 'Batu Asah', 'Botol Kecap', 'Box Donat', 'Celemek', 'Ember', 'Garpu', 'Gas Portable', 'Gayung',
            'Jepitan Bakaran', 'Keranjang Sampah', 'Keset Kaki', 'Kuningan Kompor', 'Mancis', 'Panci', 'Perangkap Tikus','Pisau', 'Regulator', 'Sapu', 'Saringan', 'Selang Gas', 'Sendok', 'Serbet','tampi', 'Tudung Saji', 'Toples','tempat bakaran',
        ],
        elektronik: [
            'Fitting', 'Isolasi', 'Kabel', 'Kalkulator', 'Lampu LED', 'Plug', 'Saklar', 'Socket','Stop Kontak', 'Test Pen'
        ],
        perkakas: [
            'Elbow', 'Evamatic', 'Klem', 'Kran', 'Kuas', 'Lem Lilin', 'Mata Gerinda', 'Meteran', 'Obeng',
            'Paku', 'Sarung Tangan', 'Seal Tape', 'Selang', 'Skop', 'Skrap', 'Tali tambang', 'Thinner'
        ],
        perlengkapanRumah: [
            'Gembok', 'Hanger', 'Jas Hujan', 'Jepitan Baju', 'Karpet', 'Klem Selang', 'Payung', 'Polybag','TanahCampur','Tas',
        ],
        souvenir: [
            'Celengan'
        ],
        pupuk: [
            'TanahCampur'
        ],
    };
    console.log("Produk untuk kategori", category, ":", allProducts[category]);

    // Update modal title based on category
    const titles = {
        dapur: 'Peralatan Dapur',
        elektronik: 'Elektronik',
        perkakas: 'Perkakas',
        perlengkapanRumah: 'Perlengkapan Rumah',
        pupuk: 'Pupuk',
        souvenir: 'Souvenir'
    };
    modalTitle.innerHTML = titles[category] || 'Products';

    let currentProducts = [];
    let currentPage = 1;
    const productsPerPage = 6;

    function displayProducts(productsToDisplay) {
        console.log("Menampilkan produk:", productsToDisplay);
        let productHTML = productsToDisplay.map(product => `
            <div class="product-card" data-product-name="${product}">
                <img src="${staticUrl}images/${product.replace(/\s+/g, '')}.png" alt="${product}">
                <h4>${product}</h4>
            </div>
        `).join('');
        modalProducts.innerHTML = productHTML;

        console.log("Jumlah elemen product-card setelah render:", modalProducts.querySelectorAll('.product-card').length);

        // Pastikan event listener dipasang setelah elemen benar-benar ada di DOM
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

        // Tampilkan atau sembunyikan kontrol paginasi jika ada lebih dari satu halaman
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

    if (allProducts[category]) {
        currentProducts = allProducts[category];
        showPage(1); // Tampilkan halaman pertama

        // Coloring title if needed
        const categoriesWithBlueTitle = ['dapur', 'elektronik', 'perkakas', 'perlengkapanRumah', 'pupuk', 'souvenir'];
        if (categoriesWithBlueTitle.includes(category)) {
            modalTitle.classList.add('blue-title');
        } else {
            modalTitle.classList.remove('blue-title');
        }

        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden'; // Disable scroll when modal is open
        console.log("Modal ditampilkan untuk kategori:", category);
    } else {
        console.log("Kategori tidak ditemukan untuk:", category);
    }

    // Event listeners for pagination buttons
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
