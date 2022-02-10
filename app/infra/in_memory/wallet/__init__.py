import datetime
from dataclasses import dataclass

from sqlalchemy import Column, Date, Float, Integer, MetaData, String, Table
from sqlalchemy.engine.mock import MockConnection


@dataclass
class WalletInMemoryIn:
    api_key: str
    create_date_utc: datetime.datetime
    public_key: str
    btc_amount: float


@dataclass
class WalletInMemoryOut:
    api_key: str
    create_date_utc: datetime.datetime
    public_key: str
    btc_amount: float


@dataclass
class WalletInMemoryRepository:
    TABLE_NAME: str = "Wallet"

    # TODO add foreign key logic
    def get_table(self, metadata: MetaData) -> Table:
        return Table(
            self.TABLE_NAME,
            metadata,
            Column("Id", Integer, primary_key=True, nullable=False, autoincrement=True),
            Column("public_key", String, nullable=False),
            Column("btc_amount", Float, nullable=False),
            Column("create_date_utc", Date, nullable=False),
            Column("Api_key", String, nullable=False),
        )

    def create_table(self, engine: MockConnection) -> None:
        if not engine.dialect.has_table(engine.connect(), self.TABLE_NAME):
            metadata = MetaData(engine)
            self.get_table(metadata)
            metadata.create_all(engine)

    def add_wallet(
        self, engine: MockConnection, wallet: WalletInMemoryIn
    ) -> WalletInMemoryIn:
        metadata = MetaData(engine)
        tbl = self.get_table(metadata)
        ins = tbl.insert().values(
            Api_key=wallet.api_key,
            create_date_utc=wallet.create_date_utc,
            public_key=wallet.public_key,
            btc_amount=wallet.btc_amount,
        )
        con = engine.connect()
        con.execute(ins)
        return wallet

    def remove_wallet(
        self, engine: MockConnection, api_key: str
    ) -> None:
        metadata = MetaData(engine)
        tbl = self.get_table(metadata)
        ins = tbl.delete().where(tbl.c.Api_key == api_key)
        con = engine.connect()
        con.execute(ins)
        return
