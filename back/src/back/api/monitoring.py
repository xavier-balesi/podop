#
# Copyright (c) 2008-2023 Linxo, All Rights Reserved.
#
#    COPYRIGHT:
#         This software is the property of Linxo.
#         It cannot be copied, used, or modified without obtaining an
#         authorization from the authors or a person mandated by Linxo.
#         If such an authorization is provided, any modified version
#         or copy of the software has to contain this header.
#
#    WARRANTIES:
#         This software is made available by the authors in the hope
#         that it will be useful, but without any warranty.
#         Linxo is not liable for any consequence related to
#         the use of the provided software.
#

"""main module executed by the Dockerfile."""

import logging

from fastapi import FastAPI

log = logging.getLogger(__name__)

app = FastAPI()


@app.get("/monitoring/health")
async def healthcheck() -> int:
    """Healthcheck for Kubernetes."""
    return 200
