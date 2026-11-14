"""Transactional persistence adapters and deterministic demo fixtures."""
from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, Numeric, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import BuildRecord, BuildStage


class Base(DeclarativeBase):
    pass


class BuildRow(Base):
    __tablename__ = "research_builds"
    id: Mapped[str] = mapped_column(String(60), primary_key=True)
    machine_id: Mapped[str] = mapped_column(String(90), nullable=False)
    material: Mapped[str] = mapped_column(String(48), nullable=False)
    layer_count: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="queued")
    completed_layers: Mapped[int] = mapped_column(Integer, default=0)


class SensorRow(Base):
    __tablename__ = "research_sensor_samples"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    build_id: Mapped[str] = mapped_column(ForeignKey("research_builds.id"))
    layer: Mapped[int] = mapped_column(Integer)
    energy: Mapped[float] = mapped_column(Numeric(12, 5))


class BuildRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list(self) -> list[BuildRecord]:
        result = await self.session.execute(select(BuildRow).order_by(BuildRow.id))
        return [
            BuildRecord(
                id=row.id,
                machine_id=row.machine_id,
                material=row.material,
                layer_count=row.layer_count,
                status=BuildStage(row.status),
                completed_layers=row.completed_layers,
            )
            for row in result.scalars()
        ]

    async def upsert(self, build: BuildRecord) -> BuildRecord:
        entry = await self.session.get(BuildRow, build.id)
        if entry is None:
            entry = BuildRow(id=build.id)
            self.session.add(entry)
        entry.machine_id = build.machine_id
        entry.material = build.material
        entry.layer_count = build.layer_count
        entry.status = build.status.value
        entry.completed_layers = build.completed_layers
        await self.session.commit()
        return build


DEMO_BUILDS = [
    BuildRecord(
        id="DEMO-LPBF-0001", machine_id="LPBF-M01", material="Ti6Al4V",
        layer_count=2160, status=BuildStage.printing, completed_layers=1253,
    ),
    BuildRecord(
        id="DEMO-LPBF-0002", machine_id="LPBF-M02", material="Inconel718",
        layer_count=1850, status=BuildStage.inspection, completed_layers=1850,
    ),
]
