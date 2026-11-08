"""
BP Tech Inventory Management System
[MEMBER 1: Backend and Database Developer]
Database Seeder Script: Initializes tables and populates sample data.
Run this script to seed categories, suppliers, products, inventory, movements, and default admin.
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
        # 1. Seed Admin
        admin = db.query(Admin).filter(Admin.username == DEFAULT_ADMIN_USERNAME).first()
        if not admin:
            admin = Admin(
                username=DEFAULT_ADMIN_USERNAME,
                hashed_password=get_password_hash(DEFAULT_ADMIN_PASSWORD),
                email=DEFAULT_ADMIN_EMAIL,
            )
            db.add(admin)
            print(f"Created default admin: {DEFAULT_ADMIN_USERNAME} / {DEFAULT_ADMIN_PASSWORD}")

        # 2. Seed Categories
        categories_data = [
            {"name": "Processors", "desc": "CPUs from AMD Ryzen and Intel Core series"},
            {"name": "Graphics Cards", "desc": "NVIDIA GeForce and AMD Radeon GPUs for gaming & workstation"},
            {"name": "Motherboards", "desc": "AM4, AM5, LGA1700, and LGA1851 motherboards"},
            {"name": "RAM", "desc": "DDR4 and DDR5 desktop gaming memory modules"},
            {"name": "Storage", "desc": "Fast NVMe M.2 SSDs and high-capacity SATA HDDs"},
            {"name": "Power Supplies", "desc": "80 PLUS Bronze, Gold, and Platinum power supply units"},
            {"name": "PC Accessories", "desc": "Gaming peripherals, fans, cables, and PC building accessories"},
        ]

        cat_map = {}
        for c in categories_data:
            existing = db.query(Category).filter(Category.category_name == c["name"]).first()
            if not existing:
                existing = Category(category_name=c["name"], description=c["desc"])
                db.add(existing)
                db.flush()
            cat_map[c["name"]] = existing

        # 3. Seed Suppliers
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

        # 4. Seed Products with Inventory & Stock Movements
        products_data = [
            {
                "name": "AMD Ryzen 5 5600",
                "sku": "CPU-AMD-5600-NEW",
                "category": "Processors",
                "supplier": "Ban Leong Technologies",
                "condition": "New",
                "price": Decimal("529.00"),
                "stock": 14,
                "reorder": 5,
                "image": "https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?w=500&auto=format&fit=crop&q=60",
                "desc": "6 Cores, 12 Threads, Up to 4.4 GHz Max Boost, Socket AM4, PCIe 4.0 support with Wraith Stealth Cooler.",
            },
            {
                "name": "Intel Core i5-13400F",
                "sku": "CPU-INT-13400F-NEW",
                "category": "Processors",
                "supplier": "Ingram Micro Malaysia",
                "condition": "New",
                "price": Decimal("799.00"),
                "stock": 8,
                "reorder": 4,
                "image": "https://images.unsplash.com/photo-1555680202-c86f0e12f086?w=500&auto=format&fit=crop&q=60",
                "desc": "10 Cores (6P + 4E), 16 Threads, Up to 4.6 GHz, LGA1700 socket, Discrete graphics required.",
            },
            {
                "name": "NVIDIA GeForce RTX 3060 12GB (Used)",
                "sku": "GPU-NV-3060-USED-01",
                "category": "Graphics Cards",
                "supplier": "BP Tech Trade-In & Direct Sourcing",
                "condition": "Used",
                "price": Decimal("980.00"),
                "stock": 3,
                "reorder": 2,
                "image": "https://images.unsplash.com/photo-1587202372775-e229f172b9d7?w=500&auto=format&fit=crop&q=60",
                "desc": "Tested 100% stress pass (FurMark & 3DMark). 12GB GDDR6 VRAM, Ray Tracing, DLSS. 1-Month Store Warranty.",
            },
            {
                "name": "NVIDIA GeForce RTX 4060 8GB GDDR6",
                "sku": "GPU-NV-4060-NEW",
                "category": "Graphics Cards",
                "supplier": "Ban Leong Technologies",
                "condition": "New",
                "price": Decimal("1399.00"),
                "stock": 6,
                "reorder": 3,
                "image": "https://images.unsplash.com/photo-1591488320449-011701bb6704?w=500&auto=format&fit=crop&q=60",
                "desc": "Ada Lovelace architecture, DLSS 3 Frame Generation, 8GB GDDR6, 115W low TDP, brand new with 3-year warranty.",
            },
            {
                "name": "MSI B550M PRO-VDH WIFI",
                "sku": "MB-MSI-B550M-NEW",
                "category": "Motherboards",
                "supplier": "Tech Data Malaysia",
                "condition": "New",
                "price": Decimal("449.00"),
                "stock": 10,
                "reorder": 4,
                "image": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=500&auto=format&fit=crop&q=60",
                "desc": "Micro-ATX Socket AM4, PCIe 4.0, Dual M.2 slots, Built-in Wi-Fi and Bluetooth, Core Boost technology.",
            },
            {
                "name": "Kingston FURY Beast 16GB (2x8GB) DDR4 3200MHz",
                "sku": "RAM-KST-16GB-3200-NEW",
                "category": "RAM",
                "supplier": "Ingram Micro Malaysia",
                "condition": "New",
                "price": Decimal("165.00"),
                "stock": 25,
                "reorder": 8,
                "image": "https://images.unsplash.com/photo-1562976540-1502c2145186?w=500&auto=format&fit=crop&q=60",
                "desc": "High-performance low-profile heat spreader, Intel XMP 2.0 ready, AMD Ryzen compatible, Lifetime warranty.",
            },
            {
                "name": "Corsair Vengeance LPX 16GB DDR4 3200MHz (Used)",
                "sku": "RAM-COR-16GB-USED-02",
                "category": "RAM",
                "supplier": "BP Tech Trade-In & Direct Sourcing",
                "condition": "Used",
                "price": Decimal("115.00"),
                "stock": 2,
                "reorder": 3,
                "image": "https://images.unsplash.com/photo-1562976540-1502c2145186?w=500&auto=format&fit=crop&q=60",
                "desc": "Trade-in memory stick, MemTest86 verified error-free. 1-Month Store Warranty.",
            },
            {
                "name": "Kingston NV2 1TB PCIe 4.0 NVMe M.2 SSD",
                "sku": "SSD-KST-NV2-1TB-NEW",
                "category": "Storage",
                "supplier": "Ban Leong Technologies",
                "condition": "New",
                "price": Decimal("289.00"),
                "stock": 18,
                "reorder": 5,
                "image": "https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?w=500&auto=format&fit=crop&q=60",
                "desc": "Gen 4x4 NVMe PCIe performance, speeds up to 3500MB/s Read, 2100MB/s Write. 3-Year official warranty.",
            },
            {
                "name": "FSP HV PRO 650W 80 PLUS Bronze",
                "sku": "PSU-FSP-650W-NEW",
                "category": "Power Supplies",
                "supplier": "Tech Data Malaysia",
                "condition": "New",
                "price": Decimal("239.00"),
                "stock": 12,
                "reorder": 4,
                "image": "https://images.unsplash.com/photo-1587202372634-32705e3bf49c?w=500&auto=format&fit=crop&q=60",
                "desc": "True 650W continuous output, 80 PLUS Bronze certified 85% efficiency, 120mm quiet fan, flat black cables.",
            },
            {
                "name": "Thermal Grizzly Kryonaut Thermal Paste (1g)",
                "sku": "ACC-TG-KRYO-1G-NEW",
                "category": "PC Accessories",
                "supplier": "Ban Leong Technologies",
                "condition": "New",
                "price": Decimal("38.00"),
                "stock": 30,
                "reorder": 10,
                "image": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=500&auto=format&fit=crop&q=60",
                "desc": "Extremely high thermal conductivity (12.5 W/mk), ideal for CPU delidding and custom PC building.",
            },
            {
                "name": "Corsair CV550 550W 80 PLUS Bronze (Used)",
                "sku": "PSU-COR-CV550-USED",
                "category": "Power Supplies",
                "supplier": "BP Tech Trade-In & Direct Sourcing",
                "condition": "Used",
                "price": Decimal("130.00"),
                "stock": 1,
                "reorder": 2,
                "image": "https://images.unsplash.com/photo-1587202372634-32705e3bf49c?w=500&auto=format&fit=crop&q=60",
                "desc": "Clean power supply tested with voltage meter. Clean fan and capacitors. 1-Month Store Warranty.",
            },
        ]

        for p_info in products_data:
            existing = db.query(Product).filter(Product.sku == p_info["sku"]).first()
            if not existing:
                cat = cat_map[p_info["category"]]
                sup = sup_map[p_info["supplier"]]
                product = Product(
                    category_id=cat.category_id,
                    supplier_id=sup.supplier_id,
                    product_name=p_info["name"],
                    sku=p_info["sku"],
                    description=p_info["desc"],
                    condition=p_info["condition"],
                    selling_price=p_info["price"],
                    image_url=p_info["image"],
                    product_status="Active",
                )
                db.add(product)
                db.flush()

                inventory = Inventory(
                    product_id=product.product_id,
                    quantity_available=p_info["stock"],
                    reorder_level=p_info["reorder"],
                )
                db.add(inventory)

                movement = StockMovement(
                    product_id=product.product_id,
                    movement_type="IN",
                    quantity=p_info["stock"],
                    remarks="Opening stock seeded from BP Tech inventory record",
                )
                db.add(movement)

        db.commit()
        print("Database seeded successfully with initial products, inventory, and stock movements!")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
