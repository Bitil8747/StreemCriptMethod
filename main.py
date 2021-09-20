from functools import partial

import matplotlib as matplotlib
from tkinter import *
import random
from tkinter import filedialog as fd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os


def chooseFile():
    file_name = fd.askopenfilename()
    return file_name


def MGenerate():
    global var, Registers_num, OutputKey, N # количество выходных битов, т.е. длина M-последовательности
    Registers_num = 28  # количество регистров сдвига
    m = Registers_num  # старший регистр в полиноме
    l = 3  # младный регистр в полиноме
    OutputKey = []

    if(var.get() == False):
        BitList = [random.getrandbits(1) for i in range(Registers_num)] # биты регистра сдвига

        # проверка на нулевой ключ
        OK = False
        for i in range(len(BitList)):
            if (BitList[i] == 1):
                OK = True
                break
        while(OK == False):
            for i in range(len(BitList)):
                if (BitList[i] == 1):
                    OK = True
                    break
            BitList = [random.getrandbits(1) for i in range(Registers_num)]


    if (var.get() == False):
        with open("C:/Users/Airat/Desktop/lab2_Key.txt", 'w', encoding='utf-8') as file:
            file.write(''.join(str(BitList[i]) for i in range(Registers_num)))


    if (var.get()):
        with open("C:/Users/Airat/Desktop/lab2_Key.txt", 'r', encoding='utf-8') as file:
            BitString = file.read()
            BitList = [int(BitString[i]) for i in range(len(BitString))]

    key = []
    for i in BitList:
        key.append(i)

    Bit_num = 0
    while Bit_num < N:
        OutputKey.append(BitList[0])
        Tmp = BitList[m-1] ^ BitList[l-1]
        for i in range(len(BitList)-1):
            BitList[i] = BitList[i+1]
        BitList[len(BitList)-1] = Tmp
        Bit_num += 1

    with open("C:/Users/Airat/Desktop/lab2_info.txt", 'w', encoding='utf-8') as file:
        file.write("%s-битный ключ:\n"%Registers_num + ''.join(str(key[i]) for i in range(len(key)))
                   + "\n\nM-последовательность:\n"
                   + ''.join(str(OutputKey[i]) for i in range(len(OutputKey))))

    l1.config(text='')
    l2.config(text='')


def serialTest():
    global Registers_num, TestMessage, OutputKey, N # L-количество регистров, M-последовательность, длина М-последовательности

    # b = []
    # for i in TestMessage:
    #     c = "{:08b}".format(i, 'b')
    #     b.append(c)
    #
    # test_string = []
    # for i in range(len(b)):
    #     for j in range(8):
    #         test_string.append(int(list(b[i])[j]))

    test_string = []
    for i in OutputKey:
            test_string.append(i)

    k = 2 # длина серии
    #if(N-2*Registers_num > 0):
    #    Seq = [[0 for i in range(k)] for i in range(int((N-2*Registers_num)/k))] # N/k непересекающихся серий
    #else:
    Seq = [[0 for i in range(k)] for i in range(int((N)/k))]

    Index = 0
    for i in range(0, len(Seq)):
        for j in range(0, k):
            #if (N - 2 * Registers_num > 0):
            #    Seq[i][j] = test_string[2 * Registers_num + Index]
            #else:
            Seq[i][j] = test_string[Index]
            Index += 1

    F_prac = [0 for i in range(2**k)] # частота каждой двоичной комбинации
    Bit = 0
    for l in range(0, 2**k):
        a = format(Bit, ">0%sb" % k)
        for i in range(0, len(Seq)):
            if(Seq[i] == list(int(list(a)[i]) for i in range(len(list(a))))):
                F_prac[l] += 1
        Bit += 1

    F_teor = len(Seq)/(2**k) # теоретическая частота каждой комбинации

    H_square = 0 # критерий H**2 Пирсона с (2**k)-1 k степенями свободы
    for i in range(0, 2**k):
        H_square += ((F_prac[i] - F_teor)**2)/F_teor

    if(k == 2):
        if((H_square > 0.584) & (H_square < 6.251)):
            m = "Сериальный тест пройден"
        else: m = "Сериальный тест не пройден"
    if (k == 3):
        if ((H_square > 2.833) & (H_square < 12.017)):
            m = "Сериальный тест пройден"
        else:
            m = "Сериальный тест не пройден"
    if (k == 4):
        if ((H_square > 8.547) & (H_square < 22.307)):
            m = "Сериальный тест пройден"
        else:
            m = "Сериальный тест не пройден"

    l1.config(text=m+"\nКритерий Пирсона: " + str(H_square))

    with open("C:/Users/Airat/Desktop/lab2_info.txt", 'a', encoding='utf-8') as file:
        file.write('\n\n' + "Последовательность серий\n"
                   + ''.join(str(Seq)) + '\n\n' + "Сериальный тест:\nДлина серий:%s\n" %k
                   + "Критерий Пирсона: " + str(H_square) + "\n" + m)


def correlationTest():
    global Registers_num, TestMessage, OutputKey, N # L-количество регистров, M-последовательность, длина М-последовательности


    # b = []
    # for i in TestMessage:
    #     c = "{:08b}".format(i, 'b')
    #     b.append(c)
    #
    # test_string = []
    # for i in range(len(b)):
    #     for j in range(8):
    #         test_string.append(int(list(b[i])[j]))

    test_string = []
    for i in OutputKey:
        test_string.append(i)

    k = 1 # разница

    #if (N - 2 * Registers_num > 0):
    #    K = N - 2*Registers_num
    #    Xi = OutputKey[2*Registers_num:len(OutputKey)-k]
    #    Xik = OutputKey[2*Registers_num+k:]
    #else:

    K = N
    Xi = test_string[0:len(test_string)-k]
    Xik = test_string[0+k:]

    Mi = 0
    Mi2 = 0
    for i in range(len(Xi)):
        Mi += Xi[i]
        Mi2 += Xi[i]**2
    Mi = (1 / (len(Xi))) * Mi
    Mi2 = (1 / (len(Xi))) * Mi2

    Mik = 0
    Mik2 = 0
    for i in range(len(Xik)):
        Mik += Xik[i]
        Mik2 += Xik[i]**2
    Mik = (1 / (len(Xik))) * Mik
    Mik2 = (1 / (len(Xik))) * Mik2

    Di = Mi2 - (Mi)**2
    Dik = Mik2 - (Mik) ** 2

    M = 0
    for i in range(len(Xi)):
        M += (Xi[i] - Mi)*(Xik[i] - Mik)
    M = (1 / (len(Xik))) * M

    Rk = M/((Di*Dik)**(1/2))

    if(abs(Rk) <= (1/(N-1))+(2/(N-2))*(((N*(N-3))/(N+1))**(1/2))):
        m = "Статистическая связь в пределах нормы"
    else: m = "Наблюдается высокая статистическая связь"

    l2.config(text=m + "\nКоэффициент корреляции двух последовательностей: " + str(Rk))

    with open("C:/Users/Airat/Desktop/lab2_info.txt", 'a', encoding='utf-8') as file:
        file.write('\n\n' + "Корреляционный тест:\nРазница между последовательностями:%s\n" %k
                   + "Коэффициент корреляции двух последовательностей: " + str(Rk) + '\n'+ m)


def crypt():
    global Registers_num, OutputKey, N, TestMessage
    file_name = chooseFile()
    tmp, file_extension = os.path.splitext(file_name)

    OpenMessage = []
    with open(file_name, 'rb') as file:
        OpenMessage = file.read()
        file.close()
    TestMessage = OpenMessage

    if (file_extension == ".jpg"):
        with open("C:/Users/Airat/Desktop/lab2_CryptImage" + file_extension, 'wb') as file:
            N = (len(OpenMessage) - 700)*8
            MGenerate()
            a = []
            for i in range(0, len(OutputKey), 8):
                a.append(''.join(str(OutputKey[i + j]) for j in range(8)))
            for i in range(0, len(OpenMessage)):
                if (i > 700):
                    d = OpenMessage[i] ^ int(a[i - 700], 2)
                    file.write(d.to_bytes(1, "big"))
                else:
                    file.write(OpenMessage[i].to_bytes(1, "big"))
        file.close()

    if (file_extension == ".png"):
        with open("C:/Users/Airat/Desktop/lab2_CryptImage" + file_extension, 'wb') as file:
            N = (len(OpenMessage) - 700)*8
            MGenerate()
            a = []
            for i in range(0, len(OutputKey), 8):
                a.append(''.join(str(OutputKey[i + j]) for j in range(8)))
            for i in range(0, len(OpenMessage)):
                if (i > 700):
                    d = OpenMessage[i] ^ int(a[i - 700], 2)
                    file.write(d.to_bytes(1, "big"))
                else:
                    file.write(OpenMessage[i].to_bytes(1, "big"))
        file.close()

    if ((file_extension == ".mp3") | (file_extension == ".m4a")):
        with open("C:/Users/Airat/Desktop/lab2_CryptSound" + file_extension, 'wb') as file:
            N = (len(OpenMessage) - 64000)
            MGenerate()
            a = []
            #for i in range(0, len(OutputKey), 8):
            #    a.append(''.join(str(OutputKey[i + j]) for j in range(8)))
            for i in range(len(OpenMessage)):
                if (i > 64000):
                    d = OpenMessage[i] ^ OutputKey[i-64000] #int(a[i - 64000], 2)
                    file.write(d.to_bytes(1, "big"))
                else:
                    file.write(OpenMessage[i].to_bytes(1, "big"))
        file.close()

    if (file_extension == ".txt"):
        with open("C:/Users/Airat/Desktop/lab2_CryptText" + file_extension, 'wb') as file:
            N = len(OpenMessage) * 8
            MGenerate()
            a = []
            for i in range(0, len(OutputKey), 8):
                a.append(''.join(str(OutputKey[i+j]) for j in range(8)))
            for i in range(len(OpenMessage)):
                d = OpenMessage[i] ^ int(a[i], 2)
                file.write(d.to_bytes(1,"big"))
        file.close()

    if ((file_extension != ".txt") & (file_extension != ".mp3") & (file_extension != ".jpg")):
        with open("C:/Users/Airat/Desktop/lab2_CryptMessage" + file_extension, 'wb') as file:
            N = len(OpenMessage) * 8
            MGenerate()
            a = []
            for i in range(0, len(OutputKey), 8):
                a.append(''.join(str(OutputKey[i+j]) for j in range(8)))
            byte = []
            for i in range(len(OpenMessage)):
                d = OpenMessage[i] ^ int(a[i], 2)
                file.write(d.to_bytes(1,"big"))
        file.close()

    text1.delete(1.0, END)
    text2.delete(1.0, END)

    if(file_extension == ".txt"):
        message = []
        with open(file_name, 'r', encoding='utf-8') as file:
            message = file.read()
            text1.insert(1.0, "Открытый текст:\n" + ''.join(message))

        crypt_message = ''
        try:
            with open("C:/Users/Airat/Desktop/lab2_CryptText" + file_extension, 'r', encoding='ANSI') as file:
                crypt_message = file.read()
        except: crypt_message = "Ошибка при попытке чтения файла!"
        text2.insert(1.0, "Зашифрованный текст:\n" + ''.join(crypt_message))


def decrypt():
    global Registers_num, OutputKey, N, TestMessage

    file_name = chooseFile()
    tmp, file_extension = os.path.splitext(file_name)

    CryptMessage = []
    with open(file_name, 'rb') as file:
        CryptMessage = file.read()
        file.close()
    TestMessage = CryptMessage

    if (file_extension == ".jpg"):
        with open("C:/Users/Airat/Desktop/lab2_DeCryptImage" + file_extension, 'wb') as file:
            N = (len(CryptMessage) - 700)*8
            MGenerate()
            a = []
            for i in range(0, len(OutputKey), 8):
                a.append(''.join(str(OutputKey[i + j]) for j in range(8)))
            for i in range(len(CryptMessage)):
                if (i > 700):
                    d = CryptMessage[i] ^ int(a[i - 700], 2)
                    file.write(d.to_bytes(1, "big"))
                else:
                    file.write(CryptMessage[i].to_bytes(1, "big"))
        file.close()

    if (file_extension == ".png"):
        with open("C:/Users/Airat/Desktop/lab2_CryptImage" + file_extension, 'wb') as file:
            N = (len(CryptMessage) - 700)*8
            MGenerate()
            a = []
            for i in range(0, len(OutputKey), 8):
                a.append(''.join(str(OutputKey[i + j]) for j in range(8)))
            for i in range(0, len(CryptMessage)):
                if (i > 700):
                    d = CryptMessage[i] ^ int(a[i - 700], 2)
                    file.write(d.to_bytes(1, "big"))
                else:
                    file.write(CryptMessage[i].to_bytes(1, "big"))
        file.close()

    if ((file_extension == ".mp3") | (file_extension == ".m4a")):
        with open("C:/Users/Airat/Desktop/lab2_DeCryptSound" + file_extension, 'wb') as file:
            N = (len(CryptMessage) - 64000)*8
            MGenerate()
            a = []
            #for i in range(0, len(OutputKey), 8):
            #    a.append(''.join(str(OutputKey[i + j]) for j in range(8)))
            for i in range(len(CryptMessage)):
                if (i > 64000):
                    d = CryptMessage[i] ^ OutputKey[i - 64000] #int(a[i - 64000], 2)
                    file.write(d.to_bytes(1, "big"))
                else:
                    file.write(CryptMessage[i].to_bytes(1, "big"))
        file.close()

    if (file_extension == ".txt"):
        with open("C:/Users/Airat/Desktop/lab2_DeCryptText" + file_extension, 'wb') as file:
            N = len(CryptMessage)*8
            MGenerate()
            a = []
            for i in range(0, len(OutputKey), 8):
                a.append(''.join(str(OutputKey[i + j]) for j in range(0, 8)))
            byte = []
            for i in range(len(CryptMessage)):
                d = CryptMessage[i] ^ int(a[i], 2)
                file.write(d.to_bytes(1, "big"))
        file.close()

    if ((file_extension != ".txt") & (file_extension != ".mp3") & (file_extension != ".jpg")):
        with open("C:/Users/Airat/Desktop/lab2_DeCryptMessage" + file_extension, 'wb') as file:
            N = len(CryptMessage) * 8
            MGenerate()
            a = []
            for i in range(0, len(OutputKey), 8):
                a.append(''.join(str(OutputKey[i+j]) for j in range(8)))
            for i in range(len(CryptMessage)):
                d = CryptMessage[i] ^ int(a[i], 2)
                file.write(d.to_bytes(1,"big"))
        file.close()

    text1.delete(1.0, END)
    text2.delete(1.0, END)

    if (file_extension == ".txt"):
        crypt_message = ''
        try:
            with open(file_name, 'r', encoding='ANSI') as file:
                crypt_message = file.read()
        except: crypt_message = "Ошибка при попытке чтения файла!"
    text1.insert(1.0, "Зашифрованный текст:\n" + ''.join(crypt_message))

    decrypt_message = []
    with open("C:/Users/Airat/Desktop/lab2_DeCryptText" + file_extension, 'r', encoding='utf-8') as file:
        decrypt_message = file.read()
    text2.insert(1.0, "Расшифрованный текст:\n" + ''.join(decrypt_message))


matplotlib.use('TkAgg')
root = Tk()
root.title("Поточный шифр")
root.geometry("990x500")
root.resizable(False, False)

canvas = Canvas(width=990, height=600, bg="#385773")\
    .place(x=-2,y=-2)

text1 = Text(width=60, height=20, bg="#A9C6D9", fg='#1C1C1C', wrap=WORD)
text1.place(x=4, y=4)
text2 = Text(width=60, height=20,bg="#A9C6D9", fg='#1C1C1C', wrap=WORD)
text2.place(x=500, y=4)

button1 = Button(root, width=25, height=2, text="Зашифровать файл", bg="#35648C", fg='#F2F2F0', command=crypt)\
    .place(x=304, y=340)
button2 = Button(root, width=25, height=2, text="Расшифровать файл", bg="#35648C", fg='#F2F2F0', command=decrypt)\
    .place(x=500, y=340)
button3 = Button(root, width=25, height=2, text="Сериальный тест", bg="#35648C", fg='#F2F2F0', command=serialTest)\
    .place(x=304, y=400)
button4 = Button(root, width=25, height=2, text="Корреляционный тест", bg="#35648C", fg='#F2F2F0', command=correlationTest)\
    .place(x=500, y=400)

var = BooleanVar()
var.set(0)
r1 = Radiobutton(root, text='Сгенерировать ключ', width=20, height=2,
                 value = 0, variable = var, bg="#6387A6").place(x=800, y=340)
r2 = Radiobutton(root, text='Загрузить ключ из файла', width=20, height=2,
                 value = 1, variable = var, bg="#6387A6").place(x=800, y=400)

l1 = Label(root, justify=RIGHT, text="", bg="#385773", fg='#F2F2F0')
l1.place(x=260, y=445)
l2 = Label(root, justify=LEFT, text="", bg="#385773", fg='#F2F2F0')
l2.place(x=500, y=445)

root.mainloop()
