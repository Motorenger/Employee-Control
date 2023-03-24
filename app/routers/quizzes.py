from fastapi import APIRouter, Depends

from databases import Database

from fastapi_pagination import Page, Params, paginate

from utils.auth import get_user
from schemas.quizz_schemas import QuizzCreate, QuizzEdit, Quizz, QuizzFull, QuizzData, QuestionList
from schemas.user_schemas import User
from services.company_logic import CompanyService
from services.quizz_logic import QuizzService
from services.company_actions_logic import CompanyActionsService
from db.database import get_db


router = APIRouter(
    prefix="/quizzes",
    tags=["quizzes"]
)


@router.post("/{company_id}", response_model=Quizz, status_code=201)
async def create_quizz(company_id: int,
                       quizz_data: QuizzCreate, 
                       current_user: User = Depends(get_user),
                       db: Database = Depends(get_db)
                       ) -> Quizz:
    quizz_service = QuizzService(db=db, current_user=current_user)

    return await quizz_service.create_quizz(company_id=company_id, quizz_data=quizz_data)


@router.delete("/{company_id}/{quizz_id}", status_code=204)
async def delete_quizz(company_id: int,
                       quizz_id: int,
                       current_user: User = Depends(get_user),
                       db: Database = Depends(get_db)
                       ):
    quizz_service = QuizzService(db=db, current_user=current_user)

    return await quizz_service.delete_quizz(company_id=company_id, quizz_id=quizz_id)


@router.put("/{company_id}/{quizz_id}", response_model=Quizz)
async def update_quizz(company_id: int,
                       quizz_id: int,
                       quizz_data: QuizzEdit,
                       current_user: User = Depends(get_user),
                       db: Database = Depends(get_db)
                       ) -> Quizz:
    quizz_service = QuizzService(db=db, current_user=current_user)

    return await quizz_service.update_quizz(company_id=company_id,
                                             quizz_id=quizz_id,
                                             quizz_data=quizz_data
                                             )


@router.get("/{company_id}/{quizz_id}", response_model=QuestionList)
async def get_quizz(company_id: int,
                       quizz_id: int, 
                       current_user: User = Depends(get_user),
                       db: Database = Depends(get_db)
                       ) -> QuestionList:
    quizz_service = QuizzService(db=db, current_user=current_user)

    return await quizz_service.retrieve_quizz(company_id=company_id, quizz_id=quizz_id)


@router.post("/{company_id}/{quizz_id}/pass", response_model=float)
async def pass_quizz(company_id: int,
                    quizz_id: int, 
                    quizz_data: QuizzData,
                    current_user: User = Depends(get_user),
                    db: Database = Depends(get_db)
                    ) -> float:
    quizz_service = QuizzService(db=db, current_user=current_user)

    return await quizz_service.pass_quizz(company_id=company_id,
                                          quizz_id=quizz_id,
                                          quizz_data=quizz_data)
