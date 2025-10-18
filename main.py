import sys
from problema_riego import roFB  # importa la función que ya implementamos
from problema_riego import roPD
from problema_riego import roV

def read_finca(file_path: str):
    """
    Lee el archivo de entrada con formato:
    n
    ts0,tr0,p0
    ts1,tr1,p1
    ...
    """
    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    n = int(lines[0])
    finca = []
    for i in range(1, n + 1):
        ts, tr, p = map(int, lines[i].split(","))
        finca.append((ts, tr, p))
    return finca

def write_solution(file_path: str, perm, costo):
    """
    Escribe el archivo de salida con formato:
    Costo
    pi0
    pi1
    ...
    """
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(str(costo) + "\n")
        for idx in perm:
            f.write(str(idx) + "\n")

def main():
    if len(sys.argv) != 3:
        print("Uso: python main.py entrada.txt salida.txt")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    out_fb = output_file + "_FB.txt"
    out_pd = output_file + "_PD.txt"
    out_V = output_file + "_V.txt"
    finca = read_finca(input_file)

    #Se muestra la salida por medio de archivos diferentes para cada algoritmo
    perm, costo = roFB(finca) 
    perm, costo = roPD(finca)
    perm, costo = roV(finca)
    write_solution(out_fb, perm, costo)
    write_solution(out_pd, perm, costo)
    write_solution(out_V, perm, costo)

if __name__ == "__main__":
    main()
