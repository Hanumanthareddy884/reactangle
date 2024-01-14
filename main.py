from fastapi import FastAPI, HTTPException
from typing import List, Tuple

app = FastAPI()

def largest_rectangle_area(heights):
    stack = []
    max_area = 0
    i = 0
    while i < len(heights):
        if not stack or heights[i] >= heights[stack[-1]]:
            stack.append(i)
            i += 1
        else:
            top = stack.pop()
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, heights[top] * width)

    while stack:
        top = stack.pop()
        width = i if not stack else i - stack[-1] - 1
        max_area = max(max_area, heights[top] * width)

    return max_area

def find_largest_rectangle(matrix):
    if not matrix or not matrix[0]:
        raise HTTPException(status_code=400, detail="Invalid matrix")

    rows = len(matrix)
    cols = len(matrix[0])

    for row in matrix:
        if len(row) != cols:
            raise HTTPException(status_code=400, detail="Invalid matrix")

    max_area = 0
    for num in set(x for row in matrix for x in row):
        histogram = [0] * cols
        for i in range(rows):
            for j in range(cols):
                if matrix[i][j] == num:
                    histogram[j] += 1
                else:
                    histogram[j] = 0
            max_area = max(max_area, largest_rectangle_area(histogram))

    return max_area

@app.post("/largest_rectangle")
async def calculate_largest_rectangle(matrix: List[List[int]]):
    if len(matrix) >100:
        return {"Error":"The matrix must have only 100 rows and 100 columns."}
    try:
        result = find_largest_rectangle(matrix)
        return {"argest rectangle = ": result}
    except HTTPException as e:
        return e
