# MTL makefile for drug_mr 10/15/2011
# be sure to source setup.sh

CC=gcc
CXX=g++
MPICC=mpicc
GOC=6g
GOLINK=6l

CFLAGS=-g
LDFLAGS=-lm
OPENMP_FLAGS=-fopenmp
CUDA_CFLAGS = -I/usr/local/cuda/include
CUDA_LIBS = -L/usr/local/cuda/lib -lcuda -lcudart
TBB_LIBS = -ltbb -lrt
CPP11_THREADS = -std=c++11 -pthread
PTHREADS_LIBS=-lpthread
BOOST_LIBS = -I/opt/boost/include -L/opt/boost/lib -lboost_thread
ARBB_LIBS=$(TBB_LIBS) -larbb -L/opt/intel/arbb/1.0.0.022/lib/intel64/ -I/opt/intel/arbb/1.0.0.022/include/

TARGETS := dd_serial dd_omp dd_threads # dd_boost # dd_hadoop
all:  $(TARGETS)
#	hadoop jar DDHadoop.jar edu.stolaf.cs.DDHadoop $(DFS)/in $(DFS)/out

.SUFFIXES: .c .o .cu .cpp .go .6

dd_serial:  dd_serial.cpp
	$(CXX) -o dd_serial dd_serial.cpp

dd_omp:  dd_omp.cpp
	$(CXX) -o dd_omp dd_omp.cpp $(LDFLAGS) $(OPENMP_FLAGS) $(TBB_LIBS) 

dd_boost:  dd_boost.cpp
	$(CXX) -o dd_boost dd_boost.cpp $(LDFLAGS) $(TBB_LIBS) $(BOOST_LIBS) 

dd_threads: dd_threads.cpp
	$(CXX) -o dd_threads dd_threads.cpp $(LDFLAGS) $(CPP11_THREADS) $(TBB_LIBS) 

dd_hadoop:  DDHadoop.jar

DDHadoop.jar:  classes DDHadoop.java
	javac -classpath $(HADOOP_LIB) -d classes DDHadoop.java
	jar cvf DDHadoop.jar -C classes edu

classes:  
	mkdir classes

tgz:
	DIR=`pwd` ; DIR=`basename $$DIR` ; cd .. ; \
	tar cfz $$DIR.tgz $$DIR/{Makefile,setup.sh,dd_*.{cpp,java,go}}

clean:
	rm -f *.o *~ $(TARGETS) 
