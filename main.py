import sys
from problema_riego import roFB  # importa la función que ya implementamos

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

    finca = read_finca(input_file)
    perm, costo = roFB(finca)
    write_solution(output_file, perm, costo)

if __name__ == "__main__":
    main()
