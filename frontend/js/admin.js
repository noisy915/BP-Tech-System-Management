/**
 * BP Tech Inventory Management System
 * [MEMBER 3: JavaScript and Frontend Integration Developer]
 * Admin Dashboard Functionality & CRUD Operations
 */

let allProducts = [];
let allCategories = [];
let allSuppliers = [];

// ==========================================
// Offline Demo Mock Datasets (Zero-Install Mode)
// ==========================================
const MOCK_CATEGORIES = [
    { category_id: 1, category_name: "Processors" },
    { category_id: 2, category_name: "Graphics Cards" },
    { category_id: 3, category_name: "Motherboards" },
    { category_id: 4, category_name: "RAM" },
    { category_id: 5, category_name: "Storage" },
    { category_id: 6, category_name: "Power Supplies" },
    { category_id: 7, category_name: "PC Accessories" }
];

const MOCK_SUPPLIERS = [
    { supplier_id: 1, supplier_name: "Ban Leong Technologies" },
    { supplier_id: 2, supplier_name: "Ingram Micro Malaysia" },
    { supplier_id: 3, supplier_name: "Tech Data Malaysia" },
    { supplier_id: 4, supplier_name: "BP Tech Trade-In & Direct Sourcing" }
];

const DEFAULT_PRODUCTS = [
    {
        product_id: 1,
        product_name: "AMD Ryzen 5 5600",
        sku: "CPU-AMD-5600-NEW",
        condition: "New",
        selling_price: "529.00",
        description: "6 Cores, 12 Threads, Up to 4.4 GHz Max Boost, Socket AM4, PCIe 4.0 with Wraith Stealth Cooler.",
        image_url: "https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?w=500&auto=format&fit=crop&q=60",
        category_id: 1,
        category: { category_id: 1, category_name: "Processors" },
        supplier_id: 1,
        supplier: { supplier_id: 1, supplier_name: "Ban Leong Technologies" },
        product_status: "Active",
        inventory: { quantity_available: 14, reorder_level: 5, is_low_stock: false }
    },
    {
        product_id: 2,
        product_name: "NVIDIA GeForce RTX 3060 12GB (Used)",
        sku: "GPU-NV-3060-USED-01",
        condition: "Used",
        selling_price: "980.00",
        description: "Stress-tested pass. 12GB GDDR6 VRAM, Ray Tracing, DLSS. 1-Month Store Warranty.",
        image_url: "https://images.unsplash.com/photo-1587202372775-e229f172b9d7?w=500&auto=format&fit=crop&q=60",
        category_id: 2,
        category: { category_id: 2, category_name: "Graphics Cards" },
        supplier_id: 4,
        supplier: { supplier_id: 4, supplier_name: "BP Tech Trade-In & Direct Sourcing" },
        product_status: "Active",
        inventory: { quantity_available: 3, reorder_level: 4, is_low_stock: true }
    },
    {
        product_id: 3,
        product_name: "Kingston FURY Beast 16GB (2x8GB) DDR4 3200MHz",
        sku: "RAM-KST-16GB-3200-NEW",
        condition: "New",
        selling_price: "165.00",
        description: "High-performance low-profile heat spreader, Intel XMP 2.0 ready, AMD Ryzen compatible.",
        image_url: "https://images.unsplash.com/photo-1562976540-1502c2145186?w=500&auto=format&fit=crop&q=60",
        category_id: 4,
        category: { category_id: 4, category_name: "RAM" },
        supplier_id: 2,
        supplier: { supplier_id: 2, supplier_name: "Ingram Micro Malaysia" },
        product_status: "Active",
        inventory: { quantity_available: 25, reorder_level: 8, is_low_stock: false }
    },
    {
        product_id: 4,
        product_name: "Kingston NV2 1TB PCIe 4.0 NVMe M.2 SSD",
        sku: "SSD-KST-NV2-1TB-NEW",
        condition: "New",
        selling_price: "289.00",
        description: "Gen 4x4 NVMe PCIe speed up to 3500MB/s Read, 2100MB/s Write. 3-Year warranty.",
        image_url: "https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?w=500&auto=format&fit=crop&q=60",
        category_id: 5,
        category: { category_id: 5, category_name: "Storage" },
        supplier_id: 1,
        supplier: { supplier_id: 1, supplier_name: "Ban Leong Technologies" },
        product_status: "Active",
        inventory: { quantity_available: 18, reorder_level: 5, is_low_stock: false }
    },
    {
        product_id: 5,
        product_name: "Corsair CV550 550W 80 PLUS Bronze (Used)",
        sku: "PSU-COR-CV550-USED",
        condition: "Used",
        selling_price: "130.00",
        description: "Clean tested power supply with voltage tester check. 1-Month Store Warranty.",
        image_url: "https://images.unsplash.com/photo-1587202372634-32705e3bf49c?w=500&auto=format&fit=crop&q=60",
        category_id: 6,
        category: { category_id: 6, category_name: "Power Supplies" },
        supplier_id: 4,
        supplier: { supplier_id: 4, supplier_name: "BP Tech Trade-In & Direct Sourcing" },
        product_status: "Active",
        inventory: { quantity_available: 1, reorder_level: 4, is_low_stock: true }
    }
];

function getStoredProducts() {
    const raw = localStorage.getItem("bp_tech_products");
    if (raw) {
        try { return JSON.parse(raw); } catch (e) {}
    }
    localStorage.setItem("bp_tech_products", JSON.stringify(DEFAULT_PRODUCTS));
    return DEFAULT_PRODUCTS;
}

function saveStoredProducts(list) {
    localStorage.setItem("bp_tech_products", JSON.stringify(list));
}

function getStoredMovements() {
    const raw = localStorage.getItem("bp_tech_movements");
    if (raw) {
        try { return JSON.parse(raw); } catch (e) {}
    }
    const defaults = [
        { movement_id: 1, product_id: 1, product_name: "AMD Ryzen 5 5600", movement_type: "IN", quantity: 14, movement_date: new Date().toISOString(), remarks: "Initial demo stock" },
        { movement_id: 2, product_id: 2, product_name: "NVIDIA GeForce RTX 3060 12GB (Used)", movement_type: "IN", quantity: 3, movement_date: new Date().toISOString(), remarks: "Trade-in demo stock" },
        { movement_id: 3, product_id: 3, product_name: "Kingston FURY Beast 16GB (2x8GB) DDR4 3200MHz", movement_type: "IN", quantity: 25, movement_date: new Date().toISOString(), remarks: "Supplier restock" }
    ];
    localStorage.setItem("bp_tech_movements", JSON.stringify(defaults));
    return defaults;
}

function saveStoredMovements(list) {
    localStorage.setItem("bp_tech_movements", JSON.stringify(list));
}

document.addEventListener("DOMContentLoaded", async () => {
    // 1. Enforce authentication
    auth.requireAuth();

    // Check offline mode banner
    if (localStorage.getItem("bp_tech_offline_mode") === "true") {
        const banner = document.getElementById("demoModeBanner");
        if (banner) banner.style.display = "flex";
    }

    // 2. Initialize UI components & tabs
    initTabs();
    initModals();
    initAdminSearch();

    // 3. Fetch initial data
    await loadDropdownOptions();
    await refreshAllData();
});

/**
 * Toast Notification Utility
 */
function showToast(message, type = "success") {
    const toast = document.getElementById("toastAlert");
    if (!toast) return;
    toast.textContent = message;
    toast.className = `alert-toast ${type}`;
    setTimeout(() => {
        toast.className = "alert-toast";
    }, 4000);
}

/**
 * Tab Navigation Handler
 */
function initTabs() {
    const tabBtns = document.querySelectorAll(".tab-btn");
    tabBtns.forEach((btn) => {
        btn.addEventListener("click", () => {
            const targetId = btn.getAttribute("data-tab");
            tabBtns.forEach((b) => b.classList.remove("active"));
            btn.classList.add("active");

            document.querySelectorAll(".tab-pane").forEach((pane) => {
                pane.style.display = pane.id === targetId ? "block" : "none";
            });

            if (targetId === "tab-movements") {
                loadStockMovements();
            } else if (targetId === "tab-lowstock") {
                renderLowStockTable();
            }
        });
    });
}

/**
 * Modals and Form Handlers
 */
function initModals() {
    const productModal = document.getElementById("productModal");
    const stockMovementModal = document.getElementById("stockMovementModal");

    // Open Add Product
    document.getElementById("openAddProductModalBtn")?.addEventListener("click", () => {
        document.getElementById("productForm").reset();
        document.getElementById("editProductId").value = "";
        document.getElementById("productModalTitle").textContent = "Add New Product";
        document.getElementById("initialStockGroup").style.display = "grid";
        productModal.classList.add("open");
    });

    // Close Modals
    document.getElementById("closeProductModalBtn")?.addEventListener("click", () => productModal.classList.remove("open"));
    document.getElementById("cancelProductBtn")?.addEventListener("click", () => productModal.classList.remove("open"));
    document.getElementById("closeMovementModalBtn")?.addEventListener("click", () => stockMovementModal.classList.remove("open"));
    document.getElementById("cancelMovementBtn")?.addEventListener("click", () => stockMovementModal.classList.remove("open"));

    // Submit Product Form
    document.getElementById("productForm")?.addEventListener("submit", handleProductSubmit);

    // Submit Stock Movement Form
    document.getElementById("movementForm")?.addEventListener("submit", handleMovementSubmit);
}

/**
 * Admin Search Filter
 */
function initAdminSearch() {
    const searchInput = document.getElementById("adminSearchInput");
    if (!searchInput) return;

    searchInput.addEventListener("input", (e) => {
        const query = e.target.value.toLowerCase().trim();
        const filtered = allProducts.filter((p) => {
            return (
                p.product_name.toLowerCase().includes(query) ||
                p.sku.toLowerCase().includes(query) ||
                (p.category && p.category.category_name.toLowerCase().includes(query))
            );
        });
        renderInventoryTable(filtered);
    });
}

/**
 * Load Category and Supplier Dropdowns
 */
async function loadDropdownOptions() {
    try {
        allCategories = await api.getCategories();
    } catch (err) {
        console.warn("Using offline categories:", err);
        allCategories = MOCK_CATEGORIES;
    }
    const catSelect = document.getElementById("prodCategory");
    if (catSelect) {
        catSelect.innerHTML = `<option value="">Select Category</option>` +
            allCategories.map(c => `<option value="${c.category_id}">${c.category_name}</option>`).join("");
    }

    try {
        allSuppliers = await api.getSuppliers();
    } catch (err) {
        console.warn("Using offline suppliers:", err);
        allSuppliers = MOCK_SUPPLIERS;
    }
    const supSelect = document.getElementById("prodSupplier");
    if (supSelect) {
        supSelect.innerHTML = `<option value="">None / Direct Import</option>` +
            allSuppliers.map(s => `<option value="${s.supplier_id}">${s.supplier_name}</option>`).join("");
    }
}

/**
 * Refresh Products, Inventory & Stat Counters
 */
async function refreshAllData() {
    try {
        allProducts = await api.getProducts({ include_discontinued: true });
    } catch (err) {
        console.warn("Backend unavailable, loading local offline inventory:", err);
        allProducts = getStoredProducts();
        const banner = document.getElementById("demoModeBanner");
        if (banner) banner.style.display = "flex";
    }
    renderInventoryTable(allProducts);
    updateStatCounters();
}

/**
 * Render Inventory Table
 */
function renderInventoryTable(products) {
    const tbody = document.getElementById("inventoryTableBody");
    if (!tbody) return;

    if (products.length === 0) {
        tbody.innerHTML = `<tr><td colspan="8" style="text-align: center; color: var(--text-muted); padding: 30px;">No products found matching criteria.</td></tr>`;
        return;
    }

    tbody.innerHTML = products.map((p) => {
        const qty = p.inventory ? p.inventory.quantity_available : 0;
        const reorder = p.inventory ? p.inventory.reorder_level : 5;
        const isLow = qty <= reorder;

        let stockBadge = `<span class="stock-status stock-in"><span class="stock-dot"></span> ${qty} units</span>`;
        if (qty <= 0) {
            stockBadge = `<span class="stock-status stock-out"><span class="stock-dot"></span> Out of Stock (0)</span>`;
        } else if (isLow) {
            stockBadge = `<span class="stock-status stock-low"><span class="stock-dot"></span> Low (${qty} / min ${reorder})</span>`;
        }

        const conditionClass = p.condition === "New" ? "badge-new" : "badge-used";
        const statusBadge = p.product_status === "Active" 
            ? `<span style="color: var(--accent-green); font-size: 0.8rem; font-weight: 700;">● Active</span>` 
            : `<span style="color: var(--text-muted); font-size: 0.8rem; font-weight: 700;">○ Discontinued</span>`;

        return `
            <tr>
                <td><code style="color: var(--accent-cyan); font-weight: 700;">${p.sku}</code></td>
                <td>
                    <div style="font-weight: 600; color: #fff;">${p.product_name}</div>
                </td>
                <td>${p.category ? p.category.category_name : '-'}</td>
                <td><span class="badge ${conditionClass}">${p.condition}</span></td>
                <td><strong>RM ${parseFloat(p.selling_price).toFixed(2)}</strong></td>
                <td>${stockBadge}</td>
                <td>${statusBadge}</td>
                <td>
                    <div class="action-btn-group">
                        <button class="btn-sm btn-stock" onclick="openStockMovementModal(${p.product_id}, '${escapeQuote(p.product_name)}')">📦 Movement</button>
                        <button class="btn-sm btn-edit" onclick="openEditProductModal(${p.product_id})">✏️ Edit</button>
                        ${p.product_status === 'Active' ? `<button class="btn-sm btn-discontinue" onclick="discontinueProduct(${p.product_id})">⛔ Discontinue</button>` : ''}
                    </div>
                </td>
            </tr>
        `;
    }).join("");
}

/**
 * Update Metric Cards
 */
function updateStatCounters() {
    const totalProducts = allProducts.length;
    let totalStock = 0;
    let lowStockCount = 0;

    allProducts.forEach((p) => {
        if (p.inventory) {
            totalStock += p.inventory.quantity_available || 0;
            if (p.inventory.quantity_available <= p.inventory.reorder_level) {
                lowStockCount++;
            }
        }
    });

    document.getElementById("statTotalProducts").textContent = totalProducts;
    document.getElementById("statTotalStock").textContent = totalStock;
    document.getElementById("statLowStock").textContent = lowStockCount;

    // Fetch movements count
    api.getStockMovements(null, 1).then(() => {
        document.getElementById("statMovements").textContent = "Active";
    }).catch(() => {
        const localLogs = getStoredMovements();
        document.getElementById("statMovements").textContent = localLogs.length;
    });
}

/**
 * Handle Add or Edit Product Submit
 */
async function handleProductSubmit(e) {
    e.preventDefault();
    const editId = document.getElementById("editProductId").value;

    const payload = {
        product_name: document.getElementById("prodName").value.trim(),
        sku: document.getElementById("prodSku").value.trim().toUpperCase(),
        category_id: parseInt(document.getElementById("prodCategory").value),
        supplier_id: document.getElementById("prodSupplier").value ? parseInt(document.getElementById("prodSupplier").value) : null,
        condition: document.getElementById("prodCondition").value,
        selling_price: parseFloat(document.getElementById("prodPrice").value),
        image_url: document.getElementById("prodImageUrl").value.trim() || null,
        description: document.getElementById("prodDesc").value.trim() || null,
        product_status: "Active"
    };

    try {
        if (editId) {
            await api.updateProduct(editId, payload);
            showToast("Product listing updated successfully!");
        } else {
            payload.initial_stock = parseInt(document.getElementById("prodInitialStock").value) || 0;
            payload.reorder_level = parseInt(document.getElementById("prodReorderLevel").value) || 5;
            await api.createProduct(payload);
            showToast("New product created with synchronized inventory!");
        }

        document.getElementById("productModal").classList.remove("open");
        await refreshAllData();
    } catch (err) {
        // Offline demo storage fallback
        console.warn("Saving product locally in demo mode:", err);
        const stored = getStoredProducts();
        const cat = allCategories.find(c => c.category_id === payload.category_id) || { category_name: "Hardware" };
        const sup = allSuppliers.find(s => s.supplier_id === payload.supplier_id) || null;

        if (editId) {
            const index = stored.findIndex(p => p.product_id == editId);
            if (index !== -1) {
                stored[index] = {
                    ...stored[index],
                    ...payload,
                    category: cat,
                    supplier: sup
                };
            }
            showToast("Demo Mode: Product updated successfully!");
        } else {
            const newId = stored.length ? Math.max(...stored.map(p => p.product_id)) + 1 : 1;
            const initQty = parseInt(document.getElementById("prodInitialStock").value) || 0;
            const minReorder = parseInt(document.getElementById("prodReorderLevel").value) || 5;
            const newProduct = {
                product_id: newId,
                ...payload,
                category: cat,
                supplier: sup,
                inventory: {
                    quantity_available: initQty,
                    reorder_level: minReorder,
                    is_low_stock: initQty <= minReorder
                }
            };
            stored.unshift(newProduct);
            showToast("Demo Mode: New product added to local inventory!");
        }
        saveStoredProducts(stored);
        document.getElementById("productModal").classList.remove("open");
        await refreshAllData();
    }
}

/**
 * Open Edit Product Modal
 */
window.openEditProductModal = function(productId) {
    const p = allProducts.find(item => item.product_id === productId);
    if (!p) return;

    document.getElementById("editProductId").value = p.product_id;
    document.getElementById("productModalTitle").textContent = "Edit Product Details";
    document.getElementById("prodName").value = p.product_name;
    document.getElementById("prodSku").value = p.sku;
    document.getElementById("prodCategory").value = p.category_id;
    document.getElementById("prodSupplier").value = p.supplier_id || "";
    document.getElementById("prodCondition").value = p.condition;
    document.getElementById("prodPrice").value = p.selling_price;
    document.getElementById("prodImageUrl").value = p.image_url || "";
    document.getElementById("prodDesc").value = p.description || "";

    // Hide initial stock inputs when editing existing product
    document.getElementById("initialStockGroup").style.display = "none";

    document.getElementById("productModal").classList.add("open");
};

/**
 * Open Stock Movement Modal
 */
window.openStockMovementModal = function(productId, productName) {
    document.getElementById("movementForm").reset();
    document.getElementById("moveProductId").value = productId;
    document.getElementById("moveProductName").value = productName;
    document.getElementById("stockMovementModal").classList.add("open");
};

/**
 * Submit Stock Movement
 */
async function handleMovementSubmit(e) {
    e.preventDefault();
    const productId = parseInt(document.getElementById("moveProductId").value);
    const movementType = document.getElementById("moveType").value;
    const quantity = parseInt(document.getElementById("moveQuantity").value);
    const remarks = document.getElementById("moveRemarks").value.trim() || null;

    if (!quantity || quantity <= 0) {
        alert("Quantity must be greater than zero.");
        return;
    }

    try {
        await api.recordStockMovement({
            product_id: productId,
            movement_type: movementType,
            quantity: quantity,
            remarks: remarks
        });

        showToast(`Stock transaction (${movementType}) recorded successfully!`);
        document.getElementById("stockMovementModal").classList.remove("open");
        await refreshAllData();
    } catch (err) {
        // Offline demo fallback
        console.warn("Recording stock movement locally in demo mode:", err);
        const stored = getStoredProducts();
        const prod = stored.find(p => p.product_id === productId);
        if (prod) {
            if (!prod.inventory) prod.inventory = { quantity_available: 0, reorder_level: 5 };
            if (movementType === "IN") {
                prod.inventory.quantity_available += quantity;
            } else if (movementType === "OUT") {
                prod.inventory.quantity_available = Math.max(0, prod.inventory.quantity_available - quantity);
            } else if (movementType === "ADJUSTMENT") {
                prod.inventory.quantity_available = quantity;
            }
            prod.inventory.is_low_stock = prod.inventory.quantity_available <= prod.inventory.reorder_level;
            saveStoredProducts(stored);

            const movements = getStoredMovements();
            movements.unshift({
                movement_id: movements.length ? Math.max(...movements.map(m => m.movement_id)) + 1 : 1,
                product_id: productId,
                product_name: prod.product_name,
                movement_type: movementType,
                quantity: quantity,
                movement_date: new Date().toISOString(),
                remarks: remarks || "Demo movement"
            });
            saveStoredMovements(movements);

            showToast(`Demo Mode: Stock transaction (${movementType}) recorded!`);
            document.getElementById("stockMovementModal").classList.remove("open");
            await refreshAllData();
        } else {
            alert("Product not found.");
        }
    }
}

/**
 * Discontinue / Soft-Delete Product
 */
window.discontinueProduct = async function(productId) {
    if (confirm("Are you sure you want to discontinue this product? It will be archived and hidden from public search while preserving stock movement logs.")) {
        try {
            await api.deleteProduct(productId);
            showToast("Product marked as Discontinued.");
            await refreshAllData();
        } catch (err) {
            const stored = getStoredProducts();
            const prod = stored.find(p => p.product_id === productId);
            if (prod) {
                prod.product_status = "Discontinued";
                saveStoredProducts(stored);
                showToast("Demo Mode: Product marked as Discontinued.");
                await refreshAllData();
            }
        }
    }
};

/**
 * Load Stock Movement Logs
 */
async function loadStockMovements() {
    const tbody = document.getElementById("movementsTableBody");
    if (!tbody) return;

    tbody.innerHTML = `<tr><td colspan="6" style="text-align: center; color: var(--text-muted); padding: 30px;">Loading audit logs...</td></tr>`;

    let logs = [];
    try {
        logs = await api.getStockMovements(null, 50);
    } catch (err) {
        console.warn("Using offline stock movement logs:", err);
        logs = getStoredMovements();
    }

    if (logs.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6" style="text-align: center; color: var(--text-muted); padding: 30px;">No movement history recorded yet.</td></tr>`;
        return;
    }

    tbody.innerHTML = logs.map(m => {
        let typeBadge = `<span style="color: var(--accent-green); font-weight: bold;">[IN] Addition</span>`;
        if (m.movement_type === "OUT") {
            typeBadge = `<span style="color: var(--accent-red); font-weight: bold;">[OUT] Deduction</span>`;
        } else if (m.movement_type === "ADJUSTMENT") {
            typeBadge = `<span style="color: var(--accent-amber); font-weight: bold;">[ADJUSTMENT] Set Qty</span>`;
        }

        const dt = new Date(m.movement_date).toLocaleString();
        return `
            <tr>
                <td>#${m.movement_id}</td>
                <td>${dt}</td>
                <td><strong>${m.product_name || `Product ID #${m.product_id}`}</strong></td>
                <td>${typeBadge}</td>
                <td><strong>${m.quantity}</strong></td>
                <td style="color: var(--text-secondary);">${m.remarks || '-'}</td>
            </tr>
        `;
    }).join("");
}

/**
 * Render Low Stock Alerts Table
 */
function renderLowStockTable() {
    const tbody = document.getElementById("lowStockTableBody");
    if (!tbody) return;

    const lowStockItems = allProducts.filter(p => p.inventory && p.inventory.quantity_available <= p.inventory.reorder_level);

    if (lowStockItems.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6" style="text-align: center; color: var(--accent-green); padding: 30px;">✅ All inventory quantities are healthy above reorder thresholds!</td></tr>`;
        return;
    }

    tbody.innerHTML = lowStockItems.map(p => {
        const qty = p.inventory.quantity_available;
        const reorder = p.inventory.reorder_level;
        return `
            <tr>
                <td><code style="color: var(--accent-cyan);">${p.sku}</code></td>
                <td><strong>${p.product_name}</strong></td>
                <td><span style="color: var(--accent-amber); font-weight: 800; font-size: 1.1rem;">${qty}</span> units remaining</td>
                <td>Min ${reorder} units</td>
                <td>${p.supplier ? p.supplier.supplier_name : 'Direct'}</td>
                <td>
                    <button class="btn-sm btn-stock" onclick="openStockMovementModal(${p.product_id}, '${escapeQuote(p.product_name)}')">+ Add Inbound Stock</button>
                </td>
            </tr>
        `;
    }).join("");
}

function escapeQuote(str) {
    return str.replace(/'/g, "\\'");
}
