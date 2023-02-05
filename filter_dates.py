import pandas as pd
from datetime import datetime, timedelta, date

endingYear = datetime.now().year
endingMonth = datetime.now().month
endingDay = datetime.now().day

sdate = date(2019, 1, 1)   
edate = date(endingYear,endingMonth,endingDay)

delta = edate - sdate 

dayList = []

for i in range(delta.days + 1):
    day = sdate + timedelta(days=i)
    dayString = str(day)
    dayList.append(dayString)

Filter_Dates = pd.DataFrame(dayList,columns=['Dates'])

print(Filter_Dates)