import datetime
import random

class BankAccount:
    def __init__(self, name, pin, initial_deposit):
        self.name = name
        self.pin = pin
        self.balance = float(initial_deposit)
        self.account_number = random.randint(10000000, 99999999)
        self.history = [f"Account opened with initial deposit: ${initial_deposit:.2f} at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"]
        self.loan_amount = 0.0
        self.failed_login_attempts = 0
        self.is_locked = False

    def get_masked_pin(self):
        return "****"

class BankingSystem:
    def __init__(self):
        self.accounts = {} # Key: account_number, Value: BankAccount object
        self.current_user = None
        self.admin_passcode = "admin123"

    def display_banner(self):
        print("\n" + "="*60)
        print("               PY-BANK ENTERPRISE SYSTEM")
        print("="*60)

    # --- OPERATION 1: Create Account ---
    def create_account(self):
        print("\n--- [1] Create New Account ---")
        name = input("Enter your full name: ").strip()
        if not name:
            print("[ERROR] Name cannot be empty.")
            return
        
        while True:
            pin = input("Set a 4-digit PIN: ").strip()
            if pin.isdigit() and len(pin) == 4:
                break
            print("[ERROR] Invalid PIN. Must be exactly 4 digits.")

        try:
            deposit = float(input("Enter initial deposit amount ($): "))
            if deposit < 0:
                print("[ERROR] Deposit cannot be negative.")
                return
        except ValueError:
            print("[ERROR] Please enter a valid number.")
            return

        new_acc = BankAccount(name, pin, deposit)
        self.accounts[new_acc.account_number] = new_acc
        print("\n[SUCCESS] Account successfully created!")
        print(f"-> Your Account Number is: {new_acc.account_number}")
        print(f"-> Initial Balance: ${new_acc.balance:.2f}")

    # --- OPERATION 2: Login ---
    def login(self):
        print("\n--- [2] Account Login ---")
        try:
            acc_num = int(input("Enter your 8-digit Account Number: "))
        except ValueError:
            print("[ERROR] Invalid format.")
            return False

        if acc_num not in self.accounts:
            print("[ERROR] Account not found.")
            return False

        account = self.accounts[acc_num]

        if account.is_locked:
            print("[CRITICAL] This account is locked due to multiple failed login attempts. Contact support.")
            return False

        pin = input("Enter your 4-digit PIN: ").strip()
        if account.pin == pin:
            account.failed_login_attempts = 0 # Reset on successful login
            self.current_user = account
            print(f"\n[WELCOME] Logged in successfully. Hello, {self.current_user.name}!")
            return True
        else:
            account.failed_login_attempts += 1
            remaining = 3 - account.failed_login_attempts
            print(f"[ERROR] Incorrect PIN. Attempts remaining: {remaining}")
            if account.failed_login_attempts >= 3:
                account.is_locked = True
                print("[CRITICAL] Maximum login attempts reached. Account has been locked.")
            return False

    # --- OPERATION 3: Deposit Money ---
    def deposit(self):
        print("\n--- [3] Deposit Funds ---")
        try:
            amount = float(input("Enter amount to deposit ($): "))
            if amount <= 0:
                print("[ERROR] Amount must be greater than zero.")
                return
            self.current_user.balance += amount
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            self.current_user.history.append(f"Deposited: +${amount:.2f} at {timestamp}")
            print(f"[SUCCESS] Successfully deposited ${amount:.2f}. New Balance: ${self.current_user.balance:.2f}")
        except ValueError:
            print("[ERROR] Invalid input. Enter a valid number.")

    # --- OPERATION 4: Withdraw Money ---
    def withdraw(self):
        print("\n--- [4] Withdraw Funds ---")
        try:
            amount = float(input("Enter amount to withdraw ($): "))
            if amount <= 0:
                print("[ERROR] Amount must be greater than zero.")
                return
            if amount > self.current_user.balance:
                print("[ERROR] Insufficient funds.")
                return
            self.current_user.balance -= amount
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            self.current_user.history.append(f"Withdrew: -${amount:.2f} at {timestamp}")
            print(f"[SUCCESS] Successfully withdrew ${amount:.2f}. Remaining Balance: ${self.current_user.balance:.2f}")
        except ValueError:
            print("[ERROR] Invalid input. Enter a valid number.")

    # --- OPERATION 5: Check Balance ---
    def check_balance(self):
        print("\n--- [5] Check Balance ---")
        print(f"-> Current Account Balance: ${self.current_user.balance:.2f}")

    # --- OPERATION 6: Transfer Funds ---
    def transfer(self):
        print("\n--- [6] Fund Transfer ---")
        try:
            target_acc = int(input("Enter recipient's 8-digit Account Number: "))
        except ValueError:
            print("[ERROR] Invalid account number format.")
            return

        if target_acc not in self.accounts:
            print("[ERROR] Recipient account does not exist.")
            return
        
        if target_acc == self.current_user.account_number:
            print("[ERROR] You cannot transfer funds to your own account.")
            return

        try:
            amount = float(input("Enter amount to transfer ($): "))
            if amount <= 0:
                print("[ERROR] Amount must be greater than zero.")
                return
            if amount > self.current_user.balance:
                print("[ERROR] Insufficient funds for transfer.")
                return

            self.current_user.balance -= amount
            self.accounts[target_acc].balance += amount

            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            self.current_user.history.append(f"Transferred -${amount:.2f} to Account #{target_acc} at {timestamp}")
            self.accounts[target_acc].history.append(f"Received +${amount:.2f} from Account #{self.current_user.account_number} at {timestamp}")

            print(f"[SUCCESS] Successfully transferred ${amount:.2f} to Account #{target_acc}.")
            print(f"-> Your New Balance: ${self.current_user.balance:.2f}")
        except ValueError:
            print("[ERROR] Invalid amount entered.")

    # --- OPERATION 7: Transaction History ---
    def transaction_history(self):
        print("\n--- [7] Transaction History ---")
        print(f"Statement for Account #{self.current_user.account_number}:")
        print("-" * 50)
        for record in self.current_user.history:
            print(f" * {record}")
        print("-" * 50)

    # --- OPERATION 8: Apply for a Loan ---
    def apply_loan(self):
        print("\n--- [8] Apply for Loan ---")
        try:
            amount = float(input("Enter loan amount requested ($): "))
            if amount <= 0:
                print("[ERROR] Invalid loan amount.")
                return
            if self.current_user.loan_amount > 0:
                print("[WARNING] You already have an active loan. Please clear it first.")
                return
            
            if self.current_user.balance >= (amount * 0.2):
                self.current_user.loan_amount = amount
                self.current_user.balance += amount
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
                self.current_user.history.append(f"Loan Approved & Credited: +${amount:.2f} at {timestamp}")
                print(f"[SUCCESS] Loan of ${amount:.2f} approved and added to your balance.")
            else:
                print("[DENIED] Loan application denied. Minimum balance requirement (20% of loan) not met.")
        except ValueError:
            print("[ERROR] Please enter a valid number.")

    # --- OPERATION 9: Pay Bills ---
    def pay_bill(self):
        print("\n--- [9] Pay Utility Bills ---")
        print("1. Electricity Bill")
        print("2. Internet Bill")
        print("3. Water Bill")
        choice = input("Select bill type (1-3): ").strip()
        
        bill_types = {"1": "Electricity", "2": "Internet", "3": "Water"}
        if choice not in bill_types:
            print("[ERROR] Invalid bill category selection.")
            return

        try:
            amount = float(input(f"Enter {bill_types[choice]} bill amount ($): "))
            if amount <= 0:
                print("[ERROR] Amount must be positive.")
                return
            if amount > self.current_user.balance:
                print("[ERROR] Insufficient funds to pay this bill.")
                return

            self.current_user.balance -= amount
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            self.current_user.history.append(f"Paid {bill_types[choice]} Bill: -${amount:.2f} at {timestamp}")
            print(f"[SUCCESS] Paid {bill_types[choice]} bill of ${amount:.2f}!")
            print(f"-> Remaining Balance: ${self.current_user.balance:.2f}")
        except ValueError:
            print("[ERROR] Invalid amount.")

    # --- OPERATION 10: Change PIN ---
    def change_pin(self):
        print("\n--- [10] Change Account PIN ---")
        old_pin = input("Enter current 4-digit PIN: ").strip()
        if old_pin != self.current_user.pin:
            print("[ERROR] Incorrect current PIN.")
            return

        while True:
            new_pin = input("Enter new 4-digit PIN: ").strip()
            if new_pin.isdigit() and len(new_pin) == 4:
                if new_pin == old_pin:
                    print("[ERROR] New PIN cannot be the same as the old PIN.")
                    continue
                self.current_user.pin = new_pin
                print("[SUCCESS] PIN successfully updated!")
                break
            print("[ERROR] Invalid format. Must be exactly 4 digits.")

    # --- OPERATION 11: Account Summary ---
    def account_summary(self):
        print("\n--- [11] Account Summary ---")
        print(f"-> Account Holder Name : {self.current_user.name}")
        print(f"-> Account Number      : {self.current_user.account_number}")
        print(f"-> Account PIN         : {self.current_user.get_masked_pin()}")
        print(f"-> Available Balance   : ${self.current_user.balance:.2f}")
        print(f"-> Active Loan Amount  : ${self.current_user.loan_amount:.2f}")
        print(f"-> Total Transactions  : {len(self.current_user.history)}")

    # --- OPERATION 12: Savings Interest Calculator (New) ---
    def calculate_interest(self):
        print("\n--- [12] Savings Interest Calculator ---")
        try:
            rate = float(input("Enter annual interest rate (%): "))
            years = int(input("Enter duration (years): "))
            if rate < 0 or years < 0:
                print("[ERROR] Values cannot be negative.")
                return
            
            future_balance = self.current_user.balance * ((1 + (rate / 100)) ** years)
            earned = future_balance - self.current_user.balance
            print(f"\n[CALCULATION RESULTS]")
            print(f"-> Initial Principal: ${self.current_user.balance:.2f}")
            print(f"-> Estimated Interest Earned: ${earned:.2f}")
            print(f"-> Projected Total Balance after {years} years: ${future_balance:.2f}")
        except ValueError:
            print("[ERROR] Please enter valid numbers.")

    # --- OPERATION 13: Close Account ---
    def close_account(self):
        print("\n--- [13] Close Account ---")
        confirm = input("[WARNING] Are you sure you want to permanently close your account? (yes/no): ").strip().lower()
        if confirm == 'yes':
            acc_num = self.current_user.account_number
            del self.accounts[acc_num]
            print("[SUCCESS] Account closed successfully.")
            self.current_user = None
            return True
        else:
            print("[INFO] Account closure cancelled.")
            return False

    # --- OPERATION 14: Admin Portal (System Manager View) ---
    def admin_portal(self):
        print("\n--- [14] Bank Manager Admin Portal ---")
        passcode = input("Enter admin passcode: ").strip()
        if passcode != self.admin_passcode:
            print("[ERROR] Incorrect passcode. Access denied.")
            return

        total_capital = sum(acc.balance for acc in self.accounts.values())
        total_loans = sum(acc.loan_amount for acc in self.accounts.values())
        
        print("\n" + "="*40)
        print("          SYSTEM ADMIN DASHBOARD")
        print("="*40)
        print(f"-> Total Active Accounts: {len(self.accounts)}")
        print(f"-> Total Bank Capital   : ${total_capital:.2f}")
        print(f"-> Total Outstanding    : ${total_loans:.2f}")
        print("-" * 40)
        print("Registered Account Numbers:")
        for acc_num, acc in self.accounts.items():
            status = "LOCKED" if acc.is_locked else "ACTIVE"
            print(f" - #{acc_num} | {acc.name} | Balance: ${acc.balance:.2f} | [{status}]")
        print("="*40)

    # --- Main User Menu Loop ---
    def user_menu(self):
        while self.current_user:
            print(f"\n--- Menu | User: {self.current_user.name} (Acc: {self.current_user.account_number}) ---")
            print(" 3. Deposit Money           | 10. Change PIN")
            print(" 4. Withdraw Money          | 11. Account Summary")
            print(" 5. Check Balance           | 12. Interest Calculator")
            print(" 6. Transfer Funds          | 13. Close Account")
            print(" 7. Transaction History     | 14. Logout")
            print(" 8. Apply for Loan          |")
            print(" 9. Pay Utility Bills       |")
            
            choice = input("\nChoose an operation (3-14): ").strip()

            if choice == '3':
                self.deposit()
            elif choice == '4':
                self.withdraw()
            elif choice == '5':
                self.check_balance()
            elif choice == '6':
                self.transfer()
            elif choice == '7':
                self.transaction_history()
            elif choice == '8':
                self.apply_loan()
            elif choice == '9':
                self.pay_bill()
            elif choice == '10':
                self.change_pin()
            elif choice == '11':
                self.account_summary()
            elif choice == '12':
                self.calculate_interest()
            elif choice == '13':
                is_closed = self.close_account()
                if is_closed:
                    break
            elif choice == '14':
                print(f"[INFO] Logging out. Goodbye, {self.current_user.name}!")
                self.current_user = None
                break
            else:
                print("[ERROR] Invalid choice. Please select between 3 and 14.")

    def run(self):
        while True:
            self.display_banner()
            print("1. Create New Account")
            print("2. Login to Account")
            print("14. Admin Portal (Manager View)")
            print("0. Exit Application")
            
            main_choice = input("\nEnter your choice: ").strip()

            if main_choice == '1':
                self.create_account()
            elif main_choice == '2':
                success = self.login()
                if success:
                    self.user_menu()
            elif main_choice == '14':
                self.admin_portal()
            elif main_choice == '0':
                print("\n[INFO] Exiting application. Goodbye!")
                break
            else:
                print("[ERROR] Invalid option. Choose 0, 1, 2, or 14.")

if __name__ == "__main__":
    app = BankingSystem()
    app.run()