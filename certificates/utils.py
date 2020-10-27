from certificates.models import Fellow

import pandas as pd 

master = pd.read_excel (r"C:\Users\Administrator\OneDrive - Higher Education Commission\Applications\NFDP Successful Fellows (All Cohorts).xlsx")
master = master[master["NFDP Cohort Month"]=="September 2020 - October 2020"]
for fellow in range (len(master)):
    name = master.iloc[fellow, master.columns.get_loc ("NAME OF IPFP FELLOW")]
    cnic = master.iloc[fellow, master.columns.get_loc ("CNIC")]
    program =  master.iloc[fellow, master.columns.get_loc ("NFDP Cohort Month")]
    ID = master.iloc[fellow, master.columns.get_loc ("ID")]
    graduation = master.iloc[fellow, master.columns.get_loc ("Graduation Status")]
    new = Fellow (name=name, CNIC=cnic, program=program, ID=ID, graduation=graduation)
    new.save()






