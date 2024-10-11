
## Alembic SQL Migrations

|Command|Description|
|--|--|
|`alembic init <folder>`|Initialise new migration environment|
|`alembic revision -m <message>`|Create a new migration revision|
|`alembic upgrade <revision #>`|Run a migration|
|`alembic downgrade -1`|Run a migration to previous revision|

## Using Alembic

### Initialise Environment
In `alembic/env.py` :

```python
#change import models
import models
...

#change remove if
#if config.config_file_name is not None:
fileConfig(config.config_file_name)
...

#change set target_metadata
target_metadata = models.Base.metadata 

```

## Round Trip

### Create a revision

```bash
alembic revision -m "create user.phone_number column"
```
Generates `\alembic\versions\9f61e5cc11d1_create_user_phone_number_column.py`

### Code revisions

```python
def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))

def downgrade() -> None:
    op.drop_column('users', 'phone_number')


```

### Run migration

```bash
ID_FROM_VERSION_
alembic upgrade 9f61e5cc11d1
```
### 