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
    if 100 < len(matrix) or len(matrix[0]) > 100:
        raise HTTPException(status_code=400, detail="The matrix must have only 100 rows and columns")

    rows = len(matrix)
    cols = len(matrix[0])

    max_area = 0
    similar_number = None
    
    for num in set(x for row in matrix for x in row):
        histogram = [0] * cols
        for i in range(rows):
            for j in range(cols):
                if len(matrix[i])<=j:
                    continue
                if matrix[i][j] == num:
                    histogram[j] += 1
                else:
                    histogram[j] = 0
                current_area = largest_rectangle_area(histogram)
                if current_area > max_area:
                    max_area = current_area
                    similar_number = num

    return similar_number,max_area
@app.post("/largest_rectangle",tags=["Largest Rectangle in Matrix"])
async def largest_rectangle(matrix: List[List[int]]):
    try:
        result = find_largest_rectangle(matrix)
        return {"Largest rectangle = ": '({},{})'.format(result[0], result[1])}
    except HTTPException as e:
        return e


