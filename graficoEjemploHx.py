import matplotlib.pyplot as plt

intervalos = ["Infinity", -2.8, -2.6, -2.4, -2.2, -2.0, -1.8, -1.6, -1.4, -1.2, -1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0, "Infinity"]

frecuencia = [119, 124, 209, 347, 556, 827, 1345, 1880, 2650, 3331, 4348, 5269, 6365, 7029, 7731, 7958, 7943, 7607, 7028, 6363, 5280, 4313, 3395, 2555, 1874, 1316, 846, 611, 363, 186, 112, 120]

# Graficamos los resultados
plt.plot(intervalos, frecuencia, label="Histogram")
plt.xlabel("RVALUE de 'x'")
plt.ylabel("Frecuencia")
plt.title("Histogram de [num] hx := histogram(‘x’, 1000, 30, -3.0, 3.0);")
plt.legend("num u1 := 'uniform()'; \nnum u2 := 'uniform()'; \nnum x := 'sqrt(-2 * ln(u1)) * cos(2 * pi() * u2)';")
plt.show()
