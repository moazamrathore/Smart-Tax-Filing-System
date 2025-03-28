import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os

def calculate_tax(amount):
    return amount * 0.15

def calculate_property_tax(property_value):
    return property_value * 0.01

def calculate_car_tax(car_value):
    return car_value * 0.05

def plot_bar_chart(tax_details):
    fig, ax = plt.subplots(figsize=(6, 4)) 
    tax_types = list(tax_details.keys())
    tax_values = list(tax_details.values())
    bars = ax.bar(tax_types, tax_values, color=["skyblue", "orange", "green", "red"])
    
    ax.set_title("Tax Breakdown by Type", fontsize=12)
    ax.set_ylabel("Tax Amount (PKR)", fontsize=10)
    ax.set_xlabel("Tax Type", fontsize=10)

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height, f"PKR", ha="center", va="bottom", fontsize=8)
    
    st.pyplot(fig)

def plot_pie_chart(tax_details):
    fig, ax = plt.subplots(figsize=(6, 4))
    tax_types = list(tax_details.keys())
    tax_values = list(tax_details.values())
    ax.pie(tax_values, labels=tax_types, autopct="%1.1f%%", startangle=140, colors=["lightcoral", "lightskyblue", "yellowgreen", "gold"])
    ax.set_title("Total Tax Breakdown", fontsize=12)
    st.pyplot(fig)

def save_user_data(user_data):
    file_path = "user_data.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        new_entry = pd.DataFrame([user_data])
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv(file_path, index=False)
    else:
        df = pd.DataFrame([user_data])
        df.to_csv(file_path, index=False)

def main():
    st.set_page_config(page_title="Pakistan Tax Calculator", layout="centered")
    st.image("D:\MOAZAM\MOAZAM FAST UNIVERSITY\Sixth semester\Programming for finance\Assignment 2/latestincometaxcalculatorupdated.jpg", width=800)
    st.title("📊 Pakistan Tax Calculator")
    st.markdown("Welcome to the **Tax Filing App**! Enter your details below to calculate your tax liability.")
    st.header("👤 Personal Details")
    name = st.text_input("Full Name:")
    address = st.text_input("Address:")
    cnic = st.text_input("CNIC (without dashes):", max_chars=13)
    
    if cnic and len(cnic) != 13:
        st.error("CNIC must be 13 digits long.")
        return

    st.header("📋 User Category")
    user_category = st.selectbox("Select your category:", ["Salaried", "Corporate", "Business", "Other"])
    st.header("💰 Income Details")
    salary = st.number_input("Annual Salary (PKR):", min_value=0.0, step=1000.0)
    business_income = st.number_input("Business Income (PKR):", min_value=0.0, step=1000.0)

    st.header("🏠 Asset Details")
    st.subheader("Property")
    owns_property = st.checkbox("Do you own a property?")
    property_location = None
    property_value = 0
    if owns_property:
        property_location = st.text_input("Property Location:")
        property_value = st.number_input("Property Value (PKR):", min_value=0.0, step=1000.0)

    st.subheader("Car")
    owns_car = st.checkbox("Do you own a car?")
    car_name, car_model, car_plate, car_value = None, None, None, 0
    if owns_car:
        car_name = st.text_input("Car Name:")
        car_model = st.text_input("Car Model:")
        car_plate = st.text_input("Car Plate Number:")
        car_value = st.number_input("Car Value (PKR):", min_value=0.0, step=1000.0)

    if st.button("Generate Tax Report"):
        st.header("📄 Tax Report")
        
        salary_tax = calculate_tax(salary)
        business_tax = calculate_tax(business_income)
        property_tax = calculate_property_tax(property_value) if owns_property else 0
        car_tax = calculate_car_tax(car_value) if owns_car else 0
        total_tax = salary_tax + business_tax + property_tax + car_tax

        st.subheader("👤 User Details")
        user_details = {
            "Name": name,
            "Address": address,
            "CNIC": cnic,
            "Category": user_category,
            "Annual Salary (PKR)": salary,
            "Business Income (PKR)": business_income,
            "Car Name": car_name if owns_car else "N/A",
            "Car Model": car_model if owns_car else "N/A",
            "Car Plate Number": car_plate if owns_car else "N/A",
            "Car Value (PKR)": car_value if owns_car else 0,
            "Property Location": property_location if owns_property else "N/A",
            "Property Value (PKR)": property_value if owns_property else 0
        }
        for key, value in user_details.items():
            st.write(f"**{key}:** {value}")

        st.subheader("💵 Tax Breakdown")
        report_data = {
            "Detail": ["Annual Salary Tax", "Business Income Tax", "Property Tax", "Car Tax", "Total Tax"],
            "Amount (PKR)": [salary_tax, business_tax, property_tax, car_tax, total_tax]
        }
        report_df = pd.DataFrame(report_data)
        st.table(report_df)

        total_tax = salary_tax + business_tax + property_tax + car_tax
        st.subheader("💵 Total Tax Liability")
        st.success(f"Total Tax to Pay: PKR {total_tax:,.2f}")

        tax_details = {
            "Salary Tax": salary_tax,
            "Business Tax": business_tax,
            "Property Tax": property_tax,
            "Car Tax": car_tax
        }
        st.subheader("📊 Tax Breakdown Visualization")
        
        st.markdown("Bar Chart")
        plot_bar_chart(tax_details)

        st.markdown("Pie Chart")
        plot_pie_chart(tax_details)

        user_data = {
            "CNIC": cnic,
            "Name": name,
            "Address": address,
            "Category": user_category,
            "Salary": salary,
            "Business Income": business_income,
            "Property Value": property_value if owns_property else 0,
            "Car Value": car_value if owns_car else 0,
            "Total Tax": total_tax
        }
        save_user_data(user_data)

        st.download_button(
            label="Download Tax Report as CSV",
            data=report_df.to_csv(index=False),
            file_name="tax_report.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
