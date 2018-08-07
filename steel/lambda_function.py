import json
import xlrd
import boto3

print("Lambda function started")

xls_name = 'ISO10383_MIC.xls'	# Excel file name
sheet_name = 'MICs List by CC'	# Sheet name whose data needs to be converted

def lambda_handler(event, context):
    # TODO implement
    s3 = boto3.resource('s3')	# calling S3 service
    s3.Bucket('sourceexceldata').download_file(xls_name, '/tmp/' + xls_name)	# download the file from S3 bucket and storing in /tmp folder

    workbook = xlrd.open_workbook('/tmp/ISO10383_MIC.xls')	# opening the xls file
    worksheet = workbook.sheet_by_name(sheet_name)			# opening the particular sheet

    data = []
    keys = [v.value for v in worksheet.row(0)]		# getting all column first row as keys
    for row_number in range(worksheet.nrows):
        if row_number == 0:
            continue
        row_data = {}
        for col_number, cell in enumerate(worksheet.row(row_number)):
            row_data[keys[col_number]] = cell.value
        data.append(row_data)

	# dumping data in json file
    with open('/tmp/steeleye.json', 'w') as json_file:
        json_file.write(json.dumps(data))

	# reading the json data
    with open('/tmp/steeleye.json') as f:
        string = f.read()
	
	# encoding the data in proper string
    encoded_string = string.encode("utf-8")
	
	# uploading data in S3 bucket
    s3.Bucket('sourceexceldata').put_object(Key='steeleye.json', Body=encoded_string, ACL='public-read')

    print("Success")
    return ''
