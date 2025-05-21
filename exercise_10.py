from abc import ABC, abstractmethod

class Observer(ABC):
    def __init__(self, interested_stock=None):
        self.interested_stock = interested_stock  

    @abstractmethod
    def update(self, stock_name: str, new_price: float):
        if self.interested_stock and self.interested_stock != stock_name:
            return  
        pass

class Subject(ABC):
    @abstractmethod
    def attach(self, observer: Observer):
        pass
    
    @abstractmethod
    def detach(self, observer: Observer):
        pass
    
    @abstractmethod
    def notify_observers(self):
        pass

class StockExchange(Subject):
    def __init__(self, max_subscribers=3):  
        self._observers = []
        self._stock_name = ""
        self._stock_price = 0.0
        self.max_subscribers = max_subscribers

    def set_stock_price(self, stock_name: str, new_price: float):
        self._stock_name = stock_name
        self._stock_price = new_price
        self.notify_observers()

    def attach(self, observer: Observer):
        if len(self._observers) >= self.max_subscribers:
            print("Ліміт підписників досягнуто!")
            return
        self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def notify_observers(self):
        for observer in self._observers:
            observer.update(self._stock_name, self._stock_price)

class Investor(Observer):
    def __init__(self, name: str, interested_stock=None):
        super().__init__(interested_stock)
        self._name = name

    def update(self, stock_name: str, new_price: float):
        if self.interested_stock and self.interested_stock != stock_name:
            return
        print(f"Інвестор {self._name} повідомлений: Акція {stock_name} змінила ціну на {new_price}")

class Broker(Observer):
    def __init__(self, name: str, interested_stock=None):
        super().__init__(interested_stock)
        self._name = name

    def update(self, stock_name: str, new_price: float):
        if self.interested_stock and self.interested_stock != stock_name:
            return
        print(f"Брокер {self._name} повідомлений: Акція {stock_name} тепер коштує {new_price}")

def run_test():
    stock_exchange = StockExchange(max_subscribers=3)

    investor1 = Investor("Олександр", interested_stock="Google")
    investor2 = Investor("Марія")  
    broker = Broker("Компанія 'ТрейдМакс'")

    stock_exchange.attach(investor1)
    stock_exchange.attach(investor2)
    stock_exchange.attach(broker)

    stock_exchange.set_stock_price("Apple", 145.50)
    stock_exchange.set_stock_price("Google", 2730.20) 
    stock_exchange.set_stock_price("Microsoft", 310.00) 

    stock_exchange.detach(investor2)

    stock_exchange.set_stock_price("Tesla", 700.00) 


def interactive_management():
    stock_exchange = StockExchange(max_subscribers=3)

    while True:
        print("\n1. Додати підписника")
        print("2. Видалити підписника")
        print("3. Змінити курс акцій")
        print("4. Вийти")
        choice = input("Оберіть дію: ")

        if choice == '1':
            name = input("Введіть ім'я підписника: ")
            subscriber_type = input("Виберіть тип підписника (investor/broker): ").lower()
            stock_interest = input("Акція, яку підписник хоче відслідковувати (leave blank for all): ").strip()

            if subscriber_type == 'investor':
                stock_exchange.attach(Investor(name, stock_interest or None))
            elif subscriber_type == 'broker':
                stock_exchange.attach(Broker(name, stock_interest or None))
            else:
                print("Невірний тип підписника!")

        elif choice == '2':
            name = input("Введіть ім'я підписника, якого хочете видалити: ")
            found = False
            for observer in stock_exchange._observers:
                if isinstance(observer, Investor) and observer._name == name:
                    stock_exchange.detach(observer)
                    found = True
                    break
                elif isinstance(observer, Broker) and observer._name == name:
                    stock_exchange.detach(observer)
                    found = True
                    break

            if not found:
                print("Підписник не знайдений.")

        elif choice == '3':
            stock_name = input("Введіть назву акції: ")
            price = float(input("Введіть нову ціну: "))
            stock_exchange.set_stock_price(stock_name, price)

        elif choice == '4':
            break
        else:
            print("Невірний вибір!")

if __name__ == "__main__":
    print("Тестування шаблону Observer...")
    run_test()

    print("\nІнтерактивне управління підписниками:")
    interactive_management()