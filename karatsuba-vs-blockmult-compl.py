import random
import math
import time
import pandas as pd
from IPython.display import display, HTML
import matplotlib.pyplot as plt

mult_escalares = 0
sum_escalares = 0
llam_recursivas = -1
bases = [16, 32, 64, 128]
Ns = [64, 128, 256, 512, 1024, 2048]
results = []

def sumar_en(C, offset, P):
    global sum_escalares
    if offset < 0 or offset + len(P) > len(C):
        raise ValueError('Error en las parámetros de sumar_en: Índice fuera de límites.')
    for k in range(len(P)):
        C[offset + k] += P[k]
        sum_escalares += 1
    return C

def mult_clasica(A, B):
    global mult_escalares, sum_escalares
    nA, nB = len(A), len(B)
    C = [0]*(nA + nB - 1)
    for i in range(nA):
        for j in range(nB):
            C[i + j] += A[i]*B[j]
            mult_escalares += 1
            sum_escalares += 1
    return C

def suma(A, B):
    global sum_escalares
    if len(A) != len(B):
        raise ValueError("Las listas a sumar deben tener la misma longitud después de la división.")
    suma = []
    for i in range(len(A)):
        suma.append(A[i] + B[i])
        sum_escalares += 1
    return suma

def mult_bloques(A, B):
    global llam_recursivas, base
    llam_recursivas += 1
    n = max(len(A), len(B))
    A, B = A + [0]*(n - len(A)), B + [0]*(n - len(B))
    if n <= base:
        return mult_clasica(A, B)
    m = math.floor(n/2)
    A0, A1 = A[:m], A[m:n]
    B0, B1 = B[:m], B[m:n]
    P0 = mult_bloques(A0, B0)
    P01 = mult_bloques(A0, B1)
    P10 = mult_bloques(A1, B0)
    P1 = mult_bloques(A1, B1)
    C = [0 for _ in range(2*n - 1)]
    sumar_en(C, 0, P0)
    sumar_en(C, m, P01)
    sumar_en(C, m, P10)
    sumar_en(C, 2*m, P1)
    return C

def karatsuba(A, B):
    global sum_escalares, llam_recursivas, base
    llam_recursivas += 1
    n = max(len(A), len(B))
    A, B = A + [0]*(n - len(A)), B + [0]*(n - len(B))
    if n <= base:
        return mult_clasica(A, B)
    m = math.floor(n/2)
    A0, A1 = A[:m], A[m:n]
    B0, B1 = B[:m], B[m:n]
    P0 = karatsuba(A0, B0)
    P1 = karatsuba(A1, B1)
    P2 = karatsuba(suma(A0, A1), suma(B0, B1))
    M = [P2[i] - P0[i] - P1[i] for i in range(len(P2))]
    sum_escalares += 2*len(P2)
    C = [0 for _ in range(2*n - 1)]
    sumar_en(C, 0, P0)
    sumar_en(C, m, M)
    sumar_en(C, 2*m, P1)
    return C

def probar_metodo(metodo_func, metodo_name, n, base, A, B, D = []):
    global mult_escalares, sum_escalares, llam_recursivas
    inicio = time.perf_counter()
    C = metodo_func(A, B)
    fin = time.perf_counter()
    tiempo = f"{(fin - inicio)*1000: .3g}"
    if n > base:
      prof = math.floor(math.log2(n/base))
    else:
      prof = 0
    results.append({"n": n, "BASE": base, "Método": metodo_name, "Tiempo (ms)": tiempo, "Mult. escalares": \
                    mult_escalares, "Sumas escalares": sum_escalares, "Llamadas": llam_recursivas, "Prof.": \
                    prof, "Mem. auxiliar": 0, "KARATSUBA(A,B) =? MULTBLOQUES(A,B)": "..." if C != D else True})
    mult_escalares, sum_escalares, llam_recursivas = 0, 0, -1
    return C

# Registrar los datos para cada combinación de n con BASE
for n in Ns:
    A = [random.randint(-10**3, 10**3) for _ in range(n)]
    B = [random.randint(-10**3, 10**3) for _ in range(n)]
    for base in bases:
        # Probar MULTBLOQUES
        C = probar_metodo(mult_bloques, "Bloques", n, base, A, B)

        # Probar KARATSUBA
        D = probar_metodo(karatsuba, "Karatsuba", n, base, A, B, C)

def filtrar_busquedas(metodo, base):
  return [result for result in results if result.get("Método") == metodo and result.get("BASE") == base]

def mostrar_graficas(base):
    if base not in bases:
      raise ValueError("BASE no válida")
    karatsuba_results = filtrar_busquedas("Karatsuba", base)
    df_karatsuba_results = pd.DataFrame(karatsuba_results)
    bloques_results = filtrar_busquedas("Bloques", base)
    df_bloques_results = pd.DataFrame(bloques_results)

    plt.figure(figsize=(10, 6))
    plt.plot(
        df_karatsuba_results['n'],
        df_karatsuba_results['Tiempo (ms)'],
        marker = 'o', label = 'Karatsuba'
    )
    plt.plot(
        df_bloques_results['n'],
        df_bloques_results['Tiempo (ms)'],
        marker = 'o', 
        color = 'red',
        label = 'Bloques'
    )
    plt.xlabel("Tamaño de la entrada (n)")
    plt.ylabel("Tiempo de ejecución (ms)")
    plt.text(
        30,
        0.2,
        'n*',
        fontsize = 12,
        font = 'serif',
    )
    plt.text(
        100,
        1.2,
        'n*',
        fontsize = 12,
        font = 'serif',
    )
    plt.text(
        200,
        2,
        'n*',
        fontsize = 12,
        font = 'serif',
    )
    plt.text(
        450,
        3,
        'n*',
        fontsize = 12,
        font = 'serif',
    )
    plt.text(
        1000,
        4.2,
        'n*',
        fontsize = 12,
        font = 'serif',
    )
    plt.text(
        2000,
        5.2,
        'n*',
        fontsize = 12,
        font = 'serif',
    )
    plt.title(f'Comparación de tiempo vs. n con base = {base}')
    plt.grid(True)
    plt.legend()
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.plot(
        df_karatsuba_results['n'],
        df_karatsuba_results['Mult. escalares'],
        marker = 'o', 
        label = 'Karatsuba'
    )
    plt.plot(
        df_bloques_results['n'],
        df_bloques_results['Mult. escalares'],
        marker = 'o', 
        color = 'red',
        label = 'Bloques'
    )
    plt.xlabel("Tamaño de la entrada (n)")
    plt.ylabel("# multiplicaciones escalares")
    plt.title(f'Comparación de mult. escalares vs. n con base = {base}')
    plt.grid(True)
    plt.legend()
    plt.show()

def main():
    # Mostrar los resultados
    print('Resultados')
    df_results = pd.DataFrame(results)
    centrar_todo = [{'selector': '*', 'props': [('text-align', 'center')]}]
    df_final_estilizado = df_results.style.set_table_styles(centrar_todo).hide(axis="index")
    display(df_final_estilizado)
    
    # Mostrar gráficas para todas las bases
    for base in bases:
      mostrar_graficas(base)

if __name__ == "__main__":
    main()
