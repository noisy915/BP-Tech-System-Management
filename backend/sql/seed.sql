-- ====================================================================
-- BP TECH INVENTORY MANAGEMENT SYSTEM
-- [MEMBER 1: Backend and Database Developer]
-- PostgreSQL Sample Seed Data
-- ====================================================================

-- Default Admin (Password: admin123 hashed with bcrypt)
INSERT INTO admins (username, hashed_password, email) VALUES
('admin', '$2b$12$K.FmX6dKxZJ414g3s8/Z3e2F4P20n8YmH7pWfQ1nFqZ02lUoY3S1u', 'admin@bptech.com');

-- Categories
INSERT INTO categories (category_name, description) VALUES
('Processors', 'CPUs from AMD Ryzen and Intel Core series'),
('Graphics Cards', 'NVIDIA GeForce and AMD Radeon GPUs for gaming & workstation'),
('Motherboards', 'AM4, AM5, LGA1700, and LGA1851 motherboards'),
('RAM', 'DDR4 and DDR5 desktop gaming memory modules'),
('Storage', 'Fast NVMe M.2 SSDs and high-capacity SATA HDDs'),
('Power Supplies', '80 PLUS Bronze, Gold, and Platinum power supply units'),
('PC Accessories', 'Gaming peripherals, fans, cables, and PC building accessories');

-- Suppliers
INSERT INTO suppliers (supplier_name, contact_number, email, address) VALUES
('Ban Leong Technologies', '+603-7956-6300', 'sales@banleong.com.my', 'Petaling Jaya, Selangor, Malaysia'),
('Ingram Micro Malaysia', '+603-7952-8188', 'orders@ingrammicro.com.my', 'Kuala Lumpur, Malaysia'),
('Tech Data Malaysia', '+603-7880-9999', 'info@techdata.com.my', 'Subang Jaya, Selangor, Malaysia'),
('BP Tech Trade-In & Direct Sourcing', '+601-2345-6789', 'tradein@bptech.com.my', 'Batu Pahat, Johor, Malaysia');

-- Products
INSERT INTO products (category_id, supplier_id, product_name, sku, description, condition, selling_price, image_url, product_status) VALUES
(1, 1, 'AMD Ryzen 5 5600', 'CPU-AMD-5600-NEW', '6 Cores, 12 Threads, Up to 4.4 GHz Max Boost, Socket AM4, PCIe 4.0 support with Wraith Stealth Cooler.', 'New', 529.00, 'https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?w=500&auto=format&fit=crop&q=60', 'Active'),
(1, 2, 'Intel Core i5-13400F', 'CPU-INT-13400F-NEW', '10 Cores (6P + 4E), 16 Threads, Up to 4.6 GHz, LGA1700 socket, Discrete graphics required.', 'New', 799.00, 'https://images.unsplash.com/photo-1555680202-c86f0e12f086?w=500&auto=format&fit=crop&q=60', 'Active'),
(2, 4, 'NVIDIA GeForce RTX 3060 12GB (Used)', 'GPU-NV-3060-USED-01', 'Tested 100% stress pass (FurMark & 3DMark). 12GB GDDR6 VRAM, Ray Tracing, DLSS. 1-Month Store Warranty.', 'Used', 980.00, 'https://images.unsplash.com/photo-1587202372775-e229f172b9d7?w=500&auto=format&fit=crop&q=60', 'Active'),
(2, 1, 'NVIDIA GeForce RTX 4060 8GB GDDR6', 'GPU-NV-4060-NEW', 'Ada Lovelace architecture, DLSS 3 Frame Generation, 8GB GDDR6, 115W low TDP, brand new with 3-year warranty.', 'New', 1399.00, 'https://images.unsplash.com/photo-1591488320449-011701bb6704?w=500&auto=format&fit=crop&q=60', 'Active'),
(3, 3, 'MSI B550M PRO-VDH WIFI', 'MB-MSI-B550M-NEW', 'Micro-ATX Socket AM4, PCIe 4.0, Dual M.2 slots, Built-in Wi-Fi and Bluetooth, Core Boost technology.', 'New', 449.00, 'https://images.unsplash.com/photo-1518770660439-4636190af475?w=500&auto=format&fit=crop&q=60', 'Active'),
(4, 2, 'Kingston FURY Beast 16GB (2x8GB) DDR4 3200MHz', 'RAM-KST-16GB-3200-NEW', 'High-performance low-profile heat spreader, Intel XMP 2.0 ready, AMD Ryzen compatible, Lifetime warranty.', 'New', 165.00, 'https://images.unsplash.com/photo-1562976540-1502c2145186?w=500&auto=format&fit=crop&q=60', 'Active'),
(4, 4, 'Corsair Vengeance LPX 16GB DDR4 3200MHz (Used)', 'RAM-COR-16GB-USED-02', 'Trade-in memory stick, MemTest86 verified error-free. 1-Month Store Warranty.', 'Used', 115.00, 'https://images.unsplash.com/photo-1562976540-1502c2145186?w=500&auto=format&fit=crop&q=60', 'Active'),
(5, 1, 'Kingston NV2 1TB PCIe 4.0 NVMe M.2 SSD', 'SSD-KST-NV2-1TB-NEW', 'Gen 4x4 NVMe PCIe performance, speeds up to 3500MB/s Read, 2100MB/s Write. 3-Year official warranty.', 'New', 289.00, 'https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?w=500&auto=format&fit=crop&q=60', 'Active'),
(6, 3, 'FSP HV PRO 650W 80 PLUS Bronze', 'PSU-FSP-650W-NEW', 'True 650W continuous output, 80 PLUS Bronze certified 85% efficiency, 120mm quiet fan, flat black cables.', 'New', 239.00, 'https://images.unsplash.com/photo-1587202372634-32705e3bf49c?w=500&auto=format&fit=crop&q=60', 'Active'),
(7, 1, 'Thermal Grizzly Kryonaut Thermal Paste (1g)', 'ACC-TG-KRYO-1G-NEW', 'Extremely high thermal conductivity (12.5 W/mk), ideal for CPU delidding and custom PC building.', 'New', 38.00, 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=500&auto=format&fit=crop&q=60', 'Active'),
(6, 4, 'Corsair CV550 550W 80 PLUS Bronze (Used)', 'PSU-COR-CV550-USED', 'Clean power supply tested with voltage meter. Clean fan and capacitors. 1-Month Store Warranty.', 'Used', 130.00, 'https://images.unsplash.com/photo-1587202372634-32705e3bf49c?w=500&auto=format&fit=crop&q=60', 'Active');

-- Inventory (1:1 with Products)
INSERT INTO inventory (product_id, quantity_available, reorder_level) VALUES
(1, 14, 5),
(2, 8, 4),
(3, 3, 2),
(4, 6, 3),
(5, 10, 4),
(6, 25, 8),
(7, 2, 3),
(8, 18, 5),
(9, 12, 4),
(10, 30, 10),
(11, 1, 2);

-- Stock Movements (Initial Opening Stock Log)
INSERT INTO stock_movements (product_id, movement_type, quantity, remarks) VALUES
(1, 'IN', 14, 'Initial stock import'),
(2, 'IN', 8, 'Initial stock import'),
(3, 'IN', 3, 'Trade-in purchase from customer'),
(4, 'IN', 6, 'Initial stock import'),
(5, 'IN', 10, 'Initial stock import'),
(6, 'IN', 25, 'Initial stock import'),
(7, 'IN', 2, 'Trade-in purchase from customer'),
(8, 'IN', 18, 'Initial stock import'),
(9, 'IN', 12, 'Initial stock import'),
(10, 'IN', 30, 'Initial stock import'),
(11, 'IN', 1, 'Trade-in purchase from customer');
