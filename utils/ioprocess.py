def read_puzzle(filepath):
    grid = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue  
                
                row = []
                tokens = line.split() if ' ' in line else list(line)
                
                for token in tokens:
                    if token in ['.', '_', '-1']:
                        row.append(-1)
                    elif token == '0':
                        row.append(0)
                    elif token == '1':
                        row.append(1)
                    else:
                        raise ValueError(f"Invalid Token '{token}' in {filepath}")
                grid.append(row)
                
        return grid
        
    except FileNotFoundError:
        print(f"Error: Not Found '{filepath}'")
        return None
    except Exception as e:
        print(f"Error: Cannot Read {e}")
        return None
