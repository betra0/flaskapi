edad = input('ingrese su edad: ')
try:
    edad = int(edad)

except ValueError as e:
    print("Hubo un error", e)

    edad = int(input('ingrese su edad: '))
