import numpy as np

# Вхідні дані
expected_returns = np.array([0.10, 0.20, 0.50])  # Сподівані норми прибутку
std_devs = np.array([0.02, 0.10, 0.20])  # Стандартні відхилення
correlation_matrix = np.array([[1, 0, 0], [0, 1, -0.6], [0, -0.6, 1]])  # Кореляції

# Матриця коваріації
cov_matrix = np.outer(std_devs, std_devs) * correlation_matrix

# Функція для обчислення ризику (стандартного відхилення портфеля)
def portfolio_risk(weights, cov_matrix):
    return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

# Функція для обчислення прибутковості портфеля
def portfolio_return(weights, expected_returns):
    return np.dot(weights, expected_returns)

# Функція для мінімізації ризику
def minimize_risk():
    best_risk = float('inf')
    best_weights = None

    for w1 in np.linspace(0, 1, 100):
        for w2 in np.linspace(0, 1 - w1, 100):
            w3 = 1 - w1 - w2
            weights = np.array([w1, w2, w3])
            risk = portfolio_risk(weights, cov_matrix)
            if risk < best_risk:
                best_risk = risk
                best_weights = weights

    return best_weights, portfolio_return(best_weights, expected_returns), best_risk

# Функція для досягнення приросту капіталу при певному рівні прибутку
def target_return(mC):
    best_risk = float('inf')
    best_weights = None

    for w1 in np.linspace(0, 1, 100):
        for w2 in np.linspace(0, 1 - w1, 100):
            w3 = 1 - w1 - w2
            weights = np.array([w1, w2, w3])
            ret = portfolio_return(weights, expected_returns)
            risk = portfolio_risk(weights, cov_matrix)
            if abs(ret - mC) < 0.01 and risk < best_risk:  # Шукаємо при заданому mC
                best_risk = risk
                best_weights = weights

    return best_weights, portfolio_return(best_weights, expected_returns), best_risk

# Функція для максимального приросту капіталу при фіксованому рівні ризику
def target_risk(sigmaC):
    best_return = -float('inf')
    best_weights = None

    for w1 in np.linspace(0, 1, 100):
        for w2 in np.linspace(0, 1 - w1, 100):
            w3 = 1 - w1 - w2
            weights = np.array([w1, w2, w3])
            ret = portfolio_return(weights, expected_returns)
            risk = portfolio_risk(weights, cov_matrix)
            if abs(risk - sigmaC) < 0.01 and ret > best_return:  # Шукаємо при заданому ризику
                best_return = ret
                best_weights = weights

    return best_weights, portfolio_return(best_weights, expected_returns), portfolio_risk(best_weights, cov_matrix)

# Головна функція для запуску задач
def main(RF):
    print(f"\nОптимальні структури портфеля для RF = {RF}%:")
    
    # а) Мінімізація ризику
    weights_a, return_a, risk_a = minimize_risk()
    print("\nа) Збереження капіталу (мінімальний ризик):")
    print(f"Ваги: {weights_a}")
    print(f"Сподівана норма прибутку: {return_a * 100:.2f}%")
    print(f"Ризик: {risk_a * 100:.2f}%")
    
    # б) Приріст капіталу при mC = 30%
    mC = 0.30
    weights_b, return_b, risk_b = target_return(mC)
    print("\nб) Приріст капіталу при mC = 30%:")
    print(f"Ваги: {weights_b}")
    print(f"Сподівана норма прибутку: {return_b * 100:.2f}%")
    print(f"Ризик: {risk_b * 100:.2f}%")
    
    # в) Приріст капіталу при σС = 15%
    sigmaC = 0.15
    weights_c, return_c, risk_c = target_risk(sigmaC)
    print("\nв) Приріст капіталу при σС = 15%:")
    print(f"Ваги: {weights_c}")
    print(f"Сподівана норма прибутку: {return_c * 100:.2f}%")
    print(f"Ризик: {risk_c * 100:.2f}%")

if __name__ == "__main__":
    # Виклик для RF = -10
    main(RF=-10)

    # Виклик для RF = -100
    main(RF=-100)
