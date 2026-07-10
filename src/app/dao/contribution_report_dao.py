from datetime import date

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.community_model import Community
from app.models.family_model import Family
from app.models.familycontribution_model import FamilyContribution
from app.models.forane_model import Forane
from app.models.individual_model import Individual
from app.models.individualcontribution_model import IndividualContribution
from app.models.institution_model import Institution
from app.models.institutioncontribution_model import InstitutionContribution
from app.models.parish_model import Parish


class ContributionReportDAO:
    async def get_entity(self, db: AsyncSession, entity_type: str, entity_id: int):
        if entity_type == "family":
            stmt = (
                select(
                    Family.fam_id.label("id"),
                    Family.fam_code.label("code"),
                    Family.fam_house_name.label("name"),
                    Family.fam_house_name.label("house_name"),
                    Family.fam_head_name.label("head_name"),
                    Family.fam_phone_number.label("phone_number"),
                    Community.com_id.label("community_id"),
                    Community.com_code.label("community_code"),
                    Community.com_name.label("community_name"),
                    Parish.par_id.label("parish_id"),
                    Parish.par_code.label("parish_code"),
                    Parish.par_name.label("parish_name"),
                    Parish.par_location.label("parish_location"),
                    Parish.par_vicar_name.label("parish_vicar_name"),
                    Forane.for_id.label("forane_id"),
                    Forane.for_code.label("forane_code"),
                    Forane.for_name.label("forane_name"),
                    Forane.for_location.label("forane_location"),
                    Forane.for_vicar_name.label("forane_vicar_name"),
                )
                .join(Community, Community.com_id == Family.fam_com_id)
                .outerjoin(Parish, Parish.par_id == Community.com_par_id)
                .outerjoin(
                    Forane,
                    or_(
                        Forane.for_id == Community.com_for_id,
                        Forane.for_id == Parish.par_for_id,
                    ),
                )
                .where(
                    Family.fam_id == entity_id,
                    Family.fam_is_deleted == False,
                    Community.com_is_deleted == False,
                )
            )
        elif entity_type == "parish":
            stmt = (
                select(
                    Parish.par_id.label("id"),
                    Parish.par_code.label("code"),
                    Parish.par_name.label("name"),
                    Parish.par_location.label("location"),
                    Parish.par_vicar_name.label("vicar_name"),
                    Parish.par_contact_number.label("contact_number"),
                    Forane.for_id.label("forane_id"),
                    Forane.for_code.label("forane_code"),
                    Forane.for_name.label("forane_name"),
                    Forane.for_location.label("forane_location"),
                    Forane.for_vicar_name.label("forane_vicar_name"),
                )
                .join(Forane, Forane.for_id == Parish.par_for_id)
                .where(
                    Parish.par_id == entity_id,
                    Parish.par_is_deleted == False,
                    Forane.for_is_deleted == False,
                )
            )
        elif entity_type == "forane":
            stmt = (
                select(
                    Forane.for_id.label("id"),
                    Forane.for_code.label("code"),
                    Forane.for_name.label("name"),
                    Forane.for_location.label("location"),
                    Forane.for_vicar_name.label("vicar_name"),
                    Forane.for_contact_number.label("contact_number"),
                )
                .where(Forane.for_id == entity_id, Forane.for_is_deleted == False)
            )
        elif entity_type == "individual":
            stmt = (
                select(
                    Individual.ind_id.label("id"),
                    Individual.ind_code.label("code"),
                    Individual.ind_full_name.label("name"),
                    Individual.ind_phone_number.label("phone_number"),
                    Individual.ind_email.label("email"),
                    Individual.ind_address.label("address"),
                )
                .where(Individual.ind_id == entity_id, Individual.ind_is_deleted == False)
            )
        else:
            stmt = (
                select(
                    Institution.ins_id.label("id"),
                    Institution.ins_code.label("code"),
                    Institution.ins_name.label("name"),
                    Institution.ins_type.label("type"),
                    Institution.ins_address.label("address"),
                    Institution.ins_phone.label("phone"),
                    Institution.ins_email.label("email"),
                    Institution.ins_website.label("website"),
                    Institution.ins_head_name.label("head_name"),
                )
                .where(Institution.ins_id == entity_id, Institution.ins_is_deleted == False)
            )

        result = await db.execute(stmt)
        return result.mappings().one_or_none()

    async def get_family_contribution_rows(
        self,
        db: AsyncSession,
        entity_type: str,
        entity_id: int,
        from_date: date,
        to_date: date,
    ):
        stmt = (
            select(
                FamilyContribution.fcon_id.label("id"),
                FamilyContribution.fcon_amount.label("amount"),
                FamilyContribution.fcon_date.label("date"),
                FamilyContribution.fcon_purpose.label("purpose"),
                Family.fam_id.label("family_id"),
                Family.fam_code.label("family_code"),
                Family.fam_house_name.label("family_house_name"),
                Family.fam_head_name.label("family_head_name"),
                Family.fam_phone_number.label("family_phone_number"),
                Community.com_id.label("community_id"),
                Community.com_code.label("community_code"),
                Community.com_name.label("community_name"),
                Parish.par_id.label("parish_id"),
                Parish.par_code.label("parish_code"),
                Parish.par_name.label("parish_name"),
                Parish.par_location.label("parish_location"),
                Parish.par_vicar_name.label("parish_vicar_name"),
                Parish.par_contact_number.label("parish_contact_number"),
                Forane.for_id.label("forane_id"),
                Forane.for_code.label("forane_code"),
                Forane.for_name.label("forane_name"),
                Forane.for_location.label("forane_location"),
                Forane.for_vicar_name.label("forane_vicar_name"),
                Forane.for_contact_number.label("forane_contact_number"),
            )
            .join(Family, Family.fam_id == FamilyContribution.fcon_fam_id)
            .join(Community, Community.com_id == Family.fam_com_id)
            .outerjoin(Parish, Parish.par_id == Community.com_par_id)
            .outerjoin(
                Forane,
                or_(
                    Forane.for_id == Community.com_for_id,
                    Forane.for_id == Parish.par_for_id,
                ),
            )
            .where(
                FamilyContribution.fcon_is_deleted == False,
                Family.fam_is_deleted == False,
                Community.com_is_deleted == False,
                FamilyContribution.fcon_date >= from_date,
                FamilyContribution.fcon_date <= to_date,
            )
            .order_by(FamilyContribution.fcon_date, FamilyContribution.fcon_id)
        )

        if entity_type == "family":
            stmt = stmt.where(Family.fam_id == entity_id)
        elif entity_type == "parish":
            stmt = stmt.where(Community.com_par_id == entity_id, Parish.par_is_deleted == False)
        elif entity_type == "forane":
            stmt = stmt.where(
                Forane.for_id == entity_id,
                Forane.for_is_deleted == False,
                or_(Parish.par_id.is_(None), Parish.par_is_deleted == False),
            )

        result = await db.execute(stmt)
        return result.mappings().all()

    async def get_individual_contribution_rows(
        self,
        db: AsyncSession,
        individual_id: int,
        from_date: date,
        to_date: date,
    ):
        stmt = (
            select(
                IndividualContribution.icon_id.label("id"),
                IndividualContribution.icon_amount.label("amount"),
                IndividualContribution.icon_date.label("date"),
                IndividualContribution.icon_purpose.label("purpose"),
                Individual.ind_id.label("individual_id"),
                Individual.ind_code.label("individual_code"),
                Individual.ind_full_name.label("individual_name"),
                Individual.ind_phone_number.label("individual_phone_number"),
                Individual.ind_email.label("individual_email"),
                Individual.ind_address.label("individual_address"),
            )
            .join(Individual, Individual.ind_id == IndividualContribution.icon_ind_id)
            .where(
                IndividualContribution.icon_ind_id == individual_id,
                IndividualContribution.icon_is_deleted == False,
                Individual.ind_is_deleted == False,
                IndividualContribution.icon_date >= from_date,
                IndividualContribution.icon_date <= to_date,
            )
            .order_by(IndividualContribution.icon_date, IndividualContribution.icon_id)
        )
        result = await db.execute(stmt)
        return result.mappings().all()

    async def get_institution_contribution_rows(
        self,
        db: AsyncSession,
        institution_id: int,
        from_date: date,
        to_date: date,
    ):
        stmt = (
            select(
                InstitutionContribution.incon_id.label("id"),
                InstitutionContribution.incon_amount.label("amount"),
                InstitutionContribution.incon_date.label("date"),
                InstitutionContribution.incon_purpose.label("purpose"),
                Institution.ins_id.label("institution_id"),
                Institution.ins_code.label("institution_code"),
                Institution.ins_name.label("institution_name"),
                Institution.ins_type.label("institution_type"),
                Institution.ins_address.label("institution_address"),
                Institution.ins_phone.label("institution_phone"),
                Institution.ins_email.label("institution_email"),
                Institution.ins_website.label("institution_website"),
                Institution.ins_head_name.label("institution_head_name"),
            )
            .join(Institution, Institution.ins_id == InstitutionContribution.incon_ins_id)
            .where(
                InstitutionContribution.incon_ins_id == institution_id,
                InstitutionContribution.incon_is_deleted == False,
                Institution.ins_is_deleted == False,
                InstitutionContribution.incon_date >= from_date,
                InstitutionContribution.incon_date <= to_date,
            )
            .order_by(InstitutionContribution.incon_date, InstitutionContribution.incon_id)
        )
        result = await db.execute(stmt)
        return result.mappings().all()


daoContributionReport = ContributionReportDAO()
