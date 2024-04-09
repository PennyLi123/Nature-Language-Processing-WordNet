import inspect, time
from wn2graph import setupGraph, config, cyphers, pullData
import timeit


def main():
    print("this is main()")
    # compare()

    start = timeit.default_timer()


    start = time.time()

    setupGraph.initWNGraph()

    end = time.time()
    print(f"Finished in: {end - start}")

    # testQuery2()

    cyphers.shortestPathFormNodes("open", "close")

    test = cyphers.word2word()

    for item in test[0]:
        print(f"{item} is key, {test[0][item]} is value")

    cyphers.count4eachRelation()

    cyphers.checkExsistsGDSgraph()

    cyphers.distinctSynsetsfrom()

    setupGraph.IndexesConstraints()


if __name__ == "__main__":
    print("run from main()")
    main()