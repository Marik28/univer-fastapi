from fastapi import APIRouter, Depends

from ..models.groups import Group
from ..services.groups import GroupsService

router = APIRouter(prefix="/groups")


@router.get("/", response_model=list[Group])
async def get_groups_list(
        service: GroupsService = Depends()
):
    return service.get_list()
