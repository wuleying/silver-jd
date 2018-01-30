PROJECT_NAME=silver-jd
PACKAGE = github.com/wuleying/silver-jd
BASE_DIR = $(GOPATH)/src/$(PACKAGE)
BIN_DIR=$(BASE_DIR)/bin

# Go parameters
GO_CMD=go
GO_BUILD=$(GO_CMD) build
GO_CLEAN=$(GO_CMD) clean
GO_TEST=$(GO_CMD) test
GO_GET=$(GO_CMD) get

all: build

build:
	@echo [INFO] BASE=$(BASE)
	@echo [INFO] BIN_DIR=$(BIN_DIR)
	$(GO_BUILD) -o $(BIN_DIR)/$(PROJECT_NAME) -v $(BASE_DIR)/*.go
	@echo "Build completed"

clean:
	$(GO_CLEAN)
	rm $(BIN_DIR)/$(PROJECT_NAME)
	@echo "Clean completed"

test:
	@echo "Todo"

run:
	$(BIN_DIR)/$(PROJECT_NAME)