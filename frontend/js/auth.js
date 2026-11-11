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
                const data = await api.login(username, password);
                localStorage.setItem(CONFIG.AUTH_TOKEN_KEY, data.access_token);
                localStorage.setItem(CONFIG.AUTH_USER_KEY, data.username);
                localStorage.removeItem("bp_tech_offline_mode");
                window.location.href = "admin-dashboard.html";
            } catch (err) {
                const isNetworkError = !err.message || err.message.includes("fetch") || err.message.includes("NetworkError");
                
                // Offline Demo Mode Fallback (Works with 0 installations!)
                if (isNetworkError && username.toLowerCase() === "admin" && password === "admin123") {
                    localStorage.setItem(CONFIG.AUTH_TOKEN_KEY, "demo_offline_token_2026");
                    localStorage.setItem(CONFIG.AUTH_USER_KEY, "admin (Demo Mode)");
                    localStorage.setItem("bp_tech_offline_mode", "true");
                    window.location.href = "admin-dashboard.html";
                    return;
                }

                if (isNetworkError) {
                    loginAlert.innerHTML = `⚠️ <strong>Backend Server Offline:</strong><br>No Python/PostgreSQL server detected on port 8000.<br>You can still log in using Demo Credentials: <code>admin</code> / <code>admin123</code>`;
                } else {
                    loginAlert.textContent = err.message || "Invalid administrator credentials. Please try again.";
                }
                loginAlert.style.display = "block";
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
        adminGreeting.textContent = `Logged in as: ${auth.getUsername()}`;
    }
});
