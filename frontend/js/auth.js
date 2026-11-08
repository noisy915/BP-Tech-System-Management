/**
 * BP Tech Inventory Management System
 * [MEMBER 3: JavaScript and Frontend Integration Developer]
 * Admin Authentication & Session Management
 */

const auth = {
    /**
     * Check if administrator is logged in
     */
    isAuthenticated() {
        return !!localStorage.getItem(CONFIG.AUTH_TOKEN_KEY);
    },

    /**
     * Check if running in offline demo mode
     */
    isOfflineMode() {
        return localStorage.getItem("bp_tech_offline_mode") === "true";
    },

    /**
     * Get active admin username
     */
    getUsername() {
        return localStorage.getItem(CONFIG.AUTH_USER_KEY) || "Administrator";
    },

    /**
     * Log out administrator and clear storage
     */
    logout() {
        localStorage.removeItem(CONFIG.AUTH_TOKEN_KEY);
        localStorage.removeItem(CONFIG.AUTH_USER_KEY);
        localStorage.removeItem("bp_tech_offline_mode");
        window.location.href = "admin-login.html";
    },

    /**
     * Protect admin dashboard: Redirect if not authenticated
     */
    requireAuth() {
        if (!this.isAuthenticated()) {
            window.location.href = "admin-login.html";
        }
    }
};

// Handle Login Page Logic
document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("loginForm");
    const loginAlert = document.getElementById("loginAlert");
    const loginBtn = document.getElementById("loginBtn");

    if (loginForm) {
        // If already logged in, redirect directly to dashboard
        if (auth.isAuthenticated()) {
            window.location.href = "admin-dashboard.html";
            return;
        }

        loginForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const username = document.getElementById("username").value.trim();
            const password = document.getElementById("password").value;

            if (!username || !password) return;

            loginBtn.disabled = true;
            loginBtn.textContent = "Authenticating...";
            loginAlert.style.display = "none";

            try {
                // 1. Attempt authentication with FastAPI backend
                const data = await api.login(username, password);
                localStorage.setItem(CONFIG.AUTH_TOKEN_KEY, data.access_token);
                localStorage.setItem(CONFIG.AUTH_USER_KEY, data.username);
                localStorage.removeItem("bp_tech_offline_mode");
                window.location.href = "admin-dashboard.html";
            } catch (err) {
                console.warn("Backend API login attempt failed:", err);

                // Detect network / fetch failure (backend server not started or connection refused)
                const isNetworkError = !err.message || 
                    err.message.includes("Failed to fetch") || 
                    err.message.includes("NetworkError") || 
                    err.message.includes("Load failed") ||
                    err.name === "TypeError";

                if (isNetworkError) {
                    // Check default admin demo credentials
                    if (username === "admin" && password === "admin123") {
                        localStorage.setItem(CONFIG.AUTH_TOKEN_KEY, "bp_tech_demo_token");
                        localStorage.setItem(CONFIG.AUTH_USER_KEY, "admin");
                        localStorage.setItem("bp_tech_offline_mode", "true");
                        window.location.href = "admin-dashboard.html";
                        return;
                    }

                    loginAlert.innerHTML = `
                        <strong>⚠️ Backend Server Offline:</strong><br>
                        Cannot connect to <code>${CONFIG.API_BASE_URL}</code>.<br><br>
                        <strong>To connect live database:</strong><br>
                        Run <code>uvicorn main:app --reload</code> in the <code>backend/</code> folder.<br><br>
                        <strong>To preview offline:</strong><br>
                        Sign in with Username: <strong>admin</strong> | Password: <strong>admin123</strong>
                    `;
                    loginAlert.style.display = "block";
                } else {
                    // Backend responded but credentials rejected (e.g. 401 Unauthorized)
                    loginAlert.textContent = err.message || "Invalid administrator credentials. Please check your username and password.";
                    loginAlert.style.display = "block";
                }
            } finally {
                loginBtn.disabled = false;
                loginBtn.textContent = "Sign In to Dashboard";
            }
        });
    }

    // Handle Admin Dashboard Logout Button
    const logoutBtn = document.getElementById("logoutBtn");
    if (logoutBtn) {
        logoutBtn.addEventListener("click", () => {
            if (confirm("Are you sure you want to log out from the administrator portal?")) {
                auth.logout();
            }
        });
    }

    // Display admin greeting if on dashboard
    const adminGreeting = document.getElementById("adminUserGreeting");
    if (adminGreeting) {
        const modeBadge = auth.isOfflineMode() ? " (Demo Mode)" : "";
        adminGreeting.textContent = `Logged in as: ${auth.getUsername()}${modeBadge}`;
    }
});
