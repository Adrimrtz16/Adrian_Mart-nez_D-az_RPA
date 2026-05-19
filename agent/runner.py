import json
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

from shared.templating import render_workflow

PROCEDURES_DIR = Path("procedures")

class WorkflowRunner:
    def __init__(self, headless=False):
        self.headless = headless

    def run(self, workflow_id: str, params: dict):
        start = time.time()

        workflow = self._load_workflow(workflow_id)
        rendered = render_workflow(workflow, params)

        last_message = ""

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=self.headless
                )

                page = browser.new_page()

                print(f"[Runner] Opening {rendered['url']}")
                page.goto(
                    rendered["url"],
                    wait_until="networkidle",
                    timeout=60000
                )

                for i, step in enumerate(rendered["steps"], 1):
                    print(
                        f"[Runner] Step {i}: {step['type']}"
                    )
                    self._execute_step(page, step)
                    time.sleep(1.5)

                # Intentar leer toast final
                try:
                    toast = page.locator("#toast")

                    if toast.is_visible():
                        last_message = toast.inner_text()

                except:
                    pass

                browser.close()

            duration = round(
                time.time() - start,
                2
            )

            return {
                "status": "ok",
                "duration": duration,
                "last_message": last_message
            }

        except Exception as e:
            duration = round(
                time.time() - start,
                2
            )

            return {
                "status": "error",
                "duration": duration,
                "error": str(e)
            }

    def _load_workflow(self, workflow_id):
        path = PROCEDURES_DIR / f"{workflow_id}.workflow.json"

        if not path.exists():
            raise FileNotFoundError(
                f"No existe workflow: {workflow_id}"
            )

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _execute_step(self, page, step):
        step_type = step["type"]

        if step_type == "wait":
            page.wait_for_timeout(
                step["ms"]
            )

        elif step_type == "click":
            page.wait_for_load_state(
                "networkidle"
            )

            locator = self._locator(
                page,
                step["target"]
            )

            locator.wait_for(
                state="visible",
                timeout=10000
            )

            locator.click()

        elif step_type == "type":
            page.wait_for_load_state("networkidle")

            locator = self._locator(page, step["target"])
            locator.wait_for(
                state="visible",
                timeout=10000
            )

            locator.click()
            locator.fill(str(step["value"]))

        elif step_type == "select":
            page.wait_for_load_state(
                "networkidle"
            )

            locator = self._locator(
                page,
                step["target"]
            )

            locator.wait_for(
                state="visible",
                timeout=10000
            )

            locator.select_option(
                step["value"]
            )

        elif step_type == "wait_for_text":
            locator = self._locator(
                page,
                step["target"]
            )

            locator.wait_for(
                state="visible",
                timeout=5000
            )

            page.wait_for_function(
                f"""
                () => document
                    .querySelector('{step["target"]["value"]}')
                    .innerText
                    .includes('{step["contains"]}')
                """
            )

        else:
            raise ValueError(
                f"Step no soportado: {step_type}"
            )

    def _locator(self, page, target):
        by = target["by"]
        value = target["value"]

        if by == "id":
            return page.locator(
                f"#{value}"
            )

        if by == "name":
            return page.locator(
                f'[name="{value}"]'
            )

        if by == "css":
            return page.locator(value)

        raise ValueError(
            f"Selector no soportado: {by}"
        )


def run_workflow_file(
    workflow_id,
    parameters,
    headless=False
):
    runner = WorkflowRunner(
        headless=headless
    )

    return runner.run(
        workflow_id,
        parameters
    )