"""replace_restaurants_with_mockdata

Revision ID: 3c4d5e6f7a8b
Revises: 2b3c4d5e6f7a
Create Date: 2026-04-25
"""
from alembic import op

revision = '3c4d5e6f7a8b'
down_revision = '2b3c4d5e6f7a'
branch_labels = None
depends_on = None

# Image URLs from frontend constants.ts
COVER = {
    'si':  'https://images.unsplash.com/photo-1668236543090-82eba5ee5976?w=800&q=80',
    'cafe':'https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=800&q=80',
    'sar': 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=800&q=80',
    'bak': 'https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=800&q=80',
    'ana': 'https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=800&q=80',
    'edf': 'https://images.unsplash.com/photo-1622597467836-f3e6707b0ff5?w=800&q=80',
    'coc': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=80',
    'mam': 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=800&q=80',
}
IMG = {
    'dosa':     'https://images.unsplash.com/photo-1668236543090-82eba5ee5976?w=400&q=80',
    'idli':     'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=400&q=80',
    'biryani':  'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=400&q=80',
    'paneer':   'https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=400&q=80',
    'thali':    'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=400&q=80',
    'coffee':   'https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=400&q=80',
    'juice':    'https://images.unsplash.com/photo-1622597467836-f3e6707b0ff5?w=400&q=80',
    'sandwich': 'https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=400&q=80',
    'bakery':   'https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=400&q=80',
    'sugar':    'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&q=80',
}


def upgrade() -> None:
    # Clear existing seed data
    op.execute("DELETE FROM menu_items")
    op.execute("DELETE FROM menu_categories")
    op.execute("DELETE FROM restaurants")

    # 8 restaurants matching frontend mockData
    op.execute(f"""
        INSERT INTO restaurants (id, name, cuisine_type, description, floor_number,
            opening_time, closing_time, is_open, rating, min_order_amount,
            estimated_delivery_minutes, image_url)
        VALUES
          ('a0000001-0000-0000-0000-000000000001','Southern Delight','South Indian',
           'Authentic South Indian breakfast & meals served fresh all day.',
           'Ground Floor, Block A','08:00','21:00',TRUE,4.5,80,15,'{COVER["si"]}'),
          ('a0000002-0000-0000-0000-000000000001','Kaffeehaus','Café & Beverages',
           'Specialty coffee, sandwiches and quick bakes for your work breaks.',
           '1st Floor, Block B','07:30','22:00',TRUE,4.3,60,10,'{COVER["cafe"]}'),
          ('a0000003-0000-0000-0000-000000000001','Saravana Bhavan','South Indian',
           'The classic Saravana Bhavan experience — dosas, vadas, filter coffee.',
           'Ground Floor, Block C','08:00','21:00',TRUE,4.7,80,15,'{COVER["sar"]}'),
          ('a0000004-0000-0000-0000-000000000001','Supreme Bakers','Bakery & Snacks',
           'Fresh-baked puffs, pastries, breads and quick snacks throughout the day.',
           'Ground Floor, Block A','08:00','20:00',TRUE,4.4,50,10,'{COVER["bak"]}'),
          ('a0000005-0000-0000-0000-000000000001','Anandam','North Indian',
           'Hearty North & South Indian thalis, curries and home-style meals.',
           '2nd Floor, Block D','10:00','21:00',TRUE,4.6,100,20,'{COVER["ana"]}'),
          ('a0000006-0000-0000-0000-000000000001','EDF Juice','Beverages',
           'Cold-pressed juices, smoothies and healthy refreshers.',
           'Ground Floor, Block B','09:00','20:00',TRUE,4.5,40,5,'{COVER["edf"]}'),
          ('a0000007-0000-0000-0000-000000000001','Cococane Juicery','Beverages',
           'Sugarcane, tender coconut and refreshing beverages on the go.',
           'Ground Floor, Block C','09:00','20:00',TRUE,4.4,40,5,'{COVER["coc"]}'),
          ('a0000008-0000-0000-0000-000000000001','Mamta Food Restaurant','North Indian',
           'Generous North Indian portions with classic dal, sabzi and biryani.',
           '1st Floor, Block D','10:00','21:00',TRUE,4.3,100,20,'{COVER["mam"]}')
        ON CONFLICT (id) DO NOTHING
    """)

    # Categories
    op.execute("""
        INSERT INTO menu_categories (id, restaurant_id, name, display_order, is_active) VALUES
          ('b0000001-0001-0000-0000-000000000001','a0000001-0000-0000-0000-000000000001','Breakfast',1,TRUE),
          ('b0000001-0002-0000-0000-000000000001','a0000001-0000-0000-0000-000000000001','Mains',2,TRUE),
          ('b0000001-0003-0000-0000-000000000001','a0000001-0000-0000-0000-000000000001','Beverages',3,TRUE),
          ('b0000002-0001-0000-0000-000000000001','a0000002-0000-0000-0000-000000000001','Beverages',1,TRUE),
          ('b0000002-0002-0000-0000-000000000001','a0000002-0000-0000-0000-000000000001','Snacks',2,TRUE),
          ('b0000002-0003-0000-0000-000000000001','a0000002-0000-0000-0000-000000000001','Desserts',3,TRUE),
          ('b0000003-0001-0000-0000-000000000001','a0000003-0000-0000-0000-000000000001','Breakfast',1,TRUE),
          ('b0000003-0002-0000-0000-000000000001','a0000003-0000-0000-0000-000000000001','Mains',2,TRUE),
          ('b0000003-0003-0000-0000-000000000001','a0000003-0000-0000-0000-000000000001','Beverages',3,TRUE),
          ('b0000004-0001-0000-0000-000000000001','a0000004-0000-0000-0000-000000000001','Snacks',1,TRUE),
          ('b0000004-0002-0000-0000-000000000001','a0000004-0000-0000-0000-000000000001','Desserts',2,TRUE),
          ('b0000005-0001-0000-0000-000000000001','a0000005-0000-0000-0000-000000000001','Mains',1,TRUE),
          ('b0000005-0002-0000-0000-000000000001','a0000005-0000-0000-0000-000000000001','Breakfast',2,TRUE),
          ('b0000005-0003-0000-0000-000000000001','a0000005-0000-0000-0000-000000000001','Beverages',3,TRUE),
          ('b0000006-0001-0000-0000-000000000001','a0000006-0000-0000-0000-000000000001','Beverages',1,TRUE),
          ('b0000007-0001-0000-0000-000000000001','a0000007-0000-0000-0000-000000000001','Beverages',1,TRUE),
          ('b0000008-0001-0000-0000-000000000001','a0000008-0000-0000-0000-000000000001','Mains',1,TRUE),
          ('b0000008-0002-0000-0000-000000000001','a0000008-0000-0000-0000-000000000001','Breakfast',2,TRUE),
          ('b0000008-0003-0000-0000-000000000001','a0000008-0000-0000-0000-000000000001','Beverages',3,TRUE)
        ON CONFLICT (id) DO NOTHING
    """)

    # Southern Delight menu (R1)
    R1,B1,M1,V1 = 'a0000001-0000-0000-0000-000000000001','b0000001-0001-0000-0000-000000000001','b0000001-0002-0000-0000-000000000001','b0000001-0003-0000-0000-000000000001'
    op.execute(f"""INSERT INTO menu_items (category_id,restaurant_id,name,description,price,is_available,is_vegetarian,image_url,prep_time_minutes) VALUES
      ('{B1}','{R1}','Masala Dosa','Crisp dosa stuffed with spiced potato masala',60,TRUE,TRUE,'{IMG["dosa"]}',12),
      ('{B1}','{R1}','Plain Dosa','Classic golden crisp dosa with chutney & sambar',45,TRUE,TRUE,'{IMG["dosa"]}',10),
      ('{B1}','{R1}','Idli (2 pcs) with Sambar','Soft steamed rice cakes with hot sambar',40,TRUE,TRUE,'{IMG["idli"]}',8),
      ('{B1}','{R1}','Medu Vada (2 pcs)','Crispy lentil donuts served with chutney',45,TRUE,TRUE,'{IMG["idli"]}',10),
      ('{B1}','{R1}','Pongal with Sambar','Comforting rice & lentil porridge with ghee',55,TRUE,TRUE,'{IMG["thali"]}',10),
      ('{M1}','{R1}','Mini Meals','Light meal with rice, sambar, rasam & curd',90,TRUE,TRUE,'{IMG["thali"]}',15),
      ('{M1}','{R1}','Full Meals','Traditional South Indian thali with sides & sweet',120,TRUE,TRUE,'{IMG["thali"]}',20),
      ('{M1}','{R1}','Uthappam','Thick pancake topped with onion & tomato',65,TRUE,TRUE,'{IMG["dosa"]}',12),
      ('{M1}','{R1}','Lemon Rice','Tangy lemon rice with peanuts & curry leaves',55,TRUE,TRUE,'{IMG["thali"]}',10),
      ('{V1}','{R1}','Filter Coffee','Strong South Indian style filter coffee',25,TRUE,TRUE,'{IMG["coffee"]}',5)""")

    # Kaffeehaus menu (R2)
    R2,BV2,SN2,DS2 = 'a0000002-0000-0000-0000-000000000001','b0000002-0001-0000-0000-000000000001','b0000002-0002-0000-0000-000000000001','b0000002-0003-0000-0000-000000000001'
    op.execute(f"""INSERT INTO menu_items (category_id,restaurant_id,name,description,price,is_available,is_vegetarian,image_url,prep_time_minutes) VALUES
      ('{BV2}','{R2}','Cappuccino','Espresso topped with steamed milk foam',80,TRUE,TRUE,'{IMG["coffee"]}',5),
      ('{BV2}','{R2}','Latte','Smooth espresso with steamed milk',90,TRUE,TRUE,'{IMG["coffee"]}',5),
      ('{BV2}','{R2}','Cold Coffee','Chilled blended coffee with ice cream',95,TRUE,TRUE,'{IMG["coffee"]}',5),
      ('{BV2}','{R2}','Masala Chai','Spiced Indian milk tea',30,TRUE,TRUE,'{IMG["coffee"]}',5),
      ('{SN2}','{R2}','Veg Club Sandwich','Triple-decker with veggies, cheese & chutney',110,TRUE,TRUE,'{IMG["sandwich"]}',10),
      ('{SN2}','{R2}','Paneer Grilled Sandwich','Grilled sandwich with spicy paneer filling',120,TRUE,TRUE,'{IMG["sandwich"]}',10),
      ('{SN2}','{R2}','Croissant','Buttery, flaky French pastry',70,TRUE,TRUE,'{IMG["bakery"]}',5),
      ('{SN2}','{R2}','French Fries','Crispy golden fries with seasoning',90,TRUE,TRUE,'{IMG["sandwich"]}',8),
      ('{DS2}','{R2}','Chocolate Muffin','Warm chocolate muffin with chocolate chips',65,TRUE,TRUE,'{IMG["bakery"]}',5),
      ('{DS2}','{R2}','Brownie','Dense, fudgy chocolate brownie',75,TRUE,TRUE,'{IMG["bakery"]}',5)""")

    # Saravana Bhavan menu (R3 — same as Southern Delight)
    R3,B3,M3,V3 = 'a0000003-0000-0000-0000-000000000001','b0000003-0001-0000-0000-000000000001','b0000003-0002-0000-0000-000000000001','b0000003-0003-0000-0000-000000000001'
    op.execute(f"""INSERT INTO menu_items (category_id,restaurant_id,name,description,price,is_available,is_vegetarian,image_url,prep_time_minutes) VALUES
      ('{B3}','{R3}','Masala Dosa','Crisp dosa stuffed with spiced potato masala',60,TRUE,TRUE,'{IMG["dosa"]}',12),
      ('{B3}','{R3}','Plain Dosa','Classic golden crisp dosa with chutney & sambar',45,TRUE,TRUE,'{IMG["dosa"]}',10),
      ('{B3}','{R3}','Idli (2 pcs) with Sambar','Soft steamed rice cakes with hot sambar',40,TRUE,TRUE,'{IMG["idli"]}',8),
      ('{B3}','{R3}','Medu Vada (2 pcs)','Crispy lentil donuts served with chutney',45,TRUE,TRUE,'{IMG["idli"]}',10),
      ('{B3}','{R3}','Pongal with Sambar','Comforting rice & lentil porridge with ghee',55,TRUE,TRUE,'{IMG["thali"]}',10),
      ('{M3}','{R3}','Mini Meals','Light meal with rice, sambar, rasam & curd',90,TRUE,TRUE,'{IMG["thali"]}',15),
      ('{M3}','{R3}','Full Meals','Traditional South Indian thali with sides & sweet',120,TRUE,TRUE,'{IMG["thali"]}',20),
      ('{M3}','{R3}','Uthappam','Thick pancake topped with onion & tomato',65,TRUE,TRUE,'{IMG["dosa"]}',12),
      ('{M3}','{R3}','Lemon Rice','Tangy lemon rice with peanuts & curry leaves',55,TRUE,TRUE,'{IMG["thali"]}',10),
      ('{V3}','{R3}','Filter Coffee','Strong South Indian style filter coffee',25,TRUE,TRUE,'{IMG["coffee"]}',5)""")

    # Supreme Bakers (R4)
    R4,SN4,DS4 = 'a0000004-0000-0000-0000-000000000001','b0000004-0001-0000-0000-000000000001','b0000004-0002-0000-0000-000000000001'
    op.execute(f"""INSERT INTO menu_items (category_id,restaurant_id,name,description,price,is_available,is_vegetarian,image_url,prep_time_minutes) VALUES
      ('{SN4}','{R4}','Veg Puff','Flaky puff stuffed with spiced vegetables',30,TRUE,TRUE,'{IMG["bakery"]}',5),
      ('{SN4}','{R4}','Paneer Puff','Flaky puff with spicy paneer filling',40,TRUE,TRUE,'{IMG["bakery"]}',5),
      ('{SN4}','{R4}','Bread Loaf','Soft, fresh-baked bread loaf',50,TRUE,TRUE,'{IMG["bakery"]}',10),
      ('{SN4}','{R4}','Butter Bun','Soft bun with a buttery glaze',20,TRUE,TRUE,'{IMG["bakery"]}',5),
      ('{SN4}','{R4}','Egg Puff','Flaky puff with spiced boiled egg',35,TRUE,FALSE,'{IMG["bakery"]}',5),
      ('{SN4}','{R4}','Samosa (2 pcs)','Crispy samosa with potato-pea filling',40,TRUE,TRUE,'{IMG["bakery"]}',5),
      ('{SN4}','{R4}','Cookies (3 pcs)','Assorted freshly-baked cookies',50,TRUE,TRUE,'{IMG["bakery"]}',5),
      ('{DS4}','{R4}','Cream Roll','Crisp pastry filled with sweet cream',45,TRUE,TRUE,'{IMG["bakery"]}',5),
      ('{DS4}','{R4}','Black Forest Pastry','Chocolate sponge with cream & cherries',80,TRUE,TRUE,'{IMG["bakery"]}',5),
      ('{DS4}','{R4}','Chocolate Truffle Cake slice','Rich chocolate truffle cake slice',90,TRUE,TRUE,'{IMG["bakery"]}',5)""")

    # Anandam (R5 — North Indian)
    R5,MN5,BK5,BV5 = 'a0000005-0000-0000-0000-000000000001','b0000005-0001-0000-0000-000000000001','b0000005-0002-0000-0000-000000000001','b0000005-0003-0000-0000-000000000001'
    op.execute(f"""INSERT INTO menu_items (category_id,restaurant_id,name,description,price,is_available,is_vegetarian,image_url,prep_time_minutes) VALUES
      ('{MN5}','{R5}','Paneer Butter Masala with 2 Rotis','Creamy tomato-based paneer curry with rotis',130,TRUE,TRUE,'{IMG["paneer"]}',20),
      ('{MN5}','{R5}','Dal Tadka with Rice','Yellow dal tempered with ghee, served with rice',100,TRUE,TRUE,'{IMG["thali"]}',15),
      ('{MN5}','{R5}','Veg Biryani','Fragrant basmati rice with mixed vegetables',120,TRUE,TRUE,'{IMG["biryani"]}',20),
      ('{MN5}','{R5}','Chole Bhature','Spicy chickpea curry with fluffy bhature',90,TRUE,TRUE,'{IMG["paneer"]}',15),
      ('{MN5}','{R5}','Rajma Chawal','Kidney bean curry with steamed rice',100,TRUE,TRUE,'{IMG["thali"]}',15),
      ('{MN5}','{R5}','Veg Thali','Complete meal with curries, dal, roti & rice',140,TRUE,TRUE,'{IMG["thali"]}',20),
      ('{MN5}','{R5}','Matar Paneer','Cottage cheese & green peas in spiced gravy',120,TRUE,TRUE,'{IMG["paneer"]}',15),
      ('{MN5}','{R5}','Mixed Veg Curry','Seasonal vegetables in onion-tomato gravy',100,TRUE,TRUE,'{IMG["paneer"]}',15),
      ('{BK5}','{R5}','Aloo Paratha with Curd','Stuffed potato paratha with fresh curd',80,TRUE,TRUE,'{IMG["paneer"]}',12),
      ('{BV5}','{R5}','Lassi (Sweet/Salted)','Chilled yogurt drink, sweet or salted',45,TRUE,TRUE,'{IMG["juice"]}',5)""")

    # EDF Juice (R6)
    R6,BV6 = 'a0000006-0000-0000-0000-000000000001','b0000006-0001-0000-0000-000000000001'
    op.execute(f"""INSERT INTO menu_items (category_id,restaurant_id,name,description,price,is_available,is_vegetarian,image_url,prep_time_minutes) VALUES
      ('{BV6}','{R6}','Fresh Orange Juice','100% freshly-squeezed orange juice',60,TRUE,TRUE,'{IMG["juice"]}',5),
      ('{BV6}','{R6}','Watermelon Juice','Chilled watermelon juice, no sugar added',55,TRUE,TRUE,'{IMG["juice"]}',5),
      ('{BV6}','{R6}','Mango Shake','Thick mango milkshake with real mango',80,TRUE,TRUE,'{IMG["juice"]}',5),
      ('{BV6}','{R6}','Mixed Fruit Juice','Seasonal fruits blended fresh',70,TRUE,TRUE,'{IMG["juice"]}',5),
      ('{BV6}','{R6}','Sugarcane Juice','Fresh sugarcane juice with lemon & ginger',40,TRUE,TRUE,'{IMG["sugar"]}',5),
      ('{BV6}','{R6}','Tender Coconut Water','Naturally hydrating tender coconut water',50,TRUE,TRUE,'{IMG["sugar"]}',5),
      ('{BV6}','{R6}','Lemon Mint Soda','Refreshing lemon-mint sparkling soda',45,TRUE,TRUE,'{IMG["juice"]}',5),
      ('{BV6}','{R6}','Avocado Smoothie','Creamy avocado smoothie with honey',110,TRUE,TRUE,'{IMG["juice"]}',5),
      ('{BV6}','{R6}','Pineapple Juice','Fresh pineapple juice, lightly chilled',60,TRUE,TRUE,'{IMG["juice"]}',5),
      ('{BV6}','{R6}','Rose Milk','Chilled milk with rose syrup & basil seeds',50,TRUE,TRUE,'{IMG["juice"]}',5)""")

    # Cococane Juicery (R7 — same menu as EDF)
    R7,BV7 = 'a0000007-0000-0000-0000-000000000001','b0000007-0001-0000-0000-000000000001'
    op.execute(f"""INSERT INTO menu_items (category_id,restaurant_id,name,description,price,is_available,is_vegetarian,image_url,prep_time_minutes) VALUES
      ('{BV7}','{R7}','Fresh Orange Juice','100% freshly-squeezed orange juice',60,TRUE,TRUE,'{IMG["juice"]}',5),
      ('{BV7}','{R7}','Watermelon Juice','Chilled watermelon juice, no sugar added',55,TRUE,TRUE,'{IMG["juice"]}',5),
      ('{BV7}','{R7}','Mango Shake','Thick mango milkshake with real mango',80,TRUE,TRUE,'{IMG["juice"]}',5),
      ('{BV7}','{R7}','Mixed Fruit Juice','Seasonal fruits blended fresh',70,TRUE,TRUE,'{IMG["juice"]}',5),
      ('{BV7}','{R7}','Sugarcane Juice','Fresh sugarcane juice with lemon & ginger',40,TRUE,TRUE,'{IMG["sugar"]}',5),
      ('{BV7}','{R7}','Tender Coconut Water','Naturally hydrating tender coconut water',50,TRUE,TRUE,'{IMG["sugar"]}',5),
      ('{BV7}','{R7}','Lemon Mint Soda','Refreshing lemon-mint sparkling soda',45,TRUE,TRUE,'{IMG["juice"]}',5),
      ('{BV7}','{R7}','Rose Milk','Chilled milk with rose syrup & basil seeds',50,TRUE,TRUE,'{IMG["juice"]}',5),
      ('{BV7}','{R7}','Pineapple Juice','Fresh pineapple juice, lightly chilled',60,TRUE,TRUE,'{IMG["juice"]}',5),
      ('{BV7}','{R7}','Avocado Smoothie','Creamy avocado smoothie with honey',110,TRUE,TRUE,'{IMG["juice"]}',5)""")

    # Mamta Food Restaurant (R8 — North Indian, same menu as Anandam)
    R8,MN8,BK8,BV8 = 'a0000008-0000-0000-0000-000000000001','b0000008-0001-0000-0000-000000000001','b0000008-0002-0000-0000-000000000001','b0000008-0003-0000-0000-000000000001'
    op.execute(f"""INSERT INTO menu_items (category_id,restaurant_id,name,description,price,is_available,is_vegetarian,image_url,prep_time_minutes) VALUES
      ('{MN8}','{R8}','Paneer Butter Masala with 2 Rotis','Creamy tomato-based paneer curry with rotis',130,TRUE,TRUE,'{IMG["paneer"]}',20),
      ('{MN8}','{R8}','Dal Tadka with Rice','Yellow dal tempered with ghee, served with rice',100,TRUE,TRUE,'{IMG["thali"]}',15),
      ('{MN8}','{R8}','Veg Biryani','Fragrant basmati rice with mixed vegetables',120,TRUE,TRUE,'{IMG["biryani"]}',20),
      ('{MN8}','{R8}','Chole Bhature','Spicy chickpea curry with fluffy bhature',90,TRUE,TRUE,'{IMG["paneer"]}',15),
      ('{MN8}','{R8}','Rajma Chawal','Kidney bean curry with steamed rice',100,TRUE,TRUE,'{IMG["thali"]}',15),
      ('{MN8}','{R8}','Veg Thali','Complete meal with curries, dal, roti & rice',140,TRUE,TRUE,'{IMG["thali"]}',20),
      ('{MN8}','{R8}','Matar Paneer','Cottage cheese & green peas in spiced gravy',120,TRUE,TRUE,'{IMG["paneer"]}',15),
      ('{MN8}','{R8}','Mixed Veg Curry','Seasonal vegetables in onion-tomato gravy',100,TRUE,TRUE,'{IMG["paneer"]}',15),
      ('{BK8}','{R8}','Aloo Paratha with Curd','Stuffed potato paratha with fresh curd',80,TRUE,TRUE,'{IMG["paneer"]}',12),
      ('{BV8}','{R8}','Lassi (Sweet/Salted)','Chilled yogurt drink, sweet or salted',45,TRUE,TRUE,'{IMG["juice"]}',5)""")


def downgrade() -> None:
    op.execute("DELETE FROM menu_items")
    op.execute("DELETE FROM menu_categories")
    op.execute("DELETE FROM restaurants")
