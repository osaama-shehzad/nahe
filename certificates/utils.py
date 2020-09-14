# from .models import Fellow
from certificates.models import Fellow
import pandas as pd 

master = pd.read_excel (r"C:\Users\Administrator\OneDrive - Higher Education Commission\Applications\NFDP Successful Fellows (All Cohorts).xlsx")

for fellow in range (len(master)):
    name = master.iloc[fellow, master.columns.get_loc ("NAME OF IPFP FELLOW")]
    cnic = master.iloc[fellow, master.columns.get_loc ("CNIC")]
    program =  master.iloc[fellow, master.columns.get_loc ("NFDP Cohort Month")]
    new = Fellow (name=name, CNIC=cnic, program=program)
    new.save()


