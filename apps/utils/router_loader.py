import logging
import os
import importlib
from aiogram import Router


def load_routers():
    router = Router()
    handlers_dir = os.path.join(os.path.dirname(__file__), '..', 'handlers')
    routers_found = False
    logging.info("Loading routers...")

    for root, dirs, files in os.walk(handlers_dir):
        if "handlers.py" in files:
            relative_path = os.path.relpath(root, handlers_dir)
            module_name = f"apps.handlers.{relative_path.replace(os.sep, '.')}.handlers"
            module_name = module_name.lstrip('.')

            module = importlib.import_module(module_name)

            if hasattr(module, "router"):
                routers_found = True
                logging.info(f"Loading... {module_name}.py")
                router.include_router(module.router)
            else:
                logging.warning(f"Router is not issue. {module_name}")

    if not routers_found:
        logging.warning("No one router is found.")

    logging.info("Routers are loaded.")
    return router
