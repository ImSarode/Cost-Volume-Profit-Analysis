import streamlit as st
from backend.cvp_calculations import calculate_cvp, calculate_target_profit
import plotly.graph_objects as go

def run():
    # Title and Description for CVP Analysis
    st.markdown("<h1 style='text-align: left; color: #4CAF50;'>Cost-Volume-Profit (CVP) Analysis</h1>", 
                unsafe_allow_html=True)
    st.write(
        """
        <div style='text-align: left;'>
        This tool helps you analyze your business's cost structure and profit potential. 
        Enter your cost and pricing parameters to calculate break-even points, contribution margins, 
        and perform sensitivity analysis.
        </div>
        """, 
        unsafe_allow_html=True)

    # Sidebar for input fields with icons for a better visual appeal
    st.sidebar.header("Enter Parameters 🛠️")
    fxd_costs = st.sidebar.number_input("Fixed Costs ($)", min_value=0.0, value=2000.0, step=100.0)
    var_costs = st.sidebar.number_input("Variable Cost per Unit ($)", min_value=0.0, value=25.0, step=10.0)
    sell_price = st.sidebar.number_input("Selling Price per Unit ($)", min_value=0.0, value=50.0, step=10.0)
    sales_volume = st.sidebar.number_input("Sales Volume (units)", min_value=0, value=300, step=50)

    # Input validation
    if sell_price <= var_costs:
        st.sidebar.error("Selling price must be greater than variable cost per unit.")
    else:
        # Perform calculations
        results = calculate_cvp(fxd_costs, var_costs, sell_price, sales_volume)
        if "error" in results:
            st.error(results["error"])
        else:
            # Display Basic CVP Analysis
            st.markdown("<h2 style='text-align: left; color: #4CAF50;'>Basic CVP Analysis</h2>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            col3, col4 = st.columns(2)
            col1.metric("Contribution Margin per Unit", f"${results['contribution_margin']:.2f}")
            col2.metric("Contribution Margin Ratio", f"{results['contribution_margin_ratio']:.2%}")
            col3.metric("Break-Even Point (Units)", f"{results['break_even_units']:.2f} units")
            col4.metric("Margin of Safety", f"{results['margin_of_safety']:.2f}%")

            # Display Operating Leverage
            st.markdown("<h2 style='text-align: left; color: #4CAF50;'>Operating Leverage</h2>", unsafe_allow_html=True)
            col5, col6 = st.columns(2)
            col5.metric("Operating Leverage", f"{results['operating_leverage']:.2f}")
            col6.metric("Operating Profit", f"${results['operating_income']:.2f}")

            # Target Profit Analysis
            tgt_profit = st.sidebar.number_input("Desired Profit ($)", min_value=0.0, value=3000.0, step=100.0)
            target_results = calculate_target_profit(fxd_costs, var_costs, sell_price, tgt_profit)
            st.markdown("<h2 style='text-align: left; color: #4CAF50;'>Target Profit Analysis</h2>", 
                        unsafe_allow_html=True)
            st.metric("Units Required to Achieve Desired Profit", f"{target_results['target_units']} units")

            # Enhanced Visualizations using Plotly
            st.markdown("<h2 style='text-align: left; color: #4CAF50;'>Break-Even Analysis Chart</h2>", 
                        unsafe_allow_html=True)
            fig = go.Figure()

            # Adding Fixed Cost Line
            fig.add_trace(go.Scatter(
                x=[0, sales_volume],
                y=[fxd_costs, fxd_costs],
                mode='lines',
                name='Fixed Costs',
                line=dict(color='blue', width=2, dash='dash')
            ))

            # Adding Total Cost Line
            fig.add_trace(go.Scatter(
                x=[0, sales_volume],
                y=[fxd_costs, fxd_costs + (var_costs * sales_volume)],
                mode='lines',
                name='Total Cost',
                line=dict(color='red', width=2)
            ))

            # Adding Total Revenue Line
            fig.add_trace(go.Scatter(
                x=[0, sales_volume],
                y=[0, sell_price * sales_volume],
                mode='lines',
                name='Total Revenue',
                line=dict(color='green', width=2)
            ))

            # Adding Vertical Line for Break-Even Point
            break_even_sales = results['break_even_units'] * sell_price
            fig.add_trace(go.Scatter(
                x=[results['break_even_units'], results['break_even_units']],
                y=[0, break_even_sales],
                mode='lines',
                name='Break-Even',
                line=dict(color='white', width=2, dash='dot'),
                showlegend=False
            ))

            # Adding Vertical Line for Target Profit
            target_revenue = tgt_profit + fxd_costs + (var_costs * target_results['target_units'])
            fig.add_trace(go.Scatter(
                x=[target_results['target_units'], target_results['target_units']],
                y=[0, target_revenue],
                mode='lines',
                name='Target Profit',
                line=dict(color='yellow', width=2, dash='dot'),
                showlegend=False
            ))

            # Break-Even and Target Profit annotations
            fig.add_annotation(
                x=results['break_even_units'],
                y=break_even_sales,
                text="Break-Even",
                showarrow=True,
                arrowhead=7,
                ax=0,
                ay=-40,
                arrowcolor="white"
            )
            fig.add_annotation(
                x=target_results['target_units'],
                y=target_revenue,
                text="Target Profit",
                showarrow=True,
                arrowhead=7,
                ax=0,
                ay=-40,
                arrowcolor="yellow"
            )

            # Format and Display the Plot
            fig.update_layout(
                xaxis_title='Sales Volume (Units)',
                yaxis_title='Dollars ($)',
                legend=dict(x=0, y=1),
                margin=dict(l=40, r=40, t=60, b=40),
                showlegend=True
            )
            st.plotly_chart(fig, use_container_width=True)

