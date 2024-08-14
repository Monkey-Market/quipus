import sys


def read_version():
    try:
        with open(".project-version", "r") as f:
            version = f.read().strip()
            return version
    except FileNotFoundError:
        print("Archivo .project-version no encontrado.")
        sys.exit(1)


def write_version(version):
    with open(".project-version", "w") as f:
        f.write(version)


def increment_version(version, part):
    parts = version.split(".")
    if part == "major":
        parts[0] = str(int(parts[0]) + 1)
        parts[1] = "0"
        parts[2] = "0"
    elif part == "minor":
        parts[1] = str(int(parts[1]) + 1)
        parts[2] = "0"
    elif part == "patch":
        parts[2] = str(int(parts[2]) + 1)
    else:
        print("El argumento debe ser 'major', 'minor' o 'patch'.")
        sys.exit(1)
    return ".".join(parts)


def main():
    version = read_version() or "0.0.0"

    if len(sys.argv) != 2:
        print("Uso: python script.py <major|minor|patch>")
        sys.exit(1)

    part = sys.argv[1]
    if part not in ["major", "minor", "patch"]:
        print("El argumento debe ser 'major', 'minor' o 'patch'.")
        sys.exit(1)

    new_version = increment_version(version, part)
    write_version(new_version)
    print(f"Versión incrementada a: {new_version}")


if __name__ == "__main__":
    main()
