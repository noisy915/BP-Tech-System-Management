const CART_STORAGE_KEY = "bp_tech_cart";

function getCart() {
    try {
        const stored = localStorage.getItem(CART_STORAGE_KEY);
        return stored ? JSON.parse(stored) : [];
    } catch (e) {
        return [];
    }
}

function saveCart(cart) {
    try {
        localStorage.setItem(CART_STORAGE_KEY, JSON.stringify(cart));
    } catch (e) {}
    updateCartUI();
}

function addToCart(product, openDrawer = false) {
    const cart = getCart();
    const maxStock = product.inventory ? product.inventory.quantity_available : 99;

    if (maxStock <= 0) {
        alert("Sorry, this component is currently out of stock.");
        return;
    }

    const existing = cart.find((item) => item.product_id == product.product_id);
    if (existing) {
        if (existing.quantity < maxStock) {
            existing.quantity += 1;
        } else {
            alert(`Maximum available stock (${maxStock}) reached for this item.`);
        }
    } else {
        cart.push({
            product_id: product.product_id,
            product_name: product.product_name,
            sku: product.sku,
            condition: product.condition,
            selling_price: parseFloat(product.selling_price),
            image_url: product.image_url,
            quantity: 1,
            max_stock: maxStock
        });
    }

    saveCart(cart);
    if (openDrawer) {
        openCartDrawer();
    }
}

function buyNow(product) {
    addToCart(product, true);
}

function updateCartQty(productId, delta) {
    let cart = getCart();
    const item = cart.find((i) => i.product_id == productId);
    if (!item) return;

    item.quantity += delta;
    if (item.quantity <= 0) {
        cart = cart.filter((i) => i.product_id != productId);
    } else if (item.max_stock && item.quantity > item.max_stock) {
        item.quantity = item.max_stock;
        alert(`Only ${item.max_stock} unit(s) available in stock.`);
    }
    saveCart(cart);
}

function removeFromCart(productId) {
    const cart = getCart().filter((i) => i.product_id != productId);
    saveCart(cart);
}

function clearCart() {
    saveCart([]);
}

function toggleCartDrawer() {
    const drawer = document.getElementById("cartDrawer");
    const overlay = document.getElementById("cartOverlay");
    if (!drawer || !overlay) return;
    drawer.classList.toggle("open");
    overlay.classList.toggle("open");
}

function openCartDrawer() {
    const drawer = document.getElementById("cartDrawer");
    const overlay = document.getElementById("cartOverlay");
    if (drawer && overlay) {
        drawer.classList.add("open");
        overlay.classList.add("open");
    }
}

function updateCartUI() {
    const cart = getCart();
    const totalCount = cart.reduce((sum, item) => sum + item.quantity, 0);
    const totalPrice = cart.reduce((sum, item) => sum + item.selling_price * item.quantity, 0);

    const badge = document.getElementById("cartCountBadge");
    if (badge) badge.textContent = totalCount;

    const totalEl = document.getElementById("cartTotalPrice");
    if (totalEl) totalEl.textContent = `RM ${totalPrice.toFixed(2)}`;

    const container = document.getElementById("cartItemsContainer");
    if (!container) return;

    if (cart.length === 0) {
        container.innerHTML = `<div class="cart-empty-msg">Your cart is empty. Browse components and click "Add to Cart" or "Buy Now".</div>`;
        return;
    }

    container.innerHTML = cart
        .map(
            (item) => `
        <div class="cart-item">
            <img src="${item.image_url || 'https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?w=500'}" alt="${item.product_name}" class="cart-item-img">
            <div class="cart-item-info">
                <div class="cart-item-title">${item.product_name}</div>
                <div class="cart-item-meta">${item.condition} • RM ${item.selling_price.toFixed(2)}</div>
                <div class="cart-qty-controls">
                    <button type="button" onclick="updateCartQty(${item.product_id}, -1)">−</button>
                    <span>${item.quantity}</span>
                    <button type="button" onclick="updateCartQty(${item.product_id}, 1)">+</button>
                    <button type="button" class="cart-remove-link" onclick="removeFromCart(${item.product_id})">Remove</button>
                </div>
            </div>
        </div>
    `
        )
        .join("");
}

function checkoutCartWhatsApp() {
    const cart = getCart();
    if (cart.length === 0) {
        alert("Your cart is empty!");
        return;
    }

    const phone = typeof CONFIG !== "undefined" && CONFIG.WHATSAPP_PHONE ? CONFIG.WHATSAPP_PHONE : "60123456789";
    let total = 0;
    let lines = ["Hi BP Tech, I would like to purchase the following items from my cart:", ""];

    cart.forEach((item, index) => {
        const sub = item.selling_price * item.quantity;
        total += sub;
        lines.push(`${index + 1}. ${item.product_name} (${item.condition}) x${item.quantity} - RM ${sub.toFixed(2)}`);
    });

    lines.push("");
    lines.push(`*Total Order Amount: RM ${total.toFixed(2)}*`);
    lines.push("Please confirm stock availability and payment details.");

    const url = `https://wa.me/${phone}?text=${encodeURIComponent(lines.join("\n"))}`;
    window.open(url, "_blank");
}

document.addEventListener("DOMContentLoaded", updateCartUI);