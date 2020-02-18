from django import forms
from main.models import Order
from django.core.exceptions import ValidationError

alpha = set('аоуыэяеёюибвгдйжзклмнпрстфхцчшщАОУЫЭЯЕЁЮИБВГДЙЖЗКЛМНПРСТФХЦЧШЩіІїЇґҐ ')

#валидатор имени
def name_validator(name):
    for char in name:
        if char in alpha:
            pass
        else:
            raise ValidationError('Недопустимые символы в имени',)

#валидатор номера
def phone_validator(phone):
    if phone[0] == '+' and\
        phone[4] == '(' and\
        phone[7] == ')' and\
        phone[11] == "-" and\
        phone[14]== "-":
        phone = phone.replace('+', '')
        phone = phone.replace('(', '')
        phone = phone.replace(')', '')
        phone = phone.replace('-', '')
        if len(phone) != 12:
            raise ValidationError('Номер должен состоять из 12-ти цифр')
        else:
            for char in phone:
                try:
                    int(char)
                except:
                    raise ValidationError('Введите номер в формате +380(ХХ)ХХХ-ХХ-ХХ')
    else:
        raise ValidationError('Введите номер в формате +380(ХХ)ХХХ-ХХ-ХХ')


class OrderForm (forms.Form):

    client_name = forms.CharField(validators=[name_validator])
    client_phone = forms.CharField(validators=[phone_validator])
    address = forms.CharField()
    destination = forms.CharField()
    desired_time = forms.TimeField(error_messages={'invalid': "Неверный формат времени"})

    class Meta:
        model = Order

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['client_name'].label = 'Имя'
        self.fields['client_name'].help_text = 'Только керилические буквы'
        self.fields['client_phone'].label = 'Номер'
        self.fields['client_phone'].help_text = 'Введите номер в формате +380(ХХ)ХХХ-ХХ-ХХ'
        self.fields['address'].label = 'Стартовый адресс'
        self.fields['destination'].label = 'Конечный адресс'
        self.fields['desired_time'].label = 'Время'
        self.fields['desired_time'].help_text = 'Введите желаемое время в формате HH:MM'


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'