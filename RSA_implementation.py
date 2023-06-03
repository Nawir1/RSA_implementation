#############################################################
#GUI MODEL FOR THE RSA PROGRAM################################
#############################################################

import tkinter
import tkinter.messagebox
import customtkinter
from customtkinter import END
import random
import sys
import time
import hashlib


class APP(customtkinter.CTk):
    def __init__(self):
        self.selection = None
        self.message = None
        self.public_key = None
        self.private_key = None
        super().__init__()

        ########################
        #Configuring the window#
        ########################
        self.title('Implementing RSA using Python')
        self.geometry(f'{1100}x{580}')


        ########################
        #Cofiguring grid layout#
        ########################
        self.grid_columnconfigure(1, weight = 1)
        self.grid_columnconfigure((2, 3), weight = 0)
        self.grid_rowconfigure((0, 1, 2), weight = 1)

        #########################
        #Sidebar#################
        ##########################

        self.sidebar_frame = customtkinter.CTkFrame(self, width = 140, height = 100, corner_radius = 0)
        self.sidebar_frame.grid(row = 0, column = 0, rowspan = 4, sticky = "nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight = 1)
        self.label = customtkinter.CTkLabel(self.sidebar_frame, text = "Hello Bob Welcome!!\nThis is a program that implements RSA\nencryption/decryption using Python", font = customtkinter.CTkFont(size = 15))
        self.label.grid(row = 0, column = 0, padx = 20, pady = 10)

        ########################
        ## Text Box#############
        ########################
        self.textbox = customtkinter.CTkTextbox(self, width = 500, fg_color = "#B0CFDE" , text_color = "#00008B")
        self.textbox.grid(row = 0, column = 1, rowspan = 4, sticky = "nsew", padx = (20, 0), pady = (20, 0))

        ########################
        # Input dialog##########
        ########################
        self.selection_button = customtkinter.CTkButton(self.sidebar_frame, text = "Click to Start", command = self.main, fg_color = "#F8F8FF", text_color="#5A5A5A")
        self.selection_button.grid(row = 1, column = 0, padx = 20, pady = (10, 10))
    def main(self):
        selection = customtkinter.CTkInputDialog(text = "Enter 1 for Encryption, 2 for Decryption::", title = "RSA Selection", fg_color="#77BFC7", button_fg_color="#5F9EA0")

        self.selection = selection.get_input()
        if int(self.selection) == 1:
            self.textbox.insert(END, f'*****************************************************************************************************************************\n')
            self.textbox.insert(END, f'*****************************************************************************************************************************\n')

            self.textbox.insert(END, "Performing Encryption\n")

            m = customtkinter.CTkInputDialog(text = 'Enter the Message to encrypt', title = 'Message Input', fg_color="#77BFC7", button_fg_color="#5F9EA0")

            self.message = m.get_input()

            self.textbox.insert(END, "You need the public key from the other Party\n")
            N = customtkinter.CTkInputDialog(text = 'Enter the N from the shared public key', title = 'Input n', fg_color="#77BFC7", button_fg_color="#5F9EA0")
            n = int(N.get_input())

            ee = customtkinter.CTkInputDialog(text = 'Enter the E from the shared public key', title = 'Input e', fg_color="#77BFC7", button_fg_color="#5F9EA0")

            e = int(ee.get_input())
            self.public_key = (n, e)
            
            encrypted, message_sign = self.encryption()

            self.textbox.insert(END, f"The Encrypted text is \n{encrypted}\nSignature is :: {message_sign}\n")


        elif int(self.selection) == 2:
            self.textbox.insert(END, f'\n###########################################################################################################################\n')
            self.textbox.insert(END, f'\n###########################################################################################################################\n')
            self.textbox.insert(END, "Performing PubKey Generation and/or Decryption\n")
            self.textbox.insert(END, "Generating prime Numbers\n")

            p, q = self.generate_keys()

            self.textbox.insert(END, f'Done!! \n')

            self.textbox.insert(END, f'Calculating N\n')
            n = p * q

            self.textbox.insert(END, f'Done\n')

            self.textbox.insert(END, "Calculating Carmichael\'s Totient\n")
            c_totient = self.lcm(p - 1, q - 1)
            self.textbox.insert(END, f'Done\n')

            self.textbox.insert(END, f'Calculating E\n')
            e = self.euler_totient(2, int(c_totient))
            self.textbox.insert(END, f'Done\n')

            self.textbox.insert(END, f'Calculating decryption key\n')
            __, d, _ = self.eea(e, c_totient)
            d = int((int(d) + c_totient) % c_totient)
            self.textbox.insert(END, f'Done\n')

#
            self.private_key = (d, n)
            self.textbox.insert(END, f'Your Public Key is \nN = {(n)}\nE = {(e)}\nPrimes are ::\np = {p}\nq = {q}\n')
            
            response = customtkinter.CTkInputDialog(text = "Do you wish to continue to message Decryption (Y = Yes): ?", title = "Decryption Dialog", fg_color="#77BFC7", button_fg_color="#5F9EA0")
            res = response.get_input()
            if res != 'Y':
                sys.exit(0)
            p_1 = customtkinter.CTkInputDialog(text = 'Enter prime p:: ', title = 'Prime p', fg_color="#77BFC7", button_fg_color="#5F9EA0")
            p_2 = int(p_1.get_input())
            q_1 = customtkinter.CTkInputDialog(text = 'Enter prime q:: ',  title = 'Prime q', fg_color="#77BFC7", button_fg_color="#5F9EA0")
            q_2 = int(q_1.get_input())
            assert type(p_2) == int and p_2 == p, self.textbox.insert("0.0", 'p must be an integer and same as system-generated value\n')
            assert type(q_2) == int and q_2 == q, self.textbox.insert("0.0", 'q must be an integer and same as system-genarated value\n')
            m = customtkinter.CTkInputDialog(text = 'Enter encrypted message: ', title = 'Encrypted text input', fg_color="#77BFC7", button_fg_color="#5F9EA0")
            self.message = m.get_input()
            s = customtkinter.CTkInputDialog(text = 'Enter its signature:', title = 'Message signature', fg_color="#77BFC7", button_fg_color="#5F9EA0")
            message_s = s.get_input()


            decrypted_text = self.decryption()
            self.textbox.insert(END, f'Your decrypted text is \n{self.decryption()}\nThe hash is {message_s == hashlib.sha256(decrypted_text.encode()).hexdigest()}\n')


        else:
            self.textbox.insert(END, f'NULL Value program will terminate in 10 seconds')
            time.sleep(10)
            sys.exit(0)

    #####################
    # Decryption Method##
    #####################
    def get_diff(self):
        """Generating p and q"""
        p = random.getrandbits(12)
        q = random.getrandbits(12)
        if p %2 == 0:
            p = p - 1
        if q % 2 == 0:
            q = q - 1
        p_len = len(str(p))
        q_len = len(str(q))
        if p_len > q_len:
            greater_len = p_len
        else:
            greater_len = q_len

        difflen = len(str(p - q))

        if difflen < 1:
            difflen *= 1
        while (difflen < greater_len):
            return self.get_diff()
        return p, q

    ########################
    #Euclidean##############
    ########################
    def euclidean(self, a, b):
        if a == 0:
            return b
        return self.euclidean(b%a, a)

    #######################
    #Extended Euclidean ###
    ########################
    def eea(self, a, b):

        if a == 0:
            return b, 0, 1
        euclidean_gcd, x, y = self.eea(b%a, a)
        x1 = y - (b // a) * x
        y1 = x
        return euclidean_gcd, x1, y1

    #########################
    ## Euler Totient ########
    #########################
    def euler_totient(self, rvalue, n):

        coprime = []
        for i in range(rvalue, n - 1):
            if self.euclidean(n, i) == 1:
                coprime.append(i)
        return coprime[-1]

    #############################
    #Miller Rabin################
    #############################
    def miller_rabin(self, p, base):
        k = 0
        m = p - 1
        while m % 2 == 0:
            k += 1
            m //= 2
        for i in range(base):
            a = random.randint(2, p - 2)
            x = pow(a, m, p)
            x = int(x)
            if (x == p - 1):
                return True
            while (m != p - 1):
                x = pow(x, 2, p)
                m *= 2
                if (x == p - 1):
                    return True
        return False

    ###########################
    #Generating primes#########
    ###########################
    def generate_keys(self):

        p_isprime = False
        q_isprime = False
        while (p_isprime and q_isprime) != True:
            p, q = self.get_diff()
            p_coprime = self.euler_totient(1, p)
            q_coprime = self.euler_totient(1, q)
            p_isprime = self.miller_rabin(p, p_coprime)
            q_isprime = self.miller_rabin(q, q_coprime)
        return p, q

    ##########################
    ## LCM ###################
    ##########################
    def lcm(self, a, b):
        return (abs(a * b) / self.euclidean(a, b))

    ##########################
    # ENCRYPTION #############
    ##########################
    def encryption(self):
        n, e = self.public_key
        encrypted = ''
        for literal in self.message:
            crypt = pow(ord(literal), e, n)
            encrypted += str(crypt)
            encrypted += '.'
        message_signature = hashlib.sha256(self.message.encode()).hexdigest()
        return encrypted, message_signature

    ########################
    ## DECRYPTION ##########
    ########################
    def decryption(self):
        d, n = self.private_key

        decrypted = ''
        val = ''
        for literal in self.message:
            if literal != '.':
                val += literal
            elif len(val) != 0:
                decrypt = chr(pow(int(val), d, n) % 128)
                decrypted += decrypt
                val = ''
        return decrypted







if __name__ == '__main__':
    app = APP()
    app.mainloop()
