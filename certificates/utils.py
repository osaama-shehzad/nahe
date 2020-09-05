# from .models import Fellow
from certificates.models import Fellow
import pandas as pd 

master = pd.read_excel (r"C:\Users\Administrator\OneDrive - Higher Education Commission\Applications\Encryption Record-3.0.xlsx")
allowed = ["JUN-JUL20", "APR-MAY20"]

for fellow in range (len(master)):
    name = master.iloc[fellow, master.columns.get_loc ("NAME OF IPFP FELLOW")]
    cnic = master.iloc[fellow, master.columns.get_loc ("CNIC")]
    program =  master.iloc[fellow, master.columns.get_loc ("NFDP Cohort Month")]
    if program in allowed: 
        new = Fellow (name=name, CNIC=cnic, program=program)
        new.save()


