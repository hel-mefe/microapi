.PHONY: help run run-example test test-watch lint clean

# =========================================================
# MicroAPI v0.9
# Minimal FastAPI re-coded from scratch
# =========================================================

# -----------------------------
# ANSI colors (teal branding)
# -----------------------------
TEAL   := \033[38;5;37m
WHITE  := \033[97m
GRAY   := \033[90m
RESET  := \033[0m
BOLD   := \033[1m
GREEN  := \033[38;5;35m

# -----------------------------
# Commands
# -----------------------------
PYTHON  := python3
UVICORN := uvicorn

APP_MODULE     := microapi.app:app
EXAMPLE_MODULE := example:app

# -----------------------------
# ASCII Banner
# -----------------------------
define MICROAPI_BANNER
$(TEAL)$(BOLD)
███╗   ███╗ ██╗  ██████╗ ██████╗  █████╗ ██████╗ ██╗
████╗ ████║ ██║ ██╔════╝ ██╔══██╗██╔══██╗██╔══██╗██║
██╔████╔██║ ██║ ██║      ██████╔╝███████║██████╔╝██║
██║╚██╔╝██║ ██║ ██║      ██╔══██╗██╔══██║██╔═══╝ ██║
██║ ╚═╝ ██║ ██║ ╚██████╗ ██║  ██║██║  ██║██║     ██║
╚═╝     ╚═╝ ╚═╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝
$(RESET)
$(WHITE)MicroAPI v0.9$(RESET)
$(GREEN)Minimal FastAPI re-coded from scratch$(RESET)

endef
export MICROAPI_BANNER

# -----------------------------
# Targets
# -----------------------------

help:
	@printf "$$MICROAPI_BANNER"
	@echo ""
	@echo "$(WHITE)Available commands:$(RESET)"
	@echo ""
	@echo "  $(TEAL)make run$(RESET)           Run the MicroAPI framework"
	@echo "  $(TEAL)make run-example$(RESET)   Run the example application"
	@echo "  $(TEAL)make test$(RESET)          Run tests"
	@echo "  $(TEAL)make test-watch$(RESET)    Run tests in watch mode"
	@echo "  $(TEAL)make lint$(RESET)          Basic syntax check"
	@echo "  $(TEAL)make clean$(RESET)         Clean cache files"
	@echo ""

run:
	@printf "$$MICROAPI_BANNER"
	@echo "$(TEAL)▶ Running MicroAPI$(RESET)"
	$(UVICORN) $(APP_MODULE) --reload

run-example:
	@printf "$$MICROAPI_BANNER"
	@echo "$(TEAL)▶ Running example application$(RESET)"
	$(UVICORN) $(EXAMPLE_MODULE) --reload

test:
	@printf "$$MICROAPI_BANNER"
	@echo "$(TEAL)▶ Running tests$(RESET)"
	$(PYTHON) -m pytest -q

test-watch:
	@printf "$$MICROAPI_BANNER"
	@echo "$(TEAL)▶ Running tests (watch mode)$(RESET)"
	$(PYTHON) -m pytest -q -x --lf --disable-warnings --maxfail=1

lint:
	@printf "$$MICROAPI_BANNER"
	@echo "$(TEAL)▶ Linting (syntax check)$(RESET)"
	$(PYTHON) -m compileall microapi

clean:
	@echo "$(TEAL)▶ Cleaning cache files$(RESET)"
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

