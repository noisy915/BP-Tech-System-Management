/**
 * BP Tech Inventory Management System
 * [MEMBER 3: JavaScript and Frontend Integration Developer]
 * Central API Client Helper using Fetch API
 */

const api = {
    /**
     * Get authorized headers if admin token exists
     */
    getHeaders(isJSON = true) {
        const headers = {};
        if (isJSON) {
            headers["Content-Type"] = "application/json";
        }
        const token = localStorage.getItem(CONFIG.AUTH_TOKEN_KEY);
        if (token) {
            headers["Authorization"] = `Bearer ${token}`;
        }
        return headers;
    },

    /**
     * Generic fetch wrapper with error handling
     */
    async request(endpoint, options = {}) {
        const url = `${CONFIG.API_BASE_URL}${endpoint}`;
        try {
            const response = await fetch(url, options);

            // Handle unauthorized redirect
            if (response.status === 401 && !url.includes("/auth/login")) {
                localStorage.removeItem(CONFIG.AUTH_TOKEN_KEY);
                localStorage.removeItem(CONFIG.AUTH_USER_KEY);
                if (window.location.pathname.includes("admin-dashboard")) {
                    window.location.href = "admin-login.html";
                }
            }

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || `HTTP Error ${response.status}: ${response.statusText}`);
            }

            if (response.status === 204) {
                return null;
            }

            return await response.json();
        } catch (error) {
            console.error(`API Request failed [${endpoint}]:`, error);
            throw error;
        }
    },

    // ==========================================
    // Authentication Endpoints
    // ==========================================
    async login(username, password) {
        return this.request("/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });
    },

    async getMe() {
        return this.request("/auth/me", {
            headers: this.getHeaders()
        });
    },

    // ==========================================
    // Products Endpoints
    // ==========================================
    async getProducts({ category_id = null, condition = null, search = null, status = null } = {}) {
        const params = new URLSearchParams();
        if (category_id) params.append("category_id", category_id);
        if (condition) params.append("condition", condition);
        if (search) params.append("search", search);
        if (status) params.append("status", status);

        const query = params.toString() ? `?${params.toString()}` : "";
        return this.request(`/products${query}`);
    },

    async getProduct(productId) {
        return this.request(`/products/${productId}`);
    },

    async createProduct(productData) {
        return this.request("/products", {
            method: "POST",
            headers: this.getHeaders(),
            body: JSON.stringify(productData)
        });
    },

    async updateProduct(productId, productData) {
        return this.request(`/products/${productId}`, {
            method: "PUT",
            headers: this.getHeaders(),
            body: JSON.stringify(productData)
        });
    },

    async deleteProduct(productId, force = false) {
        return this.request(`/products/${productId}?force=${force}`, {
            method: "DELETE",
            headers: this.getHeaders()
        });
    },

    // ==========================================
    // Categories Endpoints
    // ==========================================
    async getCategories() {
        return this.request("/categories");
    },

    async createCategory(categoryData) {
        return this.request("/categories", {
            method: "POST",
            headers: this.getHeaders(),
            body: JSON.stringify(categoryData)
        });
    },

    // ==========================================
    // Suppliers Endpoints
    // ==========================================
    async getSuppliers() {
        return this.request("/suppliers", {
            headers: this.getHeaders()
        });
    },

    async createSupplier(supplierData) {
        return this.request("/suppliers", {
            method: "POST",
            headers: this.getHeaders(),
            body: JSON.stringify(supplierData)
        });
    },

    // ==========================================
    // Inventory Endpoints
    // ==========================================
    async getInventory(lowStockOnly = false) {
        const query = lowStockOnly ? "?low_stock_only=true" : "";
        return this.request(`/inventory${query}`, {
            headers: this.getHeaders()
        });
    },

    async updateInventory(inventoryId, invData) {
        return this.request(`/inventory/${inventoryId}`, {
            method: "PUT",
            headers: this.getHeaders(),
            body: JSON.stringify(invData)
        });
    },

    // ==========================================
    // Stock Movements Endpoints
    // ==========================================
    async getStockMovements(productId = null, limit = 50) {
        const params = new URLSearchParams();
        if (productId) params.append("product_id", productId);
        params.append("limit", limit);
        return this.request(`/stock-movements?${params.toString()}`, {
            headers: this.getHeaders()
        });
    },

    async recordStockMovement(movementData) {
        return this.request("/stock-movements", {
            method: "POST",
            headers: this.getHeaders(),
            body: JSON.stringify(movementData)
        });
    }
};
