def calculate_cvp(fixed_costs, variable_cost_per_unit, selling_price_per_unit, sales_volume):
    contribution_margin = selling_price_per_unit - variable_cost_per_unit
    contribution_margin_ratio = contribution_margin / selling_price_per_unit
    break_even_units = fixed_costs / contribution_margin
    break_even_sales = break_even_units * selling_price_per_unit
   
    # Operating Leverage Calculation
    total_contribution_margin = contribution_margin * sales_volume
    operating_income = total_contribution_margin - fixed_costs
    operating_leverage = total_contribution_margin / operating_income if operating_income != 0 else float('inf')

    # Margin of Safety Calculation
    actual_sales = sales_volume * selling_price_per_unit
    margin_of_safety = ((actual_sales - break_even_sales) / actual_sales) * 100 if actual_sales > 0 else 0

    return {
        'contribution_margin': contribution_margin,
        'contribution_margin_ratio': contribution_margin_ratio,
        'break_even_units': break_even_units,
        'margin_of_safety': margin_of_safety,
        'operating_leverage': operating_leverage,
        'total_contribution_margin': total_contribution_margin,
        'operating_income': operating_income
    }

def calculate_target_profit(fixed_costs, variable_cost, selling_price, target_profit):
    contribution_margin = selling_price - variable_cost
    target_units = (fixed_costs + target_profit) / contribution_margin
    
    return {
        "target_units": target_units
    }

def calculate_target_profit_sales_mix(products, fixed_costs, target_profit):
    total_contribution_margin = sum((p['sell_price'] - p['var_cost']) * (p['mix_percentage'] / 100) for p in products)
    target_units = (fixed_costs + target_profit) / total_contribution_margin if total_contribution_margin > 0 else None
    target_profit_sales_volume = {
        p['product_name']: target_units * (p['mix_percentage'] / 100) if target_units is not None else None for p in products
    }
    return {
        "total_contribution_margin": total_contribution_margin,
        "target_units": target_units,
        "target_profit_sales_volume": target_profit_sales_volume
    }

def calculate_sales_mix(products, fixed_costs, target_profit=None):
    # Calculate the weighted average contribution margin and selling price per unit
    total_sales_volume = sum(p['sales_volume'] for p in products)
    weighted_contribution_margin = sum(
        (p['sell_price'] - p['var_cost']) * (p['mix_percentage'] / 100) for p in products
    )
    weighted_selling_price = sum(
        p['sell_price'] * (p['mix_percentage'] / 100) for p in products
    )

    # Error handling for zero contribution margin
    if weighted_contribution_margin == 0:
        return {"error": "Contribution margin is zero. Check product pricing and costs."}

    # Calculate break-even and target units
    break_even_units = fixed_costs / weighted_contribution_margin
    target_units = None
    if target_profit is not None:
        target_units = (fixed_costs + target_profit) / weighted_contribution_margin

    # Calculate break-even sales and target sales in dollars
    break_even_sales = break_even_units * weighted_selling_price
    target_sales = target_units * weighted_selling_price if target_units is not None else None

    return {
        "weighted_contribution_margin": weighted_contribution_margin,
        "break_even_units": break_even_units,
        "target_units": target_units,
        "break_even_sales": break_even_sales,
        "target_sales": target_sales
    }
