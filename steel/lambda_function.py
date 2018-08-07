import json
import xlrd
import boto3

print("Test")

xls_name = 'ISO10383_MIC.xls'
sheet_name = 'MICs List by CC'


def lambda_handler(event, context):
    # TODO implement
    s3 = boto3.resource('s3')
    s3.Bucket('sourceexceldata').download_file(xls_name, '/tmp/' + xls_name)

    workbook = xlrd.open_workbook('/tmp/ISO10383_MIC.xls')
    worksheet = workbook.sheet_by_name(sheet_name)

    data = []
    keys = [v.value for v in worksheet.row(0)]
    for row_number in range(worksheet.nrows):
        if row_number == 0:
            continue
        row_data = {}
        for col_number, cell in enumerate(worksheet.row(row_number)):
            row_data[keys[col_number]] = cell.value
        data.append(row_data)

    with open('/tmp/steeleye.json', 'w') as json_file:
        json_file.write(json.dumps(data))

    with open('/tmp/steeleye.json') as f:
        string = f.read()

    encoded_string = string.encode("utf-8")
    s3.Bucket('sourceexceldata').put_object(Key='steeleye.json', Body=encoded_string, ACL='public-read')

    print("Success")
    return ''
