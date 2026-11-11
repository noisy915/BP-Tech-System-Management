"""
BP Tech Inventory Management System
[MEMBER 1: Backend and Database Developer]
Database Seeder Script: Initializes tables and populates real BP Tech pricelist data.
Run from backend/ directory: python -m app.seed_data
Updated: 2026-11-12 — Full pricelist sync from BP Tech Price Sheet (10/11/2026)
"""

from decimal import Decimal
from app.database import Base, engine, SessionLocal
from app.models import Category, Supplier, Product, Inventory, StockMovement, Admin
from app.auth_utils import get_password_hash
from app.config import (
    DEFAULT_ADMIN_USERNAME,
    DEFAULT_ADMIN_PASSWORD,
    DEFAULT_ADMIN_EMAIL,
)


def seed_database():
    print("Creating all tables in database...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # ─────────────────────────────────────────
        # 1. ADMIN
        # ─────────────────────────────────────────
        admin = db.query(Admin).filter(Admin.username == DEFAULT_ADMIN_USERNAME).first()
        if not admin:
            admin = Admin(
                username=DEFAULT_ADMIN_USERNAME,
                hashed_password=get_password_hash(DEFAULT_ADMIN_PASSWORD),
                email=DEFAULT_ADMIN_EMAIL,
            )
            db.add(admin)
            print(f"Created default admin: {DEFAULT_ADMIN_USERNAME} / {DEFAULT_ADMIN_PASSWORD}")

        # ─────────────────────────────────────────
        # 2. CATEGORIES
        # ─────────────────────────────────────────
        categories_data = [
            {"name": "GPU",           "desc": "Graphics cards — new and used, NVIDIA GeForce series. Trade-in accepted."},
            {"name": "CPU",           "desc": "Processors — AMD Ryzen (AM4/AM5) and Intel. Trade-in accepted."},
            {"name": "Motherboard",   "desc": "Motherboards — AM4, AM5, Intel DDR4 and DDR5 platforms. Trade-in accepted."},
            {"name": "RAM",           "desc": "Memory — DDR4, DDR5 desktop and SODIMM laptop RAM."},
            {"name": "SSD",           "desc": "Solid State Drives — SATA 2.5\" and NVMe M.2."},
            {"name": "HDD",           "desc": "Hard Disk Drives — 2.5\" and 3.5\" storage."},
            {"name": "PSU",           "desc": "Power Supply Units — 80 PLUS certified, various wattages."},
            {"name": "Case",          "desc": "PC cases — Micro-ATX and Mid-Tower with fan bundles."},
            {"name": "CPU Cooler",    "desc": "Air coolers and AIO liquid coolers for CPU."},
            {"name": "Monitor",       "desc": "PC monitors — FHD IPS panels with high refresh rates."},
            {"name": "Fan",           "desc": "Case fans and laptop cooling fans — ARGB and USB magic fans."},
            {"name": "Keyboard",      "desc": "Gaming and mechanical keyboards."},
            {"name": "Mouse",         "desc": "Wired and wireless gaming mice."},
            {"name": "Headset",       "desc": "Gaming headsets — wired and wireless."},
            {"name": "Speaker",       "desc": "PC speakers."},
            {"name": "Controller",    "desc": "Gaming controllers — wired and wireless."},
            {"name": "Accessories",   "desc": "Miscellaneous PC accessories, cables, adapters, and thermal compounds."},
        ]

        cat_map = {}
        for c in categories_data:
            existing = db.query(Category).filter(Category.category_name == c["name"]).first()
            if not existing:
                existing = Category(category_name=c["name"], description=c["desc"])
                db.add(existing)
                db.flush()
            cat_map[c["name"]] = existing

        # ─────────────────────────────────────────
        # 3. SUPPLIERS
        # ─────────────────────────────────────────
        suppliers_data = [
            {
                "name": "Ban Leong Technologies",
                "phone": "+603-7956-6300",
                "email": "sales@banleong.com.my",
                "address": "Petaling Jaya, Selangor, Malaysia",
            },
            {
                "name": "Ingram Micro Malaysia",
                "phone": "+603-7952-8188",
                "email": "orders@ingrammicro.com.my",
                "address": "Kuala Lumpur, Malaysia",
            },
            {
                "name": "Tech Data Malaysia",
                "phone": "+603-7880-9999",
                "email": "info@techdata.com.my",
                "address": "Subang Jaya, Selangor, Malaysia",
            },
            {
                "name": "BP Tech Trade-In & Direct Sourcing",
                "phone": "+601-2345-6789",
                "email": "tradein@bptech.com.my",
                "address": "Batu Pahat, Johor, Malaysia",
            },
        ]

        sup_map = {}
        for s in suppliers_data:
            existing = db.query(Supplier).filter(Supplier.supplier_name == s["name"]).first()
            if not existing:
                existing = Supplier(
                    supplier_name=s["name"],
                    contact_number=s["phone"],
                    email=s["email"],
                    address=s["address"],
                )
                db.add(existing)
                db.flush()
            sup_map[s["name"]] = existing

        # Shorthand supplier aliases
        BL  = "Ban Leong Technologies"
        IM  = "Ingram Micro Malaysia"
        TD  = "Tech Data Malaysia"
        TI  = "BP Tech Trade-In & Direct Sourcing"

        # ─────────────────────────────────────────
        # 4. PRODUCTS  (name, sku, category, supplier, condition, price, stock, reorder, desc)
        # Prices from BP Tech pricelist dated 10/11/2026
        # ─────────────────────────────────────────
        products_data = [

            # ── GPU USED ──────────────────────────────────────────────────────
            {"name": "ASUS GTX 1660 SUPER 6GB GAMING OC (Used)",
             "sku": "GPU-ASUS-1660S-USED",   "cat": "GPU", "sup": TI,
             "cond": "Used",  "price": Decimal("599.00"),  "stock": 2, "reorder": 1,
             "desc": "ASUS GTX 1660 SUPER 6GB GAMING OC. Tested 100% — stress & FurMark pass. 1-Month Store Warranty."},

            {"name": "ZOTAC GAMING RTX 2060 6GB TWIN EDGE (Used)",
             "sku": "GPU-ZTC-2060-USED",     "cat": "GPU", "sup": TI,
             "cond": "Used",  "price": Decimal("699.00"),  "stock": 2, "reorder": 1,
             "desc": "ZOTAC RTX 2060 6GB TWIN EDGE. Ray Tracing, DLSS. Tested & verified. 1-Month Store Warranty."},

            {"name": "MSI RTX 2060 SUPER 8GB VENTUS 2X (Used)",
             "sku": "GPU-MSI-2060S-USED",    "cat": "GPU", "sup": TI,
             "cond": "Used",  "price": Decimal("699.00"),  "stock": 2, "reorder": 1,
             "desc": "MSI RTX 2060 SUPER 8GB VENTUS 2X. 8GB GDDR6 VRAM. Tested. 1-Month Store Warranty."},

            {"name": "PNY RTX 3060 8GB VERTO (Used)",
             "sku": "GPU-PNY-3060-USED",     "cat": "GPU", "sup": TI,
             "cond": "Used",  "price": Decimal("899.00"),  "stock": 2, "reorder": 1,
             "desc": "PNY RTX 3060 8GB VERTO. DLSS, Ray Tracing. Tested. 1-Month Store Warranty."},

            {"name": "COLORFUL RTX 3060TI 8GB NB-V (Used)",
             "sku": "GPU-COL-3060TI-USED",   "cat": "GPU", "sup": TI,
             "cond": "Used",  "price": Decimal("1249.00"), "stock": 1, "reorder": 1,
             "desc": "COLORFUL RTX 3060TI 8GB NB-V. Tested. 1-Month Store Warranty."},

            {"name": "GIGABYTE RTX 2080TI 11GB GAMING OC (Used)",
             "sku": "GPU-GBT-2080TI-USED",   "cat": "GPU", "sup": TI,
             "cond": "Used",  "price": Decimal("1249.00"), "stock": 1, "reorder": 1,
             "desc": "GIGABYTE RTX 2080TI 11GB GAMING OC. 11GB GDDR6X. Tested. 1-Month Store Warranty."},

            {"name": "PALIT RTX 3070TI 8GB GAMING PRO (Used)",
             "sku": "GPU-PLT-3070TI-USED",   "cat": "GPU", "sup": TI,
             "cond": "Used",  "price": Decimal("1599.00"), "stock": 1, "reorder": 1,
             "desc": "PALIT RTX 3070TI 8GB GAMING PRO. Tested. 1-Month Store Warranty."},

            {"name": "ZOTAC GAMING RTX 4060TI 8GB TWIN EDGE (Used)",
             "sku": "GPU-ZTC-4060TI-USED",   "cat": "GPU", "sup": TI,
             "cond": "Used",  "price": Decimal("1799.00"), "stock": 1, "reorder": 1,
             "desc": "ZOTAC RTX 4060TI 8GB TWIN EDGE. Ada Lovelace, DLSS 3. Tested. 1-Month Store Warranty."},

            {"name": "COLORFUL RTX 5060 8GB GAMING DUO (Used)",
             "sku": "GPU-COL-5060-USED",     "cat": "GPU", "sup": TI,
             "cond": "Used",  "price": Decimal("1899.00"), "stock": 1, "reorder": 1,
             "desc": "COLORFUL RTX 5060 8GB GAMING DUO. Blackwell arch. Tested. 1-Month Store Warranty."},

            {"name": "GIGABYTE RTX 4080 16GB GAMING OC (Used)",
             "sku": "GPU-GBT-4080-USED",     "cat": "GPU", "sup": TI,
             "cond": "Used",  "price": Decimal("4899.00"), "stock": 1, "reorder": 1,
             "desc": "GIGABYTE RTX 4080 16GB GAMING OC. 16GB GDDR6X. Tested. 1-Month Store Warranty."},

            # ── GPU NEW ───────────────────────────────────────────────────────
            {"name": "ARKTEK GTX 1660 SUPER 6GB",
             "sku": "GPU-ARK-1660S-NEW",     "cat": "GPU", "sup": BL,
             "cond": "New",   "price": Decimal("999.00"),  "stock": 5, "reorder": 2,
             "desc": "ARKTEK GTX 1660 SUPER 6GB. Brand new, box sealed. Great for 1080p gaming."},

            {"name": "ARKTEK RTX 2060 SUPER 8GB",
             "sku": "GPU-ARK-2060S-NEW",     "cat": "GPU", "sup": BL,
             "cond": "New",   "price": Decimal("1399.00"), "stock": 4, "reorder": 2,
             "desc": "ARKTEK RTX 2060 SUPER 8GB. Brand new. Ray Tracing, DLSS support."},

            {"name": "COLORFUL RTX 5050 8GB GAMING DUO",
             "sku": "GPU-COL-5050-NEW",      "cat": "GPU", "sup": BL,
             "cond": "New",   "price": Decimal("1699.00"), "stock": 4, "reorder": 2,
             "desc": "COLORFUL RTX 5050 8GB GAMING DUO. Blackwell, DLSS 4, brand new."},

            {"name": "GIGABYTE RTX 5060 8GB GAMING OC",
             "sku": "GPU-GBT-5060-NEW",      "cat": "GPU", "sup": BL,
             "cond": "New",   "price": Decimal("2199.00"), "stock": 3, "reorder": 2,
             "desc": "GIGABYTE RTX 5060 8GB GAMING OC. Blackwell, DLSS 4, brand new."},

            {"name": "PALIT RTX 5060 8GB INFINITY 2 OC",
             "sku": "GPU-PLT-5060-NEW",      "cat": "GPU", "sup": BL,
             "cond": "New",   "price": Decimal("2099.00"), "stock": 3, "reorder": 2,
             "desc": "PALIT RTX 5060 8GB INFINITY 2 OC. Blackwell, brand new."},

            # ── CPU AM4 ───────────────────────────────────────────────────────
            {"name": "AMD Ryzen 5 5500",
             "sku": "CPU-AMD-5500-NEW",      "cat": "CPU", "sup": BL,
             "cond": "New",   "price": Decimal("439.00"),  "stock": 10, "reorder": 4,
             "desc": "AMD Ryzen 5 5500, 6C/12T, up to 4.2GHz, Socket AM4, PCIe 3.0."},

            {"name": "AMD Ryzen 5 5600",
             "sku": "CPU-AMD-5600-NEW",      "cat": "CPU", "sup": BL,
             "cond": "New",   "price": Decimal("599.00"),  "stock": 10, "reorder": 4,
             "desc": "AMD Ryzen 5 5600, 6C/12T, up to 4.4GHz, Socket AM4, PCIe 4.0 with Wraith Stealth."},

            {"name": "AMD Ryzen 5 5600X",
             "sku": "CPU-AMD-5600X-NEW",     "cat": "CPU", "sup": BL,
             "cond": "New",   "price": Decimal("649.00"),  "stock": 8, "reorder": 3,
             "desc": "AMD Ryzen 5 5600X, 6C/12T, up to 4.6GHz, Socket AM4, PCIe 4.0 with Wraith Stealth."},

            {"name": "AMD Ryzen 7 5700X",
             "sku": "CPU-AMD-5700X-NEW",     "cat": "CPU", "sup": BL,
             "cond": "New",   "price": Decimal("749.00"),  "stock": 6, "reorder": 3,
             "desc": "AMD Ryzen 7 5700X, 8C/16T, up to 4.6GHz, Socket AM4, PCIe 4.0."},

            {"name": "AMD Ryzen 9 3900X",
             "sku": "CPU-AMD-3900X-NEW",     "cat": "CPU", "sup": BL,
             "cond": "New",   "price": Decimal("599.00"),  "stock": 4, "reorder": 2,
             "desc": "AMD Ryzen 9 3900X, 12C/24T, up to 4.6GHz, Socket AM4, PCIe 4.0 with Wraith Prism."},

            # ── CPU AM5 ───────────────────────────────────────────────────────
            {"name": "AMD Ryzen 5 7500F",
             "sku": "CPU-AMD-7500F-NEW",     "cat": "CPU", "sup": BL,
             "cond": "New",   "price": Decimal("549.00"),  "stock": 8, "reorder": 3,
             "desc": "AMD Ryzen 5 7500F, 6C/12T, up to 5.0GHz, Socket AM5, PCIe 5.0, DDR5."},

            {"name": "AMD Ryzen 5 7600X",
             "sku": "CPU-AMD-7600X-NEW",     "cat": "CPU", "sup": BL,
             "cond": "New",   "price": Decimal("749.00"),  "stock": 6, "reorder": 3,
             "desc": "AMD Ryzen 5 7600X, 6C/12T, up to 5.3GHz, Socket AM5, PCIe 5.0."},

            {"name": "AMD Ryzen 7 9700X",
             "sku": "CPU-AMD-9700X-NEW",     "cat": "CPU", "sup": BL,
             "cond": "New",   "price": Decimal("1099.00"), "stock": 5, "reorder": 2,
             "desc": "AMD Ryzen 7 9700X, 8C/16T, up to 5.5GHz, Socket AM5, Zen 5 architecture."},

            {"name": "AMD Ryzen 7 7800X3D",
             "sku": "CPU-AMD-7800X3D-NEW",   "cat": "CPU", "sup": BL,
             "cond": "New",   "price": Decimal("1449.00"), "stock": 4, "reorder": 2,
             "desc": "AMD Ryzen 7 7800X3D, 8C/16T, up to 5.0GHz, 3D V-Cache, top gaming CPU for AM5."},

            {"name": "AMD Ryzen 7 9800X3D",
             "sku": "CPU-AMD-9800X3D-NEW",   "cat": "CPU", "sup": BL,
             "cond": "New",   "price": Decimal("1999.00"), "stock": 3, "reorder": 2,
             "desc": "AMD Ryzen 7 9800X3D, 8C/16T, up to 5.7GHz, Zen 5 + 3D V-Cache, ultimate gaming CPU."},

            # ── CPU INTEL ─────────────────────────────────────────────────────
            {"name": "Intel Core i5-11400F",
             "sku": "CPU-INT-11400F-NEW",    "cat": "CPU", "sup": IM,
             "cond": "New",   "price": Decimal("299.00"),  "stock": 6, "reorder": 3,
             "desc": "Intel Core i5-11400F, 6C/12T, up to 4.4GHz, LGA1200, requires discrete GPU."},

            {"name": "Intel Core i5-12400F",
             "sku": "CPU-INT-12400F-NEW",    "cat": "CPU", "sup": IM,
             "cond": "New",   "price": Decimal("449.00"),  "stock": 8, "reorder": 3,
             "desc": "Intel Core i5-12400F, 6C/12T, up to 4.4GHz, LGA1700, DDR4/DDR5, requires discrete GPU."},

            {"name": "Intel Core i5-14400F",
             "sku": "CPU-INT-14400F-NEW",    "cat": "CPU", "sup": IM,
             "cond": "New",   "price": Decimal("649.00"),  "stock": 6, "reorder": 3,
             "desc": "Intel Core i5-14400F, 10C/16T, up to 4.7GHz, LGA1700, requires discrete GPU."},

            {"name": "Intel Ultra 7 270K Plus",
             "sku": "CPU-INT-U7-270K-NEW",   "cat": "CPU", "sup": IM,
             "cond": "New",   "price": Decimal("1699.00"), "stock": 2, "reorder": 1,
             "desc": "Intel Core Ultra 7 270K, Arrow Lake, up to 5.2GHz, LGA1851, DDR5."},

            # ── MOTHERBOARD AM4 ───────────────────────────────────────────────
            {"name": "MSI A520M-A PRO",
             "sku": "MB-MSI-A520M-PRO-NEW",  "cat": "Motherboard", "sup": TD,
             "cond": "New",   "price": Decimal("269.00"),  "stock": 8, "reorder": 3,
             "desc": "MSI A520M-A PRO, Micro-ATX, Socket AM4, DDR4, PCIe 3.0, USB 3.2 Gen1."},

            {"name": "MSI B550M-A PRO",
             "sku": "MB-MSI-B550M-PRO-NEW",  "cat": "Motherboard", "sup": TD,
             "cond": "New",   "price": Decimal("379.00"),  "stock": 8, "reorder": 3,
             "desc": "MSI B550M-A PRO, Micro-ATX, Socket AM4, DDR4, PCIe 4.0, Dual M.2."},

            {"name": "ASRock A520M/AC",
             "sku": "MB-ASR-A520M-AC-NEW",   "cat": "Motherboard", "sup": TD,
             "cond": "New",   "price": Decimal("299.00"),  "stock": 6, "reorder": 3,
             "desc": "ASRock A520M/AC, Micro-ATX, AM4, DDR4, built-in WiFi & Bluetooth."},

            {"name": "GIGABYTE B550M DS3H AC R2",
             "sku": "MB-GBT-B550M-DS3H-NEW", "cat": "Motherboard", "sup": TD,
             "cond": "New",   "price": Decimal("490.00"),  "stock": 6, "reorder": 2,
             "desc": "GIGABYTE B550M DS3H AC R2, Micro-ATX, AM4, DDR4, PCIe 4.0, WiFi & BT."},

            {"name": "GIGABYTE X570I AORUS PRO WIFI",
             "sku": "MB-GBT-X570I-AORUS-NEW","cat": "Motherboard", "sup": TD,
             "cond": "New",   "price": Decimal("649.00"),  "stock": 3, "reorder": 1,
             "desc": "GIGABYTE X570I AORUS PRO WIFI, Mini-ITX, AM4, DDR4, PCIe 4.0, WiFi 6."},

            {"name": "COLORFUL A520M-K",
             "sku": "MB-COL-A520M-K-NEW",    "cat": "Motherboard", "sup": TD,
             "cond": "New",   "price": Decimal("249.00"),  "stock": 8, "reorder": 3,
             "desc": "COLORFUL A520M-K, Micro-ATX, AM4, DDR4, budget entry-level board."},

            {"name": "COLORFUL CVN B550M GAMING FROZEN V15",
             "sku": "MB-COL-B550M-FRZ-NEW",  "cat": "Motherboard", "sup": TD,
             "cond": "New",   "price": Decimal("479.00"),  "stock": 5, "reorder": 2,
             "desc": "COLORFUL CVN B550M GAMING FROZEN V15, Micro-ATX, AM4, DDR4, PCIe 4.0, ARGB."},

            {"name": "ASUS PRIME B550M-K ARGB",
             "sku": "MB-ASUS-B550M-K-NEW",   "cat": "Motherboard", "sup": TD,
             "cond": "New",   "price": Decimal("445.00"),  "stock": 5, "reorder": 2,
             "desc": "ASUS PRIME B550M-K ARGB, Micro-ATX, AM4, DDR4, PCIe 4.0, Dual M.2."},

            # ── MOTHERBOARD AM5 ───────────────────────────────────────────────
            {"name": "MSI PRO A620AM-B EVO",
             "sku": "MB-MSI-A620AM-EVO-NEW",  "cat": "Motherboard", "sup": TD,
             "cond": "New",   "price": Decimal("379.00"),  "stock": 6, "reorder": 2,
             "desc": "MSI PRO A620AM-B EVO, Micro-ATX, AM5, DDR5, PCIe 5.0, budget AM5 board."},

            {"name": "MSI B650M-A PRO WIFI",
             "sku": "MB-MSI-B650M-PRO-NEW",   "cat": "Motherboard", "sup": TD,
             "cond": "New",   "price": Decimal("599.00"),  "stock": 5, "reorder": 2,
             "desc": "MSI B650M-A PRO WIFI, Micro-ATX, AM5, DDR5, PCIe 5.0, WiFi 6E."},

            {"name": "MSI MAG B850 TOMAHAWK MAX WIFI",
             "sku": "MB-MSI-B850-TMH-NEW",    "cat": "Motherboard", "sup": TD,
             "cond": "New",   "price": Decimal("999.00"),  "stock": 4, "reorder": 2,
             "desc": "MSI MAG B850 TOMAHAWK MAX WIFI, ATX, AM5, DDR5, PCIe 5.0, WiFi 7."},

            {"name": "ASRock B650M-H/M.2+ WIFI",
             "sku": "MB-ASR-B650M-H-NEW",     "cat": "Motherboard", "sup": TD,
             "cond": "New",   "price": Decimal("529.00"),  "stock": 5, "reorder": 2,
             "desc": "ASRock B650M-H/M.2+ WIFI, Micro-ATX, AM5, DDR5, PCIe 5.0, WiFi 6."},

            {"name": "ASRock B850M-X WIFI",
             "sku": "MB-ASR-B850M-X-NEW",     "cat": "Motherboard", "sup": TD,
             "cond": "New",   "price": Decimal("630.00"),  "stock": 4, "reorder": 2,
             "desc": "ASRock B850M-X WIFI, Micro-ATX, AM5, DDR5, PCIe 5.0, WiFi 7."},

            {"name": "GIGABYTE B650M GAMING WIFI",
             "sku": "MB-GBT-B650M-GM-NEW",    "cat": "Motherboard", "sup": TD,
             "cond": "New",   "price": Decimal("555.00"),  "stock": 5, "reorder": 2,
             "desc": "GIGABYTE B650M GAMING WIFI, Micro-ATX, AM5, DDR5, PCIe 5.0, WiFi 6E."},

            {"name": "GIGABYTE B850M FORCE WIFI V2",
             "sku": "MB-GBT-B850M-FRC-NEW",   "cat": "Motherboard", "sup": TD,
             "cond": "New",   "price": Decimal("645.00"),  "stock": 4, "reorder": 2,
             "desc": "GIGABYTE B850M FORCE WIFI V2, Micro-ATX, AM5, DDR5, PCIe 5.0, WiFi 7."},

            {"name": "GIGABYTE X870 EAGLE WIFI7",
             "sku": "MB-GBT-X870-EAGLE-NEW",  "cat": "Motherboard", "sup": TD,
             "cond": "New",   "price": Decimal("899.00"),  "stock": 3, "reorder": 1,
             "desc": "GIGABYTE X870 EAGLE WIFI7, ATX, AM5, DDR5, PCIe 5.0, WiFi 7, premium X870 platform."},

            {"name": "ASUS TUF B850M-PLUS WIFI7",
             "sku": "MB-ASUS-B850M-TUF-NEW",  "cat": "Motherboard", "sup": TD,
             "cond": "New",   "price": Decimal("899.00"),  "stock": 4, "reorder": 2,
             "desc": "ASUS TUF B850M-PLUS WIFI7, Micro-ATX, AM5, DDR5, PCIe 5.0, WiFi 7."},

            {"name": "ASUS TUF B850M-PLUS WIFI7 WHITE",
             "sku": "MB-ASUS-B850M-TUF-WHT",  "cat": "Motherboard", "sup": TD,
             "cond": "New",   "price": Decimal("949.00"),  "stock": 3, "reorder": 1,
             "desc": "ASUS TUF B850M-PLUS WIFI7 (White Edition), Micro-ATX, AM5, DDR5, PCIe 5.0, WiFi 7."},

            {"name": "COLORFUL CVN B850I GAMING FROZEN V15",
             "sku": "MB-COL-B850I-FRZ-NEW",   "cat": "Motherboard", "sup": TD,
             "cond": "New",   "price": Decimal("749.00"),  "stock": 3, "reorder": 1,
             "desc": "COLORFUL CVN B850I GAMING FROZEN V15, Mini-ITX, AM5, DDR5, PCIe 5.0."},

            # ── MOTHERBOARD INTEL DDR4 ────────────────────────────────────────
            {"name": "ASUS TUF GAMING Z490-PLUS WIFI",
             "sku": "MB-ASUS-Z490-TUF-NEW",   "cat": "Motherboard", "sup": TD,
             "cond": "New",   "price": Decimal("399.00"),  "stock": 3, "reorder": 1,
             "desc": "ASUS TUF GAMING Z490-PLUS WIFI, ATX, LGA1200, DDR4, PCIe 3.0, WiFi 6."},

            {"name": "COLORFUL H610I SMART WIFI V20",
             "sku": "MB-COL-H610I-NEW",        "cat": "Motherboard", "sup": TD,
             "cond": "New",   "price": Decimal("499.00"),  "stock": 3, "reorder": 1,
             "desc": "COLORFUL H610I SMART WIFI V20, Mini-ITX, LGA1700, DDR4, WiFi."},

            # ── MOTHERBOARD INTEL DDR5 ────────────────────────────────────────
            {"name": "ASRock H610M-HDV/M.2 D5",
             "sku": "MB-ASR-H610M-D5-NEW",     "cat": "Motherboard", "sup": TD,
             "cond": "New",   "price": Decimal("299.00"),  "stock": 6, "reorder": 2,
             "desc": "ASRock H610M-HDV/M.2 D5, Micro-ATX, LGA1700, DDR5, budget Intel DDR5 board."},

            {"name": "COLORFUL CVN Z790D5 GAMING PRO",
             "sku": "MB-COL-Z790-D5-NEW",      "cat": "Motherboard", "sup": TD,
             "cond": "New",   "price": Decimal("599.00"),  "stock": 3, "reorder": 1,
             "desc": "COLORFUL CVN Z790D5 GAMING PRO, ATX, LGA1700, DDR5, PCIe 5.0, ARGB."},

            {"name": "MSI MPG B760I EDGE WIFI ITX",
             "sku": "MB-MSI-B760I-EDGE-NEW",   "cat": "Motherboard", "sup": TD,
             "cond": "New",   "price": Decimal("599.00"),  "stock": 3, "reorder": 1,
             "desc": "MSI MPG B760I EDGE WIFI, Mini-ITX, LGA1700, DDR5, PCIe 5.0, WiFi 6E."},

            {"name": "ASUS TUF GAMING Z790-PRO WIFI",
             "sku": "MB-ASUS-Z790-TUF-NEW",    "cat": "Motherboard", "sup": TD,
             "cond": "New",   "price": Decimal("899.00"),  "stock": 3, "reorder": 1,
             "desc": "ASUS TUF GAMING Z790-PRO WIFI, ATX, LGA1700, DDR5, PCIe 5.0, WiFi 6E."},

            {"name": "GIGABYTE B860M EAGLE WIFI6E",
             "sku": "MB-GBT-B860M-EAGLE-NEW",  "cat": "Motherboard", "sup": TD,
             "cond": "New",   "price": Decimal("660.00"),  "stock": 4, "reorder": 2,
             "desc": "GIGABYTE B860M EAGLE WIFI6E, Micro-ATX, LGA1851, DDR5, PCIe 5.0, WiFi 6E."},

            {"name": "MSI PRO B860M-A WIFI",
             "sku": "MB-MSI-B860M-A-NEW",      "cat": "Motherboard", "sup": TD,
             "cond": "New",   "price": Decimal("760.00"),  "stock": 3, "reorder": 1,
             "desc": "MSI PRO B860M-A WIFI, Micro-ATX, LGA1851, DDR5, PCIe 5.0, WiFi 6E."},

            # ── SSD SATA ──────────────────────────────────────────────────────
            {"name": "Netac 256GB 2.5\" SATA SSD",
             "sku": "SSD-NTC-256-SATA-NEW",    "cat": "SSD", "sup": BL,
             "cond": "New",   "price": Decimal("209.00"),  "stock": 15, "reorder": 5,
             "desc": "Netac 256GB 2.5\" SATA SSD, up to 540MB/s read. Great budget OS drive."},

            {"name": "AGI 256GB 2.5\" SATA SSD",
             "sku": "SSD-AGI-256-SATA-NEW",    "cat": "SSD", "sup": BL,
             "cond": "New",   "price": Decimal("219.00"),  "stock": 12, "reorder": 5,
             "desc": "AGI 256GB 2.5\" SATA SSD, up to 520MB/s read."},

            {"name": "Kingston A400 480GB 2.5\" SATA SSD",
             "sku": "SSD-KST-480-SATA-NEW",    "cat": "SSD", "sup": BL,
             "cond": "New",   "price": Decimal("379.00"),  "stock": 10, "reorder": 4,
             "desc": "Kingston A400 480GB SATA SSD, up to 500MB/s read, 450MB/s write."},

            {"name": "AGI 512GB 2.5\" SATA SSD",
             "sku": "SSD-AGI-512-SATA-NEW",    "cat": "SSD", "sup": BL,
             "cond": "New",   "price": Decimal("379.00"),  "stock": 10, "reorder": 4,
             "desc": "AGI 512GB 2.5\" SATA SSD."},

            {"name": "Addlink S20 1TB 2.5\" SATA SSD",
             "sku": "SSD-ADD-1TB-SATA-NEW",    "cat": "SSD", "sup": BL,
             "cond": "New",   "price": Decimal("609.00"),  "stock": 8, "reorder": 3,
             "desc": "Addlink S20 1TB SATA SSD, up to 560MB/s read. High capacity SATA drive."},

            # ── SSD NVMe ──────────────────────────────────────────────────────
            {"name": "Netac 256GB NVMe SSD",
             "sku": "SSD-NTC-256-NVME-NEW",    "cat": "SSD", "sup": BL,
             "cond": "New",   "price": Decimal("249.00"),  "stock": 12, "reorder": 5,
             "desc": "Netac 256GB M.2 NVMe SSD, PCIe 3.0, up to 2100MB/s read."},

            {"name": "PNY CS1031 500GB NVMe SSD",
             "sku": "SSD-PNY-500-NVME-NEW",    "cat": "SSD", "sup": BL,
             "cond": "New",   "price": Decimal("435.00"),  "stock": 10, "reorder": 4,
             "desc": "PNY CS1031 500GB M.2 NVMe SSD, PCIe 3.0."},

            {"name": "Kingston NV3 500GB NVMe Gen4 SSD",
             "sku": "SSD-KST-500-NVME-GEN4-NEW","cat": "SSD", "sup": BL,
             "cond": "New",   "price": Decimal("449.00"),  "stock": 10, "reorder": 4,
             "desc": "Kingston NV3 500GB M.2 NVMe SSD, PCIe 4.0, up to 3500MB/s read."},

            {"name": "Samsung 990 Pro 1TB NVMe SSD",
             "sku": "SSD-SAM-1TB-990PRO-NEW",  "cat": "SSD", "sup": BL,
             "cond": "New",   "price": Decimal("529.00"),  "stock": 8, "reorder": 3,
             "desc": "Samsung 990 Pro 1TB M.2 NVMe SSD, PCIe 4.0, up to 7450MB/s read. Available with 1M/3M/6M warranty options (RM529/RM579/RM629)."},

            # ── HDD ───────────────────────────────────────────────────────────
            {"name": "500GB HDD",
             "sku": "HDD-500GB-USED",          "cat": "HDD", "sup": TI,
             "cond": "Used",  "price": Decimal("40.00"),   "stock": 10, "reorder": 5,
             "desc": "500GB 2.5\" Hard Disk Drive. Tested. Great for secondary storage."},

            # ── RAM DDR4 ──────────────────────────────────────────────────────
            {"name": "Fanxiang UD02R 8GB DDR4 3200MHz",
             "sku": "RAM-FXG-8G-DDR4-NEW",     "cat": "RAM", "sup": BL,
             "cond": "New",   "price": Decimal("299.00"),  "stock": 12, "reorder": 5,
             "desc": "Fanxiang UD02R 8GB DDR4 3200MHz desktop RAM."},

            {"name": "Corsair Vengeance RGB 8GBx2 DDR4 3200MHz",
             "sku": "RAM-COR-16G-RGB-DDR4-NEW","cat": "RAM", "sup": BL,
             "cond": "New",   "price": Decimal("449.00"),  "stock": 10, "reorder": 4,
             "desc": "Corsair Vengeance RGB 16GB (2x8GB) DDR4 3200MHz. RGB lighting, XMP 2.0."},

            {"name": "Adata XPG D35G RGB 8GB DDR4 3200MHz",
             "sku": "RAM-ADA-8G-D35G-DDR4-NEW","cat": "RAM", "sup": BL,
             "cond": "New",   "price": Decimal("249.00"),  "stock": 12, "reorder": 5,
             "desc": "Adata XPG D35G RGB 8GB DDR4 3200MHz. RGB, XMP 2.0."},

            {"name": "Adata XPG D41 RGB 8GBx2 DDR4 3200MHz",
             "sku": "RAM-ADA-16G-D41-DDR4-NEW","cat": "RAM", "sup": BL,
             "cond": "New",   "price": Decimal("449.00"),  "stock": 8, "reorder": 3,
             "desc": "Adata XPG D41 RGB 16GB (2x8GB) DDR4 3200MHz. RGB, XMP 2.0."},

            {"name": "Adata XPG D50 RGB 8GBx2 DDR4 3200MHz White",
             "sku": "RAM-ADA-16G-D50-DDR4-WHT","cat": "RAM", "sup": BL,
             "cond": "New",   "price": Decimal("449.00"),  "stock": 6, "reorder": 2,
             "desc": "Adata XPG D50 RGB 16GB (2x8GB) DDR4 3200MHz, White edition."},

            {"name": "SK Hynix 16GB DDR4 3200MHz",
             "sku": "RAM-SKH-16G-DDR4-NEW",    "cat": "RAM", "sup": BL,
             "cond": "New",   "price": Decimal("399.00"),  "stock": 8, "reorder": 3,
             "desc": "SK Hynix 16GB DDR4 3200MHz desktop RAM."},

            {"name": "Patriot Viper RGB 8GBx2 DDR4 3200MHz",
             "sku": "RAM-PAT-16G-VIPER-DDR4-NEW","cat": "RAM", "sup": BL,
             "cond": "New",   "price": Decimal("449.00"),  "stock": 8, "reorder": 3,
             "desc": "Patriot Viper RGB 16GB (2x8GB) DDR4 3200MHz. RGB, XMP 2.0."},

            {"name": "Kingston HyperX 16GB DDR4 2666MHz",
             "sku": "RAM-KST-16G-HX-2666-NEW", "cat": "RAM", "sup": BL,
             "cond": "New",   "price": Decimal("379.00"),  "stock": 6, "reorder": 3,
             "desc": "Kingston HyperX 16GB DDR4 2666MHz desktop RAM."},

            # ── RAM DDR5 ──────────────────────────────────────────────────────
            {"name": "Klevv Cras V RGB 32GB DDR5 6000MT/s CL30",
             "sku": "RAM-KLV-32G-DDR5-NEW",    "cat": "RAM", "sup": BL,
             "cond": "New",   "price": Decimal("2099.00"), "stock": 3, "reorder": 1,
             "desc": "Klevv Cras V RGB 32GB DDR5 6000MT/s CL30. High-performance DDR5."},

            {"name": "Kingston Fury Beast RGB 8GBx2 DDR5 5600MT/s",
             "sku": "RAM-KST-16G-FRBST-DDR5-NEW","cat": "RAM", "sup": BL,
             "cond": "New",   "price": Decimal("999.00"),  "stock": 5, "reorder": 2,
             "desc": "Kingston Fury Beast RGB 16GB (2x8GB) DDR5 5600MT/s."},

            {"name": "Corsair Vengeance RGB 16GB DDR5 6000MT/s CL36",
             "sku": "RAM-COR-16G-RGB-DDR5-NEW","cat": "RAM", "sup": BL,
             "cond": "New",   "price": Decimal("1199.00"), "stock": 4, "reorder": 2,
             "desc": "Corsair Vengeance RGB 16GB DDR5 6000MT/s CL36."},

            {"name": "Patriot 16GBx2 DDR5 6400MT/s CL34",
             "sku": "RAM-PAT-32G-DDR5-NEW",    "cat": "RAM", "sup": BL,
             "cond": "New",   "price": Decimal("1999.00"), "stock": 3, "reorder": 1,
             "desc": "Patriot 32GB (2x16GB) DDR5 6400MT/s CL34. High-speed DDR5 kit."},

            # ── RAM SODIMM ────────────────────────────────────────────────────
            {"name": "Acer SD100 8GB DDR4 3200MHz SODIMM",
             "sku": "RAM-ACR-8G-SD100-SODIMM-NEW","cat": "RAM", "sup": BL,
             "cond": "New",   "price": Decimal("299.00"),  "stock": 8, "reorder": 3,
             "desc": "Acer SD100 8GB DDR4 3200MHz SODIMM for laptops."},

            {"name": "SSTC 16GB DDR4 3200MHz SODIMM",
             "sku": "RAM-SST-16G-SODIMM-NEW",  "cat": "RAM", "sup": BL,
             "cond": "New",   "price": Decimal("549.00"),  "stock": 6, "reorder": 2,
             "desc": "SSTC 16GB DDR4 3200MHz SODIMM for laptops."},

            {"name": "Kingston Fury Impact 32GB DDR4 3200MHz SODIMM",
             "sku": "RAM-KST-32G-SODIMM-NEW",  "cat": "RAM", "sup": BL,
             "cond": "New",   "price": Decimal("799.00"),  "stock": 4, "reorder": 2,
             "desc": "Kingston Fury Impact 32GB DDR4 3200MHz SODIMM for laptops."},

            {"name": "Samsung 8GB DDR5 5200MHz SODIMM",
             "sku": "RAM-SAM-8G-DDR5-SODIMM-NEW","cat": "RAM", "sup": BL,
             "cond": "New",   "price": Decimal("449.00"),  "stock": 6, "reorder": 2,
             "desc": "Samsung 8GB DDR5 5200MHz SODIMM for DDR5 laptops."},

            # ── PSU ───────────────────────────────────────────────────────────
            {"name": "Gamdias Aura GP750 80+ 750W",
             "sku": "PSU-GMD-750W-NEW",         "cat": "PSU", "sup": BL,
             "cond": "New",   "price": Decimal("179.00"),  "stock": 8, "reorder": 3,
             "desc": "Gamdias Aura GP750 750W 80+ certified PSU."},

            {"name": "Gigabyte P550SS 80+ Silver 550W",
             "sku": "PSU-GBT-P550SS-NEW",       "cat": "PSU", "sup": BL,
             "cond": "New",   "price": Decimal("185.00"),  "stock": 8, "reorder": 3,
             "desc": "Gigabyte P550SS 550W 80+ Silver certified PSU."},

            {"name": "Gigabyte P650SS 80+ Silver 650W",
             "sku": "PSU-GBT-P650SS-NEW",       "cat": "PSU", "sup": BL,
             "cond": "New",   "price": Decimal("215.00"),  "stock": 8, "reorder": 3,
             "desc": "Gigabyte P650SS 650W 80+ Silver certified PSU."},

            {"name": "Thermaltake Smart BX3 750W 80+ Bronze",
             "sku": "PSU-TTK-BX3-750W-NEW",     "cat": "PSU", "sup": BL,
             "cond": "New",   "price": Decimal("230.00"),  "stock": 6, "reorder": 2,
             "desc": "Thermaltake Smart BX3 750W 80+ Bronze PSU."},

            {"name": "Deepcool PFX 500W 80+ Bronze",
             "sku": "PSU-DPC-PFX-500W-NEW",     "cat": "PSU", "sup": BL,
             "cond": "New",   "price": Decimal("169.00"),  "stock": 8, "reorder": 3,
             "desc": "Deepcool PFX 500W 80+ Bronze PSU."},

            {"name": "Slevnergy Quantum 500W 80+",
             "sku": "PSU-SLV-Q500W-NEW",        "cat": "PSU", "sup": BL,
             "cond": "New",   "price": Decimal("125.00"),  "stock": 10, "reorder": 4,
             "desc": "Slevnergy Quantum 500W 80+ PSU. Budget pick."},

            {"name": "Slevnergy Quantum 600W 80+",
             "sku": "PSU-SLV-Q600W-NEW",        "cat": "PSU", "sup": BL,
             "cond": "New",   "price": Decimal("145.00"),  "stock": 10, "reorder": 4,
             "desc": "Slevnergy Quantum 600W 80+ PSU."},

            {"name": "Slevnergy Inspire 1000W 80+ Gold ATX3.1",
             "sku": "PSU-SLV-1000W-GOLD-NEW",   "cat": "PSU", "sup": BL,
             "cond": "New",   "price": Decimal("580.00"),  "stock": 4, "reorder": 2,
             "desc": "Slevnergy Inspire 1000W 80+ Gold ATX3.1 PSU. High-wattage for flagship builds."},

            {"name": "1st Player ACK 500W 80+",
             "sku": "PSU-1ST-ACK-500W-NEW",     "cat": "PSU", "sup": BL,
             "cond": "New",   "price": Decimal("165.00"),  "stock": 8, "reorder": 3,
             "desc": "1st Player ACK 500W 80+ PSU."},

            {"name": "1st Player DK6.0 Premium 600W 80+ Bronze Full Modular",
             "sku": "PSU-1ST-DK6-600W-NEW",     "cat": "PSU", "sup": BL,
             "cond": "New",   "price": Decimal("200.00"),  "stock": 6, "reorder": 2,
             "desc": "1st Player DK6.0 Premium 600W 80+ Bronze, Full Modular PSU."},

            {"name": "1st Player Steampunk 850W 80+ Gold Full Modular",
             "sku": "PSU-1ST-SPK-850W-NEW",     "cat": "PSU", "sup": BL,
             "cond": "New",   "price": Decimal("349.00"),  "stock": 4, "reorder": 2,
             "desc": "1st Player Steampunk 850W 80+ Gold, Full Modular PSU."},

            {"name": "Aigo AP550W 80+ White",
             "sku": "PSU-AIG-550W-WHT-NEW",     "cat": "PSU", "sup": BL,
             "cond": "New",   "price": Decimal("165.00"),  "stock": 8, "reorder": 3,
             "desc": "Aigo AP550W 80+ White PSU. White coloured for white builds."},

            {"name": "FSP VIC WD 650W 80+",
             "sku": "PSU-FSP-VIC-WD-650W-NEW",  "cat": "PSU", "sup": BL,
             "cond": "New",   "price": Decimal("175.00"),  "stock": 8, "reorder": 3,
             "desc": "FSP VIC WD 650W 80+ PSU."},

            {"name": "FSP VIC BD 650W 80+ Bronze ATX3.1",
             "sku": "PSU-FSP-VIC-BD-650W-NEW",  "cat": "PSU", "sup": BL,
             "cond": "New",   "price": Decimal("205.00"),  "stock": 6, "reorder": 2,
             "desc": "FSP VIC BD 650W 80+ Bronze ATX3.1 PSU."},

            {"name": "FSP VIC GD 850W 80+ Gold ATX3.1 PCIE5.0",
             "sku": "PSU-FSP-VIC-GD-850W-NEW",  "cat": "PSU", "sup": BL,
             "cond": "New",   "price": Decimal("350.00"),  "stock": 4, "reorder": 2,
             "desc": "FSP VIC GD 850W 80+ Gold ATX3.1 PCIE5.0 PSU. For high-end builds."},

            {"name": "FSP Dagger Pro SFX 650W 80+ Gold",
             "sku": "PSU-FSP-DGR-SFX-650W-NEW", "cat": "PSU", "sup": BL,
             "cond": "New",   "price": Decimal("200.00"),  "stock": 4, "reorder": 2,
             "desc": "FSP Dagger Pro SFX 650W 80+ Gold PSU. Compact SFX form factor for ITX builds."},

            {"name": "Cooler Master V750 SFX Gold",
             "sku": "PSU-CM-V750-SFX-NEW",      "cat": "PSU", "sup": BL,
             "cond": "New",   "price": Decimal("299.00"),  "stock": 3, "reorder": 1,
             "desc": "Cooler Master V750 SFX Gold 750W PSU. Fully modular, SFX form factor."},

            # ── CASE ──────────────────────────────────────────────────────────
            {"name": "Tecware VXO M + 3 ARGB Fan",
             "sku": "CASE-TW-VXOM-NEW",         "cat": "Case", "sup": BL,
             "cond": "New",   "price": Decimal("135.00"),  "stock": 8, "reorder": 3,
             "desc": "Tecware VXO M Micro-ATX case, includes 3x ARGB fans."},

            {"name": "Tecware Neo M3+ + 3 ARGB Fan",
             "sku": "CASE-TW-NEOM3-NEW",        "cat": "Case", "sup": BL,
             "cond": "New",   "price": Decimal("135.00"),  "stock": 8, "reorder": 3,
             "desc": "Tecware Neo M3+ Micro-ATX case, includes 3x ARGB fans."},

            {"name": "Tecware Aero M TG + 4 ARGB Fan",
             "sku": "CASE-TW-AEROM-NEW",        "cat": "Case", "sup": BL,
             "cond": "New",   "price": Decimal("145.00"),  "stock": 6, "reorder": 2,
             "desc": "Tecware Aero M TG Micro-ATX tempered glass case, includes 4x ARGB fans."},

            {"name": "Tecware Timber M + 3 Fan",
             "sku": "CASE-TW-TMBR-NEW",         "cat": "Case", "sup": BL,
             "cond": "New",   "price": Decimal("169.00"),  "stock": 6, "reorder": 2,
             "desc": "Tecware Timber M wood-panel Micro-ATX case, includes 3 fans."},

            {"name": "Tecware Vertex TG + 6 ARGB Fan",
             "sku": "CASE-TW-VRTX-NEW",         "cat": "Case", "sup": BL,
             "cond": "New",   "price": Decimal("205.00"),  "stock": 5, "reorder": 2,
             "desc": "Tecware Vertex TG Mid-Tower tempered glass case, includes 6x ARGB fans."},

            {"name": "Tecware VXN+ + 6 ARGB Fan",
             "sku": "CASE-TW-VXNP-NEW",         "cat": "Case", "sup": BL,
             "cond": "New",   "price": Decimal("209.00"),  "stock": 5, "reorder": 2,
             "desc": "Tecware VXN+ Mid-Tower case, includes 6x ARGB fans."},

            {"name": "Formula V Air Mesh G5 + 5 ARGB Fan",
             "sku": "CASE-FV-G5-NEW",            "cat": "Case", "sup": BL,
             "cond": "New",   "price": Decimal("189.00"),  "stock": 5, "reorder": 2,
             "desc": "Formula V Air Mesh G5 case with mesh front panel, includes 5x ARGB fans."},

            {"name": "Formula V Crystal Z6M + 6 ARGB Fan",
             "sku": "CASE-FV-Z6M-NEW",           "cat": "Case", "sup": BL,
             "cond": "New",   "price": Decimal("259.00"),  "stock": 4, "reorder": 2,
             "desc": "Formula V Crystal Z6M panoramic glass case. Available in Black and White. Includes 6x ARGB fans."},

            {"name": "Jonsbo C6 + 3 ARGB Fan",
             "sku": "CASE-JNB-C6-NEW",           "cat": "Case", "sup": BL,
             "cond": "New",   "price": Decimal("198.00"),  "stock": 4, "reorder": 2,
             "desc": "Jonsbo C6 Micro-ATX case. Available in Black and White. Includes 3x ARGB fans."},

            {"name": "FSP S190-WA + 5 ARGB Fan White",
             "sku": "CASE-FSP-S190-WHT-NEW",     "cat": "Case", "sup": BL,
             "cond": "New",   "price": Decimal("195.00"),  "stock": 4, "reorder": 2,
             "desc": "FSP S190-WA White edition case, includes 5x ARGB fans."},

            {"name": "Deepcool CG330 + 3 ARGB Fan White",
             "sku": "CASE-DPC-CG330-WHT-NEW",    "cat": "Case", "sup": BL,
             "cond": "New",   "price": Decimal("229.00"),  "stock": 4, "reorder": 2,
             "desc": "Deepcool CG330 White case, includes 3x ARGB fans."},

            {"name": "Slevcase Nexis + 3 ARGB Fan",
             "sku": "CASE-SLV-NEXIS-NEW",        "cat": "Case", "sup": BL,
             "cond": "New",   "price": Decimal("135.00"),  "stock": 8, "reorder": 3,
             "desc": "Slevcase Nexis case. Available in Black and White. Includes 3x ARGB fans."},

            {"name": "Slevcase Lumira + 3 ARGB Fan",
             "sku": "CASE-SLV-LUMIRA-NEW",       "cat": "Case", "sup": BL,
             "cond": "New",   "price": Decimal("219.00"),  "stock": 5, "reorder": 2,
             "desc": "Slevcase Lumira case. Available in Black and White. Includes 3x ARGB fans."},

            {"name": "NZXT S5 RGB + 3 ARGB Fan",
             "sku": "CASE-NZXT-S5-RGB-NEW",      "cat": "Case", "sup": BL,
             "cond": "New",   "price": Decimal("235.00"),  "stock": 4, "reorder": 2,
             "desc": "NZXT S5 RGB Mid-Tower case. Available in Black and White. Includes 3x ARGB fans."},

            # ── CPU COOLER AIR ────────────────────────────────────────────────
            {"name": "ID-Cooling SE-214-XT ARGB Cooler",
             "sku": "COOL-IDC-SE214XT-NEW",      "cat": "CPU Cooler", "sup": BL,
             "cond": "New",   "price": Decimal("99.00"),   "stock": 10, "reorder": 4,
             "desc": "ID-Cooling SE-214-XT ARGB air cooler. 4 heatpipes, 120mm ARGB fan."},

            {"name": "ID-Cooling Frozn A410 TD Digital Cooler Black",
             "sku": "COOL-IDC-A410-BLK-NEW",     "cat": "CPU Cooler", "sup": BL,
             "cond": "New",   "price": Decimal("119.00"),  "stock": 8, "reorder": 3,
             "desc": "ID-Cooling Frozn A410 TD Digital CPU cooler, Black edition."},

            {"name": "ID-Cooling Frozn A620 Pro SE ARGB Cooler White",
             "sku": "COOL-IDC-A620-WHT-NEW",     "cat": "CPU Cooler", "sup": BL,
             "cond": "New",   "price": Decimal("159.00"),  "stock": 6, "reorder": 2,
             "desc": "ID-Cooling Frozn A620 Pro SE ARGB CPU cooler, White edition. Dual tower."},

            {"name": "DeepCool AK620 G2 Wooden Air Cooler White",
             "sku": "COOL-DPC-AK620-WHT-NEW",    "cat": "CPU Cooler", "sup": BL,
             "cond": "New",   "price": Decimal("259.00"),  "stock": 4, "reorder": 2,
             "desc": "DeepCool AK620 G2 Wooden air cooler, White edition. Premium dual-tower design."},

            {"name": "Aigo Darkflash ICE 200 Pro RGB Cooler",
             "sku": "COOL-AIG-ICE200-NEW",       "cat": "CPU Cooler", "sup": BL,
             "cond": "New",   "price": Decimal("59.00"),   "stock": 12, "reorder": 5,
             "desc": "Aigo Darkflash ICE 200 Pro RGB CPU cooler. Budget pick."},

            {"name": "Cooler Master Hyper 212 ARGB Cooler",
             "sku": "COOL-CM-H212-ARGB-NEW",     "cat": "CPU Cooler", "sup": BL,
             "cond": "New",   "price": Decimal("89.00"),   "stock": 10, "reorder": 4,
             "desc": "Cooler Master Hyper 212 ARGB. Classic reliable single-tower cooler."},

            {"name": "Super Flower Cooldex ST4 ARGB Cooler",
             "sku": "COOL-SF-ST4-ARGB-NEW",      "cat": "CPU Cooler", "sup": BL,
             "cond": "New",   "price": Decimal("89.00"),   "stock": 8, "reorder": 3,
             "desc": "Super Flower Cooldex ST4 ARGB CPU cooler."},

            {"name": "Thermalright AXP90-X53 Low Profile Cooler",
             "sku": "COOL-TRL-AXP90-NEW",        "cat": "CPU Cooler", "sup": BL,
             "cond": "New",   "price": Decimal("129.00"),  "stock": 6, "reorder": 2,
             "desc": "Thermalright AXP90-X53 low profile CPU cooler. Ideal for SFF/ITX builds."},

            # ── CPU COOLER AIO ────────────────────────────────────────────────
            {"name": "Aigo Darkflash Twister DX-240 ARGB Liquid Cooler White",
             "sku": "COOL-AIG-DX240-WHT-NEW",    "cat": "CPU Cooler", "sup": BL,
             "cond": "New",   "price": Decimal("159.00"),  "stock": 6, "reorder": 2,
             "desc": "Aigo Darkflash Twister DX-240 240mm ARGB AIO liquid cooler, White."},

            {"name": "Thermalright Aqua Elite 240 ARGB Liquid Cooler White",
             "sku": "COOL-TRL-AE240-WHT-NEW",    "cat": "CPU Cooler", "sup": BL,
             "cond": "New",   "price": Decimal("179.00"),  "stock": 5, "reorder": 2,
             "desc": "Thermalright Aqua Elite 240 ARGB 240mm AIO liquid cooler, White."},

            {"name": "Cooler Master Elite 240 ARGB Liquid Cooler",
             "sku": "COOL-CM-E240-ARGB-NEW",     "cat": "CPU Cooler", "sup": BL,
             "cond": "New",   "price": Decimal("199.00"),  "stock": 5, "reorder": 2,
             "desc": "Cooler Master Elite 240 ARGB 240mm AIO liquid cooler."},

            {"name": "ID-Cooling FX240 LCD ARGB Liquid Cooler Black",
             "sku": "COOL-IDC-FX240-BLK-NEW",    "cat": "CPU Cooler", "sup": BL,
             "cond": "New",   "price": Decimal("249.00"),  "stock": 4, "reorder": 2,
             "desc": "ID-Cooling FX240 LCD ARGB 240mm AIO cooler, Black. LCD display on pump head."},

            {"name": "ID-Cooling FX360 INF ARGB Liquid Cooler Black",
             "sku": "COOL-IDC-FX360-BLK-NEW",    "cat": "CPU Cooler", "sup": BL,
             "cond": "New",   "price": Decimal("299.00"),  "stock": 3, "reorder": 1,
             "desc": "ID-Cooling FX360 INF ARGB 360mm AIO cooler, Black."},

            {"name": "Lovingcool DP240-01 LCD ARGB Liquid Cooler Black",
             "sku": "COOL-LVC-DP240-BLK-NEW",    "cat": "CPU Cooler", "sup": BL,
             "cond": "New",   "price": Decimal("245.00"),  "stock": 4, "reorder": 2,
             "desc": "Lovingcool DP240-01 LCD ARGB 240mm AIO cooler, Black."},

            {"name": "Lovingcool DP360-01 LCD ARGB Liquid Cooler Black",
             "sku": "COOL-LVC-DP360-BLK-NEW",    "cat": "CPU Cooler", "sup": BL,
             "cond": "New",   "price": Decimal("299.00"),  "stock": 3, "reorder": 1,
             "desc": "Lovingcool DP360-01 LCD ARGB 360mm AIO cooler, Black."},

            {"name": "Deepcool LE500 240 ARGB Liquid Cooler Black",
             "sku": "COOL-DPC-LE500-BLK-NEW",    "cat": "CPU Cooler", "sup": BL,
             "cond": "New",   "price": Decimal("189.00"),  "stock": 4, "reorder": 2,
             "desc": "Deepcool LE500 240 ARGB 240mm AIO liquid cooler, Black."},

            # ── MONITOR ───────────────────────────────────────────────────────
            {"name": "ViewSonic VA27G1-H 27\" FHD 144Hz IPS",
             "sku": "MON-VS-VA27G1-NEW",         "cat": "Monitor", "sup": IM,
             "cond": "New",   "price": Decimal("439.00"),  "stock": 5, "reorder": 2,
             "desc": "ViewSonic VA27G1-H 27-inch FHD (1920x1080) 144Hz IPS gaming monitor."},

            {"name": "ViewSonic VA24G1-H 24\" FHD 144Hz IPS",
             "sku": "MON-VS-VA24G1-NEW",         "cat": "Monitor", "sup": IM,
             "cond": "New",   "price": Decimal("339.00"),  "stock": 6, "reorder": 2,
             "desc": "ViewSonic VA24G1-H 24-inch FHD (1920x1080) 144Hz IPS gaming monitor."},

            {"name": "ViewSonic VA22E2-H 22\" FHD 100Hz IPS",
             "sku": "MON-VS-VA22E2-NEW",         "cat": "Monitor", "sup": IM,
             "cond": "New",   "price": Decimal("269.00"),  "stock": 8, "reorder": 3,
             "desc": "ViewSonic VA22E2-H 22-inch FHD (1920x1080) 100Hz IPS monitor."},

            # ── FANS ──────────────────────────────────────────────────────────
            {"name": "TRILLIONX USB Magic Fan (For Laptop & Router)",
             "sku": "FAN-TRX-USB-MAGIC-NEW",     "cat": "Fan", "sup": BL,
             "cond": "New",   "price": Decimal("69.00"),   "stock": 15, "reorder": 5,
             "desc": "TRILLIONX USB Magic Fan for laptop and router cooling."},

            {"name": "TRILLIONX Magic Fans Box 4pcs",
             "sku": "FAN-TRX-MAGIC-4PCS-NEW",    "cat": "Fan", "sup": BL,
             "cond": "New",   "price": Decimal("50.00"),   "stock": 15, "reorder": 5,
             "desc": "TRILLIONX Magic Fans Box set of 4pcs."},

            {"name": "TRILLIONX Double Layer LED Fan Box 4pcs",
             "sku": "FAN-TRX-LED-4PCS-NEW",      "cat": "Fan", "sup": BL,
             "cond": "New",   "price": Decimal("55.00"),   "stock": 12, "reorder": 5,
             "desc": "TRILLIONX Double Layer LED Fan 4pcs. Available in Blue/Red/White/Purple/Green."},

            {"name": "TRILLIONX Luna ARGB Magic Fan Box Set 4pcs",
             "sku": "FAN-TRX-LUNA-4PCS-NEW",     "cat": "Fan", "sup": BL,
             "cond": "New",   "price": Decimal("75.00"),   "stock": 10, "reorder": 4,
             "desc": "TRILLIONX Luna ARGB Magic Fan box set of 4pcs."},

            {"name": "TRILLIONX UFO Magic Fan Box 4pcs",
             "sku": "FAN-TRX-UFO-4PCS-NEW",      "cat": "Fan", "sup": BL,
             "cond": "New",   "price": Decimal("98.00"),   "stock": 10, "reorder": 4,
             "desc": "TRILLIONX UFO Magic Fan box set of 4pcs."},

            {"name": "TRILLIONX Crystal Autosync Fan Box 4pcs",
             "sku": "FAN-TRX-CRYSTAL-4PCS-NEW",  "cat": "Fan", "sup": BL,
             "cond": "New",   "price": Decimal("69.00"),   "stock": 10, "reorder": 4,
             "desc": "TRILLIONX Crystal Autosync ARGB Fan box set of 4pcs."},

            {"name": "ARGB Case Fan",
             "sku": "FAN-ARGB-CASE-NEW",          "cat": "Fan", "sup": BL,
             "cond": "New",   "price": Decimal("21.00"),   "stock": 50, "reorder": 15,
             "desc": "Generic ARGB 120mm case fan. Compatible with all standard motherboard ARGB headers."},

            # ── KEYCAP ────────────────────────────────────────────────────────
            {"name": "TRILLIONX Doubleshot Mechanical Keyboard ABS Keycap",
             "sku": "KYCAP-TRX-ABS-NEW",          "cat": "Accessories", "sup": BL,
             "cond": "New",   "price": Decimal("15.00"),   "stock": 30, "reorder": 10,
             "desc": "TRILLIONX Doubleshot ABS Keycap set. Available in Black/Green/Grey/Orange/Pink/Purple/Red/Sky Blue/White/Yellow/Coffee."},

            # ── KEYBOARD ──────────────────────────────────────────────────────
            {"name": "Marvo Gaming CM310 3-In-1 Gaming Combo Black",
             "sku": "KB-MARVO-CM310-BLK-NEW",     "cat": "Keyboard", "sup": BL,
             "cond": "New",   "price": Decimal("90.00"),   "stock": 10, "reorder": 4,
             "desc": "Marvo Gaming CM310 3-In-1 Gaming Combo (Keyboard + Mouse + Headset), Black."},

            {"name": "Marvo Gaming CM310 3-In-1 Gaming Combo White",
             "sku": "KB-MARVO-CM310-WHT-NEW",     "cat": "Keyboard", "sup": BL,
             "cond": "New",   "price": Decimal("95.00"),   "stock": 8, "reorder": 3,
             "desc": "Marvo Gaming CM310 3-In-1 Gaming Combo (Keyboard + Mouse + Headset), White."},

            {"name": "Marvo Gaming KG933G Saber 61 Mechanical Keyboard",
             "sku": "KB-MARVO-KG933G-NEW",        "cat": "Keyboard", "sup": BL,
             "cond": "New",   "price": Decimal("79.00"),   "stock": 10, "reorder": 4,
             "desc": "Marvo Gaming KG933G Saber 61 Mechanical Keyboard, 60% layout."},

            {"name": "Voicsky Pulse 75 Cloudy Tactile Dark",
             "sku": "KB-VSK-P75-CLOUD-DRK-NEW",   "cat": "Keyboard", "sup": BL,
             "cond": "New",   "price": Decimal("169.00"),  "stock": 6, "reorder": 2,
             "desc": "Voicsky Pulse 75 Cloudy Tactile Switch keyboard, Dark colourway. 75% layout."},

            {"name": "Voicsky Pulse 75 Cloudy Tactile Lavender",
             "sku": "KB-VSK-P75-CLOUD-LAV-NEW",   "cat": "Keyboard", "sup": BL,
             "cond": "New",   "price": Decimal("169.00"),  "stock": 5, "reorder": 2,
             "desc": "Voicsky Pulse 75 Cloudy Tactile Switch keyboard, Lavender colourway. 75% layout."},

            {"name": "Voicsky Pulse 75 Tone Linear Light",
             "sku": "KB-VSK-P75-TONE-LGT-NEW",    "cat": "Keyboard", "sup": BL,
             "cond": "New",   "price": Decimal("169.00"),  "stock": 5, "reorder": 2,
             "desc": "Voicsky Pulse 75 Tone Linear Switch keyboard, Light colourway. 75% layout."},

            {"name": "Voicsky Pulse 96 Cloudy Tactile Aurora",
             "sku": "KB-VSK-P96-CLOUD-AUR-NEW",   "cat": "Keyboard", "sup": BL,
             "cond": "New",   "price": Decimal("189.00"),  "stock": 5, "reorder": 2,
             "desc": "Voicsky Pulse 96 Cloudy Tactile Switch keyboard, Aurora colourway. 96% layout."},

            {"name": "Voicsky Pulse 96 Cloudy Tactile Forest",
             "sku": "KB-VSK-P96-CLOUD-FOR-NEW",   "cat": "Keyboard", "sup": BL,
             "cond": "New",   "price": Decimal("189.00"),  "stock": 5, "reorder": 2,
             "desc": "Voicsky Pulse 96 Cloudy Tactile Switch keyboard, Forest colourway. 96% layout."},

            {"name": "Voicsky Echo 75 Cloudy Tactile Light",
             "sku": "KB-VSK-E75-CLOUD-LGT-NEW",   "cat": "Keyboard", "sup": BL,
             "cond": "New",   "price": Decimal("219.00"),  "stock": 4, "reorder": 2,
             "desc": "Voicsky Echo 75 Cloudy Tactile Switch keyboard, Light colourway. 75% gasket mount."},

            {"name": "Voicsky Nimbus 65 Tone Linear Dark",
             "sku": "KB-VSK-N65-TONE-DRK-NEW",    "cat": "Keyboard", "sup": BL,
             "cond": "New",   "price": Decimal("215.00"),  "stock": 4, "reorder": 2,
             "desc": "Voicsky Nimbus 65 Tone Linear Switch keyboard, Dark colourway. 65% layout."},

            {"name": "Voicsky Atmos 87 Tone Linear Dark",
             "sku": "KB-VSK-A87-TONE-DRK-NEW",    "cat": "Keyboard", "sup": BL,
             "cond": "New",   "price": Decimal("280.00"),  "stock": 4, "reorder": 2,
             "desc": "Voicsky Atmos 87 Tone Linear Switch keyboard, Dark colourway. TKL layout."},

            # ── MOUSE ─────────────────────────────────────────────────────────
            {"name": "Marvo WM111 Wireless Mouse",
             "sku": "MOUSE-MARVO-WM111-NEW",      "cat": "Mouse", "sup": BL,
             "cond": "New",   "price": Decimal("39.00"),   "stock": 15, "reorder": 5,
             "desc": "Marvo WM111 Wireless Mouse. Budget wireless mouse."},

            {"name": "Marvo Gaming M292 White",
             "sku": "MOUSE-MARVO-M292-WHT-NEW",   "cat": "Mouse", "sup": BL,
             "cond": "New",   "price": Decimal("40.00"),   "stock": 12, "reorder": 5,
             "desc": "Marvo Gaming M292 White wired gaming mouse."},

            {"name": "Marvo Gaming M355 + G1 Gaming Combo",
             "sku": "MOUSE-MARVO-M355G1-NEW",     "cat": "Mouse", "sup": BL,
             "cond": "New",   "price": Decimal("45.00"),   "stock": 10, "reorder": 4,
             "desc": "Marvo Gaming M355 + G1 Gaming Combo (Mouse + Mousepad)."},

            {"name": "Marvo Gaming M727 White Gaming Mouse",
             "sku": "MOUSE-MARVO-M727-WHT-NEW",   "cat": "Mouse", "sup": BL,
             "cond": "New",   "price": Decimal("69.00"),   "stock": 10, "reorder": 4,
             "desc": "Marvo Gaming M727 White wired gaming mouse."},

            {"name": "Marvo Gaming Fit Lite G1 Gaming Mouse Black",
             "sku": "MOUSE-MARVO-FITG1-BLK-NEW",  "cat": "Mouse", "sup": BL,
             "cond": "New",   "price": Decimal("89.00"),   "stock": 8, "reorder": 3,
             "desc": "Marvo Gaming Fit Lite G1 Gaming Mouse, Black."},

            {"name": "Marvo Gaming Fit Lite G1 Gaming Mouse White",
             "sku": "MOUSE-MARVO-FITG1-WHT-NEW",  "cat": "Mouse", "sup": BL,
             "cond": "New",   "price": Decimal("89.00"),   "stock": 6, "reorder": 2,
             "desc": "Marvo Gaming Fit Lite G1 Gaming Mouse, White."},

            {"name": "Marvo Gaming M803W Black Wireless Gaming Mouse",
             "sku": "MOUSE-MARVO-M803W-BLK-NEW",  "cat": "Mouse", "sup": BL,
             "cond": "New",   "price": Decimal("65.00"),   "stock": 8, "reorder": 3,
             "desc": "Marvo Gaming M803W Wireless Gaming Mouse, Black."},

            {"name": "Marvo Gaming M803W White/Blue Wireless Gaming Mouse",
             "sku": "MOUSE-MARVO-M803W-WB-NEW",   "cat": "Mouse", "sup": BL,
             "cond": "New",   "price": Decimal("69.00"),   "stock": 6, "reorder": 2,
             "desc": "Marvo Gaming M803W Wireless Gaming Mouse, White/Blue colourway."},

            {"name": "Fantech Hive UX2 Gaming Mouse",
             "sku": "MOUSE-FT-HIVE-UX2-NEW",      "cat": "Mouse", "sup": BL,
             "cond": "New",   "price": Decimal("129.00"),  "stock": 6, "reorder": 2,
             "desc": "Fantech Hive UX2 wired gaming mouse."},

            {"name": "AOC GM180B Wired Gaming Mouse",
             "sku": "MOUSE-AOC-GM180B-NEW",        "cat": "Mouse", "sup": IM,
             "cond": "New",   "price": Decimal("49.00"),   "stock": 10, "reorder": 4,
             "desc": "AOC GM180B wired gaming mouse."},

            {"name": "AOC GM190B Wired Gaming Mouse",
             "sku": "MOUSE-AOC-GM190B-NEW",        "cat": "Mouse", "sup": IM,
             "cond": "New",   "price": Decimal("49.00"),   "stock": 10, "reorder": 4,
             "desc": "AOC GM190B wired gaming mouse."},

            {"name": "AOC GM220B Wireless Gaming Mouse Black",
             "sku": "MOUSE-AOC-GM220B-BLK-NEW",   "cat": "Mouse", "sup": IM,
             "cond": "New",   "price": Decimal("69.00"),   "stock": 6, "reorder": 2,
             "desc": "AOC GM220B Wireless Gaming Mouse, Black."},

            {"name": "Acer Predator Cestus 327 Gaming Mouse",
             "sku": "MOUSE-ACR-C327-NEW",          "cat": "Mouse", "sup": IM,
             "cond": "New",   "price": Decimal("69.00"),   "stock": 6, "reorder": 2,
             "desc": "Acer Predator Cestus 327 wired gaming mouse."},

            {"name": "Acer Predator Cestus 330 Gaming Mouse",
             "sku": "MOUSE-ACR-C330-NEW",          "cat": "Mouse", "sup": IM,
             "cond": "New",   "price": Decimal("79.00"),   "stock": 5, "reorder": 2,
             "desc": "Acer Predator Cestus 330 wired gaming mouse."},

            # ── HEADSET ───────────────────────────────────────────────────────
            {"name": "Marvo Gaming H8325 Pulz 30 Gaming Headset",
             "sku": "HS-MARVO-H8325-NEW",          "cat": "Headset", "sup": BL,
             "cond": "New",   "price": Decimal("59.00"),   "stock": 10, "reorder": 4,
             "desc": "Marvo Gaming H8325 Pulz 30 wired gaming headset."},

            {"name": "Marvo Gaming H8326 Akari 40 Gaming Headset",
             "sku": "HS-MARVO-H8326-NEW",          "cat": "Headset", "sup": BL,
             "cond": "New",   "price": Decimal("59.00"),   "stock": 10, "reorder": 4,
             "desc": "Marvo Gaming H8326 Akari 40 wired gaming headset."},

            {"name": "AOC ACG2510BK Wired RGB Gaming Headset Black",
             "sku": "HS-AOC-ACG2510BK-NEW",        "cat": "Headset", "sup": IM,
             "cond": "New",   "price": Decimal("69.00"),   "stock": 8, "reorder": 3,
             "desc": "AOC ACG2510BK Wired RGB Gaming Headset, Black."},

            {"name": "Tecware Q3 Wireless Gaming Headset",
             "sku": "HS-TW-Q3-NEW",                "cat": "Headset", "sup": BL,
             "cond": "New",   "price": Decimal("153.00"),  "stock": 5, "reorder": 2,
             "desc": "Tecware Q3 Wireless Gaming Headset."},

            {"name": "HyperX Cloud Stinger 2 Gaming Headset White",
             "sku": "HS-HX-STNGR2-WHT-NEW",        "cat": "Headset", "sup": IM,
             "cond": "New",   "price": Decimal("209.00"),  "stock": 4, "reorder": 2,
             "desc": "HyperX Cloud Stinger 2 Gaming Headset, White edition."},

            # ── SPEAKER ───────────────────────────────────────────────────────
            {"name": "Vinnfier Icon 100 Speaker",
             "sku": "SPK-VNF-ICON100-NEW",         "cat": "Speaker", "sup": BL,
             "cond": "New",   "price": Decimal("35.00"),   "stock": 10, "reorder": 4,
             "desc": "Vinnfier Icon 100 compact desktop speaker."},

            # ── CONTROLLER ────────────────────────────────────────────────────
            {"name": "Marvo Gaming GT-019 Pact 40 Gaming Controller",
             "sku": "CTRL-MARVO-GT019-NEW",        "cat": "Controller", "sup": BL,
             "cond": "New",   "price": Decimal("69.00"),   "stock": 8, "reorder": 3,
             "desc": "Marvo Gaming GT-019 Pact 40 wired gaming controller."},

            {"name": "Marvo Gaming GT-80 Pact 60 Wireless Gaming Controller",
             "sku": "CTRL-MARVO-GT80-NEW",         "cat": "Controller", "sup": BL,
             "cond": "New",   "price": Decimal("99.00"),   "stock": 6, "reorder": 2,
             "desc": "Marvo Gaming GT-80 Pact 60 wireless gaming controller."},

            # ── ACCESSORIES / MISC ────────────────────────────────────────────
            {"name": "WiFi 6 & Bluetooth Adapter",
             "sku": "ACC-WIFI6-BT-NEW",            "cat": "Accessories", "sup": BL,
             "cond": "New",   "price": Decimal("39.00"),   "stock": 15, "reorder": 5,
             "desc": "WiFi 6 & Bluetooth PCIe adapter card."},

            {"name": "Orico 2.5\" Hard Drive Enclosure",
             "sku": "ACC-ORC-HDD-ENC-NEW",         "cat": "Accessories", "sup": BL,
             "cond": "New",   "price": Decimal("29.00"),   "stock": 15, "reorder": 5,
             "desc": "Orico 2.5\" USB3.0 Hard Drive Enclosure. For SATA SSD/HDD."},

            {"name": "Mercusys AC1200 WiFi/Bluetooth PCIe Adapter",
             "sku": "ACC-MRC-AC1200-NEW",          "cat": "Accessories", "sup": BL,
             "cond": "New",   "price": Decimal("89.00"),   "stock": 10, "reorder": 4,
             "desc": "Mercusys AC1200 Dual-Band WiFi & Bluetooth 4.2 PCIe Adapter."},

            {"name": "Cooler Master Thermal Compound Kit",
             "sku": "ACC-CM-THERM-KIT-NEW",        "cat": "Accessories", "sup": BL,
             "cond": "New",   "price": Decimal("15.00"),   "stock": 30, "reorder": 10,
             "desc": "Cooler Master Thermal Compound kit for CPU/GPU."},

            {"name": "AOC AM102H2 Desk Mount Monitor Arm",
             "sku": "ACC-AOC-AM102H2-NEW",         "cat": "Accessories", "sup": IM,
             "cond": "New",   "price": Decimal("135.00"),  "stock": 5, "reorder": 2,
             "desc": "AOC AM102H2 Single Monitor Desk Mount Arm, Black & Orange."},

            {"name": "Thermalright TF-7 Thermal Paste",
             "sku": "ACC-TRL-TF7-NEW",             "cat": "Accessories", "sup": BL,
             "cond": "New",   "price": Decimal("15.00"),   "stock": 30, "reorder": 10,
             "desc": "Thermalright TF-7 high performance thermal paste."},

            {"name": "AsiaHorse Extension Cable 4-Kit",
             "sku": "ACC-ASH-EXT-4KIT-NEW",        "cat": "Accessories", "sup": BL,
             "cond": "New",   "price": Decimal("85.00"),   "stock": 10, "reorder": 4,
             "desc": "AsiaHorse Extension Cable 4-Kit: Mobo 24pin x1, PCIE 6+2pin x2, CPU 4+4pin x1. Sleeve cables."},

            {"name": "Flexible ARGB Board Mobo 24pin",
             "sku": "ACC-ARGB-BOARD-24P-NEW",      "cat": "Accessories", "sup": BL,
             "cond": "New",   "price": Decimal("89.00"),   "stock": 8, "reorder": 3,
             "desc": "Flexible ARGB LED Board for Motherboard 24-pin connector. Aesthetic cable mod."},

            {"name": "Flexible ARGB Board GPU",
             "sku": "ACC-ARGB-BOARD-GPU-NEW",      "cat": "Accessories", "sup": BL,
             "cond": "New",   "price": Decimal("89.00"),   "stock": 8, "reorder": 3,
             "desc": "Flexible ARGB LED Board for GPU power connector. Aesthetic cable mod."},

            {"name": "Slev.30 Extension Cable 4-Kit",
             "sku": "ACC-SLV-EXT-4KIT-NEW",        "cat": "Accessories", "sup": BL,
             "cond": "New",   "price": Decimal("69.00"),   "stock": 10, "reorder": 4,
             "desc": "Slev.30 Extension Cable 4-Kit: Mobo 24pin x1, PCIE 6+2pin x2, CPU 4+4pin x1. Budget sleeve cables."},

            {"name": "HDMI Cable",
             "sku": "ACC-CABLE-HDMI-NEW",          "cat": "Accessories", "sup": BL,
             "cond": "New",   "price": Decimal("29.00"),   "stock": 25, "reorder": 8,
             "desc": "Standard HDMI cable."},

            {"name": "Power Cord",
             "sku": "ACC-CABLE-POWE-NEW",          "cat": "Accessories", "sup": BL,
             "cond": "New",   "price": Decimal("25.00"),   "stock": 20, "reorder": 8,
             "desc": "Standard PC power cord (IEC C13 to 3-pin plug)."},

            {"name": "DP to HDMI Converter",
             "sku": "ACC-CONV-DP-HDMI-NEW",        "cat": "Accessories", "sup": BL,
             "cond": "New",   "price": Decimal("25.00"),   "stock": 15, "reorder": 5,
             "desc": "DisplayPort to HDMI converter/adapter."},

            {"name": "DisplayPort Cable",
             "sku": "ACC-CABLE-DP-NEW",            "cat": "Accessories", "sup": BL,
             "cond": "New",   "price": Decimal("29.00"),   "stock": 15, "reorder": 5,
             "desc": "Standard DisplayPort cable."},
        ]

        # ─────────────────────────────────────────
        # 5. INSERT PRODUCTS + INVENTORY + MOVEMENTS
        # ─────────────────────────────────────────
        inserted = 0
        skipped = 0
        for p in products_data:
            existing = db.query(Product).filter(Product.sku == p["sku"]).first()
            if existing:
                skipped += 1
                continue

            cat = cat_map[p["cat"]]
            sup = sup_map[p["sup"]]

            product = Product(
                category_id=cat.category_id,
                supplier_id=sup.supplier_id,
                product_name=p["name"],
                sku=p["sku"],
                description=p["desc"],
                condition=p["cond"],
                selling_price=p["price"],
                image_url=None,
                product_status="Active",
            )
            db.add(product)
            db.flush()

            db.add(Inventory(
                product_id=product.product_id,
                quantity_available=p["stock"],
                reorder_level=p["reorder"],
            ))

            db.add(StockMovement(
                product_id=product.product_id,
                movement_type="IN",
                quantity=p["stock"],
                remarks="Opening stock — seeded from BP Tech pricelist 10/11/2026",
            ))
            inserted += 1

        db.commit()
        print(f"Seeding complete! Inserted: {inserted} products, Skipped (already exist): {skipped}")
        print("All categories, suppliers, inventory and stock movements updated.")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
