import csv


header = ["user_id", "company_id", "quizz_id", "created_at", "questions", "correct", "average_result"]

async def generate_csv(file_name, data):
    path = f"/usr/src/backend/app/files/{file_name}.csv"
    with open(path, 'w+') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([column for column in header])
        for record in data:
            writer.writerow([value for value in record.values()])
    return path