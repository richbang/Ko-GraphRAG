# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

"""ParquetTableEmitter module."""

import logging
import traceback

import pandas as pd
from pyarrow.lib import ArrowInvalid, ArrowTypeError

from graphrag.index.storage import PipelineStorage
from graphrag.index.typing import ErrorHandlerFn

from .table_emitter import TableEmitter

log = logging.getLogger(__name__)

class ParquetTableEmitter(TableEmitter):
    """ParquetTableEmitter class."""

    _storage: PipelineStorage
    _on_error: ErrorHandlerFn

    def __init__(
        self,
        storage: PipelineStorage,
        on_error: ErrorHandlerFn,
    ):
        """Create a new Parquet Table Emitter."""
        self._storage = storage
        self._on_error = on_error

    async def preprocess_and_emit(self, filename: str, data: pd.DataFrame) -> None:
        """Preprocess data and emit to storage."""
        def preprocess_findings_column(df):
            def ensure_struct(x):
                if isinstance(x, dict):
                    return x
                elif pd.isnull(x).any():
                    return None
                else:
                    return {'value': x}

            df['findings'] = df['findings'].apply(ensure_struct)
            return df

        # Apply preprocessing
        data = preprocess_findings_column(data)
        await self._storage.set(filename, data.to_parquet())

    async def emit(self, name: str, data: pd.DataFrame) -> None:
        """Emit a dataframe to storage."""
        filename = f"{name}.parquet"
        log.info("Emitting parquet table %s", filename)
        
        try:
            await self._storage.set(filename, data.to_parquet())
        except (ArrowTypeError, ArrowInvalid) as e:
            log.warning("Initial parquet save failed, preprocessing data and retrying due to error: %s", str(e))
            try:
                await self.preprocess_and_emit(filename, data)
            except Exception as ex:
                log.exception("Error while emitting parquet table after retry")
                self._on_error(
                    ex,
                    traceback.format_exc(),
                    None,
                )
        except Exception as e:
            log.exception("Unexpected error while emitting parquet table")
            self._on_error(
                e,
                traceback.format_exc(),
                None,
            )