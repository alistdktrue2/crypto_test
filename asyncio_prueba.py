def frutas():
    yield 1
    yield "manzana"
    yield "pera"


g=frutas()


print("next:" ,next(g))
print("next:" ,next(g))
print("next:" ,next(g))