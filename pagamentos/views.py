from django.shortcuts import render
from datetime import datetime, timedelta, date

"""data = datetime.today() + timedelta(days=20)
print(data.day)


DIAS = [
    'Segunda-feira',
    'Terça-feira',
    'Quarta-feira',
    'Quinta-Feira',
    'Sexta-feira',
    'Sábado',
    'Domingo'
]

print(datetime.today().hour)
print(datetime.today().second)
s = datetime.today().second

while True:
    segundo = datetime.today().second
    if segundo == 10 or segundo == 20 or segundo == 30 or segundo == 40 or segundo == 50 or segundo == 59:
        if s != segundo:
            print(segundo)
            s = segundo"""




def teste(req):
    return render (req, 'pagamentos/teste.html')

