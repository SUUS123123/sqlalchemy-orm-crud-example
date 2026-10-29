"""Small SQLAlchemy 2.x ORM example with CRUD operations and a repository."""

from decimal import Decimal

from sqlalchemy import Numeric, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    def __repr__(self) -> str:
        return f"Product(id={self.id}, name={self.name!r}, price={self.price})"


class ProductRepository:
    """Keeps database operations for Product in one place."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, name: str, price: Decimal) -> Product:
        product = Product(name=name, price=price)
        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)
        return product

    def get_by_id(self, product_id: int) -> Product | None:
        return self.session.get(Product, product_id)

    def get_all(self) -> list[Product]:
        statement = select(Product).order_by(Product.id)
        return list(self.session.scalars(statement))

    def update(
        self,
        product_id: int,
        *,
        name: str | None = None,
        price: Decimal | None = None,
    ) -> Product | None:
        product = self.get_by_id(product_id)
        if product is None:
            return None

        if name is not None:
            product.name = name
        if price is not None:
            product.price = price

        self.session.commit()
        self.session.refresh(product)
        return product

    def delete(self, product_id: int) -> bool:
        product = self.get_by_id(product_id)
        if product is None:
            return False

        self.session.delete(product)
        self.session.commit()
        return True


def main() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        products = ProductRepository(session)

        created = products.create("Laptop", Decimal("79990.00"))
        print("CREATE:", created)

        print("READ:", products.get_by_id(created.id))
        print("LIST:", products.get_all())

        updated = products.update(created.id, price=Decimal("74990.00"))
        print("UPDATE:", updated)

        print("DELETE:", products.delete(created.id))
        print("LIST AFTER DELETE:", products.get_all())


if __name__ == "__main__":
    main()
