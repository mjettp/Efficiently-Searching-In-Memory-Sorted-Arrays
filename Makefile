GCCCXX=g++
GCCCXXFLAGS=-std=c++17

CLANGHOME=./clang5
CLANGCXX=$(CLANGHOME)/bin/clang++
CLANGCXXFLAGS=-std=c++17 -stdlib=libc++

OS := $(shell uname)
ifeq ($(OS),Darwin)
	LDFLAGS=-Xpreprocessor -fopenmp -lomp
else
	LDFLAGS=-fopenmp
endif

HEADERS=src/benchmark.h src/datasets.h src/benchmark_utils.h \
		src/algorithms/binary_search.h src/padded_vector.h \
		src/util.h src/algorithms/div.h src/algorithms/linear_search.h \
		src/algorithms/sip.h src/algorithms/tip.h
SOURCES=src/benchmark.cc

.PHONY: run gdb clean perf

##### Run Targets ######
run : searchbench experiments.tsv

gdb : debug
gdb :
	gdb --args ./debug experiments.tsv

perf : CLANGCXXFLAGS += -O3 -DNDEBUG -DINFINITE_REPEAT
perf :
	$(CLANGCXX) $(CLANGCXXFLAGS) $(SOURCES) -o$@ $(LDFLAGS)
	perf record -F99 -g ./perf experiments.tsv

clean:
	rm -f ./searchbench ./debug ./dump

## GCC ###############
####### Build Targets #########

searchbench: GCCCXXFLAGS += -O3 -DNDEBUG
searchbench: $(SOURCES) $(HEADERS)
	$(GCCCXX) $(GCCCXXFLAGS) $(SOURCES) -osearchbench $(LDFLAGS)

debug : GCCCXXFLAGS += -O0
debug : $(SOURCES) $(HEADERS)
		$(GCCCXX) $(GCCCXXFLAGS) $(SOURCES) -odebug $(LDFLAGS)

dump : src/dump.cc src/benchmark.h
	$(CXX) $(GCCCXXFLAGS) src/dump.cc -odump $(LDFLAGS)

## CLANG ######################
####### Build Targets #########

clang5_searchbench: CLANGCXXFLAGS += -O3 -DNDEBUG
clang5_searchbench: $(SOURCES) $(HEADERS)
	$(CLANGCXX) $(CLANGCXXFLAGS) $(SOURCES) -osearchbench $(LDFLAGS)

clang5_debug: CLANGCXXFLAGS += -O0
clang5_debug: $(SOURCES) $(HEADERS)
	$(CLANGCXX) $(CLANGCXXFLAGS) $(SOURCES) -odebug $(LDFLAGS)

clang5_dump: src/dump.cc src/benchmark.h
	$(CLANGCXX) $(CLANGCXXFLAGS) src/dump.cc -o $dump $(LDFLAGS)