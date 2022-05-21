from enum import IntEnum
import numpy as np

class FilingStatus(IntEnum):
    SINGLE = 0
    MARRIED_JOINT = 1
    MARRIED_SEPARATE = 2
    HEAD_OF_HOUSEHOLD = 3

class TaxBracket():

    def __init__(self, lower_income, upper_income, 
                 year, tax_rate, filing_status, maximum_tax):
        self.lower_income = lower_income
        self.upper_income = upper_income
        self.year = year
        self.tax_rate = tax_rate
        self.filing_status = filing_status
        self.maximum_tax = maximum_tax

    @classmethod
    def default(cls):
        return TaxBracket(0, 0, 0, 0, FilingStatus.SINGLE, 0)

class TaxCalculator():

    tax_brackets = []

    def __init__(self, income, tax_brackets: list[TaxBracket]):
        self.income = income
        self.tax_brackets = tax_brackets

    def income_greater_than_tax_bracket(self, tax_bracket: TaxBracket):
        return self.income > tax_bracket.upper_income

    def get_maximum_tax(self, tax_bracket: TaxBracket):
        return tax_bracket.maximum_tax

    def calculate_bracket_tax(self, bracket: TaxBracket):
        if self.income > bracket.upper_income: 
            print(f'Income too high for this bracket. Income:{self.income}, Bracket Upper Income:{bracket.upper_income}')
            return 0
        
        # +1 since lower limit is inclusive.
        # e.g. $9951 lower income limit and $9951 income should result in $1 taxable income.
        taxable_income = self.income - bracket.lower_income + 1
        bracket_tax = taxable_income * bracket.tax_rate
        return bracket_tax
    
    def calculate_total_tax(self):
        total_tax = 0
        for tax_bracket in self.tax_brackets:
            tax = 0
            end_loop = False
            if(self.income_greater_than_tax_bracket(tax_bracket)):
                tax = self.get_maximum_tax(tax_bracket)
            else:
                tax = self.calculate_bracket_tax(tax_bracket)
                end_loop = True

            total_tax += tax
            if(end_loop):
                break

        #return int(round(total_tax))
        return total_tax

tax_bracket_a = TaxBracket(0, 9950, 2022, 0.10, FilingStatus.SINGLE, 300)

default_tax_bracket = TaxBracket.default()

brackets = [
    TaxBracket(1, 9950, 2021, 0.10, FilingStatus.SINGLE, 995),
    TaxBracket(9951, 40525, 2021, 0.12, FilingStatus.SINGLE, 3668.88),
    TaxBracket(40526, 86375, 2021, 0.22, FilingStatus.SINGLE, 10086.78),
    TaxBracket(86376, 164925, 2021, 0.24, FilingStatus.SINGLE, 18851.76),
    TaxBracket(164926, 209425, 2021, 0.32, FilingStatus.SINGLE, 14239.68),
    TaxBracket(209426, 523600, 2021, 0.35, FilingStatus.SINGLE, 109960.90),
    TaxBracket(523601, float('inf'), 2021, 0.37, FilingStatus.SINGLE, 0)
]

tax_calculator = TaxCalculator(0, brackets)

incomes = np.arange(80000,380001, 5000)

taxes_list = []

for income in incomes:
    tax_calculator.income = income
    taxes_list.append(tax_calculator.calculate_total_tax())

taxes = np.array(taxes_list)

print(incomes)
print(taxes)



print(tax_calculator.calculate_total_tax())
