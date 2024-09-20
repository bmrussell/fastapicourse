# Pydantic v1 vs Pydantic v2

FastAPI is now compatible with both Pydantic v1 and Pydantic v2.

Based on how new the version of FastAPI you are using, there could be small method name changes.


The three biggest are:
1. `.dict()` function is now renamed to `.model_dump()`
2. `schema_extra` function within a Config class is now renamed to `json_schema_extra`
3. Optional variables need a `=None` example: id: `Optional[int] = None`
