import json

def return_book(member_id, book_id):
    
    with open("data.json", "r") as file:
     loaded_data = json.load(file)

    for loan in loaded_data["loans"]:
        if loan["book_isbn"] == book_id and loan["member_id"] == member_id:
            
            loaded_data["loans"].remove(loan)

            with open("data.json", "w") as file:
                json.dump(loaded_data, file, indent=4)
            
            return loaded_data
    
    loaded_data = {"Error": "Loan does not exist"}
    return loaded_data
    