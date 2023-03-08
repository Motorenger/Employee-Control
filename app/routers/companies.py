from fastapi import APIRouter, Depends

from databases import Database

from fastapi_pagination import Page, Params, paginate

from schemas.company_schemas import Company, CompanyBase, CompanyUpdate
from schemas.user_schemas import User
from utils.auth import CurrentUser
from services.logic import CompanyService
from db.database import get_db


router = APIRouter(
    prefix="/companies",
    tags=["companies"]
)

@router.get("/", response_model=Page[Company])
async def companies_list(params: Params = Depends(), current_user: User = Depends(CurrentUser), db: Database = Depends(get_db)) -> Page:
    company_service = CompanyService(db=db, current_user= await current_user.user())

    companies = await company_service.get_companies()
    return paginate(companies.companies, params)


@router.get("/{company_id}", response_model=Company)
async def companies_list(company_id: int, 
                         current_user: User = Depends(CurrentUser),
                         db: Database = Depends(get_db)
                        ) -> Company:
    company_service = CompanyService(db=db, current_user= await current_user.user())

    company = await company_service.retrieve_company(company_id=company_id)
    return company


@router.post("/create", response_model=Company, status_code=201)
async def companies_create(company: CompanyBase,
                         current_user: User = Depends(CurrentUser),
                         db: Database = Depends(get_db)
                        ) -> Company:
    company_service = CompanyService(db=db, current_user= await current_user.user())

    company = await company_service.create_company(company=company)
    return company


@router.put("/{company_id}", response_model=Company)
async def company_update(company_id: int,
                         company_data: CompanyUpdate,
                         current_user: User = Depends(CurrentUser),
                         db: Database = Depends(get_db)
                        ) -> Company:
    company_service = CompanyService(db=db, current_user= await current_user.user())

    company = await company_service.update_company(company_id=company_id,
                                                   company_data=company_data
                                                  )
    return company


@router.delete("/{company_id}", status_code=204)
async def company_delete(company_id: int, current_user: User = Depends(CurrentUser), db: Database = Depends(get_db)):
    company_service = CompanyService(db=db, current_user= await current_user.user())

    await company_service.delete_company(company_id=company_id)
