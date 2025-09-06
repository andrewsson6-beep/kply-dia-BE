
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, insert, select
from app.models.institution_model import Institution
from app.schema.institutions_schema import InstitutionsInfoSchemaBase
class InstitutionDAO:
    """Institutions database operation class"""

    def __init__(self, model):
        self.model = model
    
    async def institutions_list_query(self, db: AsyncSession) -> Institution:
       stmt = (select(self.model))
       result = await db.execute(stmt)
       return result.scalars().all()
    
    async def create_institution(self, db: AsyncSession, institution_data: InstitutionsInfoSchemaBase) -> Institution:
        # Get the highest unique number
        stmt_max = select(func.max(self.model.ins_unique_no))
        result = await db.execute(stmt_max)
        max_unique_no = result.scalar()

        # Start from 1001 if table is empty
        if not max_unique_no:
            new_unique_no = 1001
        else:
            new_unique_no = max_unique_no + 1

        # Generate institution code
        new_code = f"INS-{new_unique_no}"

        stmt = (
            insert(self.model)
            .values(
                ins_for_id=institution_data.insForId,
                ins_par_id=institution_data.insParId,
                ins_unique_no=new_unique_no,
                ins_code=new_code,
                ins_name=institution_data.insName,
                ins_type=institution_data.insType,
                ins_address=institution_data.insAddress,
                ins_phone=institution_data.insPhone,
                ins_email=institution_data.insEmail,
                ins_website=institution_data.insWebsite,
                ins_head_name=institution_data.insHeadName,
            )
            .returning(self.model)
        )
        result = await db.execute(stmt)
        await db.commit()
        return result.scalar_one()
    

dao_institutions:InstitutionDAO = InstitutionDAO(Institution)
