from flask import Flask, Blueprint, redirect, render_template, request
from models.transaction import Transaction
import repositories.transaction_repository as transaction_repository
import repositories.merchant_repository as merchant_repository
import repositories.tag_repository as tag_repository
import datetime

transactions_blueprint = Blueprint("transactions", __name__)

@transactions_blueprint.route("/transactions")
def transactions():
    transactions = transaction_repository.select_all()
    total = transaction_repository.total()
    return render_template("transactions/index.html", transactions=transactions, total=total)


@transactions_blueprint.route("/transactions/new")
def new_transaction():
    merchants = merchant_repository.select_all()
    tags = tag_repository.select_all()
    return render_template("transactions/new.html", merchants=merchants, tags=tags)


@transactions_blueprint.route("/transactions", methods=["POST"])
def create_transaction():
    amount = request.form["amount"]
    merchant_id = request.form["merchant_id"]
    tag_id = request.form["tag_id"]
    merchant = merchant_repository.select(merchant_id)
    tag = tag_repository.select(tag_id)
    new_transaction = Transaction(amount, merchant, tag)
    transaction_repository.save(new_transaction)
    return redirect("/transactions")