import argparse
import asyncio
from decimal import Decimal

from sqlalchemy import func, or_, select

from app.models.community_model import Community
from app.models.family_model import Family
from app.models.familycontribution_model import FamilyContribution
from app.models.forane_model import Forane
from app.models.individual_model import Individual
from app.models.individualcontribution_model import IndividualContribution
from app.models.institution_model import Institution
from app.models.institutioncontribution_model import InstitutionContribution
from app.models.parish_model import Parish
from database.db import async_db_session


ZERO = Decimal("0.00")


def money(value):
    return value if value is not None else ZERO


def print_mismatches(title, rows, limit):
    mismatches = [row for row in rows if money(row.stored_total) != money(row.actual_total)]
    print(f"\n{title}")
    print(f"checked={len(rows)} mismatches={len(mismatches)}")
    for row in mismatches[:limit]:
        diff = money(row.stored_total) - money(row.actual_total)
        print(
            f"id={row.id} code={row.code} name={row.name!r} "
            f"stored={money(row.stored_total)} actual={money(row.actual_total)} "
            f"diff={diff} count={row.contribution_count}"
        )


async def audit_parishes(db, target_id=None):
    stmt = (
        select(
            Parish.par_id.label("id"),
            Parish.par_code.label("code"),
            Parish.par_name.label("name"),
            Parish.par_total_contribution_amount.label("stored_total"),
            func.coalesce(func.sum(FamilyContribution.fcon_amount), 0).label("actual_total"),
            func.count(FamilyContribution.fcon_id).label("contribution_count"),
        )
        .select_from(Parish)
        .outerjoin(Community, Community.com_par_id == Parish.par_id)
        .outerjoin(Family, Family.fam_com_id == Community.com_id)
        .outerjoin(
            FamilyContribution,
            (FamilyContribution.fcon_fam_id == Family.fam_id)
            & (FamilyContribution.fcon_is_deleted == False),
        )
        .where(
            Parish.par_is_deleted == False,
            or_(Community.com_id.is_(None), Community.com_is_deleted == False),
            or_(Family.fam_id.is_(None), Family.fam_is_deleted == False),
        )
        .group_by(Parish.par_id)
        .order_by(Parish.par_id)
    )
    if target_id:
        stmt = stmt.where(Parish.par_id == target_id)
    result = await db.execute(stmt)
    return result.all()


async def audit_foranes(db, target_id=None):
    stmt = (
        select(
            Forane.for_id.label("id"),
            Forane.for_code.label("code"),
            Forane.for_name.label("name"),
            Forane.for_total_contribution_amount.label("stored_total"),
            func.coalesce(func.sum(FamilyContribution.fcon_amount), 0).label("actual_total"),
            func.count(FamilyContribution.fcon_id).label("contribution_count"),
        )
        .select_from(Forane)
        .outerjoin(
            Parish,
            (Parish.par_for_id == Forane.for_id) & (Parish.par_is_deleted == False),
        )
        .outerjoin(
            Community,
            (
                ((Community.com_par_id == Parish.par_id) | (Community.com_for_id == Forane.for_id))
                & (Community.com_is_deleted == False)
            ),
        )
        .outerjoin(
            Family,
            (Family.fam_com_id == Community.com_id) & (Family.fam_is_deleted == False),
        )
        .outerjoin(
            FamilyContribution,
            (FamilyContribution.fcon_fam_id == Family.fam_id)
            & (FamilyContribution.fcon_is_deleted == False),
        )
        .where(Forane.for_is_deleted == False)
        .group_by(Forane.for_id)
        .order_by(Forane.for_id)
    )
    if target_id:
        stmt = stmt.where(Forane.for_id == target_id)
    result = await db.execute(stmt)
    return result.all()


async def audit_families(db, target_id=None):
    stmt = (
        select(
            Family.fam_id.label("id"),
            Family.fam_code.label("code"),
            Family.fam_house_name.label("name"),
            Family.fam_total_contribution_amount.label("stored_total"),
            func.coalesce(func.sum(FamilyContribution.fcon_amount), 0).label("actual_total"),
            func.count(FamilyContribution.fcon_id).label("contribution_count"),
        )
        .select_from(Family)
        .outerjoin(
            FamilyContribution,
            (FamilyContribution.fcon_fam_id == Family.fam_id)
            & (FamilyContribution.fcon_is_deleted == False),
        )
        .where(Family.fam_is_deleted == False)
        .group_by(Family.fam_id)
        .order_by(Family.fam_id)
    )
    if target_id:
        stmt = stmt.where(Family.fam_id == target_id)
    result = await db.execute(stmt)
    return result.all()


async def audit_individuals(db, target_id=None):
    stmt = (
        select(
            Individual.ind_id.label("id"),
            Individual.ind_code.label("code"),
            Individual.ind_full_name.label("name"),
            Individual.ind_total_contribution_amount.label("stored_total"),
            func.coalesce(func.sum(IndividualContribution.icon_amount), 0).label("actual_total"),
            func.count(IndividualContribution.icon_id).label("contribution_count"),
        )
        .select_from(Individual)
        .outerjoin(
            IndividualContribution,
            (IndividualContribution.icon_ind_id == Individual.ind_id)
            & (IndividualContribution.icon_is_deleted == False),
        )
        .where(Individual.ind_is_deleted == False)
        .group_by(Individual.ind_id)
        .order_by(Individual.ind_id)
    )
    if target_id:
        stmt = stmt.where(Individual.ind_id == target_id)
    result = await db.execute(stmt)
    return result.all()


async def audit_institutions(db, target_id=None):
    stmt = (
        select(
            Institution.ins_id.label("id"),
            Institution.ins_code.label("code"),
            Institution.ins_name.label("name"),
            Institution.ins_total_contribution_amount.label("stored_total"),
            func.coalesce(func.sum(InstitutionContribution.incon_amount), 0).label("actual_total"),
            func.count(InstitutionContribution.incon_id).label("contribution_count"),
        )
        .select_from(Institution)
        .outerjoin(
            InstitutionContribution,
            (InstitutionContribution.incon_ins_id == Institution.ins_id)
            & (InstitutionContribution.incon_is_deleted == False),
        )
        .where(Institution.ins_is_deleted == False)
        .group_by(Institution.ins_id)
        .order_by(Institution.ins_id)
    )
    if target_id:
        stmt = stmt.where(Institution.ins_id == target_id)
    result = await db.execute(stmt)
    return result.all()


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--entity", choices=["family", "parish", "forane", "individual", "institution"])
    parser.add_argument("--id", type=int)
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()

    async with async_db_session() as db:
        audits = {
            "family": ("Families", audit_families),
            "parish": ("Parishes", audit_parishes),
            "forane": ("Foranes", audit_foranes),
            "individual": ("Individuals", audit_individuals),
            "institution": ("Institutions", audit_institutions),
        }
        selected = {args.entity: audits[args.entity]} if args.entity else audits
        for entity, (title, audit_fn) in selected.items():
            rows = await audit_fn(db, args.id if args.entity == entity else None)
            print_mismatches(title, rows, args.limit)


if __name__ == "__main__":
    asyncio.run(main())
