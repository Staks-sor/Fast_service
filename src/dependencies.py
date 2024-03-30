from typing import Annotated

from fastapi import Depends

from src.uow import UoW, UoWInterface

UowDep = Annotated[UoWInterface, Depends(UoW)]
