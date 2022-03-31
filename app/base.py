from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi_sqlalchemy import db
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status

from core.database import Base

ModelType = TypeVar("ModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, SchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, id: Any) -> Optional[ModelType]:
        obj = db.session.query(self.model).filter(self.model.id == id).first()
        if obj:
            return obj
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Запись не найдена.",
        )

    def get_multi(
        self,  *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return db.session.query(self.model).offset(skip).limit(limit).all()

    def get_all(self):
        return db.session.query(self.model).all()

    def create(self, *, obj_in: SchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.session.add(db_obj)
        db.session.commit()
        db.session.refresh(db_obj)
        return db_obj

    def update(
        self,
        *,
        db_obj: ModelType,
        obj_in: Union[SchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.session.add(db_obj)
        db.session.commit()
        db.session.refresh(db_obj)
        return db_obj

    def remove(self, *, id) -> ModelType:
        obj = db.session.query(self.model).get(id)
        db.session.delete(obj)
        db.session.commit()
        return obj
