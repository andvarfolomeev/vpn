from typing import Annotated

from fastapi import Depends

from wg_service.unit_of_work.unit_of_work import UnitOfWork

UnitOfWorkDep = Annotated[UnitOfWork, Depends(UnitOfWork)]
