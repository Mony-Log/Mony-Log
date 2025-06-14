from dataclasses import dataclass
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

import sqlalchemy as sa

from monylog.backend.expense.entities.expense import Expense, ExpenseTag
from monylog.backend.expense.entities.log import ExpenseLog
from monylog.shared_kernel.infra.database.sqla.mixin import SyncSqlaMixIn
from monylog.shared_kernel.infra.fastapi.dtos.response import PaginationList

from .dtos.request import CreateExpenseRequest
from .services.calculrator import ExpenseGroupSumCalculator, ExpenseSumCalculator
from . import exceptions

if TYPE_CHECKING:
    from monylog.shared_kernel.infra.fastapi.dtos.request import Pageable

    from .dtos.request import ExpenseQeuryRequest


@dataclass
class ExpenseUseCase(SyncSqlaMixIn):
    def append_tag(self, name: str, color: str = "#00f0f0") -> ExpenseTag:
        with self.db.session() as session:
            stmt = sa.select(ExpenseTag).where(ExpenseTag.name == name)
            tag = session.execute(stmt).scalar()
            if tag:
                return tag
            tag = ExpenseTag.build(name=name, color=color)
            session.add(tag)
            session.commit()
        return tag

    def get_tags(self) -> list[ExpenseTag]:
        with self.db.session() as session:
            stmt = sa.select(ExpenseTag).order_by(ExpenseTag.created_at.desc())
            tags = session.execute(stmt).scalars().all()
        return tags

    def delete_tag(self, id: str | None, name: str | None) -> None:
        with self.db.session() as session:
            if id is not None:
                stmt = sa.delete(ExpenseTag).where(ExpenseTag.id == id)
            if name is not None:
                stmt = sa.delete(ExpenseTag).where(ExpenseTag.name == name)
            session.execute(stmt)
            session.commit()

    def update_tag(self, id: str, **kw) -> ExpenseTag:
        with self.db.session() as session:
            stmt = sa.update(ExpenseTag).where(ExpenseTag.id == id).values(**kw)
            session.execute(stmt)
            session.commit()
            tag = session.get(ExpenseTag, id)
        return tag

    def sum_expenses(self, start_date: str, end_date: str) -> Decimal:
        with self.db.session() as session:
            stmt = sa.select(Expense).where(Expense.date >= start_date, Expense.date <= end_date)
            expenses = session.execute(stmt).scalars().all()
        return Expense.calculate(ExpenseSumCalculator, expenses).total

    def group_sum_expenses(self, start_date: str, end_date: str) -> dict[str, Decimal]:
        with self.db.session() as session:
            stmt = sa.select(Expense).where(Expense.date >= start_date, Expense.date <= end_date)
            expenses = session.execute(stmt).scalars().all()
        return Expense.calculate(ExpenseGroupSumCalculator, expenses).groups

    def log_generate_expense_from_message(self, result):
        with self.db.session() as session:
            model = ExpenseLog(request_id=result.id, data=result.model_dump(mode="json"))
            session.add(model)
            session.commit()

    def create_expense(
        self,
        payload: CreateExpenseRequest,
    ):
        with self.db.session() as session:
            tags = self.get_tags()
            tags_dict = {tag.name: tag for tag in tags}
            models = []
            for expense in payload.expenses:
                model = Expense(
                    title=expense.title,
                    amount=expense.amount,
                    dt=expense.dt,
                    type=expense.type,
                    data={"request_id": payload.request_id},
                )
                tags = [tags_dict[tag] for tag in expense.tags if tag in tags_dict]
                model.tags.extend(tags)
                models.append(model)
            session.add_all(models)
            session.commit()

    def get_expenses(
        self,
        payload: "ExpenseQeuryRequest",
    ) -> list[Expense]:
        with self.db.session() as session:
            stmt = sa.select(Expense)
            stmt = stmt.offset(payload.offset).limit(payload.limit)
            if payload.start_date and payload.end_date:
                stmt = stmt.where(Expense.dt >= payload.start_date, Expense.dt <= payload.end_date)

            expenses = session.execute(stmt).scalars().all()
            total = session.execute(sa.select(sa.func.count()).select_from(stmt.cte())).scalar_one()
        return PaginationList.build(data=expenses, total=total)

    def get_expense_by_id(self, id: int) -> Optional[Expense]:
        with self.db.session() as session:
            stmt = sa.select(Expense).where(Expense.id == id)
            expense = session.execute(stmt).scalar_one_or_none()
        return expense

    def edit_expense_node(self, id: int, note: str) -> Expense:
        expense = self.get_expense_by_id(id)
        if expense is None:
            raise exceptions.ExpenseNotFoundException(f"Expense with id {id} not found.")
        with self.db.session() as session:
            expense.note = note
            session.merge(expense)
            session.commit()
        return expense
