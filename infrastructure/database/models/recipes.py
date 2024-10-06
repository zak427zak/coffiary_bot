from datetime import datetime
from typing import Optional

from sqlalchemy import String, Integer, DateTime, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimestampMixin, TableNameMixin


class Recipe(Base, TimestampMixin, TableNameMixin):
    """
    This class represents a recipe in the Coffiary application.

    Attributes:
        id (Mapped[int]): The unique identifier of the recipe.
        user_id (Mapped[int]): The ID of the user who created the recipe.
        name (Mapped[str]): The name of the recipe.
        photo_url (Mapped[Optional[str]]): The photo URL of the recipe.
        water_volume (Mapped[Optional[Numeric]]): The volume of water used.
        water_temperature (Mapped[Optional[Numeric]]): The temperature of water used.
        amount_of_coffee (Mapped[Optional[Numeric]]): The amount of coffee used.
        brew_time (Mapped[Optional[Numeric]]): The brewing time in seconds.
        grind_size (Mapped[Optional[Numeric]]): The grind size used.
        grade (Mapped[Optional[Numeric]]): The grade of the recipe.
        coffee_type (Mapped[Optional[str]]): The type of coffee used.
        description (Mapped[Optional[str]]): The description of the recipe.
        add_date (Mapped[Optional[datetime]]): The date the recipe was added.
        month_block (Mapped[Optional[str]]): The month block information.
        day_block (Mapped[Optional[str]]): The day block information.
    """

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, index=True)
    name: Mapped[str] = mapped_column(String(300))
    photo_url: Mapped[Optional[str]] = mapped_column(String(400))
    water_volume: Mapped[Optional[Numeric]] = mapped_column(Numeric(4, 0))
    water_temperature: Mapped[Optional[Numeric]] = mapped_column(Numeric(4, 1))
    amount_of_coffee: Mapped[Optional[Numeric]] = mapped_column(Numeric(4, 1))
    brew_time: Mapped[Optional[Numeric]] = mapped_column(Numeric(6, 0))
    grind_size: Mapped[Optional[Numeric]] = mapped_column(Numeric(2, 0))
    grade: Mapped[Optional[Numeric]] = mapped_column(Numeric(2, 0))
    coffee_type: Mapped[Optional[str]] = mapped_column(Text)
    description: Mapped[Optional[str]] = mapped_column(Text)
    add_date: Mapped[Optional[datetime]] = mapped_column(DateTime)
    month_block: Mapped[Optional[str]] = mapped_column(String(50))
    day_block: Mapped[Optional[str]] = mapped_column(String(50))

    def __repr__(self):
        return f"<Recipe {self.id} {self.name}>"

    def generate_stars(self):
        dic = {1: "1️⃣", 2: "2️⃣", 3: "3️⃣", 4: "4️⃣", 5: "5️⃣", 6: "6️⃣", 7: "7️⃣", 8: "8️⃣", 9: "9️⃣", 10: "🔟"}
        return dic[self.grade] if self.grade in dic else ""

    def to_dict(self, current_user):
        build_result = f"📖 {self.name}\n\n" \
                       f"<b>Объем воды:</b> {self.water_volume} мл.\n" \
                       f"<b>Кофе:</b> {self.amount_of_coffee} гр.\n" \
                       f"<b>Температура воды:</b> {self.water_temperature} °C\n" \
                       f"<b>Время заваривания:</b> {self.brew_time} сек.\n" \
                       f"<b>Размер помола:</b> {self.grind_size} щелчк.\n" \
                       f"<b>Что за кофе:</b> {self.coffee_type}\n\n" \
                       f"💬 <b>Впечатления:</b> {self.description}\n\n" \
                       f"⭐ <b>Оценка:</b> {self.generate_stars()} из 🔟"
        data = {'text': build_result, 'image': self.photo_url}
        return data