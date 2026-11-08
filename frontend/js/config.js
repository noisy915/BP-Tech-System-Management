/**
 * BP Tech Inventory Management System
 * [MEMBER 3: JavaScript and Frontend Integration Developer]
 * Client-side Configuration
 */

const CONFIG = {
    // Backend API base URL
    // When served via FastAPI static mount (/app), uses relative /api; otherwise connects to port 8000
    API_BASE_URL: window.location.port === "8000" 
        ? `${window.location.origin}/api` 
        : "http://127.0.0.1:8000/api",

    // BP Tech Official WhatsApp Contact (format: CountryCode + Number without + or 0)
    // 60 = Malaysia
    WHATSAPP_PHONE: "60123456789",

    // Shop Information
    SHOP_NAME: "BP Tech Computer Shop",
    SHOP_LOCATION: "Batu Pahat, Johor, Malaysia",

    // Storage Keys
    AUTH_TOKEN_KEY: "bp_tech_admin_token",
    AUTH_USER_KEY: "bp_tech_admin_username"
};
