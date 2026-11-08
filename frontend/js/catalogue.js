/**
 * BP Tech Inventory Management System
 * [MEMBER 3: JavaScript and Frontend Integration Developer]
 * Customer Product Catalogue Client Script
 * Handles category filtering, condition toggling, search, dynamic card rendering, and WhatsApp link generation.
 */

// Fallback demo products for instant UI preview when backend server is offline
const MOCK_PRODUCTS = [
    {
        product_id: 1,
        product_name: "AMD Ryzen 5 5600",
        sku: "CPU-AMD-5600-NEW",
        condition: "New",
        selling_price: "529.00",
        description: "6 Cores, 12 Threads, Up to 4.4 GHz Max Boost, Socket AM4, PCIe 4.0 with Wraith Stealth Cooler.",
        image_url: "https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?w=500&auto=format&fit=crop&q=60",
        category: { category_name: "Processors" },
        inventory: { quantity_available: 14, is_low_stock: false }
    },
    {
        product_id: 2,
        product_name: "NVIDIA GeForce RTX 3060 12GB (Used)",
        sku: "GPU-NV-3060-USED-01",
        condition: "Used",
        selling_price: "980.00",
        description: "Stress-tested pass. 12GB GDDR6 VRAM, Ray Tracing, DLSS. 1-Month Store Warranty.",
        image_url: "https://images.unsplash.com/photo-1587202372775-e229f172b9d7?w=500&auto=format&fit=crop&q=60",
        category: { category_name: "Graphics Cards" },
        inventory: { quantity_available: 3, is_low_stock: true }
    },
    {
        product_id: 3,
        product_name: "Kingston FURY Beast 16GB (2x8GB) DDR4 3200MHz",
        sku: "RAM-KST-16GB-3200-NEW",
        condition: "New",
        selling_price: "165.00",
        description: "High-performance low-profile heat spreader, Intel XMP 2.0 ready, AMD Ryzen compatible.",
        image_url: "https://images.unsplash.com/photo-1562976540-1502c2145186?w=500&auto=format&fit=crop&q=60",
        category: { category_name: "RAM" },
        inventory: { quantity_available: 25, is_low_stock: false }
    },
    {
        product_id: 4,
        product_name: "Kingston NV2 1TB PCIe 4.0 NVMe M.2 SSD",
        sku: "SSD-KST-NV2-1TB-NEW",
        condition: "New",
        selling_price: "289.00",
        description: "Gen 4x4 NVMe PCIe speed up to 3500MB/s Read, 2100MB/s Write. 3-Year warranty.",
        image_url: "https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?w=500&auto=format&fit=crop&q=60",
        category: { category_name: "Storage" },
        inventory: { quantity_available: 18, is_low_stock: false }
    },
    {
        product_id: 5,
        product_name: "Corsair CV550 550W 80 PLUS Bronze (Used)",
        sku: "PSU-COR-CV550-USED",
        condition: "Used",
        selling_price: "130.00",
        description: "Clean tested power supply with voltage tester check. 1-Month Store Warranty.",
        image_url: "https://images.unsplash.com/photo-1587202372634-32705e3bf49c?w=500&auto=format&fit=crop&q=60",
        category: { category_name: "Power Supplies" },
        inventory: { quantity_available: 1, is_low_stock: true }
    }
];

let activeCategoryId = "";
let activeCondition = "";
let currentSearchTerm = "";
let activeComponentType = "";

document.addEventListener("DOMContentLoaded", () => {
    initFilters();
    loadCategories();
    loadProducts();
});

function initFilters() {
    // Search input & button
    const searchInput = document.getElementById("searchInput");
    const searchBtn = document.getElementById("searchBtn");

    if (searchBtn && searchInput) {
        searchBtn.addEventListener("click", () => {
            currentSearchTerm = searchInput.value.trim();
            loadProducts();
        });

        searchInput.addEventListener("keyup", (e) => {
            if (e.key === "Enter") {
                currentSearchTerm = searchInput.value.trim();
                loadProducts();
            }
        });
    }

    // Component dropdown filter
    const componentDropdown = document.getElementById("componentDropdown");
    if (componentDropdown) {
        componentDropdown.addEventListener("change", (e) => {
            activeComponentType = e.target.value;
            loadProducts();
        });
    }

    // Condition buttons
    const conditionBtns = document.querySelectorAll("#conditionToggles .condition-btn");
    conditionBtns.forEach((btn) => {
        btn.addEventListener("click", () => {
            conditionBtns.forEach((b) => b.classList.remove("active"));
            btn.classList.add("active");
            activeCondition = btn.getAttribute("data-condition");
            loadProducts();
        });
    });

    // Update WhatsApp links with config phone number
    const heroWhatsappBtn = document.getElementById("heroWhatsappBtn");
    if (heroWhatsappBtn) {
        heroWhatsappBtn.href = whatsapp.getCustomPCLink();
    }
    const floatingWhatsapp = document.getElementById("floatingWhatsapp");
    if (floatingWhatsapp) {
        floatingWhatsapp.href = whatsapp.getGeneralEnquiryLink();
    }
    const footerWhatsappLink = document.getElementById("footerWhatsappLink");
    if (footerWhatsappLink) {
        footerWhatsappLink.href = `https://wa.me/${CONFIG.WHATSAPP_PHONE}`;
        footerWhatsappLink.textContent = `WhatsApp: +${CONFIG.WHATSAPP_PHONE}`;
    }
}

/**
 * Load categories from API and create filter pills
 */
async function loadCategories() {
    const pillsContainer = document.getElementById("categoryPills");
    if (!pillsContainer) return;

    try {
        const categories = await api.getCategories();
        pillsContainer.innerHTML = `<button class="pill ${!activeCategoryId ? 'active' : ''}" data-category-id="">All Categories</button>`;

        categories.forEach((cat) => {
            const btn = document.createElement("button");
            btn.className = `pill ${activeCategoryId == cat.category_id ? 'active' : ''}`;
            btn.setAttribute("data-category-id", cat.category_id);
            btn.textContent = cat.category_name;
            btn.addEventListener("click", () => {
                document.querySelectorAll("#categoryPills .pill").forEach((p) => p.classList.remove("active"));
                btn.classList.add("active");
                activeCategoryId = cat.category_id;
                loadProducts();
            });
            pillsContainer.appendChild(btn);
        });

        // Add click listener for 'All Categories'
        const allBtn = pillsContainer.querySelector("button[data-category-id='']");
        if (allBtn) {
            allBtn.addEventListener("click", () => {
                document.querySelectorAll("#categoryPills .pill").forEach((p) => p.classList.remove("active"));
                allBtn.classList.add("active");
                activeCategoryId = "";
                loadProducts();
            });
        }
    } catch (err) {
        console.warn("Could not load categories from API, using default filter set.");
    }
}

/**
 * Load and render products matching filters
 */
async function loadProducts() {
    const grid = document.getElementById("productsGrid");
    const countDisplay = document.getElementById("productCount");
    if (!grid) return;

    grid.innerHTML = `<div style="grid-column: 1/-1; text-align: center; padding: 40px; color: var(--text-muted);">Fetching live inventory...</div>`;

    let products = [];
    try {
        products = await api.getProducts({
            category_id: activeCategoryId || null,
            condition: activeCondition || null,
            search: currentSearchTerm || null
        });
    } catch (err) {
        console.warn("Backend API not reachable. Rendering offline preview catalog.", err);
        // Offline fallback filter
        products = MOCK_PRODUCTS.filter((p) => {
            if (activeCondition && p.condition !== activeCondition) return false;
            if (currentSearchTerm) {
                const term = currentSearchTerm.toLowerCase();
                const match = p.product_name.toLowerCase().includes(term) || p.sku.toLowerCase().includes(term);
                if (!match) return false;
            }
            return true;
        });
    }

    // Filter by Component Type Dropdown
    if (activeComponentType) {
        const comp = activeComponentType.toUpperCase();
        products = products.filter((p) => {
            const sku = (p.sku || "").toUpperCase();
            const name = (p.product_name || "").toUpperCase();
            const desc = (p.description || "").toUpperCase();
            const cat = (p.category && p.category.category_name ? p.category.category_name : "").toUpperCase();

            switch (comp) {
                case "CPU":
                    return sku.startsWith("CPU") || cat.includes("PROCESSOR") || name.includes("RYZEN") || name.includes("INTEL") || name.includes("CPU") || desc.includes("PROCESSOR");
                case "GPU":
                    return sku.startsWith("GPU") || cat.includes("GRAPHIC") || name.includes("GEFORCE") || name.includes("RTX") || name.includes("GTX") || name.includes("RADEON") || name.includes("GPU");
                case "MOBO":
                    return sku.startsWith("MB") || sku.startsWith("MOBO") || cat.includes("MOTHERBOARD") || name.includes("MOTHERBOARD") || name.includes("B550") || name.includes("B650") || name.includes("Z790");
                case "RAM":
                    return sku.startsWith("RAM") || cat.includes("RAM") || name.includes("RAM") || name.includes("DDR4") || name.includes("DDR5") || desc.includes("MEMORY");
                case "SSD":
                    return sku.startsWith("SSD") || (cat.includes("STORAGE") && (name.includes("SSD") || desc.includes("NVME") || desc.includes("SSD"))) || name.includes("SSD") || desc.includes("NVME");
                case "HDD":
                    return sku.startsWith("HDD") || name.includes("HDD") || name.includes("HARD DISK") || desc.includes("HARD DISK");
                case "PSU":
                    return sku.startsWith("PSU") || cat.includes("POWER") || name.includes("PSU") || name.includes("POWER SUPPLY") || desc.includes("POWER SUPPLY");
                case "PC CASE":
                    return sku.includes("CASE") || name.includes("CASE") || desc.includes("CHASSIS") || desc.includes("TOWER");
                case "CPU COOLER":
                    return sku.includes("COOL") || name.includes("COOLER") || desc.includes("COOLER") || desc.includes("AIO");
                case "CASING FAN":
                    return sku.includes("FAN") || name.includes("FAN");
                case "MONITOR":
                    return sku.includes("MON") || name.includes("MONITOR");
                case "KEYBOARD":
                    return sku.includes("KB") || name.includes("KEYBOARD");
                case "MOUSE":
                    return sku.includes("MOUSE") || name.includes("MOUSE");
                case "HEADSET":
                    return sku.includes("HEAD") || name.includes("HEADSET") || name.includes("HEADPHONE");
                case "SPEAKER":
                    return sku.includes("SPK") || name.includes("SPEAKER");
                case "CONTROLLER":
                    return sku.includes("CTRL") || name.includes("CONTROLLER") || name.includes("GAMEPAD");
                default:
                    return sku.includes(comp) || name.includes(comp) || cat.includes(comp);
            }
        });
    }

    if (countDisplay) {
        countDisplay.textContent = `${products.length} product(s) available`;
    }

    if (products.length === 0) {
        grid.innerHTML = `
            <div style="grid-column: 1/-1; text-align: center; padding: 60px 20px;">
                <h4 style="font-size: 1.25rem; color: #fff; margin-bottom: 8px;">No components found</h4>
                <p style="color: var(--text-secondary); margin-bottom: 20px;">Try adjusting your search keywords or clearing the category filter.</p>
                <button class="btn-primary" onclick="resetFilters()">Reset All Filters</button>
            </div>
        `;
        return;
    }

    grid.innerHTML = "";
    products.forEach((product) => {
        grid.appendChild(createProductCard(product));
    });
}

/**
 * Construct Product Card DOM element
 */
function createProductCard(product) {
    const card = document.createElement("div");
    card.className = "product-card";

    const qty = product.inventory ? product.inventory.quantity_available : 0;
    const isLow = product.inventory ? product.inventory.is_low_stock : false;

    let stockBadgeHTML = "";
    if (qty <= 0) {
        stockBadgeHTML = `<div class="stock-status stock-out"><span class="stock-dot"></span> Out of Stock</div>`;
    } else if (isLow) {
        stockBadgeHTML = `<div class="stock-status stock-low"><span class="stock-dot"></span> Low Stock (${qty})</div>`;
    } else {
        stockBadgeHTML = `<div class="stock-status stock-in"><span class="stock-dot"></span> In Stock (${qty})</div>`;
    }

    const conditionBadgeClass = product.condition === "New" ? "badge-new" : "badge-used";
    const categoryName = product.category ? product.category.category_name : "Hardware";
    const waLink = whatsapp.getProductLink(product.product_name, product.condition, product.selling_price);
    const fallbackImg = "https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?w=500&auto=format&fit=crop&q=60";

    card.innerHTML = `
        <div class="product-thumb-wrap">
            <img src="${product.image_url || fallbackImg}" alt="${product.product_name}" class="product-thumb" onerror="this.src='${fallbackImg}'">
            <div class="badge-group">
                <span class="badge ${conditionBadgeClass}">${product.condition}</span>
            </div>
            <span class="badge-category">${categoryName}</span>
        </div>
        <div class="product-body">
            <div class="product-sku">${product.sku}</div>
            <h4 class="product-name" title="${product.product_name}">
                <a href="product-detail.html?id=${product.product_id}" style="color: #fff; text-decoration: none;">${product.product_name}</a>
            </h4>
            <p class="product-desc">${product.description || 'No detailed specifications listed.'}</p>
            <div class="product-meta">
                <div class="price-box">
                    <span class="price-label">Price</span>
                    <span class="price-value"><span>RM</span>${parseFloat(product.selling_price).toFixed(2)}</span>
                </div>
                ${stockBadgeHTML}
            </div>
            <a href="${waLink}" target="_blank" class="btn-whatsapp-product">
                <span>💬</span> Enquire on WhatsApp
            </a>
        </div>
    `;

    return card;
}

function resetFilters() {
    activeCategoryId = "";
    activeCondition = "";
    currentSearchTerm = "";
    activeComponentType = "";
    const searchInput = document.getElementById("searchInput");
    if (searchInput) searchInput.value = "";
    const componentDropdown = document.getElementById("componentDropdown");
    if (componentDropdown) componentDropdown.value = "";
    document.querySelectorAll("#conditionToggles .condition-btn").forEach((b, i) => {
        b.classList.toggle("active", i === 0);
    });
    document.querySelectorAll("#categoryPills .pill").forEach((b, i) => {
        b.classList.toggle("active", i === 0);
    });
    loadProducts();
}
