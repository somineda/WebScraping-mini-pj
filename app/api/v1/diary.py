from fastapi import APIRouter, Depends

from app.core.deps import get_current_user
from app.models import User
from app.schemas import DiaryCreate, DiaryResponse, DiaryUpdate
from app.services.diary import DiaryService

router = APIRouter(prefix="/diaries", tags=["Diaries"])


@router.post(
    "",
    response_model=DiaryResponse,
    summary="일기 작성",
    description="로그인한 사용자만 작성 가능 같은 날짜에 중복 작성 불가",
)
async def create_diary(
    data: DiaryCreate,
    current_user: User = Depends(get_current_user),
):
    diary = await DiaryService.create(current_user, data)
    return diary


@router.get(
    "",
    response_model=list[DiaryResponse],
    summary="내 일기 목록 조회",
    description="로그인한 사용자의 일기 목록을 최신순으로 조회",
)
async def get_diaries(
    current_user: User = Depends(get_current_user),
):
    diaries = await DiaryService.get_list(current_user)
    return diaries


@router.get(
    "/{diary_id}",
    response_model=DiaryResponse,
    summary="일기 상세 조회",
    description="본인이 작성한 일기만 조회 가능",
)
async def get_diary(
    diary_id: int,
    current_user: User = Depends(get_current_user),
):
    diary = await DiaryService.get_detail(current_user, diary_id)
    return diary


@router.patch(
    "/{diary_id}",
    response_model=DiaryResponse,
    summary="일기 수정",
    description="본인이 작성한 일기만 수정 가능",
)
async def update_diary(
    diary_id: int,
    data: DiaryUpdate,
    current_user: User = Depends(get_current_user),
):
    diary = await DiaryService.update(current_user, diary_id, data)
    return diary


@router.delete(
    "/{diary_id}",
    summary="일기 삭제",
    description="본인이 작성한 일기만 삭제 가능",
)
async def delete_diary(
    diary_id: int,
    current_user: User = Depends(get_current_user),
):
    await DiaryService.delete(current_user, diary_id)
    return {"message": "일기가 성공적으로 삭제되었습니다!"}