/**
 * BP Tech Inventory Management System
 * [MEMBER 3: JavaScript and Frontend Integration Developer]
 * WhatsApp Enquiry Module
 * Generates direct chat links with pre-filled enquiry messages
 */

const whatsapp = {
    /**
     * Generate WhatsApp chat link with an enquiry message for a specific product
     */
    getProductLink(productName, condition, price) {
        const priceFormatted = parseFloat(price).toFixed(2);
        const message = `Hi ${CONFIG.SHOP_NAME}, I saw the following item on your website catalogue and would like to enquire:\n\n` +
            `🖥️ *Product:* ${productName}\n` +
            `🏷️ *Condition:* ${condition}\n` +
            `💰 *Price:* RM ${priceFormatted}\n\n` +
            `Is this currently available in your Batu Pahat shop for pickup / delivery? Thank you!`;

        return `https://wa.me/${CONFIG.WHATSAPP_PHONE}?text=${encodeURIComponent(message)}`;
    },

    /**
     * Generate WhatsApp link for Custom PC building request
     */
    getCustomPCLink(budget = "flexible", specs = "Gaming / Workstation") {
        const message = `Hi ${CONFIG.SHOP_NAME}, I would like to request a quote and recommendation for a *Custom PC Build*:\n\n` +
            `🎯 *Target Usage:* ${specs}\n` +
            `💵 *Estimated Budget:* ${budget}\n\n` +
            `Could your technician suggest a parts list? Thank you!`;

        return `https://wa.me/${CONFIG.WHATSAPP_PHONE}?text=${encodeURIComponent(message)}`;
    },

    /**
     * General enquiry link
     */
    getGeneralEnquiryLink() {
        const message = `Hi ${CONFIG.SHOP_NAME}, I am browsing your online catalogue and have a general enquiry regarding PC components and services.`;
        return `https://wa.me/${CONFIG.WHATSAPP_PHONE}?text=${encodeURIComponent(message)}`;
    }
};
