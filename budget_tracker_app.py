import streamlit as st
import pandas as pd

if 'transactions' not in st.session_state:
    st.session_state.transactions = pd.DataFrame(columns=["category", "amount", "description"])

def display_menu():
    st.title("Personal Budget Tracker")
    
    menu = ["View all transactions", "Add a new transaction", "Edit an existing transaction", "Delete a transaction", "View the total balance", "Exit"]
    choice = st.sidebar.selectbox("Menu", menu)
    return choice

def view_transactions():
    if st.session_state.transactions.empty:
        st.write("No transactions to display.")
    else:
        st.write(st.session_state.transactions)

def add_transaction():
    with st.form(key='add_transaction'):
        category = st.text_input("Transaction category")
        amount = st.number_input("Transaction amount", step=0.01)
        description = st.text_input("Transaction description")
        submit_button = st.form_submit_button(label='Add Transaction')
        
        if submit_button:
            new_transaction = pd.DataFrame({"category": [category], "amount": [amount], "description": [description]})
            st.session_state.transactions = pd.concat([st.session_state.transactions, new_transaction], ignore_index=True)
            st.success("Transaction added successfully.")

def edit_transaction():
    if st.session_state.transactions.empty:
        st.write("No transactions to edit.")
    else:
        index = st.number_input("Enter the transaction number to edit", min_value=1, max_value=len(st.session_state.transactions), step=1) - 1
        if st.button("Load Transaction"):
            transaction = st.session_state.transactions.iloc[index]
            with st.form(key='edit_transaction'):
                category = st.text_input("Transaction category", value=transaction['category'])
                amount = st.number_input("Transaction amount", value=transaction['amount'], step=0.01)
                description = st.text_input("Transaction description", value=transaction['description'])
                submit_button = st.form_submit_button(label='Update Transaction')

                if submit_button:
                    st.session_state.transactions.at[index, 'category'] = category
                    st.session_state.transactions.at[index, 'amount'] = amount
                    st.session_state.transactions.at[index, 'description'] = description
                    st.success("Transaction updated successfully.")

def delete_transaction():
    if st.session_state.transactions.empty:
        st.write("No transactions to delete.")
    else:
        index = st.number_input("Enter the transaction number to delete", min_value=1, max_value=len(st.session_state.transactions), step=1) - 1
        if st.button("Delete Transaction"):
            st.session_state.transactions = st.session_state.transactions.drop(st.session_state.transactions.index[index]).reset_index(drop=True)
            st.success("Transaction deleted successfully.")

def view_balance():
    balance = st.session_state.transactions['amount'].sum()
    st.write(f"Total balance: ₹{balance:.2f}")

def main():
    choice = display_menu()
    
    if choice == "View all transactions":
        view_transactions()
    elif choice == "Add a new transaction":
        add_transaction()
    elif choice == "Edit an existing transaction":
        edit_transaction()
    elif choice == "Delete a transaction":
        delete_transaction()
    elif choice == "View the total balance":
        view_balance()
    elif choice == "Exit":
        st.write("Exiting the budget tracker. Goodbye!")

if __name__ == "__main__":
    main()
