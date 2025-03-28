#!/usr/bin/env python3
import os
import time
import webbrowser
from colorama import Fore, Style, init

# Initialize colorama for colored terminal output
init(autoreset=True)

# Global wallet dictionary for the user (ETH supported; others coming soon)
wallet = {
    "ETH": 0.0,
    "BTC": 0.0  # Coming soon
}

# Global film projects available for investment
projects = {
    "1": {"name": "Indie Film A", "required": 100000, "invested": 0},
    "2": {"name": "Documentary B", "required": 50000, "invested": 0},
    "3": {"name": "Short Film C", "required": 20000, "invested": 0}
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_border():
    print(Fore.MAGENTA + "+" + "-" * 68 + "+")

def main_menu():
    while True:
        clear_screen()
        print_border()
        print(Fore.CYAN + "|          CINEMAfi INVESTMENT COMMAND CENTER           |")
        print_border()
        print(Fore.YELLOW + "\nMAIN MENU OPTIONS:")
        print(Fore.WHITE + "  1. View Balance")
        print(Fore.WHITE + "  2. View Positions")
        print(Fore.WHITE + "  3. Exchange Positions")
        print(Fore.WHITE + "  4. Deposit Coin")
        print(Fore.WHITE + "  5. Dividends")
        print(Fore.WHITE + "  6. Transfer")
        print(Fore.WHITE + "  7. Learn")
        print(Fore.WHITE + "  8. Explore Films")
        print(Fore.WHITE + "  9. Benefits and Perks")
        print(Fore.WHITE + " 10. Launch UI")
        print(Fore.WHITE + " 11. Account Settings")  # New menu item
        print(Fore.WHITE + "  0. Exit")
        print_border()
        choice = input(Fore.CYAN + "\nEnter your choice (0-11): ").strip()
        
        if choice == "1":
            view_balance()
        elif choice == "2":
            view_positions()
        elif choice == "3":
            exchange_positions()
        elif choice == "4":
            deposit_coin()
        elif choice == "5":
            dividends()
        elif choice == "6":
            transfer()
        elif choice == "7":
            learn()
        elif choice == "8":
            explore_films()
        elif choice == "9":
            benefits_and_perks()
        elif choice == "10":
            launch_ui()
        elif choice == "11":
            account_settings()  # New function call
        elif choice == "0":
            print(Fore.YELLOW + "\nExiting CinemaFi Command Center. Goodbye!")
            break
        else:
            print(Fore.RED + "\nInvalid choice, please try again.")
            time.sleep(1)

def view_balance():
    clear_screen()
    print_border()
    print(Fore.CYAN + "|                  YOUR WALLET BALANCE                   |")
    print_border()
    for coin, amount in wallet.items():
        print(Fore.WHITE + f"{coin}: {amount:.4f}")
    print(Fore.WHITE + "\nYour wallet holds the funds available for your investments.")
    print(Fore.WHITE + "Currently, only ETH is supported. BTC and other coins are coming soon!")
    print_border()
    input(Fore.CYAN + "\nPress Enter to return to the Main Menu...")

def view_positions():
    clear_screen()
    print_border()
    print(Fore.CYAN + "|                YOUR CURRENT INVESTMENT POSITIONS         |")
    print_border()
    # Example positions from film projects
    positions = {
        "Indie Film A": "$10,000",
        "Documentary B": "$5,000",
        "Short Film C": "$2,500"
    }
    for film, pos in positions.items():
        print(Fore.WHITE + f"{film}: {pos}")
    print(Fore.WHITE + "\nThese positions show the amount invested in various film projects.")
    print_border()
    input(Fore.CYAN + "\nPress Enter to return to the Main Menu...")

def exchange_positions():
    clear_screen()
    print_border()
    print(Fore.CYAN + "|                EXCHANGE YOUR INVESTMENT POSITIONS        |")
    print_border()
    print(Fore.WHITE + "\nExchange positions allow you to trade portions of your current investments.")
    print(Fore.WHITE + "This simulated feature helps you rebalance your portfolio or adjust your exposure.")
    print(Fore.WHITE + "\nNote: This is a demo function.")
    print_border()
    input(Fore.CYAN + "\nPress Enter to return to the Main Menu...")

def deposit_coin():
    clear_screen()
    print_border()
    print(Fore.CYAN + "|                    DEPOSIT COINS                         |")
    print_border()
    print(Fore.WHITE + "\nDeposit ETH to increase your wallet balance for investments.")
    print(Fore.WHITE + "Other coins (e.g., BTC) will be supported soon!")
    try:
        amount = float(input(Fore.CYAN + "\nEnter amount of ETH to deposit: "))
        if amount <= 0:
            print(Fore.RED + "Deposit amount must be positive.")
            time.sleep(1)
            return
    except ValueError:
        print(Fore.RED + "Invalid amount entered.")
        time.sleep(1)
        return
    wallet["ETH"] += amount
    print(Fore.GREEN + f"\nSuccessfully deposited {amount:.4f} ETH!")
    print(Fore.GREEN + f"New ETH Balance: {wallet['ETH']:.4f} ETH")
    print_border()
    input(Fore.CYAN + "\nPress Enter to return to the Main Menu...")

def dividends():
    clear_screen()
    print_border()
    print(Fore.CYAN + "|                     DIVIDEND PAYMENTS                    |")
    print_border()
    print(Fore.WHITE + "\nDividends represent the share of profits distributed from film revenues.")
    print(Fore.WHITE + "They are calculated based on your investment share in each film project.")
    print(Fore.WHITE + "\nReview your dividend history and projected earnings in your account.")
    print_border()
    input(Fore.CYAN + "\nPress Enter to return to the Main Menu...")

def transfer():
    clear_screen()
    print_border()
    print(Fore.CYAN + "|                     TRANSFER FUNDS                       |")
    print_border()
    print(Fore.WHITE + "\nTransfer funds to another account or withdraw your investment.")
    print(Fore.WHITE + "Always verify the recipient details before confirming any transfers.")
    print(Fore.WHITE + "\nThis simulated function logs your transfer requests securely.")
    print_border()
    input(Fore.CYAN + "\nPress Enter to return to the Main Menu...")

def learn():
    clear_screen()
    print_border()
    print(Fore.CYAN + "|                        LEARN MORE                        |")
    print_border()
    print(Fore.WHITE + "\nWelcome to the CinemaFi learning module!")
    print(Fore.WHITE + "\nInvestment Schedule & Process:")
    print(Fore.WHITE + "  - Submission & Evaluation: Filmmakers submit projects for review.")
    print(Fore.WHITE + "  - Tokenization: Film frames are tokenized into NFTs as investment shares.")
    print(Fore.WHITE + "  - Investment Window: Investors have a set period to fund a project.")
    print(Fore.WHITE + "  - Funding & Production: Once fully funded, projects move to production.")
    print(Fore.WHITE + "  - Revenue & Dividends: Film revenues are shared as dividends based on NFT ownership.")
    print(Fore.WHITE + "\nWhat to Expect & Impact:")
    print(Fore.WHITE + "  - Transparent and democratized film funding via blockchain technology.")
    print(Fore.WHITE + "  - Cultural impact by supporting independent films and innovative storytelling.")
    print(Fore.WHITE + "  - Potential returns via dividends and market appreciation over time.")
    print(Fore.WHITE + "\nOur platform directly connects filmmakers with investors to bridge the funding gap.")
    print_border()
    input(Fore.CYAN + "\nPress Enter to return to the Main Menu...")

def explore_films():
    clear_screen()
    print_border()
    print(Fore.CYAN + "|                    EXPLORE FILM PROJECTS                   |")
    print_border()
    # Display three highlighted film projects
    for pid, details in projects.items():
        required = details["required"]
        invested = details["invested"]
        remaining = required - invested
        print(Fore.WHITE + f"{pid}. {details['name']}")
        print(Fore.WHITE + f"   Funding Required: ${required:,}")
        print(Fore.WHITE + f"   Already Invested: ${invested:,}")
        print(Fore.WHITE + f"   Remaining: ${remaining:,}\n")
    print(Fore.WHITE + "Would you like to invest in one of these projects now?")
    choice = input(Fore.CYAN + "Enter project number to invest (or press Enter to cancel): ").strip()
    if choice in projects:
        project = projects[choice]
        try:
            amount = float(input(Fore.CYAN + f"Enter amount to invest in '{project['name']}': "))
            if amount <= 0:
                print(Fore.RED + "Investment amount must be positive.")
                time.sleep(1)
                return
        except ValueError:
            print(Fore.RED + "Invalid amount entered.")
            time.sleep(1)
            return
        remaining = project["required"] - project["invested"]
        if amount > remaining:
            print(Fore.RED + f"Amount exceeds the remaining funding (${remaining:,}). Investing maximum remaining amount.")
            amount = remaining
        project["invested"] += amount
        print(Fore.GREEN + f"\nSuccessfully invested ${amount:,.2f} in '{project['name']}''!")
        print(Fore.GREEN + f"Total Invested: ${project['invested']:,.2f} out of ${project['required']:,}")
    else:
        print(Fore.YELLOW + "\nNo investment made. Returning to the Main Menu...")
    print_border()
    input(Fore.CYAN + "\nPress Enter to return to the Main Menu...")

def benefits_and_perks():
    clear_screen()
    print_border()
    print(Fore.CYAN + "|                BENEFITS & PERKS OF INVESTING               |")
    print_border()
    print(Fore.WHITE + "\nInvesting with CinemaFi unlocks exclusive benefits and perks:")
    print(Fore.WHITE + "  - Early access to film premieres and exclusive events.")
    print(Fore.WHITE + "  - Behind-the-scenes content and filmmaker Q&A sessions.")
    print(Fore.WHITE + "  - Dividend earnings based on film revenue performance.")
    print(Fore.WHITE + "  - Special investor-only rewards and merchandise discounts.")
    print(Fore.WHITE + "\nThese benefits not only enhance your investment experience but also")
    print(Fore.WHITE + "create a deeper connection with the indie film community.")
    print_border()
    input(Fore.CYAN + "\nPress Enter to return to the Main Menu...")

def launch_ui():
    clear_screen()
    print_border()
    print(Fore.CYAN + "|                     LAUNCHING UI                         |")
    print_border()
    print(Fore.WHITE + "\nLaunching the CinemaFi User Interface...")
    print(Fore.WHITE + "This will open your default web browser to the CinemaFi UI portal.")
    # Simulate launching a UI by opening a placeholder URL
    url = "http://localhost:8000/ui"  # Replace with your actual UI URL when available
    print(Fore.GREEN + f"\nOpening: {url}")
    webbrowser.open(url)
    print_border()
    input(Fore.CYAN + "\nPress Enter to return to the Main Menu...")

def account_settings():
    """New function to handle account settings like connecting to external accounts, preferences, etc."""
    while True:
        clear_screen()
        print_border()
        print(Fore.CYAN + "|                    ACCOUNT SETTINGS                      |")
        print_border()
        print(Fore.WHITE + "  1. Connect External Account")
        print(Fore.WHITE + "  2. User Preferences")
        print(Fore.WHITE + "  3. Admin Tools")
        print(Fore.WHITE + "  0. Return to Main Menu")
        print_border()
        choice = input(Fore.CYAN + "\nEnter your choice (0-3): ").strip()
        
        if choice == "1":
            connect_external_account()
        elif choice == "2":
            user_preferences()
        elif choice == "3":
            admin_tools()
        elif choice == "0":
            break
        else:
            print(Fore.RED + "\nInvalid choice, please try again.")
            time.sleep(1)

def connect_external_account():
    clear_screen()
    print_border()
    print(Fore.CYAN + "|                CONNECT EXTERNAL ACCOUNT                  |")
    print_border()
    print(Fore.WHITE + "\nIn this section, you can link external wallets or accounts for easier transfers.")
    print(Fore.WHITE + "Supported integrations will expand in the future.")
    print(Fore.WHITE + "\n(Placeholder demonstration — actual implementation may vary.)")
    print_border()
    input(Fore.CYAN + "\nPress Enter to return to Account Settings...")

def user_preferences():
    clear_screen()
    print_border()
    print(Fore.CYAN + "|                   USER PREFERENCES                       |")
    print_border()
    print(Fore.WHITE + "\nCustomize your CinemaFi experience, such as interface color themes,")
    print(Fore.WHITE + "notification settings, and more.")
    print(Fore.WHITE + "\n(Placeholder demonstration — actual implementation may vary.)")
    print_border()
    input(Fore.CYAN + "\nPress Enter to return to Account Settings...")

def admin_tools():
    clear_screen()
    print_border()
    print(Fore.CYAN + "|                     ADMIN TOOLS                          |")
    print_border()
    print(Fore.WHITE + "\nAccess advanced administrative features (if authorized).")
    print(Fore.WHITE + "This may include project approvals, user management, and auditing.")
    print(Fore.WHITE + "\n(Placeholder demonstration — actual implementation may vary.)")
    print_border()
    input(Fore.CYAN + "\nPress Enter to return to Account Settings...")

if __name__ == "__main__":
    main_menu()
