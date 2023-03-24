from fastapi import APIRouter, Depends

from databases import Database

from fastapi_pagination import Page, Params, paginate

from schemas.company_schemas import Company, CompanyBase, CompanyUpdate
from schemas.quizz_schemas import QuizzList
from schemas.invite_schemas import InviteData, InviteCreate, Invite
from schemas.request_schemas import RequestData, RequestCreate, RequestList
from schemas.user_schemas import User, UserList
from utils.auth import get_user
from services.company_logic import CompanyService
from services.company_actions_logic import CompanyActionsService
from db.database import get_db


router = APIRouter(
    prefix="/companies",
    tags=["companies"]
)


@router.get("/", response_model=Page[Company])
async def companies_list(params: Params = Depends(), current_user: User = Depends(get_user), db: Database = Depends(get_db)) -> Page:
    company_service = CompanyService(db=db, current_user=current_user)

    companies = await company_service.get_companies()
    return paginate(companies.companies, params)


@router.get("/{company_id}", response_model=Company)
async def companies_retrieve(company_id: int,
                         current_user: User = Depends(get_user),
                         db: Database = Depends(get_db)
                        ) -> Company:
    company_service = CompanyService(db=db, current_user=current_user)

    company = await company_service.retrieve_company(company_id=company_id)
    return company


@router.post("/create", response_model=Company, status_code=201)
async def companies_create(company: CompanyBase,
                         current_user: User = Depends(get_user),
                         db: Database = Depends(get_db)
                        ) -> Company:
    company_service = CompanyService(db=db, current_user=current_user)

    company = await company_service.create_company(company=company)
    return company


@router.put("/{company_id}", response_model=Company)
async def company_update(company_id: int,
                         company_data: CompanyUpdate,
                         current_user: User = Depends(get_user),
                         db: Database = Depends(get_db)
                        ) -> Company:
    company_service = CompanyService(db=db, current_user=current_user)

    company = await company_service.update_company(company_id=company_id,
                                                   company_data=company_data
                                                  )
    return company


@router.delete("/{company_id}", status_code=204)
async def company_delete(company_id: int, current_user: User = Depends(get_user), db: Database = Depends(get_db)):
    company_service = CompanyService(db=db, current_user=current_user)

    await company_service.delete_company(company_id=company_id)


# Actions

@router.get("/{company_id}/members", response_model=UserList)
async def company_members(company_id: int,
                          params: Params = Depends(), 
                          current_user: User = Depends(get_user),
                          db: Database = Depends(get_db)
                        ) -> UserList:
    company_actions_service = CompanyActionsService(company_id=company_id,
                                                    current_user=current_user,
                                                    db=db
                                                    )
    members = await company_actions_service.get_members()
    return members


@router.get("/{company_id}/invites", response_model=Page[Invite])
async def list_invites(company_id: int,
                       params: Params = Depends(), 
                       current_user: User = Depends(get_user),
                       db: Database = Depends(get_db)
                 ):
    company_actions_service = CompanyActionsService(company_id=company_id,
                                                      current_user=current_user,
                                                      db=db
                                                      )
    invites = await company_actions_service.get_invites()
    return paginate(invites.invites, params)

@router.post("/{company_id}/invite", status_code=201)
async def invite(company_id: int,
                 invite_data: InviteData,
                 current_user: User = Depends(get_user),
                 db: Database = Depends(get_db)
                 ):
        company_actions_service = CompanyActionsService(company_id=company_id,
                                                      current_user=current_user,
                                                      db=db
                                                      )
        await company_actions_service.send_invite(invite_data=invite_data)


@router.delete("/{company_id}/invite/{invite_id}", status_code=204)
async def invite_delete(invite_id: int,
                        company_id: int,
                        current_user: User = Depends(get_user),
                        db: Database = Depends(get_db)
                    ):
    company_actions_service = CompanyActionsService(company_id=company_id,
                                                    current_user=current_user,
                                                    db=db
                                                    )

    await company_actions_service.delete_invite(invite_id=invite_id)


@router.post("/request", status_code=201)
async def request(
                 request_data: RequestData,
                 current_user: User = Depends(get_user),
                 db: Database = Depends(get_db)
                 ):
        company_actions_service = CompanyActionsService(
                                                      current_user=current_user,
                                                      db=db
                                                      )
        await company_actions_service.send_request(request_data=request_data)


@router.get("/{company_id}/requests", response_model=Page[Invite])
async def list_requests(company_id: int,
                       params: Params = Depends(), 
                       current_user: User = Depends(get_user),
                       db: Database = Depends(get_db)
                 ) -> Page:
    company_actions_service = CompanyActionsService(company_id=company_id,
                                                      current_user=current_user,
                                                      db=db
                                                      )
    requests = await company_actions_service.get_requests()
    return paginate(requests.requests, params)


@router.post("/{company_id}/requests/accept/{request_id}", status_code=201)
async def request_accept(company_id: int,
                        request_id: int,
                        current_user: User = Depends(get_user),
                        db: Database = Depends(get_db)
                        ):
    company_actions_service = CompanyActionsService(company_id=company_id,
                                                    current_user=current_user,
                                                    db=db
                                                    )
    await company_actions_service.accept_request(request_id=request_id)


@router.delete("/{company_id}/requests/{request_id}", status_code=204)
async def request_delete(request_id: int,
                        company_id: int,
                        current_user: User = Depends(get_user),
                        db: Database = Depends(get_db)
                    ):
    company_actions_service = CompanyActionsService(company_id=company_id,
                                                    current_user=current_user,
                                                    db=db
                                                    )

    await company_actions_service.delete_request(request_id=request_id)


@router.delete("/{company_id}/members/{user_id}", status_code=204)
async def delete_member(company_id: int,
                        user_id: int,
                        current_user: User = Depends(get_user),
                        db: Database = Depends(get_db)
                    ):
    company_actions_service = CompanyActionsService(company_id=company_id,
                                                    current_user=current_user,
                                                    db=db
                                                    )
    await company_actions_service.delete_member(user_id=user_id)


@router.post("/{company_id}/members/admin/{user_id}", status_code=201)
async def admin(company_id: int,
                        user_id: int,
                        current_user: User = Depends(get_user),
                        db: Database = Depends(get_db)
                    ):
    company_actions_service = CompanyActionsService(company_id=company_id,
                                                    current_user=current_user,
                                                    db=db
                                                    )
    await company_actions_service.admin(user_id=user_id)


@router.delete("/{company_id}/members/admin/{user_id}", status_code=204)
async def remove_admin(company_id: int,
                        user_id: int,
                        current_user: User = Depends(get_user),
                        db: Database = Depends(get_db)
                    ):
    company_actions_service = CompanyActionsService(company_id=company_id,
                                                    current_user=current_user,
                                                    db=db
                                                    )
    await company_actions_service.remove_admins(user_id=user_id)


@router.get("/{company_id}/members/admins", response_model=UserList)
async def company_admins(company_id: int,
                          params: Params = Depends(), 
                          current_user: User = Depends(get_user),
                          db: Database = Depends(get_db)
                        ) -> UserList:
    company_actions_service = CompanyActionsService(company_id=company_id,
                                                    current_user=current_user,
                                                    db=db
                                                    )
    admins = await company_actions_service.get_admins()
    return admins


@router.get("/{company_id}/quizzes", response_model=Page)
async def company_quizzes(company_id: int,
                          params: Params = Depends(), 
                          current_user: User = Depends(get_user),
                          db: Database = Depends(get_db)
                        ) -> Page:
    company_actions_service = CompanyService(current_user=current_user,
                                            db=db
                                            )
    quizzes = await company_actions_service.list_quizzes(company_id=company_id,)
    return paginate(quizzes.quizzes, params)
