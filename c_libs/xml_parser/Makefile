CC=gcc
CFLAGS=-g -O3 -Wall -Werror
PROJECT=XML_Parser
OBJ_PATH=obj
SRC_PATH=src\
         xml
INC_PATH=SKcommon\
         src\
         xml
VPATH=$(SRC_PATH)


SRC_C:=$(foreach dir, $(SRC_PATH), $(wildcard $(dir)/*.c))
OBJ_C_0=$(notdir $(patsubst %.c, %.o, $(SRC_C)))
OBJ_C=$(foreach file, $(OBJ_C_0), $(OBJ_PATH)/$(file))

INCLUDE:=$(foreach dir, $(INC_PATH), -I $(dir))
CC_OPTS=$(INCLUDE) $(CFLAGS)

#================================
# RULE
#================================
.PHONY: all setup clean

all: setup $(PROJECT)

$(PROJECT): $(OBJ_C)
	$(CC) -o $@ $^

$(OBJ_C): $(OBJ_PATH)/%.o:%.c
	@echo "[CC] $@"
	@$(CC) $(CC_OPTS) -c -o $@ $<;
	
setup:
	-@mkdir -p $(OBJ_PATH);
	@echo "Make $(PROJECT) project";

clean:
	-@rm -f $(PROJECT)
	-@rm -rf $(OBJ_PATH)

