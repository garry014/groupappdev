class CustRegister:
    def __init__(self, ccity, cemail, cpassword, cfname, clname, cnumber):
        self.__ccity =  ccity
        self.__cemail = cemail
        self.__cpassword = cpassword
        self.__cfname = cfname
        self.__clname = clname
        self.__cnumber = cnumber

    def get_ccity(self):
        return self.__ccity
    def set_ccity(self, ccity):
        self.__ccity = ccity

    def get_cemail(self):
        return self.__cemail
    def set_cemail(self, cemail):
        self.__cemail = cemail

    def get_cpassword(self):
        return self.__cpassword
    def set_cpassword(self, cpassword):
        self.__cpassword = cpassword

    def get_cfname(self):
        return self.__cfname
    def set_cfname(self, cfname):
        self.__cfname = cfname

    def get_clname(self):
        return self.__clname
    def set_clname(self, clname):
        self.__clname = clname

    def get_cnumber(self):
        return self.__cnumber
    def set_cnumber(self, cnumber):
        self.__cnumber = cnumber

    def __str__(self):
        s = 'city: {}, email: {}, password: {}, fname: {}'.format(self.__ccity, self.__cemail, self.__cpassword,
                                                                 self.__cfname, self.__clname, self.__cnumber )
        return s

