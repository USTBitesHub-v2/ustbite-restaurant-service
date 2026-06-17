"""create_restaurant_tables_with_seed_data

Revision ID: 2b3c4d5e6f7a
Revises: 1a2b3c4d5e6f
Create Date: 2026-04-25 00:00:00

Creates restaurants, menu_categories, menu_items tables and inserts
seed data for the USTH campus canteen.
"""
from alembic import op
import sqlalchemy as sa

revision = '2b3c4d5e6f7a'
down_revision = '1a2b3c4d5e6f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # asyncpg requires ONE statement per op.execute() call

    op.execute("""
        CREATE TABLE IF NOT EXISTS restaurants (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            name VARCHAR NOT NULL,
            cuisine_type VARCHAR,
            description VARCHAR,
            floor_number VARCHAR,
            opening_time VARCHAR,
            closing_time VARCHAR,
            is_open BOOLEAN DEFAULT FALSE,
            rating NUMERIC(3,1),
            image_url VARCHAR,
            min_order_amount NUMERIC(10,2),
            estimated_delivery_minutes INTEGER
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS menu_categories (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            restaurant_id UUID NOT NULL REFERENCES restaurants(id) ON DELETE CASCADE,
            name VARCHAR NOT NULL,
            display_order INTEGER DEFAULT 0,
            is_active BOOLEAN DEFAULT TRUE
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS menu_items (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            category_id UUID NOT NULL REFERENCES menu_categories(id) ON DELETE CASCADE,
            restaurant_id UUID NOT NULL REFERENCES restaurants(id) ON DELETE CASCADE,
            name VARCHAR NOT NULL,
            description VARCHAR,
            price NUMERIC(10,2) NOT NULL,
            is_available BOOLEAN DEFAULT TRUE,
            is_vegetarian BOOLEAN DEFAULT FALSE,
            image_url VARCHAR,
            prep_time_minutes INTEGER
        )
    """)


    # ── Seed: 4 campus restaurants ──────────────────────────────────────────
    op.execute("""
        INSERT INTO restaurants (id, name, cuisine_type, description, floor_number,
            opening_time, closing_time, is_open, rating, min_order_amount,
            estimated_delivery_minutes)
        VALUES
            ('a1111111-1111-1111-1111-111111111111',
             'Malabar Kitchen', 'South Indian',
             'Authentic South Indian breakfast and lunch served fresh daily',
             '1', '08:00', '20:00', TRUE, 4.3, 50.00, 15),
            ('a2222222-2222-2222-2222-222222222222',
             'North Bites', 'North Indian',
             'Hearty North Indian meals with fresh rotis and rich curries',
             '2', '11:00', '21:00', TRUE, 4.1, 80.00, 20),
            ('a3333333-3333-3333-3333-333333333333',
             'Campus Café', 'Café',
             'Coffee, sandwiches and light bites — your go-to study break spot',
             'Ground', '07:30', '22:00', TRUE, 4.5, 40.00, 10),
            ('a4444444-4444-4444-4444-444444444444',
             'Quick Bites', 'Snacks',
             'Fast Indian street snacks to keep you going between classes',
             '3', '09:00', '19:00', TRUE, 4.0, 20.00, 5)
        ON CONFLICT (id) DO NOTHING;
    """)

    # ── Seed: Menu categories ───────────────────────────────────────────────
    op.execute("""
        INSERT INTO menu_categories (id, restaurant_id, name, display_order, is_active)
        VALUES
            -- Malabar Kitchen
            ('b1111111-1111-1111-1111-111111111111', 'a1111111-1111-1111-1111-111111111111', 'Breakfast', 1, TRUE),
            ('b1111111-1111-1111-1111-111111111112', 'a1111111-1111-1111-1111-111111111111', 'Beverages', 2, TRUE),
            ('b1111111-1111-1111-1111-111111111113', 'a1111111-1111-1111-1111-111111111111', 'Lunch', 3, TRUE),
            -- North Bites
            ('b2222222-2222-2222-2222-222222222221', 'a2222222-2222-2222-2222-222222222222', 'Starters', 1, TRUE),
            ('b2222222-2222-2222-2222-222222222222', 'a2222222-2222-2222-2222-222222222222', 'Mains', 2, TRUE),
            ('b2222222-2222-2222-2222-222222222223', 'a2222222-2222-2222-2222-222222222222', 'Breads', 3, TRUE),
            -- Campus Café
            ('b3333333-3333-3333-3333-333333333331', 'a3333333-3333-3333-3333-333333333333', 'Beverages', 1, TRUE),
            ('b3333333-3333-3333-3333-333333333332', 'a3333333-3333-3333-3333-333333333333', 'Snacks', 2, TRUE),
            -- Quick Bites
            ('b4444444-4444-4444-4444-444444444441', 'a4444444-4444-4444-4444-444444444444', 'Snacks', 1, TRUE),
            ('b4444444-4444-4444-4444-444444444442', 'a4444444-4444-4444-4444-444444444444', 'Beverages', 2, TRUE)
        ON CONFLICT (id) DO NOTHING;
    """)

    # ── Seed: Menu items ────────────────────────────────────────────────────
    op.execute("""
        INSERT INTO menu_items (id, category_id, restaurant_id, name, description,
            price, is_available, is_vegetarian, prep_time_minutes)
        VALUES
            -- Malabar Kitchen — Breakfast
            ('c1000001-0000-0000-0000-000000000001', 'b1111111-1111-1111-1111-111111111111', 'a1111111-1111-1111-1111-111111111111',
             'Masala Dosa', 'Crispy dosa with spiced potato filling and chutneys', 60.00, TRUE, TRUE, 12),
            ('c1000001-0000-0000-0000-000000000002', 'b1111111-1111-1111-1111-111111111111', 'a1111111-1111-1111-1111-111111111111',
             'Idli Sambar (2 pcs)', 'Soft steamed rice cakes with sambar and chutneys', 45.00, TRUE, TRUE, 8),
            ('c1000001-0000-0000-0000-000000000003', 'b1111111-1111-1111-1111-111111111111', 'a1111111-1111-1111-1111-111111111111',
             'Medu Vada', 'Crispy lentil fritters with sambar and coconut chutney', 50.00, TRUE, TRUE, 10),
            ('c1000001-0000-0000-0000-000000000004', 'b1111111-1111-1111-1111-111111111111', 'a1111111-1111-1111-1111-111111111111',
             'Upma', 'Savory semolina porridge with vegetables and spices', 40.00, TRUE, TRUE, 8),
            -- Malabar Kitchen — Beverages
            ('c1000002-0000-0000-0000-000000000001', 'b1111111-1111-1111-1111-111111111112', 'a1111111-1111-1111-1111-111111111111',
             'Filter Coffee', 'Traditional South Indian decoction coffee with frothy milk', 30.00, TRUE, TRUE, 5),
            ('c1000002-0000-0000-0000-000000000002', 'b1111111-1111-1111-1111-111111111112', 'a1111111-1111-1111-1111-111111111111',
             'Masala Chai', 'Spiced milk tea with ginger, cardamom and tulsi', 20.00, TRUE, TRUE, 5),
            -- Malabar Kitchen — Lunch
            ('c1000003-0000-0000-0000-000000000001', 'b1111111-1111-1111-1111-111111111113', 'a1111111-1111-1111-1111-111111111111',
             'Meals (Veg Thali)', 'Full South Indian meal with rice, dal, sabzi, papad and pickle', 120.00, TRUE, TRUE, 15),
            ('c1000003-0000-0000-0000-000000000002', 'b1111111-1111-1111-1111-111111111113', 'a1111111-1111-1111-1111-111111111111',
             'Curd Rice', 'Creamy tempered curd rice with curry leaves and mustard', 60.00, TRUE, TRUE, 5),

            -- North Bites — Starters
            ('c2000001-0000-0000-0000-000000000001', 'b2222222-2222-2222-2222-222222222221', 'a2222222-2222-2222-2222-222222222222',
             'Paneer Tikka', 'Marinated paneer grilled in tandoor with mint chutney', 150.00, TRUE, TRUE, 15),
            ('c2000001-0000-0000-0000-000000000002', 'b2222222-2222-2222-2222-222222222221', 'a2222222-2222-2222-2222-222222222222',
             'Aloo Tikki', 'Crispy spiced potato patties with chutneys', 70.00, TRUE, TRUE, 10),
            -- North Bites — Mains
            ('c2000002-0000-0000-0000-000000000001', 'b2222222-2222-2222-2222-222222222222', 'a2222222-2222-2222-2222-222222222222',
             'Dal Makhani', 'Slow-cooked black lentils in rich creamy tomato gravy', 120.00, TRUE, TRUE, 20),
            ('c2000002-0000-0000-0000-000000000002', 'b2222222-2222-2222-2222-222222222222', 'a2222222-2222-2222-2222-222222222222',
             'Paneer Butter Masala', 'Cottage cheese in creamy tomato-cashew gravy', 150.00, TRUE, TRUE, 20),
            ('c2000002-0000-0000-0000-000000000003', 'b2222222-2222-2222-2222-222222222222', 'a2222222-2222-2222-2222-222222222222',
             'Jeera Rice', 'Fragrant basmati rice tempered with cumin', 80.00, TRUE, TRUE, 10),
            -- North Bites — Breads
            ('c2000003-0000-0000-0000-000000000001', 'b2222222-2222-2222-2222-222222222223', 'a2222222-2222-2222-2222-222222222222',
             'Butter Roti (2 pcs)', 'Soft whole wheat flatbreads with butter', 25.00, TRUE, TRUE, 8),
            ('c2000003-0000-0000-0000-000000000002', 'b2222222-2222-2222-2222-222222222223', 'a2222222-2222-2222-2222-222222222222',
             'Garlic Naan (2 pcs)', 'Leavened bread baked in tandoor with garlic and butter', 50.00, TRUE, TRUE, 12),

            -- Campus Café — Beverages
            ('c3000001-0000-0000-0000-000000000001', 'b3333333-3333-3333-3333-333333333331', 'a3333333-3333-3333-3333-333333333333',
             'Cold Coffee', 'Chilled blended coffee with ice cream — campus favorite', 80.00, TRUE, TRUE, 5),
            ('c3000001-0000-0000-0000-000000000002', 'b3333333-3333-3333-3333-333333333331', 'a3333333-3333-3333-3333-333333333333',
             'Hot Cappuccino', 'Espresso with silky steamed milk foam', 70.00, TRUE, TRUE, 5),
            ('c3000001-0000-0000-0000-000000000003', 'b3333333-3333-3333-3333-333333333331', 'a3333333-3333-3333-3333-333333333333',
             'Fresh Lime Soda', 'Refreshing lime soda, sweet or salted', 50.00, TRUE, TRUE, 3),
            -- Campus Café — Snacks
            ('c3000002-0000-0000-0000-000000000001', 'b3333333-3333-3333-3333-333333333332', 'a3333333-3333-3333-3333-333333333333',
             'Grilled Sandwich', 'Cheese and veggie grilled sandwich with ketchup', 70.00, TRUE, TRUE, 8),
            ('c3000002-0000-0000-0000-000000000002', 'b3333333-3333-3333-3333-333333333332', 'a3333333-3333-3333-3333-333333333333',
             'Veg Pasta', 'Penne in creamy white sauce with mixed vegetables', 90.00, TRUE, TRUE, 12),
            ('c3000002-0000-0000-0000-000000000003', 'b3333333-3333-3333-3333-333333333332', 'a3333333-3333-3333-3333-333333333333',
             'Chocolate Brownie', 'Warm fudgy brownie with vanilla ice cream', 60.00, TRUE, TRUE, 5),

            -- Quick Bites — Snacks
            ('c4000001-0000-0000-0000-000000000001', 'b4444444-4444-4444-4444-444444444441', 'a4444444-4444-4444-4444-444444444444',
             'Samosa (2 pcs)', 'Crispy fried pastry stuffed with spiced potatoes and peas', 20.00, TRUE, TRUE, 5),
            ('c4000001-0000-0000-0000-000000000002', 'b4444444-4444-4444-4444-444444444441', 'a4444444-4444-4444-4444-444444444444',
             'Vada Pav', 'Spiced potato fritter in a soft bun — Mumbai classic', 30.00, TRUE, TRUE, 5),
            ('c4000001-0000-0000-0000-000000000003', 'b4444444-4444-4444-4444-444444444441', 'a4444444-4444-4444-4444-444444444444',
             'Masala Maggi', 'Quick noodles cooked with vegetables and spices', 50.00, TRUE, TRUE, 7),
            ('c4000001-0000-0000-0000-000000000004', 'b4444444-4444-4444-4444-444444444441', 'a4444444-4444-4444-4444-444444444444',
             'Bread Pakora', 'Spiced potato-stuffed bread deep fried in chickpea batter', 40.00, TRUE, TRUE, 6),
            -- Quick Bites — Beverages
            ('c4000002-0000-0000-0000-000000000001', 'b4444444-4444-4444-4444-444444444442', 'a4444444-4444-4444-4444-444444444444',
             'Nimbu Pani', 'Classic Indian lemonade with black salt', 25.00, TRUE, TRUE, 3),
            ('c4000002-0000-0000-0000-000000000002', 'b4444444-4444-4444-4444-444444444442', 'a4444444-4444-4444-4444-444444444444',
             'Buttermilk', 'Chilled spiced chaas with curry leaves and ginger', 20.00, TRUE, TRUE, 3)
        ON CONFLICT (id) DO NOTHING;
    """)


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS menu_items CASCADE;")
    op.execute("DROP TABLE IF EXISTS menu_categories CASCADE;")
    op.execute("DROP TABLE IF EXISTS restaurants CASCADE;")
