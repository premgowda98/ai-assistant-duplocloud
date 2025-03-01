import multiprocessing
import sys

import uvicorn
from dotenv import load_dotenv
from streamlit import runtime
from streamlit.web import cli as stcli

from api.app import app


def run_streamlit():
    sys.argv = ["streamlit", "run", "ui/app.py"]
    sys.exit(stcli.main())


def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=8005)


if __name__ == "__main__":
    if not runtime.exists():
        load_dotenv()

        fastapi_process = multiprocessing.Process(target=run_fastapi)
        streamlit_process = multiprocessing.Process(target=run_streamlit)

        fastapi_process.start()
        streamlit_process.start()

        fastapi_process.join()
        streamlit_process.join()
