#!/usr/bin/env python3
import os
import time
from colorama import Fore, Style, init

# Initialize colorama for colored terminal output
init(autoreset=True)

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
        print(Fore.WHITE + "  0. Exit")
        print_border()
        choice = input(Fore.CYAN + "\nEnter your choice (0-9): ").strip()
        
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
        elif choice == "0":
            print(Fore.YELLOW + "\nExiting Cinemafi Investment Command Center. Goodbye!")
            break
        else:
            print(Fore.RED + "\nInvalid choice, please try again.")
            time.sleep(1)

def view_balance():
    clear_screen()
    print_border()
    print(Fore.CYAN + "|                  YOUR BALANCE OVERVIEW                 |")
    print_border()
    # Example balance information
    balance = 25000.75
    print(Fore.WHITE + f"\nCurrent Balance: ${balance:,.2f}")
    print(Fore.WHITE + "\nThis is the total amount available for your investments.")
    print_border()
    input(Fore.CYAN + "\nPress Enter to return to the Main Menu...")

def view_positions():
    clear_screen()
    print_border()
    print(Fore.CYAN + "|                YOUR CURRENT INVESTMENT POSITIONS         |")
    print_border()
    # Example positions
    positions = {
        "Indie Film A": "$10,000",
        "Documentary B": "$5,000",
        "Short Film C": "$2,500"
    }
    for film, pos in positions.items():
        print(Fore.WHITE + f"{film}: {pos}")
    print(Fore.WHITE + "\nThese positions show the value of your investments in various films.")
    print_border()
    input(Fore.CYAN + "\nPress Enter to return to the Main Menu...")

def exchange_positions():
    clear_screen()
    print_border()
    print(Fore.CYAN + "|                EXCHANGE YOUR INVESTMENT POSITIONS        |")
    print_border()
    print(Fore.WHITE + "\nExchange positions allow you to trade parts of your current investments.")
    print(Fore.WHITE + "This helps you rebalance your portfolio or take advantage of market fluctuations.")
    print(Fore.WHITE + "\nNote: This is a simulated interface for demonstration purposes.")
    print_border()
    input(Fore.CYAN + "\nPress Enter to return to the Main Menu...")

def deposit_coin():
    clear_screen()
    print_border()
    print(Fore.CYAN + "|                    DEPOSIT COINS                         |")
    print_border()
    print(Fore.WHITE + "\nDeposit coins to increase your available capital for investments.")
    print(Fore.WHITE + "Follow the provided instructions to securely deposit your cryptocurrency.")
    print(Fore.WHITE + "\nFor example, send your coins to the provided wallet address and confirm the deposit.")
    print_border()
    input(Fore.CYAN + "\nPress Enter to return to the Main Menu...")

def dividends():
    clear_screen()
    print_border()
    print(Fore.CYAN + "|                     DIVIDEND PAYMENTS                    |")
    print_border()
    print(Fore.WHITE + "\nDividends represent the share of profits distributed from film revenues.")
    print(Fore.WHITE + "They are automatically calculated based on your investment proportion.")
    print(Fore.WHITE + "\nReview your dividend history to see your earnings.")
    print_border()
    input(Fore.CYAN + "\nPress Enter to return to the Main Menu...")

def transfer():
    clear_screen()
    print_border()
    print(Fore.CYAN + "|                     TRANSFER FUNDS                       |")
    print_border()
    print(Fore.WHITE + "\nTransfer funds to another account or withdraw your investment.")
    print(Fore.WHITE + "Ensure you verify recipient details before confirming any transfers.")
    print(Fore.WHITE + "\nThis feature secures your transactions and tracks your transfer history.")
    print_border()
    input(Fore.CYAN + "\nPress Enter to return to the Main Menu...")

def learn():
    clear_screen()
    print_border()
    print(Fore.CYAN + "|                        LEARN MORE                        |")
    print_border()
    print(Fore.WHITE + "\nLearn about film investments, blockchain technology, and NFT trading.")
    print(Fore.WHITE + "Educational resources help you understand market trends and investment risks.")
    print(Fore.WHITE + "\nTopics include: Investment basics, market analysis, and technical insights.")
    print_border()
    input(Fore.CYAN + "\nPress Enter to return to the Main Menu...")

def explore_films():
    clear_screen()
    print_border()
    print(Fore.CYAN + "|                    EXPLORE FILM PROJECTS                   |")
    print_border()
    print(Fore.WHITE + "\nDiscover a curated selection of film projects seeking investment.")
    print(Fore.WHITE + "Each listing provides project vision, funding requirements, and potential returns.")
    print(Fore.WHITE + "\nExplore and evaluate the films to decide where to invest.")
    print_border()
    input(Fore.CYAN + "\nPress Enter to return to the Main Menu...")

def benefits_and_perks():
    clear_screen()
    print_border()
    print(Fore.CYAN + "|                BENEFITS & PERKS OF INVESTING               |")
    print_border()
    print(Fore.WHITE + "\nInvesting with CinemaFi offers exclusive benefits and perks.")
    print(Fore.WHITE + "Enjoy early access to film releases, behind-the-scenes content, special event invites,")
    print(Fore.WHITE + "and potential dividend earnings based on your investment performance.")
    print(Fore.WHITE + "\nMaximize your returns while enjoying the cinematic experience.")
    print_border()
    input(Fore.CYAN + "\nPress Enter to return to the Main Menu...")

if __name__ == "__main__":
    main_menu()