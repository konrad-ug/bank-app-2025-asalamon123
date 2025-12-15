from flask import Flask, request, jsonify
from src.account import Account
from src.account import AccountRegistry

app = Flask(__name__)
registry = AccountRegistry()

@app.route("/api/accounts", methods=['POST'])
def create_account():
    data = request.get_json()
    print(f"Create account request: {data}")

    if registry.exists(data["pesel"]):
        return jsonify({"message": "Account with given pesel already exists"}), 409

    account = Account(data["name"], data["surname"], data["pesel"], data.get("promo_code", None))
    registry.add_account(account)
    return jsonify({"message": "Account created"}), 201

@app.route("/api/accounts", methods=['GET'])
def get_all_accounts():
    print("Get all accounts request received")
    accounts = registry.return_all()
    accounts_data = [{"name": acc.first_name, "surname": acc.last_name, "pesel":
    acc.pesel, "balance": acc.balance, "promo_code": acc.promo_code} for acc in accounts]
    return jsonify(accounts_data), 200


@app.route("/api/accounts/count", methods=['GET'])
def get_account_count():
    count = registry.count_accounts()
    return jsonify({"count": count}), 200



@app.route("/api/accounts/<pesel>", methods=['GET'])
def get_account_by_pesel(pesel):
    acc = registry.search_by_pesel(pesel)
    if acc: 
        data = {"name": acc.first_name, "surname": acc.last_name, "pesel":
                acc.pesel, "balance": acc.balance, 
                "promo_code": acc.promo_code, "history": acc.history}
        
        return jsonify(data), 200
    else: 
        return jsonify({"error": "no account found"}), 404
    

@app.route("/api/accounts/<pesel>", methods=['PATCH'])
def update_account(pesel):
    acc = registry.search_by_pesel(pesel)
    if not acc:
        return jsonify({"message": "Account not found"}), 404

    data = request.get_json()
    if "name" in data:
        acc.first_name = data["name"]
    if "surname" in data:
        acc.last_name = data["surname"]
    if "promo_code" in data:
        acc.promo_code = data["promo_code"]

    return jsonify({"message": "Account updated"}), 200

@app.route("/api/accounts/<pesel>", methods=['DELETE'])
def delete_account(pesel):
    deleted = registry.delete_account(pesel)

    if not deleted:
        return jsonify({"error": "Account not found"}), 404

    return jsonify({"message": "Account deleted"}), 200

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)


@app.route("/api/accounts/<pesel>/transfer", methods=['POST'])
def transfer(pesel):
    account = registry.search_by_pesel(pesel)
    if not account: 
        return jsonify({"error": "Account not found"}), 404
    
    data = request.get_json()
    amount = data.get("amount")
    transfer_type = data.get("type")

    if transfer_type == "incoming":
        result = account.recieve_transfer(amount)

    elif transfer_type == "outgoing": 
        result = account.send_transfer(amount)
        if not result:
            return jsonify({"message": "not enough funds"}), 422
    
    elif transfer_type == "express":
        result = account.send_express_transfer(amount)
        if not result:
            return jsonify({"message": "not enough funds"}), 422
        
    else: 
        return jsonify({"message": "wrong transfer type"}), 400
    
    return jsonify({"message": "Zlecenie przyjęto do realizacji"}), 200