import streamlit as st
import pandas as pd

# Function to display the main menu
def display_menu():
    st.title("Personal Budget Tracker")
    
    menu = ["View all transactions", "Add a new transaction", "Edit an existing transaction", "Delete a transaction", "View the total balance", "Exit"]
    choice = st.sidebar.selectbox("Menu", menu)
    return choice

# Function to view all transactions
def view_transactions(transactions):
    if transactions.empty:
        st.write("No transactions to display.")
    else:
        st.write(transactions)

# Function to add a new transaction
def add_transaction(transactions):
    with st.form(key='add_transaction'):
        category = st.text_input("Transaction category")
        amount = st.number_input("Transaction amount", step=0.01)
        description = st.text_input("Transaction description")
        submit_button = st.form_submit_button(label='Add Transaction')
        
        if submit_button:
            new_transaction = pd.DataFrame({"category": [category], "amount": [amount], "description": [description]})
            transactions = pd.concat([transactions, new_transaction], ignore_index=True)
            st.success("Transaction added successfully.")
    return transactions

# Function to edit an existing transaction
def edit_transaction(transactions):
    if transactions.empty:
        st.write("No transactions to edit.")
    else:
        index = st.number_input("Enter the transaction number to edit", min_value=1, max_value=len(transactions), step=1) - 1
        if st.button("Load Transaction"):
            transaction = transactions.iloc[index]
            category = st.text_input("Transaction category", value=transaction['category'])
            amount = st.number_input("Transaction amount", value=transaction['amount'], step=0.01)
            description = st.text_input("Transaction description", value=transaction['description'])

            if st.button("Update Transaction"):
                transactions.at[index, 'category'] = category
                transactions.at[index, 'amount'] = amount
                transactions.at[index, 'description'] = description
                st.success("Transaction updated successfully.")
    return transactions

# Function to delete a transaction
def delete_transaction(transactions):
    if transactions.empty:
        st.write("No transactions to delete.")
    else:
        index = st.number_input("Enter the transaction number to delete", min_value=1, max_value=len(transactions), step=1) - 1
        if st.button("Delete Transaction"):
            transactions = transactions.drop(transactions.index[index]).reset_index(drop=True)
            st.success("Transaction deleted successfully.")
    return transactions

# Function to view the total balance
def view_balance(transactions):
    balance = transactions['amount'].sum()
    st.write(f"Total balance: ₹{balance:.2f}")

# Main function to run the budget tracker
def main():
    st.sidebar.title("Menu")
    transactions = pd.DataFrame(columns=["category", "amount", "description"])
    choice = display_menu()
    
    if choice == "View all transactions":
        view_transactions(transactions)
    elif choice == "Add a new transaction":
        transactions = add_transaction(transactions)
    elif choice == "Edit an existing transaction":
        transactions = edit_transaction(transactions)
    elif choice == "Delete a transaction":
        transactions = delete_transaction(transactions)
    elif choice == "View the total balance":
        view_balance(transactions)
    elif choice == "Exit":
        st.write("Exiting the budget tracker. Goodbye!")

if __name__ == "__main__":
    main()
