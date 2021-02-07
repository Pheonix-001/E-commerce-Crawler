import csv

class DataWriter:

    file_name = ''
    rowtitle = []

    def __init__(self, file_name, rowtitle):
        self.file_name = file_name
        self.rowtitle = rowtitle
        

    def writer(self, data):
        f = self.file_name

        with open(f, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(self.rowtitle)
            writer.writerows(data)

