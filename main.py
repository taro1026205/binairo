#!/usr/bin/env python3
import time
import tracemalloc
from utils.ioprocess import read_puzzle
from dfs import DFSBinairo
from heuristic import HeuristicBinairo

def measure_performance(solver_instance, name):
    print(f"\n--- Running {name} ---")
    
    tracemalloc.start()
    start_time = time.perf_counter()

    is_solved = solver_instance.solve()

    end_time = time.perf_counter()
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    runtime = end_time - start_time
    peak_mem_kb = peak_mem / 1024  

    if is_solved:
        print(">> Solution Found!")
        solver_instance.print_grid(title=f"{name}")
    else:
        print(">> No Solution Found!")

    return runtime, peak_mem_kb

def main():
    filepath = "data/6x6.txt"
    initial_grid = read_puzzle(filepath)


    dfs_solver = DFSBinairo(initial_grid)
    heuristic_solver = HeuristicBinairo(initial_grid)

    dfs_solver.print_grid(title="Initial Matrix")

    dfs_time, dfs_mem = measure_performance(dfs_solver, "Blind Search (DFS)")

    heuristic_time, heuristic_mem = measure_performance(heuristic_solver, "Heuristic Search")

    print("\n" + "="*55)
    print(f"{'PRODUCTIVITY COMPARISION':^55}")
    print("="*55)
    print(f"{'ALGORITHMS':<20} | {'TIME (s)':<15} | {'MEMORY (KB)':<15}")
    print("-" * 55)
    print(f"{'DFS (Blind)':<20} | {dfs_time:<15.6f} | {dfs_mem:<15.2f}")
    print(f"{'Heuristic':<20} | {heuristic_time:<15.6f} | {heuristic_mem:<15.2f}")
    print("="*55)

if __name__ == "__main__":
    main()