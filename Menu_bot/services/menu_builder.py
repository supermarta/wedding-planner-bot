def calculate_menu_price(menu_items, guests, gastronomic_type, time_of_day):
    fixed_cost = 88 if gastronomic_type.lower() == 'alquimia' else 80
    price_per_guest = sum(item['Precio Venta'] for item in menu_items) + fixed_cost

    # Chas-specific pricing rules
    if gastronomic_type.lower() == 'chas':
        pinchos_count = sum(1 for i in menu_items if 'pinchos' in i['Tipo'].lower())
        if pinchos_count == 15 and any('carne' in i['Tipo'].lower() for i in menu_items):
            price_per_guest += 10
        if pinchos_count == 20:
            price_per_guest += 5

    if time_of_day == 'noche':
        price_per_guest += 3

    total_price = price_per_guest * guests

    if guests < 80:
        total_price += 1500  # Flat surcharge

    return round(price_per_guest, 2), round(total_price, 2)
