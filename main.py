def main():
    notifier = ConsoleNotificationService()
    bank_service = BankService()
    loan_service = LoanService(notifier)
    investment_service = InvestmentService(notifier)
    deposit_service = DepositService(notifier)

    bank_service.create_account("Клієнт", 1000.0, AccountType.SAVINGS)
    acc = bank_service.get_account()

    notifier.notify("=== СИСТЕМА УПРАВЛІННЯ БАНКОМ (PYTHON) ===", Colors.CYAN)

    while True:
        print(f"\nВласник: {acc.owner}")
        print(f"Баланс: {acc.balance:,.2f}₴ | Борг: {acc.debt:,.2f}₴")
        portfolio_val = investment_service.calculate_portfolio_value(acc)
        print(f"Портфель: {portfolio_val:,.2f}₴ | Тип: {acc.account_type.value}")

        print("\nМЕНЮ:")
        print("1. Оформити кредит   2. Купити акції    3. Продати акції")
        print("4. Погасити кредит   5. Відсотки (деп)  6. Переказати")
        print("7. Оновити ціни      8. Ринок акцій     9. Історія кредитів")
        print("10. Вийти")

        choice = input("\nВаш вибір: ")

        if choice == "10": break

        try:
            if choice == "1":
                amt = float(input("Сума: "))
                term = int(input("Термін (міс): "))
                loan_service.apply_for_loan(acc, amt, term)
            
            elif choice == "2":
                ticker = input("Тікер (AAPL/BTC): ").upper()
                qty = int(input("Кількість: "))
                investment_service.buy_stock(ticker, qty, acc)

            elif choice == "3":
                ticker = input("Тікер для продажу: ").upper()
                qty = int(input("Кількість: "))
                investment_service.sell_stock(ticker, qty, acc)

            elif choice == "4":
                loan_service.process_loan_payment(acc)

            elif choice == "5":
                deposit_service.process_interest(acc)

            elif choice == "6":
                to = input("Отримувач: ")
                amt = float(input("Сума: "))
                if bank_service.transfer(to, amt):
                    notifier.notify(f"Переказ {amt} для {to} виконано", Colors.BLUE)
                else:
                    notifier.notify("Помилка переказу", Colors.RED)

            elif choice == "7":
                investment_service.update_market_prices()
                notifier.notify("Ціни оновлено", Colors.MAGENTA)

            elif choice == "8":
                print("\nРИНОК:")
                for s in investment_service.get_market():
                    print(f"{s.ticker}: {s.price:,.2f}₴ (залишок: {s.quantity})")

            elif choice == "9":
                history = loan_service.get_history()
                print("\nІСТОРІЯ:")
                for req in history:
                    print(f"{req.status}: {req.amount}₴ ({req.interest_rate:.1%})")

        except ValueError:
            notifier.notify("Помилка вводу! Вводьте числа.", Colors.RED)

    notifier.notify("Дякуємо за використання!", Colors.CYAN)

if __name__ == "__main__":
    main()