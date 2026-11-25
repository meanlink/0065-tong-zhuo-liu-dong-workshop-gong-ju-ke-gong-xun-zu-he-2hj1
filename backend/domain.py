from pathlib import Path

from fastapi import APIRouter
from modules_api import router as modules
from checkins_api import router as checkins
from pairings_api import router as pairings
from circuits_api import router as circuits
from pairing_results import run_job

router = APIRouter(prefix="/api")
router.include_router(modules)
router.include_router(checkins)
router.include_router(pairings)
router.include_router(circuits)


def seed(connection):
    connection.execute(Path(__file__).with_name("demo.sql").read_text())
