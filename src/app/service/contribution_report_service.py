from datetime import date
from decimal import Decimal

from app.dao.contribution_report_dao import daoContributionReport
from app.schema.contribution_report_schema import ContributionReportRequestSchema
from database.db import async_db_session


class ContributionReportService:
    @staticmethod
    def _resolve_period(data: ContributionReportRequestSchema) -> tuple[int, int, date, date]:
        if data.year is not None and (data.fromYear is not None or data.toYear is not None):
            raise ValueError("Provide either year or from_year/to_year, not both")

        if data.year is not None:
            from_year = data.year
            to_year = data.year
        else:
            if data.fromYear is None or data.toYear is None:
                raise ValueError("Provide year or both from_year and to_year")
            from_year = data.fromYear
            to_year = data.toYear

        if from_year > to_year:
            raise ValueError("from_year cannot be greater than to_year")

        return from_year, to_year, date(from_year, 1, 1), date(to_year, 12, 31)

    @staticmethod
    def _format_date(value):
        return value.isoformat() if value else None

    @staticmethod
    def _money(value) -> str:
        return str(value if value is not None else Decimal("0.00"))

    def _build_family_contribution(self, row: dict) -> dict:
        source_name = row["family_house_name"]
        if row["family_head_name"]:
            source_name = f"{source_name} - {row['family_head_name']}"

        return {
            "id": row["id"],
            "source_type": "family",
            "source_id": row["family_id"],
            "source_name": source_name,
            "amount": self._money(row["amount"]),
            "date": self._format_date(row["date"]),
            "purpose": row["purpose"],
            "family": {
                "id": row["family_id"],
                "code": row["family_code"],
                "house_name": row["family_house_name"],
                "head_name": row["family_head_name"],
                "phone_number": row["family_phone_number"],
            },
            "community": {
                "id": row["community_id"],
                "code": row["community_code"],
                "name": row["community_name"],
            },
            "parish": {
                "id": row["parish_id"],
                "code": row["parish_code"],
                "name": row["parish_name"],
                "location": row["parish_location"],
                "vicar_name": row["parish_vicar_name"],
                "contact_number": row["parish_contact_number"],
            }
            if row["parish_id"]
            else None,
            "forane": {
                "id": row["forane_id"],
                "code": row["forane_code"],
                "name": row["forane_name"],
                "location": row["forane_location"],
                "vicar_name": row["forane_vicar_name"],
                "contact_number": row["forane_contact_number"],
            }
            if row["forane_id"]
            else None,
        }

    def _build_individual_contribution(self, row: dict) -> dict:
        return {
            "id": row["id"],
            "source_type": "individual",
            "source_id": row["individual_id"],
            "source_name": row["individual_name"],
            "amount": self._money(row["amount"]),
            "date": self._format_date(row["date"]),
            "purpose": row["purpose"],
            "individual": {
                "id": row["individual_id"],
                "code": row["individual_code"],
                "name": row["individual_name"],
                "phone_number": row["individual_phone_number"],
                "email": row["individual_email"],
                "address": row["individual_address"],
            },
        }

    def _build_institution_contribution(self, row: dict) -> dict:
        return {
            "id": row["id"],
            "source_type": "institution",
            "source_id": row["institution_id"],
            "source_name": row["institution_name"],
            "amount": self._money(row["amount"]),
            "date": self._format_date(row["date"]),
            "purpose": row["purpose"],
            "institution": {
                "id": row["institution_id"],
                "code": row["institution_code"],
                "name": row["institution_name"],
                "type": row["institution_type"],
                "address": row["institution_address"],
                "phone": row["institution_phone"],
                "email": row["institution_email"],
                "website": row["institution_website"],
                "head_name": row["institution_head_name"],
            },
        }

    def _build_entity(self, entity_type: str, entity: dict) -> dict:
        data = {
            "type": entity_type,
            "id": entity["id"],
            "code": entity["code"],
            "name": entity["name"],
        }

        if entity_type == "family":
            data.update(
                {
                    "house_name": entity["house_name"],
                    "head_name": entity["head_name"],
                    "phone_number": entity["phone_number"],
                    "community": {
                        "id": entity["community_id"],
                        "code": entity["community_code"],
                        "name": entity["community_name"],
                    },
                    "parish": {
                        "id": entity["parish_id"],
                        "code": entity["parish_code"],
                        "name": entity["parish_name"],
                        "location": entity["parish_location"],
                        "vicar_name": entity["parish_vicar_name"],
                    }
                    if entity["parish_id"]
                    else None,
                    "forane": {
                        "id": entity["forane_id"],
                        "code": entity["forane_code"],
                        "name": entity["forane_name"],
                        "location": entity["forane_location"],
                        "vicar_name": entity["forane_vicar_name"],
                    }
                    if entity["forane_id"]
                    else None,
                }
            )
        elif entity_type == "parish":
            data.update(
                {
                    "location": entity["location"],
                    "vicar_name": entity["vicar_name"],
                    "contact_number": entity["contact_number"],
                    "forane": {
                        "id": entity["forane_id"],
                        "code": entity["forane_code"],
                        "name": entity["forane_name"],
                        "location": entity["forane_location"],
                        "vicar_name": entity["forane_vicar_name"],
                    },
                }
            )
        elif entity_type == "forane":
            data.update(
                {
                    "location": entity["location"],
                    "vicar_name": entity["vicar_name"],
                    "contact_number": entity["contact_number"],
                }
            )
        elif entity_type == "individual":
            data.update(
                {
                    "phone_number": entity["phone_number"],
                    "email": entity["email"],
                    "address": entity["address"],
                }
            )
        else:
            data.update(
                {
                    "type_name": entity["type"],
                    "address": entity["address"],
                    "phone": entity["phone"],
                    "email": entity["email"],
                    "website": entity["website"],
                    "head_name": entity["head_name"],
                }
            )

        return data

    async def get_contribution_report(self, data: ContributionReportRequestSchema) -> dict:
        from_year, to_year, from_date, to_date = self._resolve_period(data)

        async with async_db_session() as db:
            entity = await daoContributionReport.get_entity(db, data.entityType, data.entityId)
            if not entity:
                raise ValueError(f"{data.entityType.capitalize()} not found")

            if data.entityType in {"family", "parish", "forane"}:
                rows = await daoContributionReport.get_family_contribution_rows(
                    db,
                    data.entityType,
                    data.entityId,
                    from_date,
                    to_date,
                )
                contributions = [self._build_family_contribution(row) for row in rows]
            elif data.entityType == "individual":
                rows = await daoContributionReport.get_individual_contribution_rows(
                    db,
                    data.entityId,
                    from_date,
                    to_date,
                )
                contributions = [self._build_individual_contribution(row) for row in rows]
            else:
                rows = await daoContributionReport.get_institution_contribution_rows(
                    db,
                    data.entityId,
                    from_date,
                    to_date,
                )
                contributions = [self._build_institution_contribution(row) for row in rows]

        total_amount = sum((row["amount"] or Decimal("0.00") for row in rows), Decimal("0.00"))

        return {
            "period": {
                "from_year": from_year,
                "to_year": to_year,
                "from_date": from_date.isoformat(),
                "to_date": to_date.isoformat(),
            },
            "entity": {
                **self._build_entity(data.entityType, entity),
            },
            "summary": {
                "total_amount": self._money(total_amount),
                "total_count": len(contributions),
            },
            "contributions": contributions,
        }


contributionreportservice = ContributionReportService()
