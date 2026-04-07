"""API Key 管理路由"""

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import CurrentUser, DbSession
from app.schemas.api_key import ApiKeyCreate, ApiKeyResponse, ApiKeyListResponse
from app.services.api_key_service import ApiKeyService
from app.core.exceptions import NotFoundError

router = APIRouter(prefix="/api-keys", tags=["API Key 管理"])


@router.get("", response_model=ApiKeyListResponse)
async def list_api_keys(
    current_user: CurrentUser,
    db: DbSession
):
    """获取用户的 API Keys 列表"""
    key_service = ApiKeyService(db)
    keys = await key_service.get_user_keys(str(current_user.id))

    return {
        "keys": [
            {
                "id": key.id,
                "name": key.name,
                "key_preview": f"{key.key_hash[:8]}...",  # 只显示前几个字符
                "last_used_at": key.last_used_at,
                "created_at": key.created_at,
            }
            for key in keys
        ]
    }


@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_api_key(
    key_data: ApiKeyCreate,
    current_user: CurrentUser,
    db: DbSession
):
    """创建新的 API Key"""
    key_service = ApiKeyService(db)

    # 生成并保存 API Key
    raw_key, api_key = await key_service.create_key(
        user_id=str(current_user.id),
        name=key_data.name
    )

    # 返回完整的 key（注意：只有第一次能看到完整 key）
    return {
        "id": str(api_key.id),
        "name": api_key.name,
        "key": raw_key,  # 这是唯一一次返回完整 key
        "key_preview": f"{raw_key[:8]}...",
        "created_at": api_key.created_at,
    }


@router.delete("/{key_id}")
async def delete_api_key(
    key_id: str,
    current_user: CurrentUser,
    db: DbSession
):
    """删除 API Key"""
    key_service = ApiKeyService(db)

    success = await key_service.delete_key(key_id, str(current_user.id))
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API Key not found"
        )

    return {"message": "API Key deleted successfully"}
