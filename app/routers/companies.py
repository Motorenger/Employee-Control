from fastapi import APIRouter, Depends

from databases import Database

from schemas.company_schemas import Company, CompanyBase
from schemas.user_schemas import User
from utils.auth import CurrentUser
from services.logic import CompanyService
from db.database import get_db


router = APIRouter(
    prefix="/companies",
    tags=["companies"]
)


@router.post("/create", response_model=Company)
async def companies_list(company: CompanyBase,
                         current_user: User = Depends(CurrentUser),
                         db: Database = Depends(get_db)
                        ) -> Company:
    company_service = CompanyService(db=db)
    current_user = await current_user.user()

    company = await company_service.create_company(company=company, user=current_user)
    return company
