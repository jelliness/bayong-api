from datetime import date

from sqlalchemy import Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class ProductImage(Base):
    __tablename__ = "product_images"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    image_url: Mapped[str] = mapped_column(nullable=False)
    uploaded_by: Mapped[str] = mapped_column(nullable=False)
    date_added: Mapped[date] = mapped_column(Date, nullable=False)

    product: Mapped["Product"] = relationship(back_populates="images")
