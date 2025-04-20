def calculate_menu_price(menu_items, guests, gastronomic_type, time_of_day):
    # Base cost
    fixed_cost = 88 if gastronomic_type.lower() == 'alquimia' else 80
    base_price = sum(item['Precio Venta'] for item in menu_items)
    price_per_guest = base_price + fixed_cost

    # Extra charges specific to Chas
    pinchos_count = sum(1 for i in menu_items if 'pinchos' in i['Tipo'].lower())
    has_meat = any('carne' in i['Tipo'].lower() for i in menu_items)

    if gastronomic_type.lower() == 'chas':
        if pinchos_count == 15 and has_meat:
            price_per_guest += 10
        elif pinchos_count == 20:
            price_per_guest += 5

    # Night surcharge
    night_surcharge = 3 if time_of_day.lower() == 'noche' else 0
    price_per_guest += night_surcharge

    # Calculate total price
    total_price = price_per_guest * guests

    guest_surcharge_applied = guests < 80
    if guest_surcharge_applied:
        total_price += 1500

    # Apply IVA (10%)
    iva_rate = 0.10
    total_price *= (1 + iva_rate)

    # Estimate balance percentage (optional)
    estimated_balance_percentage = (base_price / 80) * 100  # example assumption
    balance_valid = 100 <= estimated_balance_percentage <= 117

    return {
        "price_per_guest": round(price_per_guest, 2),
        "total_price": round(total_price, 2),
        "iva_applied": True,
        "night_surcharge_applied": night_surcharge > 0,
        "guest_surcharge_applied": guest_surcharge_applied,
        "pinchos_count": pinchos_count,
        "menu_balance_percentage": round(estimated_balance_percentage, 2),
        "menu_balance_valid": balance_valid
    }



'''def calculate_menu_price(menu_items, guests, gastronomic_type, time_of_day):
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

    return round(price_per_guest, 2), round(total_price, 2)'''
