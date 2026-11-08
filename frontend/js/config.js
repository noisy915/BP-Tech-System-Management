/**
 * BP Tech Inventory Management System
 * [MEMBER 3: JavaScript and Frontend Integration Developer]
 * Client-side Configuration
 */

// Dynamically resolve backend host to match current browser origin (localhost vs 127.0.0.1)
const getApiBaseUrl = () => {
    if (window.location.port === "8000") {
        return `${window.location.origin}/api`;
    }
    const currentHost = (window.location.hostname && window.location.hostname !== "") 
        ? window.location.hostname 
        : "127.0.0.1";
    return `http://${currentHost}:8000/api`;
};

const CONFIG = {
    // Backend API base URL
    API_BASE_URL: getApiBaseUrl(),

    // BP Tech Official WhatsApp Contact (Malaysia country code 60)
    WHATSAPP_PHONE: "60123456789",

    // Shop Information
    SHOP_NAME: "BP Tech Computer Shop",
    SHOP_LOCATION: "Batu Pahat, Johor, Malaysia",

    // Storage Keys
    AUTH_TOKEN_KEY: "bp_tech_admin_token",
    AUTH_USER_KEY: "bp_tech_admin_username"
};
