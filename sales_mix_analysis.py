import streamlit as st
from backend.cvp_calculations import calculate_sales_mix
import plotly.graph_objects as go

def run():
    # Title and Description for Sales Mix Analysis
    st.markdown("<h1 style='text-align: left; color: #4CAF50;'>Sales Mix Analysis</h1>", unsafe_allow_html=True)
    st.write(
        """
        <div style='text-align: left;'>
        Analyze your product mix to determine the optimal sales mix for profitability.
        Enter the cost and pricing parameters for each product to calculate break-even points and 
        perform sensitivity analysis.
        </div>
        """, 
        unsafe_allow_html=True
    )
   
    # Input Fields for Sales Mix Analysis
    fxd_costs = st.sidebar.number_input("Fixed Costs ($)", min_value=0.0, value=2000.0, step=100.0)
    tgt_profit = st.sidebar.number_input("Desired Profit ($) for Sales Mix", min_value=0.0, value=3000.0, step=100.0)
    num_products = st.sidebar.number_input("Number of Products", min_value=1, max_value=10, value=2, step=1)

    products = []
    total_sales_volume = 0

    for i in range(num_products):
        st.sidebar.markdown(f"**Product {i + 1}**")
        sell_price = st.sidebar.number_input(f"Product {i + 1} Selling Price ($)", min_value=0.0, value=50.0, step=5.0)
        var_cost = st.sidebar.number_input(f"Product {i + 1} Variable Cost per Unit ($)", min_value=0.0, value=25.0, step=5.0)
        sales_volume = st.sidebar.number_input(f"Product {i + 1} Expected Sales Volume", min_value=0, value=300, step=50)

        products.append({
            "product_name": f"Product {i + 1}",
            "sell_price": sell_price,
            "var_cost": var_cost,
            "sales_volume": sales_volume
        })
        
        total_sales_volume += sales_volume

    # Calculate Sales Mix Percentages Automatically
    for product in products:
        product['mix_percentage'] = (product['sales_volume'] / total_sales_volume) * 100 if total_sales_volume > 0 else 0

    # Calculate Sales Mix Results including Target Profit Analysis
    sales_mix_results = calculate_sales_mix(products, fxd_costs, target_profit=tgt_profit)

    # Check for errors in Sales Mix Results
    if "error" in sales_mix_results:
        st.error(sales_mix_results["error"])
    else:
        # Display Sales Mix Results if no error is found
        st.markdown("<h2 style='text-align: left; color: #4CAF50;'>Sales Mix Results</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        col1.metric("Weighted Average Contribution Margin", f"${sales_mix_results['weighted_contribution_margin']:.2f}")
        col2.metric("Break-Even Point (Units)", f"{sales_mix_results['break_even_units']:.2f} units")

        # Display Target Profit Analysis
        if sales_mix_results['target_units'] is not None:
            st.metric("Units Required to Achieve Desired Profit", f"{sales_mix_results['target_units']:.2f} units")

        # Pie Chart for Sales Mix Distribution
        st.markdown("<h2 style='text-align: left; color: #4CAF50;'>Sales Mix Distribution</h2>", unsafe_allow_html=True)
        product_labels = [product['product_name'] for product in products]
        product_mix_percentages = [product['mix_percentage'] for product in products]

        # Plot the pie chart
        fig = go.Figure(data=[go.Pie(labels=product_labels, values=product_mix_percentages, hole=.3)])
        fig.update_layout(
            margin=dict(l=40, r=40, t=40, b=40),
            showlegend=True
        )
        st.plotly_chart(fig, use_container_width=True)

        # Break-Even Graph for Sales Mix Analysis
        st.markdown("<h2 style='text-align: left; color: #4CAF50;'>Sales Mix Break-Even Analysis</h2>", unsafe_allow_html=True)

        # Calculate combined revenue, total cost, and break-even point over a range of sales volumes
        sales_volume_range = list(range(0, total_sales_volume))
        total_cost = [fxd_costs + sum(p['var_cost'] * (v * p['mix_percentage'] / 100) for p in products) for v in sales_volume_range]
        total_revenue = [sum(p['sell_price'] * (v * p['mix_percentage'] / 100) for p in products) for v in sales_volume_range]

        fig_be = go.Figure()

        # Adding Fixed Cost Line
        fig_be.add_trace(go.Scatter(
            x=sales_volume_range,
            y=[fxd_costs] * len(sales_volume_range),
            mode='lines',
            name='Fixed Costs',
            line=dict(color='blue', width=2, dash='dash')
        ))

        # Adding Total Cost Line
        fig_be.add_trace(go.Scatter(
            x=sales_volume_range,
            y=total_cost,
            mode='lines',
            name='Total Cost',
            line=dict(color='red', width=2)
        ))

        # Adding Total Revenue Line
        fig_be.add_trace(go.Scatter(
            x=sales_volume_range,
            y=total_revenue,
            mode='lines',
            name='Total Revenue',
            line=dict(color='green', width=2)
        ))

        # Adding Break-Even Line
        fig_be.add_trace(go.Scatter(
            x=[sales_mix_results['break_even_units'], sales_mix_results['break_even_units']],
            y=[0, sales_mix_results['break_even_sales']],
            mode='lines',
            name='Break-Even',
            line=dict(color='white', width=2, dash='dash'),
            showlegend=False
        ))

        # Adding Annotation for Break-Even Point
        fig_be.add_annotation(
            x=sales_mix_results['break_even_units'],
            y=sales_mix_results['break_even_sales'],
            text="Break-Even",
            showarrow=True,
            arrowhead=7,
            ax=0,
            ay=-40,
            arrowcolor="white"
        )

        # Adding Target Profit Line for Sales Mix
        if sales_mix_results['target_units'] is not None:
            fig_be.add_trace(go.Scatter(
                x=[sales_mix_results['target_units'], sales_mix_results['target_units']],
                y=[0, sales_mix_results['target_sales']],
                mode='lines',
                name='Target Profit (sales mix)',
                line=dict(color='yellow', width=2, dash='dash'),
                showlegend=False
            ))

            # Adding Annotation for Target Profit
            fig_be.add_annotation(
                x=sales_mix_results['target_units'],
                y=sales_mix_results['target_sales'],
                text="Target Profit",
                showarrow=True,
                arrowhead=7,
                ax=0,
                ay=-40,
                arrowcolor="yellow"
            )

        # Formatting the Break-Even Graph
        fig_be.update_layout(
            xaxis_title='Sales Volume (Units)',
            yaxis_title='Dollars ($)',
            margin=dict(l=40, r=40, t=60, b=40),
            showlegend=True
        )

        # Display the Break-Even Chart
        st.plotly_chart(fig_be, use_container_width=True)
