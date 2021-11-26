
### test for read encoded csv 

import csv
database = dict()
with open('1.csv', newline='') as csvfile:

    # 讀取csv檔案內容
    rows = csv.reader(csvfile)
    print(rows)

    # break out single row to database
    # and add correct piece of code according to repeat time. 
    for row in rows:
        for i in range(0, int(row[1])):
            qrcode = str(row[3])[0:-1] + str(i+1)
            dict = { qrcode : row[2] + '.wav' } # qrcode: sound_file pair
            database.update(dict)

### test print for database
# [print(data) for data in database]
        

# random test the key value pair
print(database['10453'])