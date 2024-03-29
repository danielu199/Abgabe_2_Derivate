import math

def calculate_option_price(S0, X, omega, r, n, europe, T):
    # Berechnung der notwendigen Parameter
    delta_t = T / n
    up_factor = math.exp(omega * math.sqrt(delta_t))
    down_factor = 1.0 / up_factor
    discount_factor = math.exp(-r * delta_t)

    # Berechnung des Aktienkursbaums
    stock_prices = [[S0]]

    for i in range(1, n+1):
        prev_prices = stock_prices[i-1]
        current_prices = [price * up_factor for price in prev_prices]
        current_prices.append(prev_prices[-1] * down_factor)
        stock_prices.append(current_prices)

    # Berechnung des Optionspreisbaums
    option_prices = [[max((price - X)*0.01, 0) for price in prices] for prices in stock_prices]

    #(glaube brauchen wir nicht) Berechnung der risikoneutralen Wahrscheinlichkeiten, da upward-, downwardfaktor und r kostant--> q und 1-q konstant
   #q = (1+r-down_factor)/(up_factor-down_factor)

    #checken ob europäisch oder amerikanisch

    # Arbeit von rechts nach links im Optionspreisbaum
    for i in range(n-1, -1, -1):
        for j in range(i+1):
            option_prices[i][j] = (option_prices[i+1][j] * 0.5 + option_prices[i+1][j+1] * (0.5)) * discount_factor

    if not europe:
        # Arbeit von rechts nach links im Optionspreisbaum für amerikanische calls
        for i in range(n-1, -1, -1):
            for j in range(i+1):
                option_prices[i][j] = max(option_prices[i][j],(stock_prices[i][j]-X)*0.01)

    return option_prices[0][0]

# Marktdaten
S0 = 16290.12
X = 16900
omega = 0.1748
r = 0.04886
n = 100
europe = True
T = 0.5

if __name__ == "__main__":
    for n in range(1,n+1):
        option_price = calculate_option_price(S0, X, omega, r, n, europe, T)
        print("Option price: n=", n ,' ', option_price)

